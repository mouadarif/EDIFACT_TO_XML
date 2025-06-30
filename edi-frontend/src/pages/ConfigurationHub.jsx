import React, { useState } from 'react';
import { 
  DocumentTextIcon,
  UsersIcon,
  CogIcon,
  PlusIcon
} from '@heroicons/react/24/outline';
import { DocumentTypeForm } from '../components/forms/DocumentTypeForm';
import { CustomerForm } from '../components/forms/CustomerForm';
import useAppStore from '../stores/appStore';

const TabButton = ({ active, onClick, icon: Icon, children }) => (
  <button
    onClick={onClick}
    className={`flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors ${
      active
        ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-200'
        : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-700'
    }`}
  >
    <Icon className="w-4 h-4 mr-2" />
    {children}
  </button>
);

const DocumentTypeCard = ({ documentType, onEdit, onDelete }) => (
  <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
    <div className="flex items-start justify-between">
      <div>
        <h3 className="text-lg font-medium text-gray-900 dark:text-white">
          {documentType.name}
        </h3>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Type: {documentType.type} | Code: {documentType.code}
        </p>
        <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
          {documentType.segments?.length || 0} segments configured
        </p>
      </div>
      <div className="flex space-x-2">
        <button
          onClick={() => onEdit(documentType)}
          className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-200 text-sm"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(documentType.id)}
          className="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-200 text-sm"
        >
          Delete
        </button>
      </div>
    </div>
  </div>
);

const CustomerCard = ({ customer, onEdit, onDelete }) => (
  <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
    <div className="flex items-start justify-between">
      <div>
        <h3 className="text-lg font-medium text-gray-900 dark:text-white">
          {customer.name}
        </h3>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          GLN: {customer.gln}
        </p>
        <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
          {Object.keys(customer.preferences || {}).length} preferences configured
        </p>
      </div>
      <div className="flex space-x-2">
        <button
          onClick={() => onEdit(customer)}
          className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-200 text-sm"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(customer.id)}
          className="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-200 text-sm"
        >
          Delete
        </button>
      </div>
    </div>
  </div>
);

export const ConfigurationHub = () => {
  const [activeTab, setActiveTab] = useState('document-types');
  const [showDocumentTypeForm, setShowDocumentTypeForm] = useState(false);
  const [showCustomerForm, setShowCustomerForm] = useState(false);
  const [editingDocumentType, setEditingDocumentType] = useState(null);
  const [editingCustomer, setEditingCustomer] = useState(null);

  const { 
    documentTypes, 
    customers, 
    removeDocumentType, 
    removeCustomer,
    addNotification 
  } = useAppStore();

  const handleEditDocumentType = (documentType) => {
    setEditingDocumentType(documentType);
    setShowDocumentTypeForm(true);
  };

  const handleEditCustomer = (customer) => {
    setEditingCustomer(customer);
    setShowCustomerForm(true);
  };

  const handleDeleteDocumentType = (id) => {
    if (window.confirm('Are you sure you want to delete this document type?')) {
      removeDocumentType(id);
      addNotification({
        type: 'success',
        message: 'Document type deleted successfully'
      });
    }
  };

  const handleDeleteCustomer = (id) => {
    if (window.confirm('Are you sure you want to delete this customer?')) {
      removeCustomer(id);
      addNotification({
        type: 'success',
        message: 'Customer deleted successfully'
      });
    }
  };

  const handleFormClose = () => {
    setShowDocumentTypeForm(false);
    setShowCustomerForm(false);
    setEditingDocumentType(null);
    setEditingCustomer(null);
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Configuration Hub
        </h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Manage document types, customers, and system settings
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 dark:border-gray-700">
        <nav className="flex space-x-8">
          <TabButton
            active={activeTab === 'document-types'}
            onClick={() => setActiveTab('document-types')}
            icon={DocumentTextIcon}
          >
            Document Types
          </TabButton>
          <TabButton
            active={activeTab === 'customers'}
            onClick={() => setActiveTab('customers')}
            icon={UsersIcon}
          >
            Customers
          </TabButton>
          <TabButton
            active={activeTab === 'settings'}
            onClick={() => setActiveTab('settings')}
            icon={CogIcon}
          >
            Settings
          </TabButton>
        </nav>
      </div>

      {/* Tab Content */}
      <div className="mt-6">
        {activeTab === 'document-types' && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-medium text-gray-900 dark:text-white">
                Document Types ({documentTypes.length})
              </h2>
              <button
                onClick={() => setShowDocumentTypeForm(true)}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center transition-colors"
              >
                <PlusIcon className="w-4 h-4 mr-2" />
                Add Document Type
              </button>
            </div>

            {documentTypes.length === 0 ? (
              <div className="text-center py-12">
                <DocumentTextIcon className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">
                  No document types
                </h3>
                <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                  Get started by creating a new document type.
                </p>
                <div className="mt-6">
                  <button
                    onClick={() => setShowDocumentTypeForm(true)}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                  >
                    Add Document Type
                  </button>
                </div>
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {documentTypes.map((documentType) => (
                  <DocumentTypeCard
                    key={documentType.id}
                    documentType={documentType}
                    onEdit={handleEditDocumentType}
                    onDelete={handleDeleteDocumentType}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'customers' && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-medium text-gray-900 dark:text-white">
                Customers ({customers.length})
              </h2>
              <button
                onClick={() => setShowCustomerForm(true)}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center transition-colors"
              >
                <PlusIcon className="w-4 h-4 mr-2" />
                Add Customer
              </button>
            </div>

            {customers.length === 0 ? (
              <div className="text-center py-12">
                <UsersIcon className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">
                  No customers
                </h3>
                <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                  Get started by adding a new customer.
                </p>
                <div className="mt-6">
                  <button
                    onClick={() => setShowCustomerForm(true)}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                  >
                    Add Customer
                  </button>
                </div>
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {customers.map((customer) => (
                  <CustomerCard
                    key={customer.id}
                    customer={customer}
                    onEdit={handleEditCustomer}
                    onDelete={handleDeleteCustomer}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'settings' && (
          <div className="space-y-6">
            <h2 className="text-lg font-medium text-gray-900 dark:text-white">
              System Settings
            </h2>
            
            <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
              <h3 className="text-base font-medium text-gray-900 dark:text-white mb-4">
                Processing Settings
              </h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Default Output Format
                  </label>
                  <select className="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white">
                    <option value="xml">XML</option>
                    <option value="json">JSON</option>
                    <option value="csv">CSV</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Default Batch Size
                  </label>
                  <input
                    type="number"
                    defaultValue="10"
                    min="1"
                    max="100"
                    className="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>
                
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    defaultChecked
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label className="ml-2 block text-sm text-gray-900 dark:text-white">
                    Enable auto-refresh
                  </label>
                </div>
              </div>
              
              <div className="mt-6">
                <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors">
                  Save Settings
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Forms */}
      {showDocumentTypeForm && (
        <DocumentTypeForm
          documentType={editingDocumentType}
          onClose={handleFormClose}
        />
      )}

      {showCustomerForm && (
        <CustomerForm
          customer={editingCustomer}
          onClose={handleFormClose}
        />
      )}
    </div>
  );
};

