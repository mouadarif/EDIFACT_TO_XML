const API_BASE_URL = 'http://localhost:5001';

class ApiService {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // System endpoints
  async getHealth() {
    return this.request('/api/health');
  }

  async getSystemInfo() {
    return this.request('/api/system/info');
  }

  async getStatistics() {
    return this.request('/api/statistics');
  }

  // Document Types
  async getDocumentTypes() {
    return this.request('/api/edi/document-types');
  }

  async createDocumentType(data) {
    return this.request('/api/edi/document-types', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Customers
  async getCustomers() {
    return this.request('/api/edi/customers');
  }

  async createCustomer(data) {
    return this.request('/api/edi/customers', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Processing
  async uploadFiles(files, documentType = 'ORDERS', outputFormat = 'xml') {
    const formData = new FormData();
    
    files.forEach(file => {
      formData.append('files', file);
    });
    
    formData.append('documentType', documentType);
    formData.append('outputFormat', outputFormat);

    return this.request('/api/processing/upload', {
      method: 'POST',
      body: formData,
      headers: {}, // Let browser set Content-Type for FormData
    });
  }

  async getProcessingJobs() {
    return this.request('/api/processing/jobs');
  }
}

export const apiService = new ApiService();
export default apiService;

