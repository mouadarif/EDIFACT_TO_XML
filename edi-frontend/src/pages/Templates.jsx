import React from 'react';
import { 
  DocumentTextIcon,
  PlusIcon,
  EyeIcon,
  PencilIcon,
  TrashIcon
} from '@heroicons/react/24/outline';

const TemplateCard = ({ template, onEdit, onView, onDelete }) => (
  <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
    <div className="flex items-start justify-between">
      <div>
        <h3 className="text-lg font-medium text-gray-900 dark:text-white">
          {template.name}
        </h3>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Type: {template.documentType} | Version: {template.version}
        </p>
        <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
          Last modified: {new Date(template.updatedAt).toLocaleDateString()}
        </p>
      </div>
      <div className="flex space-x-2">
        <button
          onClick={() => onView(template)}
          className="p-1.5 text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-200"
          title="View template"
        >
          <EyeIcon className="w-4 h-4" />
        </button>
        <button
          onClick={() => onEdit(template)}
          className="p-1.5 text-green-600 hover:text-green-800 dark:text-green-400 dark:hover:text-green-200"
          title="Edit template"
        >
          <PencilIcon className="w-4 h-4" />
        </button>
        <button
          onClick={() => onDelete(template.id)}
          className="p-1.5 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-200"
          title="Delete template"
        >
          <TrashIcon className="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
);

export const Templates = () => {
  // Sample templates data
  const templates = [
    {
      id: 1,
      name: 'Standard ORDERS Template',
      documentType: 'ORDERS',
      version: '1.0',
      updatedAt: '2024-01-15T10:30:00Z',
      description: 'Standard template for purchase order processing'
    },
    {
      id: 2,
      name: 'Enhanced INVOIC Template',
      documentType: 'INVOIC',
      version: '2.1',
      updatedAt: '2024-01-10T14:20:00Z',
      description: 'Enhanced invoice template with tax calculations'
    },
    {
      id: 3,
      name: 'Custom DESADV Template',
      documentType: 'DESADV',
      version: '1.5',
      updatedAt: '2024-01-05T09:15:00Z',
      description: 'Custom dispatch advice template for logistics'
    }
  ];

  const handleEdit = (template) => {
    console.log('Edit template:', template);
    // TODO: Implement template editor
  };

  const handleView = (template) => {
    console.log('View template:', template);
    // TODO: Implement template viewer
  };

  const handleDelete = (templateId) => {
    if (window.confirm('Are you sure you want to delete this template?')) {
      console.log('Delete template:', templateId);
      // TODO: Implement template deletion
    }
  };

  const handleCreateNew = () => {
    console.log('Create new template');
    // TODO: Implement template creation
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          XML Templates
        </h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Manage XML output templates for different document types
        </p>
      </div>

      {/* Action Bar */}
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <h2 className="text-lg font-medium text-gray-900 dark:text-white">
            Templates ({templates.length})
          </h2>
        </div>
        <button
          onClick={handleCreateNew}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center transition-colors"
        >
          <PlusIcon className="w-4 h-4 mr-2" />
          Create Template
        </button>
      </div>

      {/* Templates Grid */}
      {templates.length === 0 ? (
        <div className="text-center py-12">
          <DocumentTextIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">
            No templates
          </h3>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Get started by creating your first XML template.
          </p>
          <div className="mt-6">
            <button
              onClick={handleCreateNew}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Create Template
            </button>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {templates.map((template) => (
            <TemplateCard
              key={template.id}
              template={template}
              onEdit={handleEdit}
              onView={handleView}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}

      {/* Template Editor Placeholder */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
          Template Editor
        </h3>
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 text-center">
          <DocumentTextIcon className="mx-auto h-8 w-8 text-gray-400 mb-2" />
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Template editor will be available in the next version.
          </p>
          <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
            Features: Visual XML editor, syntax highlighting, validation, and preview.
          </p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
          Quick Actions
        </h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <button className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            <DocumentTextIcon className="h-6 w-6 text-blue-600 mx-auto mb-2" />
            <p className="text-sm font-medium text-gray-900 dark:text-white">
              Import Template
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Import existing XML template
            </p>
          </button>
          
          <button className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            <PlusIcon className="h-6 w-6 text-green-600 mx-auto mb-2" />
            <p className="text-sm font-medium text-gray-900 dark:text-white">
              Generate Template
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Auto-generate from EDIFACT
            </p>
          </button>
          
          <button className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            <EyeIcon className="h-6 w-6 text-purple-600 mx-auto mb-2" />
            <p className="text-sm font-medium text-gray-900 dark:text-white">
              Preview Output
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Test template with sample data
            </p>
          </button>
        </div>
      </div>
    </div>
  );
};

