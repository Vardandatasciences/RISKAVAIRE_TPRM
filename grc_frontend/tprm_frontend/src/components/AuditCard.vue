<template>
  <Card 
    class="shadow-card hover:shadow-hover transition-all cursor-pointer group"
    @click="$emit('click')"
  >
    <CardHeader class="pb-3 transition-colors">
      <div class="flex items-start justify-between">
        <div class="flex-1">
          <CardTitle class="text-lg leading-tight group-hover:text-primary transition-colors">
            {{ audit.title }}
          </CardTitle>
          <CardDescription class="mt-1 text-sm">
            <span class="font-medium">SLA:</span> {{ audit.sla_name || 'Unknown SLA' }}
          </CardDescription>
          <Badge v-if="audit.business_unit" variant="outline" class="mt-2 text-xs">
            {{ audit.business_unit }}
          </Badge>
        </div>
        <div class="flex flex-col items-end space-y-2">
          <span :class="getStatusBadgeClass(audit.status)">
            {{ formatStatusText(audit.status) }}
          </span>
          <span v-if="isOverdue" class="badge-priority-high">
            OVERDUE
          </span>
        </div>
      </div>
    </CardHeader>
    <CardContent class="space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
        <div class="space-y-3">
          <div class="flex items-center text-muted-foreground">
            <User class="w-4 h-4 mr-2 text-primary" />
            <span><strong>Auditor:</strong> {{ audit.auditor_name || 'Unknown Auditor' }}</span>
          </div>
          <div class="flex items-center text-muted-foreground">
            <Eye class="w-4 h-4 mr-2 text-primary" />
            <span><strong>Reviewer:</strong> {{ audit.reviewer_name || 'Unknown Reviewer' }}</span>
          </div>
        </div>
        <div class="space-y-3">
          <div class="flex items-center text-muted-foreground">
            <Calendar class="w-4 h-4 mr-2 text-primary" />
            <span><strong>Due:</strong> {{ formatDate(audit.due_date) }}</span>
          </div>
          <div class="flex items-center text-muted-foreground">
            <Clock class="w-4 h-4 mr-2 text-primary" />
            <span><strong>Updated:</strong> {{ formatDate(audit.updated_at) }}</span>
          </div>
        </div>
      </div>
      
      <div v-if="audit.scope" class="text-sm text-muted-foreground bg-muted/40 p-3 rounded-md">
        <strong class="text-foreground">Scope:</strong> {{ audit.scope }}
      </div>
      
      <div v-if="audit.metrics_count > 0" class="text-sm text-muted-foreground bg-blue-50 p-3 rounded-md audit-metrics-box">
        <div class="flex items-center mb-2">
          <Target class="w-4 h-4 mr-2 text-blue-600 audit-metrics-icon" />
          <strong class="text-foreground">Metrics ({{ audit.metrics_count }}):</strong>
        </div>
        <div class="text-xs text-foreground">
          {{ audit.metrics_names }}
        </div>
      </div>

      <div v-if="audit.evidence_docs_count !== undefined" class="text-sm text-muted-foreground bg-purple-50 p-3 rounded-md audit-evidence-box">
        <div class="flex items-center">
          <Paperclip class="w-4 h-4 mr-2 text-purple-600 audit-evidence-icon" />
          <div>
            <div><strong class="text-foreground">Evidence Docs:</strong> <span class="text-foreground">{{ audit.evidence_docs_count }}</span></div>
            <div v-if="audit.evidence_docs_last_updated" class="text-xs text-foreground">
              Updated {{ formatDate(audit.evidence_docs_last_updated) }}
            </div>
          </div>
        </div>
      </div>

      <div class="flex items-center justify-between pt-3 border-t border-border/50">
        <div class="flex items-center space-x-3 text-xs">
          <Badge variant="secondary" class="text-xs">
            {{ audit.audit_type }}
          </Badge>
          <Badge variant="outline" class="text-xs">
            {{ audit.frequency }}
          </Badge>
          <Badge v-if="audit.role" variant="outline" class="text-xs">
            {{ audit.role }}
          </Badge>
        </div>
        <div class="flex space-x-2">
          <Button 
            v-if="audit.status === 'created'"
            variant="default"
            size="sm"
            class="bg-gradient-to-r from-primary to-primary-glow hover:shadow-hover"
            @click.stop="handleStartAudit"
          >
            Start Audit
          </Button>
          <Button 
            v-else-if="isMyAudit && (audit.status === 'in_progress' || audit.status === 'rejected')"
            variant="default"
            size="sm"
            class="bg-gradient-to-r from-primary to-primary-glow hover:shadow-hover"
            @click.stop="handleContinueAudit"
          >
            Continue Audit
          </Button>
          <Button 
            v-else-if="isMyReview && audit.status === 'under_review'"
            variant="default"
            size="sm"
            class="bg-gradient-to-r from-green-600 to-green-700 hover:shadow-hover"
            @click.stop="handleReviewAudit"
          >
            Review Audit
          </Button>
          <Button 
            v-else
            variant="outline"
            size="sm"
            @click.stop="handleViewDetails"
          >
            View Details
          </Button>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  User,
  Calendar,
  Clock,
  Eye,
  AlertTriangle,
  Target,
  Paperclip
} from 'lucide-vue-next'
import apiService from '@/services/api.js'
import Card from '@/components/ui/card.vue'
import CardHeader from '@/components/ui/card-header.vue'
import CardTitle from '@/components/ui/card-title.vue'
import CardDescription from '@/components/ui/card-description.vue'
import CardContent from '@/components/ui/card-content.vue'
import Button from '@/components/ui/button.vue'
import Badge from '@/components/ui/badge.vue'

const props = defineProps(['audit', 'currentUserId'])
const emit = defineEmits(['click'])

const router = useRouter()

const isOverdue = computed(() => 
  new Date(props.audit.due_date) < new Date() && props.audit.status !== 'completed'
)

const isMyAudit = computed(() => props.audit.auditor_id === props.currentUserId)
const isMyReview = computed(() => props.audit.reviewer_id === props.currentUserId)

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const formatStatusText = (status) => {
  if (!status) return 'UNKNOWN'
  
  // Convert underscores to spaces and uppercase
  return String(status)
    .replace(/_/g, ' ')
    .toUpperCase()
}

const getStatusBadgeClass = (status) => {
  if (!status) return 'badge-draft'
  
  const statusLower = String(status).toLowerCase()
  
  // Map audit statuses to badge classes
  if (statusLower === 'completed') {
    return 'badge-completed' // Green
  } else if (statusLower === 'rejected') {
    return 'badge-rejected' // Red
  } else if (statusLower === 'in_progress' || statusLower === 'in progress') {
    return 'badge-in-review' // Orange
  } else if (statusLower === 'under_review' || statusLower === 'under review') {
    return 'badge-in-review' // Orange
  } else if (statusLower === 'created') {
    return 'badge-created' // Blue
  }
  
  return 'badge-draft' // Default gray
}

const handleStartAudit = async () => {
  try {
    // Update audit status to in_progress
    await apiService.updateAudit(props.audit.audit_id, { status: 'in_progress' })
    router.push(`/audit/${props.audit.audit_id}`)
  } catch (error) {
    console.error('Error starting audit:', error)
    alert('Error starting audit. Please try again.')
  }
}

const handleContinueAudit = () => {
  router.push(`/audit/${props.audit.audit_id}`)
}

const handleReviewAudit = () => {
  router.push(`/audit/${props.audit.audit_id}/review`)
}

const handleViewDetails = () => {
  router.push(`/audit/${props.audit.audit_id}`)
}
</script>

<style scoped>
@import '@/assets/components/main.css';
@import '@/assets/components/badge.css';
</style>
