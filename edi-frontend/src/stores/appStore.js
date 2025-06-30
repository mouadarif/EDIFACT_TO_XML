import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Theme, ProcessingStatus } from '../types';

const useAppStore = create(
  persist(
    (set, get) => ({
      // Theme Management
      theme: Theme.SYSTEM,
      setTheme: (theme) => set({ theme }),
      
      // Sidebar State
      sidebarCollapsed: false,
      setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
      
      // System Status
      systemStatus: 'unknown', // 'operational', 'warning', 'error', 'unknown'
      setSystemStatus: (status) => set({ systemStatus: status }),
      
      // Dashboard Data
      dashboardData: {
        health: null,
        documentTypes: [],
        customers: [],
        statistics: {
          totalProcessed: 0,
          successfulProcessed: 0,
          errorCount: 0,
          processingCount: 0
        }
      },
      setDashboardData: (data) => set({ dashboardData: data }),
      
      // Document Types
      documentTypes: [],
      setDocumentTypes: (types) => set({ documentTypes: types }),
      addDocumentType: (type) => set((state) => ({
        documentTypes: [...state.documentTypes, type]
      })),
      updateDocumentType: (id, updatedType) => set((state) => ({
        documentTypes: state.documentTypes.map(type => 
          type.id === id ? { ...type, ...updatedType } : type
        )
      })),
      removeDocumentType: (id) => set((state) => ({
        documentTypes: state.documentTypes.filter(type => type.id !== id)
      })),
      
      // Customers
      customers: [],
      setCustomers: (customers) => set({ customers }),
      addCustomer: (customer) => set((state) => ({
        customers: [...state.customers, customer]
      })),
      updateCustomer: (id, updatedCustomer) => set((state) => ({
        customers: state.customers.map(customer => 
          customer.id === id ? { ...customer, ...updatedCustomer } : customer
        )
      })),
      removeCustomer: (id) => set((state) => ({
        customers: state.customers.filter(customer => customer.id !== id)
      })),
      
      // Processing Jobs
      processingJobs: [],
      setProcessingJobs: (jobs) => set({ processingJobs: jobs }),
      addProcessingJob: (job) => set((state) => ({
        processingJobs: [...state.processingJobs, job]
      })),
      updateProcessingJob: (id, updatedJob) => set((state) => ({
        processingJobs: state.processingJobs.map(job => 
          job.id === id ? { ...job, ...updatedJob } : job
        )
      })),
      removeProcessingJob: (id) => set((state) => ({
        processingJobs: state.processingJobs.filter(job => job.id !== id)
      })),
      
      // Processing Configuration
      processingConfig: {
        documentType: 'ORDERS',
        outputFormat: 'xml',
        batchSize: 10,
        customerId: null
      },
      setProcessingConfig: (config) => set((state) => ({
        processingConfig: { ...state.processingConfig, ...config }
      })),
      
      // UI State
      loading: {
        dashboard: false,
        documentTypes: false,
        customers: false,
        processing: false
      },
      setLoading: (key, value) => set((state) => ({
        loading: { ...state.loading, [key]: value }
      })),
      
      // Error State
      errors: {},
      setError: (key, error) => set((state) => ({
        errors: { ...state.errors, [key]: error }
      })),
      clearError: (key) => set((state) => {
        const { [key]: removed, ...rest } = state.errors;
        return { errors: rest };
      }),
      clearAllErrors: () => set({ errors: {} }),
      
      // Notifications
      notifications: [],
      addNotification: (notification) => {
        const id = Date.now().toString();
        const newNotification = {
          id,
          type: 'info',
          duration: 5000,
          ...notification,
          timestamp: new Date().toISOString()
        };
        set((state) => ({
          notifications: [...state.notifications, newNotification]
        }));
        
        // Auto-remove notification after duration
        if (newNotification.duration > 0) {
          setTimeout(() => {
            get().removeNotification(id);
          }, newNotification.duration);
        }
        
        return id;
      },
      removeNotification: (id) => set((state) => ({
        notifications: state.notifications.filter(n => n.id !== id)
      })),
      clearNotifications: () => set({ notifications: [] }),
      
      // Search and Filters
      searchQuery: '',
      setSearchQuery: (query) => set({ searchQuery: query }),
      
      filters: {
        documentType: null,
        status: null,
        dateRange: null
      },
      setFilter: (key, value) => set((state) => ({
        filters: { ...state.filters, [key]: value }
      })),
      clearFilters: () => set({
        filters: {
          documentType: null,
          status: null,
          dateRange: null
        }
      }),
      
      // Statistics
      statistics: {
        totalProcessed: 0,
        successfulProcessed: 0,
        errorCount: 0,
        processingCount: 0,
        averageProcessingTime: 0,
        lastProcessedAt: null
      },
      setStatistics: (stats) => set({ statistics: stats }),
      
      // User Preferences
      preferences: {
        autoRefresh: true,
        refreshInterval: 30000, // 30 seconds
        showNotifications: true,
        compactView: false,
        defaultOutputFormat: 'xml',
        defaultBatchSize: 10
      },
      setPreference: (key, value) => set((state) => ({
        preferences: { ...state.preferences, [key]: value }
      })),
      
      // Actions
      resetStore: () => set({
        documentTypes: [],
        customers: [],
        processingJobs: [],
        errors: {},
        notifications: [],
        searchQuery: '',
        filters: {
          documentType: null,
          status: null,
          dateRange: null
        }
      })
    }),
    {
      name: 'edi-app-store',
      partialize: (state) => ({
        theme: state.theme,
        sidebarCollapsed: state.sidebarCollapsed,
        processingConfig: state.processingConfig,
        preferences: state.preferences
      })
    }
  )
);

export default useAppStore;

