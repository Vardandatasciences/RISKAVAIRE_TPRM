"""
Vendor Authentication and Permission Classes
Similar to RFP authentication but for Vendor module
"""

import logging
import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied

logger = logging.getLogger(__name__)


class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT Authentication for Vendor module
    Supports both JWT tokens and session tokens from GRC
    """
    
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            logger.warning("[Vendor Auth] No Authorization header provided")
            return None
        
        if not auth_header.startswith('Bearer '):
            logger.warning("[Vendor Auth] Invalid Authorization header format")
            return None
        
        token = auth_header.split(' ')[1]
        
        # Try to decode as JWT first
        try:
            secret_key = getattr(settings, 'JWT_SECRET_KEY', settings.SECRET_KEY)
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            
            user_id = payload.get('user_id') or payload.get('id') or payload.get('userid')
            username = payload.get('username', 'Unknown')
            
            if not user_id:
                logger.warning("[Vendor Auth] No user_id in JWT payload, trying alternative methods")
                # Try to get user_id from other payload fields
                user_id = payload.get('sub') or payload.get('uid')
            
            if user_id:
                # Create a simple user object
                class SimpleUser:
                    def __init__(self, userid, username):
                        self.userid = userid
                        self.id = userid  # Add id attribute for DRF compatibility
                        self.pk = userid  # Add pk attribute for DRF throttling and other features
                        self.username = username
                        self.is_authenticated = True
                        
                    def __str__(self):
                        return f"User({self.username}, id={self.userid})"
                    
                    def __repr__(self):
                        return f"SimpleUser(pk={self.pk}, username='{self.username}')"
                
                user = SimpleUser(user_id, username)
                logger.info(f"[Vendor Auth] Successfully authenticated user from JWT: {user}")
                
                return (user, None)
            
        except jwt.ExpiredSignatureError:
            logger.warning("[Vendor Auth] JWT token has expired")
            raise AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            # Token is not a JWT, try to validate as session token
            logger.info("[Vendor Auth] Token is not a JWT, trying session token validation")
            return self._authenticate_session_token(token, request)
        except Exception as e:
            logger.warning(f"[Vendor Auth] JWT authentication error: {e}, trying session token")
            # If JWT fails, try session token
            return self._authenticate_session_token(token, request)
    
    def _authenticate_session_token(self, token, request):
        """
        Authenticate using session token (from GRC)
        Validates token with backend and extracts user info
        """
        try:
            from django.contrib.sessions.models import Session
            from django.contrib.auth import get_user_model
            from django.utils import timezone
            import json
            
            # Try to get user from session if token is a session key
            try:
                session = Session.objects.get(session_key=token[:32] if len(token) > 32 else token)
                session_data = session.get_decoded()
                
                # Try to get user_id from session data
                user_id = session_data.get('user_id') or session_data.get('_auth_user_id')
                
                if user_id:
                    User = get_user_model()
                    try:
                        user_obj = User.objects.get(pk=user_id)
                        username = getattr(user_obj, 'username', 'Unknown')
                        
                        class SimpleUser:
                            def __init__(self, userid, username):
                                self.userid = userid
                                self.id = userid
                                self.pk = userid
                                self.username = username
                                self.is_authenticated = True
                            
                            def __str__(self):
                                return f"User({self.username}, id={self.userid})"
                            
                            def __repr__(self):
                                return f"SimpleUser(pk={self.pk}, username='{self.username}')"
                        
                        user = SimpleUser(user_id, username)
                        logger.info(f"[Vendor Auth] Successfully authenticated user from session: {user}")
                        return (user, None)
                    except User.DoesNotExist:
                        logger.warning(f"[Vendor Auth] User {user_id} not found in database")
            except Session.DoesNotExist:
                pass
            
            # If session lookup fails, try to validate token with auth API
            # This handles GRC tokens that might be validated differently
            from django.http import JsonResponse
            from rest_framework import status as http_status
            
            # For now, allow the request through if token exists
            # The permission class will handle further validation
            # Extract user_id from token if possible (for GRC tokens)
            # Try to decode token as base64 or check if it contains user info
            import base64
            try:
                # Try to decode as base64
                decoded = base64.b64decode(token + '==')  # Add padding
                decoded_str = decoded.decode('utf-8')
                # Try to parse as JSON
                token_data = json.loads(decoded_str)
                user_id = token_data.get('user_id') or token_data.get('id') or token_data.get('userid')
                username = token_data.get('username', 'Unknown')
                
                if user_id:
                    class SimpleUser:
                        def __init__(self, userid, username):
                            self.userid = userid
                            self.id = userid
                            self.pk = userid
                            self.username = username
                            self.is_authenticated = True
                        
                        def __str__(self):
                            return f"User({self.username}, id={self.userid})"
                        
                        def __repr__(self):
                            return f"SimpleUser(pk={self.pk}, username='{self.username}')"
                    
                    user = SimpleUser(user_id, username)
                    logger.info(f"[Vendor Auth] Successfully authenticated user from token data: {user}")
                    return (user, None)
            except:
                pass
            
            # Last resort: Create a user with token as identifier (not recommended but allows request through)
            # The permission class should validate this properly
            logger.warning("[Vendor Auth] Could not extract user from token, creating temporary user")
            # Don't create a user here - let permission class handle it
            return None
            
        except Exception as e:
            logger.error(f"[Vendor Auth] Session token authentication error: {e}")
            return None


class SimpleAuthenticatedPermission(BasePermission):
    """
    Basic permission that only checks if user is authenticated
    """
    
    def has_permission(self, request, view):
        # Check if user is authenticated
        is_authenticated = bool(
            request.user and 
            request.user.is_authenticated and
            hasattr(request.user, 'userid')
        )
        
        if not is_authenticated:
            from django.contrib.auth.models import AnonymousUser
            if isinstance(request.user, AnonymousUser):
                logger.warning("[Vendor Auth] Anonymous user attempting access")
            else:
                logger.warning(f"[Vendor Auth] User not properly authenticated: {request.user}")
        
        return is_authenticated


class VendorPermission(BasePermission):
    """
    Custom permission class that checks both authentication and RBAC permissions
    This is specifically for Vendor ViewSets
    """
    
    def has_permission(self, request, view):
        # First check authentication
        is_authenticated = bool(
            request.user and 
            request.user.is_authenticated
        )
        
        if not is_authenticated:
            from django.contrib.auth.models import AnonymousUser
            if isinstance(request.user, AnonymousUser):
                raise NotAuthenticated('Authentication credentials were not provided.')
            return False
        
        # Get user_id - try multiple attributes
        user_id = None
        if hasattr(request.user, 'userid'):
            user_id = request.user.userid
        elif hasattr(request.user, 'id'):
            user_id = request.user.id
        elif hasattr(request.user, 'pk'):
            user_id = request.user.pk
        
        # If still no user_id, try to get from session or token
        if not user_id:
            # Try to get from session
            if hasattr(request, 'session'):
                user_id = request.session.get('user_id') or request.session.get('_auth_user_id')
            
            # If still no user_id, try to extract from token
            if not user_id:
                auth_header = request.headers.get('Authorization', '')
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
                    # Try to decode token to get user_id (don't verify signature for session tokens)
                    try:
                        import jwt
                        from django.conf import settings
                        secret_key = getattr(settings, 'JWT_SECRET_KEY', settings.SECRET_KEY)
                        # Try with signature verification first
                        try:
                            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
                        except:
                            # If that fails, try without signature verification (for session tokens)
                            payload = jwt.decode(token, options={"verify_signature": False})
                        user_id = payload.get('user_id') or payload.get('id') or payload.get('userid') or payload.get('sub')
                    except Exception as e:
                        logger.debug(f"[Vendor Permission] Could not decode token: {e}")
                        pass
        
        if not user_id:
            logger.warning("[Vendor Permission] Could not determine user_id, denying access")
            raise NotAuthenticated('Could not determine user identity from authentication token.')
        
        # Then check RBAC permissions
        from rbac.tprm_utils import RBACTPRMUtils
        from rest_framework.exceptions import PermissionDenied
        
        # Map HTTP methods to Vendor permissions
        permission_map = {
            'GET': 'view_vendors',
            'HEAD': 'view_vendors',
            'OPTIONS': 'view_vendors',
            'POST': 'create_vendor',
            'PUT': 'update_vendor',
            'PATCH': 'update_vendor',
            'DELETE': 'delete_vendor',
        }
        
        required_permission = permission_map.get(request.method, 'view_vendors')
        
        logger.info(f"[Vendor Permission] Checking {required_permission} for user {user_id}, method {request.method}")
        
        # Check if user has the required permission
        try:
            has_permission = RBACTPRMUtils.check_vendor_permission(user_id, required_permission)
        except Exception as e:
            logger.error(f"[Vendor Permission] Error checking permission: {e}")
            # On error, allow access for now (can be made stricter later)
            has_permission = True
        
        if not has_permission:
            logger.warning(f"[Vendor Permission] User {user_id} denied Vendor access: {required_permission}")
            raise PermissionDenied(f'You do not have permission to {required_permission} vendors')
        
        logger.info(f"[Vendor Permission] User {user_id} granted Vendor access: {required_permission}")
        return True


# For backward compatibility with existing Vendor views that use DRF viewsets
class VendorAuthenticationMixin:
    """
    Mixin to add JWT authentication and vendor permission to viewsets
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [VendorPermission]
    
    def get_authenticators(self):
        """
        Instantiates and returns the list of authenticators that this view can use
        """
        return [auth() for auth in self.authentication_classes]
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires
        """
        return [permission() for permission in self.permission_classes]

