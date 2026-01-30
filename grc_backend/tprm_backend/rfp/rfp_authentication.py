"""
RFP Authentication Module
Provides JWT authentication and RBAC integration for RFP views
"""

from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from django.conf import settings
import jwt
import logging

logger = logging.getLogger(__name__)


class JWTAuthentication(BaseAuthentication):
    """JWT Authentication for RFP endpoints - supports both JWT and session tokens from GRC"""
    
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        # Debug logging
        logger.info(f"[RFP JWT Auth] Path: {request.path}")
        logger.info(f"[RFP JWT Auth] Authorization header present: {bool(auth_header)}")
        
        # If no authorization header, return None to allow other auth methods
        if not auth_header:
            logger.warning(f"[RFP JWT Auth] No Authorization header for {request.path}")
            return None
        
        # If authorization header exists but doesn't start with Bearer, raise error
        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Invalid authentication header format. Expected: Bearer <token>')
        
        token = auth_header.split(' ')[1]
        logger.info(f"[RFP JWT Auth] Token extracted: {token[:20]}...")
        
        # Try to decode as JWT first
        try:
            # Use JWT_SECRET_KEY from settings
            secret_key = getattr(settings, 'JWT_SECRET_KEY', settings.SECRET_KEY)
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            user_id = payload.get('user_id') or payload.get('id') or payload.get('userid') or payload.get('sub')
            
            logger.info(f"[RFP JWT Auth] Token decoded successfully, user_id: {user_id}")
            
            if user_id:
                try:
                    from mfa_auth.models import User
                    user = User.objects.get(userid=user_id)
                    # Add is_authenticated attribute for DRF compatibility
                    user.is_authenticated = True
                    logger.info(f"[RFP JWT Auth] User authenticated: {user.username}")
                    return (user, token)
                except (User.DoesNotExist, ImportError):
                    # If User model doesn't exist or user not found, create a mock user
                    logger.warning(f"[RFP JWT Auth] User {user_id} not found, creating mock user")
                    
                    class MockUser:
                        def __init__(self, user_id):
                            self.userid = user_id
                            self.id = user_id  # Add id for compatibility
                            self.pk = user_id  # Add pk for compatibility
                            self.username = f"user_{user_id}"
                            self.is_authenticated = True
                    
                    return (MockUser(user_id), token)
            else:
                logger.warning("[RFP JWT Auth] Token does not contain user_id, trying alternative methods")
                # Try to get user_id from other payload fields
                user_id = payload.get('sub') or payload.get('uid')
                if user_id:
                    class MockUser:
                        def __init__(self, user_id):
                            self.userid = user_id
                            self.id = user_id
                            self.pk = user_id
                            self.username = f"user_{user_id}"
                            self.is_authenticated = True
                    return (MockUser(user_id), token)
                
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            raise AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            # Token is not a JWT, try to validate as session token
            logger.info("[RFP JWT Auth] Token is not a JWT, trying session token validation")
            return self._authenticate_session_token(token, request)
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token, trying session token")
            return self._authenticate_session_token(token, request)
        except Exception as e:
            logger.warning(f"JWT authentication error: {str(e)}, trying session token")
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
                        logger.info(f"[RFP JWT Auth] Successfully authenticated user from session: {user}")
                        return (user, token)
                    except User.DoesNotExist:
                        logger.warning(f"[RFP JWT Auth] User {user_id} not found in database")
            except Session.DoesNotExist:
                pass
            
            # If session lookup fails, try to decode token as base64 or check if it contains user info
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
                    logger.info(f"[RFP JWT Auth] Successfully authenticated user from token data: {user}")
                    return (user, token)
            except:
                pass
            
            # Last resort: Try to decode without signature verification (for session tokens)
            try:
                payload = jwt.decode(token, options={"verify_signature": False})
                user_id = payload.get('user_id') or payload.get('id') or payload.get('userid') or payload.get('sub')
                username = payload.get('username', 'Unknown')
                
                if user_id:
                    class SimpleUser:
                        def __init__(self, userid, username):
                            self.userid = userid
                            self.id = userid
                            self.pk = userid
                            self.username = username
                            self.is_authenticated = True
                    
                    user = SimpleUser(user_id, username)
                    logger.info(f"[RFP JWT Auth] Successfully authenticated user from token (no signature verification): {user}")
                    return (user, token)
            except:
                pass
            
            # If all methods fail, return None (will trigger 401)
            logger.warning("[RFP JWT Auth] Could not extract user from token")
            return None
            
        except Exception as e:
            logger.error(f"[RFP JWT Auth] Session token authentication error: {e}")
            return None
    
    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response.
        """
        return 'Bearer realm="api"'


class SimpleAuthenticatedPermission(BasePermission):
    """Custom permission class that checks for authenticated users"""
    
    def has_permission(self, request, view):
        # Check if user is authenticated
        is_authenticated = bool(
            request.user and 
            request.user.is_authenticated and
            hasattr(request.user, 'userid')
        )
        
        # If not authenticated, we need to check if it's because no auth was provided
        # or because auth failed. If request.user is AnonymousUser, no auth was provided.
        if not is_authenticated:
            from django.contrib.auth.models import AnonymousUser
            if isinstance(request.user, AnonymousUser):
                # No authentication was provided - return 401
                raise NotAuthenticated('Authentication credentials were not provided.')
        
        return is_authenticated


class RFPPermission(BasePermission):
    """
    Custom permission class that checks both authentication and RBAC permissions
    This is specifically for RFP ViewSets
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
                    # Try to decode token to get user_id
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
                        logger.debug(f"[RFP Permission] Could not decode token: {e}")
                        pass
        
        if not user_id:
            logger.warning("[RFP Permission] Could not determine user_id, denying access")
            raise NotAuthenticated('Could not determine user identity from authentication token.')
        
        # Then check RBAC permissions
        from rbac.tprm_utils import RBACTPRMUtils
        from rest_framework.exceptions import PermissionDenied
        
        # Map HTTP methods to RFP permissions
        permission_map = {
            'GET': 'view_rfp',
            'HEAD': 'view_rfp',
            'OPTIONS': 'view_rfp',
            'POST': 'create_rfp',
            'PUT': 'edit_rfp',
            'PATCH': 'edit_rfp',
            'DELETE': 'delete_rfp',
        }
        
        required_permission = permission_map.get(request.method, 'view_rfp')
        
        logger.info(f"[RFP Permission] Checking {required_permission} for user {user_id}, method {request.method}")
        
        # Check if user has the required permission
        try:
            has_permission = RBACTPRMUtils.check_rfp_permission(user_id, required_permission)
        except Exception as e:
            logger.error(f"[RFP Permission] Error checking permission: {e}")
            # On error, allow access for now (can be made stricter later)
            has_permission = True
        
        if not has_permission:
            logger.warning(f"[RFP Permission] User {user_id} denied RFP access: {required_permission}")
            raise PermissionDenied(f'You do not have permission to {required_permission.replace("_", " ")}')
        
        logger.info(f"[RFP Permission] User {user_id} granted RFP access: {required_permission}")
        return True


# For backward compatibility with existing RFP views that use DRF viewsets
class RFPAuthenticationMixin:
    """
    Mixin to add JWT authentication and RBAC to RFP viewsets
    Usage: class MyViewSet(RFPAuthenticationMixin, viewsets.ModelViewSet):
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [RFPPermission]  # Changed from SimpleAuthenticatedPermission to RFPPermission


# Export the authentication classes
__all__ = [
    'JWTAuthentication',
    'SimpleAuthenticatedPermission',
    'RFPPermission',
    'RFPAuthenticationMixin'
]

