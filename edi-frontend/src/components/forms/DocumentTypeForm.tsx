import React, { useState, useEffect } from 'react';
import { XMarkIcon } from '@heroicons/react/24/outline';
import useAppStore from '../../stores/appStore';
import { DocumentType, DocumentTypeCodes, createDocumentTypeConfig } from '../../types';

export const DocumentTypeForm = ({ documentType, onClose }) => {
  const [formData, setFormData] = useState({
    type: DocumentType.ORDERS,
    code: DocumentTypeCodes[DocumentType.ORDERS],
    name: '',
    description: '',
    segments: []
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { addDocumentType, updateDocumentType, addNotification } = useAppStore();

  useEffect(() => {
    if (documentType) {
      setFormData({
        type: documentType.type || DocumentType.ORDERS,
        code: documentType.code || DocumentTypeCodes[DocumentType.ORDERS],
        name: documentType.name || '',
        description: documentType.description || '',
        segments: documentType.segments || []
      });
    }
  }, [documentType]);

  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!formData.type) {
      newErrors.type = 'Document type is required';
    }

    if (!formData.code) {
      newErrors.code = 'Code is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      const docTypeData = createDocumentTypeConfig(
        formData.type,
        formData.code,
        formData.name,
        formData.segments
      );

      if (documentType) {
        // Update existing
        updateDocumentType(documentType.id, {
          ...docTypeData,
          description: formData.description
        });
        addNotification({
          type: 'success',
          message: 'Document type updated successfully'
        });
      } else {
        // Create new
        addDocumentType({
          ...docTypeData,
          id: Date.now(),
          description: formData.description
        });
        addNotification({
          type: 'success',
          message: 'Document type created successfully'
        });
      }

      onClose();
    } catch (error) {
      addNotification({
        type: 'error',
        message: 'Failed to save document type'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleTypeChange = (type) => {
    setFormData({
      ...formData,
      type,
      code: DocumentTypeCodes[type] || ''
    });
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white dark:bg-gray-800">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
            {documentType ? 'Edit Document Type' : 'Create Document Type'}
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Document Type
            </label>
            <select
              value={formData.type}
              onChange={(e) => handleTypeChange(e.target.value)}
              className={`mt-1 block w-full border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white ${
                errors.type ? 'border-red-300' : 'border-gray-300 dark:border-gray-600'
              }`}
            >
              <option value={DocumentType.ORDERS}>ORDERS - Purchase Orders</option>
              <option value={DocumentType.INVOIC}>INVOIC - Invoices</option>
              <option value={DocumentType.DESADV}>DESADV - Dispatch Advice</option>
              <option value={DocumentType.ORDRSP}>ORDRSP - Order Response</option>
            </select>
            {errors.type && (
              <p className="mt-1 text-sm text-red-600">{errors.type}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Code
            </label>
            <input
              type="text"
              value={formData.code}
              onChange={(e) => setFormData({ ...formData, code: e.target.value })}
              className={`mt-1 block w-full border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white ${
                errors.code ? 'border-red-300' : 'border-gray-300 dark:border-gray-600'
              }`}
              placeholder="e.g., 220"
            />
            {errors.code && (
              <p className="mt-1 text-sm text-red-600">{errors.code}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Name
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className={`mt-1 block w-full border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white ${
                errors.name ? 'border-red-300' : 'border-gray-300 dark:border-gray-600'
              }`}
              placeholder="e.g., Purchase Orders"
            />
            {errors.name && (
              <p className="mt-1 text-sm text-red-600">{errors.name}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Description (Optional)
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows={3}
              className="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              placeholder="Describe this document type..."
            />
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 dark:bg-gray-600 dark:text-gray-300 dark:hover:bg-gray-500 rounded-md transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-md transition-colors"
            >
              {isSubmitting ? 'Saving...' : documentType ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

