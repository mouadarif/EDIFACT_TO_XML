// EDI Document Types
export const DocumentType = {
  ORDERS: 'ORDERS',
  INVOIC: 'INVOIC',
  DESADV: 'DESADV',
  ORDRSP: 'ORDRSP'
};

export const DocumentTypeLabels = {
  [DocumentType.ORDERS]: 'Purchase Orders',
  [DocumentType.INVOIC]: 'Invoices',
  [DocumentType.DESADV]: 'Dispatch Advice',
  [DocumentType.ORDRSP]: 'Order Response'
};

export const DocumentTypeCodes = {
  [DocumentType.ORDERS]: '220',
  [DocumentType.INVOIC]: '380',
  [DocumentType.DESADV]: '351',
  [DocumentType.ORDRSP]: '231'
};

// Processing Status
export const ProcessingStatus = {
  PENDING: 'pending',
  PROCESSING: 'processing',
  COMPLETED: 'completed',
  ERROR: 'error',
  CANCELLED: 'cancelled'
};

export const ProcessingStatusLabels = {
  [ProcessingStatus.PENDING]: 'Pending',
  [ProcessingStatus.PROCESSING]: 'Processing',
  [ProcessingStatus.COMPLETED]: 'Completed',
  [ProcessingStatus.ERROR]: 'Error',
  [ProcessingStatus.CANCELLED]: 'Cancelled'
};

// Output Formats
export const OutputFormat = {
  XML: 'xml',
  JSON: 'json',
  CSV: 'csv'
};

export const OutputFormatLabels = {
  [OutputFormat.XML]: 'XML',
  [OutputFormat.JSON]: 'JSON',
  [OutputFormat.CSV]: 'CSV'
};

// Theme
export const Theme = {
  LIGHT: 'light',
  DARK: 'dark',
  SYSTEM: 'system'
};

// API Response Types
export const createApiResponse = (data, error = null, loading = false) => ({
  data,
  error,
  loading
});

export const createProcessingJob = (id, filename, documentType, status = ProcessingStatus.PENDING) => ({
  id,
  filename,
  documentType,
  status,
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  progress: 0,
  outputFiles: []
});

export const createCustomer = (id, name, gln, preferences = {}) => ({
  id,
  name,
  gln,
  preferences,
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString()
});

export const createDocumentTypeConfig = (type, code, name, segments = []) => ({
  type,
  code,
  name,
  segments,
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString()
});

// Validation helpers
export const validateGLN = (gln) => {
  if (!gln || typeof gln !== 'string') return false;
  return /^\d{13}$/.test(gln);
};

export const validateDocumentType = (type) => {
  return Object.values(DocumentType).includes(type);
};

export const validateOutputFormat = (format) => {
  return Object.values(OutputFormat).includes(format);
};

