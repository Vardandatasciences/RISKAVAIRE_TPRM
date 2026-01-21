<template>
  <div class="add-vendor-container">
    <!-- Header -->
    <div class="add-vendor-header">
      <div>
        <h1 class="add-vendor-title">Add Vendors</h1>
        <p class="add-vendor-subtitle">Add one or more vendors to the system</p>
      </div>
      <div class="add-vendor-action-buttons">
        <button 
          class="btn btn-outline" 
          @click="addNewVendorForm"
          :disabled="isSubmitting"
          title="Add another vendor form"
        >
          <i class="fas fa-plus mr-2"></i>
          Add Another Vendor
        </button>
        <button 
          class="btn btn-primary" 
          @click="submitAllVendors" 
          :disabled="isSubmitting || vendorForms.length === 0"
          title="Submit all vendors"
        >
          <i class="fas fa-check mr-2"></i>
          {{ isSubmitting ? 'Submitting...' : `Submit ${vendorForms.length} Vendor${vendorForms.length !== 1 ? 's' : ''}` }}
        </button>
      </div>
    </div>

    <!-- Vendor Forms List -->
    <div class="vendor-forms-container">
      <div v-for="(vendorForm, index) in vendorForms" :key="vendorForm.id" class="vendor-form-card">
        <div class="vendor-form-header">
          <div class="vendor-form-title">
            <h3>Vendor #{{ index + 1 }}</h3>
            <span v-if="vendorForm.submitted" class="badge badge-success">Submitted</span>
            <span v-else-if="vendorForm.errors && Object.keys(vendorForm.errors).length > 0" class="badge badge-error">Has Errors</span>
          </div>
          <div class="vendor-form-actions">
            <button 
              v-if="vendorForms.length > 1"
              class="btn btn-danger btn-sm" 
              @click="removeVendorForm(vendorForm.id)"
              title="Remove this vendor form"
            >
              <i class="fas fa-trash"></i>
              Remove
            </button>
          </div>
        </div>

        <!-- Error Messages -->
        <div v-if="vendorForm.errors && Object.keys(vendorForm.errors).length > 0" class="error-messages">
          <div v-for="(error, field) in vendorForm.errors" :key="field" class="error-message">
            <i class="fas fa-exclamation-circle mr-1"></i>
            <strong>{{ formatFieldName(field) }}:</strong> {{ Array.isArray(error) ? error.join(', ') : error }}
          </div>
        </div>

        <!-- Vendor Form Content -->
        <div class="vendor-form-content">
          <!-- Tabs -->
          <div class="tabs">
            <button 
              v-for="tab in tabs" 
              :key="tab.id"
              class="tab-trigger"
              :class="{ 'tab-trigger-active': vendorForm.activeTab === tab.id }"
              @click="vendorForm.activeTab = tab.id"
            >
              {{ tab.label }}
            </button>
          </div>

          <!-- Company Info Tab -->
          <div v-if="vendorForm.activeTab === 'company-info'" class="tab-content">
            <div class="form-grid">
              <div class="form-item">
                <label for="vendor-code" class="form-label">Vendor Code</label>
                <input 
                  id="vendor-code" 
                  class="input" 
                  v-model="vendorForm.data.vendor_code"
                  placeholder="Enter vendor code"
                />
              </div>
              <div class="form-item">
                <label for="company-name" class="form-label">Company Name *</label>
                <input 
                  id="company-name" 
                  class="input" 
                  v-model="vendorForm.data.company_name" 
                  required
                  placeholder="Enter company name"
                />
              </div>
              <div class="form-item">
                <label for="legal-name" class="form-label">Legal Name</label>
                <input 
                  id="legal-name" 
                  class="input" 
                  v-model="vendorForm.data.legal_name"
                  placeholder="Enter legal name"
                />
              </div>
              <div class="form-item">
                <label for="business-type" class="form-label">Business Type</label>
                <select id="business-type" class="select" v-model="vendorForm.data.business_type">
                  <option value="">Select business type</option>
                  <option value="corporation">Corporation</option>
                  <option value="llc">LLC</option>
                  <option value="partnership">Partnership</option>
                  <option value="sole-proprietorship">Sole Proprietorship</option>
                </select>
              </div>
              <div class="form-item">
                <label for="tax-id" class="form-label">Tax ID</label>
                <input 
                  id="tax-id" 
                  class="input" 
                  v-model="vendorForm.data.tax_id"
                  placeholder="Enter tax ID"
                />
              </div>
              <div class="form-item">
                <label for="duns-number" class="form-label">DUNS Number</label>
                <input 
                  id="duns-number" 
                  class="input" 
                  v-model="vendorForm.data.duns_number"
                  placeholder="Enter DUNS number"
                />
              </div>
            </div>
          </div>

          <!-- Legal & Financial Tab -->
          <div v-if="vendorForm.activeTab === 'legal-financial'" class="tab-content">
            <div class="form-grid">
              <div class="form-item">
                <label for="incorporation-date" class="form-label">Incorporation Date</label>
                <input 
                  id="incorporation-date" 
                  class="input" 
                  type="date" 
                  v-model="vendorForm.data.incorporation_date"
                />
              </div>
              <div class="form-item">
                <label for="industry-sector" class="form-label">Industry Sector</label>
                <select id="industry-sector" class="select" v-model="vendorForm.data.industry_sector">
                  <option value="">Select industry</option>
                  <option value="technology">Technology</option>
                  <option value="finance">Finance</option>
                  <option value="healthcare">Healthcare</option>
                  <option value="manufacturing">Manufacturing</option>
                  <option value="retail">Retail</option>
                </select>
              </div>
              <div class="form-item">
                <label for="website" class="form-label">Website</label>
                <input 
                  id="website" 
                  class="input" 
                  v-model="vendorForm.data.website"
                  placeholder="https://example.com"
                />
              </div>
              <div class="form-item">
                <label for="annual-revenue" class="form-label">Annual Revenue</label>
                <input 
                  id="annual-revenue" 
                  class="input" 
                  type="number" 
                  step="0.01"
                  v-model.number="vendorForm.data.annual_revenue"
                  placeholder="1000000"
                />
              </div>
              <div class="form-item">
                <label for="employee-count" class="form-label">Employee Count</label>
                <input 
                  id="employee-count" 
                  class="input" 
                  type="number"
                  v-model.number="vendorForm.data.employee_count"
                  placeholder="100"
                />
              </div>
              <div class="form-item form-item-full">
                <label for="headquarters-address" class="form-label">Headquarters Address</label>
                <textarea 
                  id="headquarters-address" 
                  class="textarea" 
                  v-model="vendorForm.data.headquarters_address"
                  placeholder="123 Main St, City, State, ZIP"
                  rows="3"
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Category & Risk Tab -->
          <div v-if="vendorForm.activeTab === 'category-risk'" class="tab-content">
            <div class="form-grid">
              <div class="form-item">
                <label for="vendor-category" class="form-label">Vendor Category</label>
                <select id="vendor-category" class="select" v-model="vendorForm.data.vendor_category">
                  <option value="">Select category</option>
                  <option value="software">Software</option>
                  <option value="services">Services</option>
                  <option value="consulting">Consulting</option>
                  <option value="hardware">Hardware</option>
                  <option value="maintenance">Maintenance</option>
                </select>
              </div>
              <div class="form-item">
                <label for="risk-level" class="form-label">Risk Level</label>
                <select id="risk-level" class="select" v-model="vendorForm.data.risk_level">
                  <option value="">Select risk level</option>
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
              <div class="form-item">
                <label for="status" class="form-label">Status</label>
                <select id="status" class="select" v-model="vendorForm.data.status">
                  <option value="pending">Pending</option>
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                  <option value="suspended">Suspended</option>
                </select>
              </div>
              <div class="form-item form-item-full">
                <div class="checkbox-group">
                  <label class="checkbox-label">
                    <input 
                      type="checkbox" 
                      class="checkbox" 
                      v-model="vendorForm.data.is_critical_vendor"
                    />
                    <span>Is Critical Vendor</span>
                  </label>
                  <label class="checkbox-label">
                    <input 
                      type="checkbox" 
                      class="checkbox" 
                      v-model="vendorForm.data.has_data_access"
                    />
                    <span>Has Data Access</span>
                  </label>
                  <label class="checkbox-label">
                    <input 
                      type="checkbox" 
                      class="checkbox" 
                      v-model="vendorForm.data.has_system_access"
                    />
                    <span>Has System Access</span>
                  </label>
                </div>
              </div>
              <div class="form-item form-item-full">
                <label for="description" class="form-label">Description</label>
                <textarea 
                  id="description" 
                  class="textarea"
                  v-model="vendorForm.data.description"
                  placeholder="Vendor description and notes..."
                  rows="4"
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Contacts Tab -->
          <div v-if="vendorForm.activeTab === 'contacts'" class="tab-content">
            <div class="contacts-section">
              <div class="section-header">
                <h4>Vendor Contacts</h4>
                <button 
                  class="btn btn-primary btn-sm" 
                  @click="addContact(vendorForm.id)"
                  title="Add new contact"
                >
                  <i class="fas fa-plus mr-1"></i>
                  Add Contact
                </button>
              </div>
              <div v-if="vendorForm.contacts.length === 0" class="empty-state">
                <i class="fas fa-users empty-icon"></i>
                <p>No contacts added. Click "Add Contact" to add one.</p>
              </div>
              <div v-for="contact in vendorForm.contacts" :key="contact.id" class="contact-card">
                <div v-if="contact.isEditing" class="contact-edit">
                  <div class="form-grid">
                    <div class="form-item">
                      <label class="form-label">Name</label>
                      <input v-model="contact.name" class="input" placeholder="Contact Name" />
                    </div>
                    <div class="form-item">
                      <label class="form-label">Email</label>
                      <input v-model="contact.email" class="input" type="email" placeholder="contact@example.com" />
                    </div>
                    <div class="form-item">
                      <label class="form-label">Phone</label>
                      <input v-model="contact.phone" class="input" placeholder="+1-555-0000" />
                    </div>
                    <div class="form-item">
                      <label class="form-label">Role</label>
                      <input v-model="contact.role" class="input" placeholder="Contact Role" />
                    </div>
                  </div>
                  <div class="contact-actions">
                    <label class="checkbox-label">
                      <input type="checkbox" v-model="contact.isPrimary" class="checkbox" />
                      <span>Primary Contact</span>
                    </label>
                    <div>
                      <button class="btn btn-primary btn-sm" @click="saveContact(vendorForm.id, contact.id)">Save</button>
                      <button class="btn btn-outline btn-sm" @click="cancelEditContact(vendorForm.id, contact.id)">Cancel</button>
                    </div>
                  </div>
                </div>
                <div v-else class="contact-view">
                  <div class="contact-info">
                    <h5>{{ contact.name }}</h5>
                    <span v-if="contact.isPrimary" class="badge badge-secondary">Primary</span>
                  </div>
                  <p class="contact-details">{{ contact.email }} • {{ contact.phone }}</p>
                  <p class="contact-role">{{ contact.role }}</p>
                  <div class="contact-actions">
                    <button 
                      class="btn btn-ghost btn-sm" 
                      @click="editContact(vendorForm.id, contact.id)"
                      title="Edit contact"
                    >
                      <i class="fas fa-edit"></i>
                    </button>
                    <button 
                      class="btn btn-ghost btn-sm" 
                      @click="removeContact(vendorForm.id, contact.id)"
                      title="Delete contact"
                    >
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Documents Tab -->
          <div v-if="vendorForm.activeTab === 'documents'" class="tab-content">
            <div class="documents-section">
              <div class="section-header">
                <h4>Vendor Documents</h4>
                <button 
                  class="btn btn-primary btn-sm" 
                  @click="addDocument(vendorForm.id)"
                  title="Upload new document"
                >
                  <i class="fas fa-upload mr-1"></i>
                  Upload Document
                </button>
              </div>
              <div v-if="vendorForm.documents.length === 0" class="empty-state">
                <i class="fas fa-file empty-icon"></i>
                <p>No documents added. Click "Upload Document" to add one.</p>
              </div>
              <div v-for="doc in vendorForm.documents" :key="doc.id" class="document-card">
                <div v-if="doc.isEditing" class="document-edit">
                  <div class="form-grid">
                    <div class="form-item">
                      <label class="form-label">Document Name</label>
                      <input v-model="doc.name" class="input" placeholder="Document Name" />
                    </div>
                    <div class="form-item">
                      <label class="form-label">Document Type</label>
                      <select v-model="doc.type" class="select">
                        <option value="">Select type</option>
                        <option value="License">License</option>
                        <option value="Certificate">Certificate</option>
                        <option value="Contract">Contract</option>
                        <option value="Insurance">Insurance</option>
                        <option value="Other">Other</option>
                      </select>
                    </div>
                    <div class="form-item">
                      <label class="form-label">Version</label>
                      <input v-model="doc.version" class="input" placeholder="1.0" />
                    </div>
                    <div class="form-item">
                      <label class="form-label">Status</label>
                      <select v-model="doc.status" class="select">
                        <option value="Pending">Pending</option>
                        <option value="Approved">Approved</option>
                        <option value="Rejected">Rejected</option>
                        <option value="Expired">Expired</option>
                      </select>
                    </div>
                    <div class="form-item">
                      <label class="form-label">Expiry Date</label>
                      <input v-model="doc.expiryDate" class="input" type="date" />
                    </div>
                    <div class="form-item">
                      <label class="form-label">File Upload</label>
                      <input 
                        type="file" 
                        class="input" 
                        @change="handleFileUpload($event, vendorForm.id, doc.id)"
                        accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.xlsx,.xls"
                      />
                      <div v-if="doc.fileName" class="file-info">
                        <small>Selected: {{ doc.fileName }}</small>
                      </div>
                    </div>
                  </div>
                  <div class="document-actions">
                    <button class="btn btn-primary btn-sm" @click="saveDocument(vendorForm.id, doc.id)">Save</button>
                    <button class="btn btn-outline btn-sm" @click="cancelEditDocument(vendorForm.id, doc.id)">Cancel</button>
                  </div>
                </div>
                <div v-else class="document-view">
                  <div class="document-info">
                    <h5>{{ doc.name || 'Untitled Document' }}</h5>
                    <span class="badge" :class="getDocumentStatusClass(doc.status)">
                      {{ doc.status }}
                    </span>
                  </div>
                  <p class="document-details">{{ doc.type }} • Version {{ doc.version || 'N/A' }}</p>
                  <p v-if="doc.expiryDate" class="document-meta">Expires: {{ doc.expiryDate }}</p>
                  <div class="document-actions">
                    <button 
                      class="btn btn-ghost btn-sm" 
                      @click="editDocument(vendorForm.id, doc.id)"
                      title="Edit document"
                    >
                      <i class="fas fa-edit"></i>
                    </button>
                    <button 
                      class="btn btn-ghost btn-sm" 
                      @click="removeDocument(vendorForm.id, doc.id)"
                      title="Delete document"
                    >
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="vendorForms.length === 0" class="empty-vendor-state">
        <i class="fas fa-building empty-icon"></i>
        <h3>No Vendors Added</h3>
        <p>Click "Add Another Vendor" to start adding vendors to the system.</p>
        <button class="btn btn-primary" @click="addNewVendorForm">
          <i class="fas fa-plus mr-2"></i>
          Add First Vendor
        </button>
      </div>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="submitMessage" class="submit-message" :class="submitMessage.type">
      <i :class="submitMessage.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
      <span>{{ submitMessage.text }}</span>
      <button @click="submitMessage = null" class="close-btn">
        <i class="fas fa-times"></i>
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '@/utils/api'
import { getTprmApiUrl } from '@/utils/backendEnv'

export default {
  name: 'AddVendor',
  setup() {
    const vendorForms = ref([])
    const isSubmitting = ref(false)
    const submitMessage = ref(null)

    const tabs = [
      { id: 'company-info', label: 'Company Info' },
      { id: 'legal-financial', label: 'Legal & Financial' },
      { id: 'category-risk', label: 'Category & Risk' },
      { id: 'contacts', label: 'Contacts' },
      { id: 'documents', label: 'Documents' }
    ]

    // Create default vendor form data structure
    const createDefaultVendorForm = () => {
      const formId = Date.now().toString() + Math.random().toString(36).substr(2, 9)
      return {
        id: formId,
        activeTab: 'company-info',
        submitted: false,
        errors: {},
        data: {
          vendor_code: '',
          company_name: '',
          legal_name: '',
          business_type: '',
          tax_id: '',
          duns_number: '',
          incorporation_date: '',
          industry_sector: '',
          website: '',
          annual_revenue: null,
          employee_count: null,
          headquarters_address: '',
          vendor_category: '',
          risk_level: '',
          status: 'pending',
          is_critical_vendor: false,
          has_data_access: false,
          has_system_access: false,
          description: '',
          contacts: [],
          documents: []
        },
        contacts: [],
        documents: []
      }
    }

    // Add new vendor form
    const addNewVendorForm = () => {
      vendorForms.value.push(createDefaultVendorForm())
    }

    // Remove vendor form
    const removeVendorForm = (formId) => {
      vendorForms.value = vendorForms.value.filter(form => form.id !== formId)
    }

    // Add contact to vendor form
    const addContact = (formId) => {
      const form = vendorForms.value.find(f => f.id === formId)
      if (form) {
        const contactId = Date.now().toString() + Math.random().toString(36).substr(2, 9)
        form.contacts.push({
          id: contactId,
          name: '',
          email: '',
          phone: '',
          role: '',
          isPrimary: false,
          isEditing: true
        })
      }
    }

    // Save contact
    const saveContact = (formId, contactId) => {
      const form = vendorForms.value.find(f => f.id === formId)
      if (form) {
        const contact = form.contacts.find(c => c.id === contactId)
        if (contact) {
          contact.isEditing = false
        }
      }
    }

    // Cancel edit contact
    const cancelEditContact = (formId, contactId) => {
      const form = vendorForms.value.find(f => f.id === formId)
      if (form) {
        const contact = form.contacts.find(c => c.id === contactId)
        if (contact) {
          if (!contact.name && !contact.email) {
            // New contact with no data - remove it
            removeContact(formId, contactId)
          } else {
            contact.isEditing = false
          }
        }
      }
    }

    // Edit contact
    const editContact = (formId, contactId) => {
      const form = vendorForms.value.find(f => f.id === formId)
      if (form) {
        const contact = form.contacts.find(c => c.id === contactId)
        if (contact) {
          contact.isEditing = true
        }
      }
    }

    // Remove contact
    const removeContact = (formId, contactId) => {
      const form = vendorForms.value.find(f => f.id === formId)
      if (form) {
        form.contacts = form.contacts.filter(c => c.id !== contactId)
      }
    }

    // Add document to vendor form
    const addDocument = (formId) => {
      const form = vendorForms.value.find(f => f.id === formId)
      if (form) {
        const docId = Date.now().toString() + Math.random().toString(36).substr(2, 9)
        form.documents.push({
          id: docId,
          name: '',
          type: '',
          version: '',
          status: 'Pending',
          expiryDate: '',
          fileName: '',
          file: null,
          isEditing: true
        })
      }
    }

    // Handle file upload
    const handleFileUpload = (event, formId, docId) => {
      const form = vendorForms.value.find(f => f.id === formId)
      if (form) {
        const doc = form.documents.find(d => d.id === docId)
        if (doc) {
          const file = event.target.files[0]
          if (file) {
            // Validate file size (max 100MB)
            const maxSize = 100 * 1024 * 1024
            if (file.size > maxSize) {
              showMessage('error', 'File size cannot exceed 100MB')
              event.target.value = ''
              return
            }
            
            doc.file = file
            doc.fileName = file.name
            if (!doc.name) {
              doc.name = file.name
            }
          }
        }
      }
    }

    // Save document
    const saveDocument = (formId, docId) => {
      const form = vendorForms.value.find(f => f.id === formId)
      if (form) {
        const doc = form.documents.find(d => d.id === docId)
        if (doc) {
          doc.isEditing = false
        }
      }
    }

    // Cancel edit document
    const cancelEditDocument = (formId, docId) => {
      const form = vendorForms.value.find(f => f.id === formId)
      if (form) {
        const doc = form.documents.find(d => d.id === docId)
        if (doc) {
          if (!doc.name && !doc.file) {
            // New document with no data - remove it
            removeDocument(formId, docId)
          } else {
            doc.isEditing = false
          }
        }
      }
    }

    // Edit document
    const editDocument = (formId, docId) => {
      const form = vendorForms.value.find(f => f.id === formId)
      if (form) {
        const doc = form.documents.find(d => d.id === docId)
        if (doc) {
          doc.isEditing = true
        }
      }
    }

    // Remove document
    const removeDocument = (formId, docId) => {
      const form = vendorForms.value.find(f => f.id === formId)
      if (form) {
        form.documents = form.documents.filter(d => d.id !== docId)
      }
    }

    // Get document status class
    const getDocumentStatusClass = (status) => {
      switch (status) {
        case 'Approved': return 'badge-success'
        case 'Pending': return 'badge-warning'
        case 'Rejected': return 'badge-error'
        default: return 'badge-default'
      }
    }

    // Format field name for error messages
    const formatFieldName = (fieldName) => {
      return fieldName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
    }

    // Show message
    const showMessage = (type, text) => {
      submitMessage.value = { type, text }
      setTimeout(() => {
        submitMessage.value = null
      }, 5000)
    }

    // Validate vendor form
    const validateVendorForm = (form) => {
      const errors = {}
      
      if (!form.data.company_name || form.data.company_name.trim() === '') {
        errors.company_name = 'Company name is required'
      }

      return errors
    }

    // Submit all vendors
    const submitAllVendors = async () => {
      if (vendorForms.value.length === 0) {
        showMessage('error', 'Please add at least one vendor before submitting.')
        return
      }

      isSubmitting.value = true
      let successCount = 0
      let errorCount = 0
      const errors = []

      try {
        // Validate all forms first
        for (const form of vendorForms.value) {
          form.errors = validateVendorForm(form)
          if (Object.keys(form.errors).length > 0) {
            errorCount++
          }
        }

        if (errorCount > 0) {
          showMessage('error', `Please fix errors in ${errorCount} vendor form${errorCount !== 1 ? 's' : ''} before submitting.`)
          isSubmitting.value = false
          return
        }

        // Get user ID from localStorage
        const userId = localStorage.getItem('user_id') || localStorage.getItem('userId')
        if (!userId) {
          showMessage('error', 'User ID not found. Please log in again.')
          isSubmitting.value = false
          return
        }

        // Submit each vendor form
        for (const form of vendorForms.value) {
          try {
            // Prepare vendor data
            const vendorData = {
              ...form.data,
              UserId: parseInt(userId),
              annual_revenue: form.data.annual_revenue === '' || form.data.annual_revenue === null ? null : Number(form.data.annual_revenue),
              employee_count: form.data.employee_count === '' || form.data.employee_count === null ? null : Number(form.data.employee_count),
              contacts: form.contacts.map(c => ({
                name: c.name,
                email: c.email,
                phone: c.phone,
                role: c.role,
                isPrimary: c.isPrimary
              })),
              documents: form.documents.map(d => ({
                name: d.name,
                type: d.type,
                version: d.version,
                status: d.status,
                expiry_date: d.expiryDate || null,
                document_name: d.name,
                document_type: d.type
              })),
              status: form.data.status || 'pending'
            }

            // Submit to API using tprm_frontend's api instance which handles JWT authentication
            const response = await api.post(
              getTprmApiUrl('v1/vendor-core/temp-vendors/'),
              vendorData
            )

            if (response.data && (response.data.status === 'success' || response.status === 201)) {
              form.submitted = true
              successCount++
            } else {
              form.errors = { general: response.data?.message || 'Failed to submit vendor' }
              errorCount++
            }
          } catch (error) {
            console.error('Error submitting vendor:', error)
            const errorMessage = error.response?.data?.message || error.response?.data?.error || error.message || 'Failed to submit vendor'
            form.errors = { general: errorMessage }
            errors.push(errorMessage)
            errorCount++
          }
        }

        // Show result message
        if (successCount > 0 && errorCount === 0) {
          showMessage('success', `Successfully submitted ${successCount} vendor${successCount !== 1 ? 's' : ''}!`)
          // Optionally clear forms after successful submission
          setTimeout(() => {
            vendorForms.value = vendorForms.value.filter(f => !f.submitted)
            if (vendorForms.value.length === 0) {
              addNewVendorForm()
            }
          }, 2000)
        } else if (successCount > 0 && errorCount > 0) {
          showMessage('warning', `Submitted ${successCount} vendor${successCount !== 1 ? 's' : ''} successfully, but ${errorCount} failed.`)
        } else {
          showMessage('error', `Failed to submit ${errorCount} vendor${errorCount !== 1 ? 's' : ''}. Please check the errors and try again.`)
        }
      } catch (error) {
        console.error('Error in submitAllVendors:', error)
        showMessage('error', 'An error occurred while submitting vendors. Please try again.')
      } finally {
        isSubmitting.value = false
      }
    }

    // Initialize with one empty form
    onMounted(() => {
      addNewVendorForm()
    })

    return {
      vendorForms,
      isSubmitting,
      submitMessage,
      tabs,
      addNewVendorForm,
      removeVendorForm,
      addContact,
      saveContact,
      cancelEditContact,
      editContact,
      removeContact,
      addDocument,
      handleFileUpload,
      saveDocument,
      cancelEditDocument,
      editDocument,
      removeDocument,
      getDocumentStatusClass,
      formatFieldName,
      submitAllVendors
    }
  }
}
</script>

<style scoped>
.add-vendor-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 1rem;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.add-vendor-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e5e7eb;
  flex-wrap: wrap;
  gap: 1rem;
}

.add-vendor-title {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.add-vendor-subtitle {
  font-size: 1rem;
  color: #6b7280;
  margin: 0.5rem 0 0 0;
}

.add-vendor-action-buttons {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-wrap: wrap;
}

.vendor-forms-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.vendor-form-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.vendor-form-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background-color: #f9fafb;
}

.vendor-form-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.vendor-form-title h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
}

.vendor-form-actions {
  display: flex;
  gap: 0.5rem;
}

.vendor-form-content {
  padding: 1.5rem;
}

.error-messages {
  margin: 1rem 1.5rem;
  padding: 1rem;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 0.375rem;
}

.error-message {
  color: #991b1b;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.error-message:last-child {
  margin-bottom: 0;
}

/* Tabs */
.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.tab-trigger {
  padding: 0.75rem 1.5rem;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  color: #6b7280;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-trigger:hover {
  color: #111827;
  background-color: #f3f4f6;
}

.tab-trigger-active {
  color: #3b82f6;
  border-bottom-color: #3b82f6;
}

.tab-content {
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Form Styles */
.form-grid {
  display: grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .form-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-item-full {
  grid-column: 1 / -1;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #111827;
}

.input,
.select,
.textarea {
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  transition: all 0.2s;
  width: 100%;
  box-sizing: border-box;
}

.input:focus,
.select:focus,
.textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.textarea {
  resize: vertical;
  min-height: 80px;
}

.select {
  cursor: pointer;
}

/* Checkbox */
.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox {
  width: 1rem;
  height: 1rem;
  cursor: pointer;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2563eb;
}

.btn-outline {
  background-color: transparent;
  color: #111827;
  border-color: #e5e7eb;
}

.btn-outline:hover:not(:disabled) {
  background-color: #f3f4f6;
}

.btn-danger {
  background-color: #ef4444;
  color: white;
  border-color: #ef4444;
}

.btn-danger:hover:not(:disabled) {
  background-color: #dc2626;
}

.btn-ghost {
  background-color: transparent;
  color: #6b7280;
  border: none;
  padding: 0.5rem;
}

.btn-ghost:hover:not(:disabled) {
  background-color: #f3f4f6;
  color: #111827;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.75rem;
}

.mr-1 { margin-right: 0.25rem; }
.mr-2 { margin-right: 0.5rem; }

/* Badges */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
  border-radius: 9999px;
}

.badge-success {
  background-color: #dcfce7;
  color: #166534;
}

.badge-error {
  background-color: #fee2e2;
  color: #991b1b;
}

.badge-secondary {
  background-color: #e5e7eb;
  color: #374151;
}

.badge-warning {
  background-color: #fef3c7;
  color: #92400e;
}

.badge-default {
  background-color: #f3f4f6;
  color: #374151;
}

/* Contacts Section */
.contacts-section,
.documents-section {
  margin-top: 1rem;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.section-header h4 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
}

.contact-card,
.document-card {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  padding: 1.5rem;
  margin-bottom: 1rem;
}

.contact-info,
.document-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.contact-info h5,
.document-info h5 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
}

.contact-details,
.document-details {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0.25rem 0;
}

.contact-role,
.document-meta {
  font-size: 0.75rem;
  color: #9ca3af;
  margin: 0.25rem 0;
}

.contact-actions,
.document-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
  gap: 0.5rem;
}

.contact-edit,
.document-edit {
  padding: 1rem;
  background: white;
  border-radius: 0.375rem;
}

/* Empty State */
.empty-state,
.empty-vendor-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  text-align: center;
  color: #6b7280;
}

.empty-vendor-state {
  background: white;
  border: 2px dashed #e5e7eb;
  border-radius: 0.5rem;
  margin: 2rem 0;
}

.empty-icon {
  font-size: 3rem;
  color: #cbd5e1;
  margin-bottom: 1rem;
}

.empty-state p,
.empty-vendor-state p {
  margin: 0.5rem 0;
}

.file-info {
  margin-top: 0.5rem;
  padding: 0.5rem;
  background-color: #f3f4f6;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  color: #6b7280;
}

/* Submit Message */
.submit-message {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  max-width: 400px;
}

.submit-message.success {
  background-color: #dcfce7;
  color: #166534;
  border: 1px solid #86efac;
}

.submit-message.error {
  background-color: #fee2e2;
  color: #991b1b;
  border: 1px solid #fca5a5;
}

.submit-message.warning {
  background-color: #fef3c7;
  color: #92400e;
  border: 1px solid #fde68a;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: inherit;
  padding: 0.25rem;
  margin-left: auto;
}

/* Responsive */
@media (max-width: 768px) {
  .add-vendor-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .add-vendor-action-buttons {
    width: 100%;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .submit-message {
    right: 1rem;
    left: 1rem;
    max-width: none;
  }
}
</style>

