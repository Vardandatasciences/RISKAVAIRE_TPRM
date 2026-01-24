from rest_framework import serializers
from tprm_backend.utils.base_serializer import AutoDecryptingModelSerializer
from .models import RPQ, RPQEvaluationCriteria


class RPQEvaluationCriteriaSerializer(AutoDecryptingModelSerializer):
    """Serializer for RPQ Evaluation Criteria"""
    rpq_id = serializers.IntegerField(write_only=True, required=False)
    data_inventory = serializers.JSONField(required=False, allow_null=True)
    
    class Meta:
        model = RPQEvaluationCriteria
        fields = [
            'criteria_id', 'rpq_id', 'rpq', 'criteria_name', 'criteria_description', 
            'weight_percentage', 'evaluation_type', 'min_score', 
            'max_score', 'median_score', 'is_mandatory', 
            'veto_enabled', 'veto_threshold', 'min_word_count',
            'expected_boolean_answer', 'display_order', 'created_by', 'data_inventory'
        ]
        read_only_fields = ['criteria_id', 'created_by']
    
    def validate_data_inventory(self, value):
        if not isinstance(value, dict):
            return {}
        return value
    
    def get_rpq_id(self, obj):
        try:
            if hasattr(obj, 'rpq_id'):
                return obj.rpq_id
            elif hasattr(obj, 'rpq') and obj.rpq:
                return obj.rpq.rpq_id
        except Exception:
            pass
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rpq_id'] = self.get_rpq_id(instance)
        return representation
    
    def create(self, validated_data):
        rpq_id = validated_data.pop('rpq_id', None)
        if rpq_id and 'rpq' not in validated_data:
            from .models import RPQ
            try:
                validated_data['rpq'] = RPQ.objects.get(rpq_id=rpq_id)
            except RPQ.DoesNotExist:
                raise serializers.ValidationError({'rpq_id': 'RPQ with this ID does not exist'})
        return super().create(validated_data)
    
    def validate(self, data):
        if 'weight_percentage' in data:
            weight = data['weight_percentage']
            if weight < 0 or weight > 100:
                raise serializers.ValidationError(
                    {"weight_percentage": "Weight must be between 0 and 100"}
                )
        return data


class RPQSerializer(AutoDecryptingModelSerializer):
    """Serializer for RPQ model"""
    evaluation_criteria = RPQEvaluationCriteriaSerializer(many=True, required=False)
    data_inventory = serializers.JSONField(required=False, allow_null=True)
    
    class Meta:
        model = RPQ
        fields = [
            'rpq_id', 'rpq_number', 'rpq_title', 'description', 'rpq_type',
            'category', 'estimated_value', 'currency', 'issue_date',
            'submission_deadline', 'evaluation_period_end', 'award_date',
            'status', 'created_by', 'approved_by', 'primary_reviewer_id',
            'executive_reviewer_id', 'version_number', 'auto_approve',
            'allow_late_submissions', 'created_at', 'updated_at',
            'approval_workflow_id', 'evaluation_method', 'budget_range_min',
            'budget_range_max', 'criticality_level', 'geographical_scope',
            'compliance_requirements', 'custom_fields', 'final_evaluation_score',
            'award_decision_date', 'award_justification', 'documents', 'evaluation_criteria',
            'data_inventory', 'retentionExpiry'
        ]
        read_only_fields = ['rpq_id', 'rpq_number', 'created_at', 'updated_at']
    
    def validate_data_inventory(self, value):
        if not isinstance(value, dict):
            return {}
        return value


class RPQCreateSerializer(AutoDecryptingModelSerializer):
    """Serializer for creating RPQ"""
    data_inventory = serializers.JSONField(required=False, allow_null=True)
    
    class Meta:
        model = RPQ
        fields = [
            'rpq_id', 'rpq_number', 'rpq_title', 'description', 'rpq_type',
            'category', 'estimated_value', 'currency', 'issue_date',
            'submission_deadline', 'evaluation_period_end', 'award_date',
            'status', 'created_by', 'approved_by', 'primary_reviewer_id',
            'executive_reviewer_id', 'version_number', 'auto_approve',
            'allow_late_submissions', 'approval_workflow_id', 'evaluation_method',
            'budget_range_min', 'budget_range_max', 'criticality_level',
            'geographical_scope', 'compliance_requirements', 'custom_fields',
            'data_inventory', 'retentionExpiry', 'documents'
        ]
        read_only_fields = ['rpq_id', 'rpq_number']


class RPQListSerializer(AutoDecryptingModelSerializer):
    """Simplified serializer for RPQ list view"""
    
    class Meta:
        model = RPQ
        fields = [
            'rpq_id', 'rpq_number', 'rpq_title', 'status', 'created_at',
            'submission_deadline', 'criticality_level', 'created_by'
        ]
