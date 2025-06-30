import React, { useState, useEffect } from 'react';
import { XMarkIcon } from '@heroicons/react/24/outline';
import useAppStore from '../../stores/appStore';
import { validateGLN, createCustomer } from '../../types';

export const CustomerForm = ({ customer, onClose }) => {
  const [formData, setFormData] = useState({
    name: '',
    gln: '',
    email: '',
    phone: '',
    address: '',
    preferences: {
      defaultOutputFormat: 'xml',
      enableNotifications: true,
      customMappings: false
    }
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { addCustomer, updateCustomer, addNotification } = useAppStore();

  useEffect(() => {
    if (customer) {
      setFormData({
        name: customer.name || '',
        gln: customer.gln || '',
        email: customer.email || '',
        phone: customer.phone || '',
        address: customer.address || '',
        preferences: {
          defaultOutputFormat: customer.preferences?.defaultOutputFormat || 'xml',
          enableNotifications: customer.preferences?.enableNotifications ?? true,
          customMappings: customer.preferences?.customMappings ?? false
        }
      });
    }
  }, [customer]);

  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!formData.gln.trim()) {
      newErrors.gln = 'GLN is required';
    } else if (!validateGLN(formData.gln)) {
      newErrors.gln = 'GLN must be exactly 13 digits';
    }

    if (formData.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
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
      const customerData = createCustomer(
        customer?.id || Date.now(),
        formData.name,
        formData.gln,
        formData.preferences
      );

      const fullCustomerData = {
        ...customerData,
        email: formData.email,
        phone: formData.phone,
        address: formData.address
      };

      if (customer) {
        // Update existing
        updateCustomer(customer.id, fullCustomerData);
        addNotification({
          type: 'success',
          message: 'Customer updated successfully'
        });
      } else {
        // Create new
        addCustomer(fullCustomerData);
        addNotification({
          type: 'success',
          message: 'Customer created successfully'
        });
      }

      onClose();
    } catch (error) {
      addNotification({
        type: 'error',
        message: 'Failed to save customer'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handlePreferenceChange = (key, value) => {
    setFormData({
      ...formData,
      preferences: {
        ...formData.preferences,
        [key]: value
      }
    });
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-10 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white dark:bg-gray-800 max-h-screen overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
            {customer ? 'Edit Customer' : 'Create Customer'}
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
              Company Name *
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className={`mt-1 block w-full border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white ${
                errors.name ? 'border-red-300' : 'border-gray-300 dark:border-gray-600'
              }`}
              placeholder="e.g., ACME Corporation"
            />
            {errors.name && (
              <p className="mt-1 text-sm text-red-600">{errors.name}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              GLN (Global Location Number) *
            </label>
            <input
              type="text"
              value={formData.gln}
              onChange={(e) => setFormData({ ...formData, gln: e.target.value.replace(/\D/g, '').slice(0, 13) })}
              className={`mt-1 block w-full border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white ${
                errors.gln ? 'border-red-300' : 'border-gray-300 dark:border-gray-600'
              }`}
              placeholder="e.g., 3700123456789"
              maxLength="13"
            />
            {errors.gln && (
              <p className="mt-1 text-sm text-red-600">{errors.gln}</p>
            )}
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
              13-digit unique identifier for EDI transactions
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Email
            </label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className={`mt-1 block w-full border rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white ${
                errors.email ? 'border-red-300' : 'border-gray-300 dark:border-gray-600'
              }`}
              placeholder="contact@company.com"
            />
            {errors.email && (
              <p className="mt-1 text-sm text-red-600">{errors.email}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Phone
            </label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              className="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              placeholder="+1 (555) 123-4567"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Address
            </label>
            <textarea
              value={formData.address}
              onChange={(e) => setFormData({ ...formData, address: e.target.value })}
              rows={2}
              className="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              placeholder="Company address..."
            />
          </div>

          <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
            <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-3">
              Preferences
            </h4>
            
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Default Output Format
                </label>
                <select
                  value={formData.preferences.defaultOutputFormat}
                  onChange={(e) => handlePreferenceChange('defaultOutputFormat', e.target.value)}
                  className="mt-1 block w-full border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                >
                  <option value="xml">XML</option>
                  <option value="json">JSON</option>
                  <option value="csv">CSV</option>
                </select>
              </div>

              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  Enable Notifications
                </label>
                <button
                  type="button"
                  onClick={() => handlePreferenceChange('enableNotifications', !formData.preferences.enableNotifications)}
                  className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                    formData.preferences.enableNotifications ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-700'
                  }`}
                >
                  <span
                    className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                      formData.preferences.enableNotifications ? 'translate-x-5' : 'translate-x-0'
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  Custom Mappings
                </label>
                <button
                  type="button"
                  onClick={() => handlePreferenceChange('customMappings', !formData.preferences.customMappings)}
                  className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                    formData.preferences.customMappings ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-700'
                  }`}
                >
                  <span
                    className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                      formData.preferences.customMappings ? 'translate-x-5' : 'translate-x-0'
                    }`}
                  />
                </button>
              </div>
            </div>
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
              {isSubmitting ? 'Saving...' : customer ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

