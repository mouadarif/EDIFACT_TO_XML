import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { 
  CloudArrowUpIcon,
  DocumentTextIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ClockIcon,
  ArrowDownTrayIcon,
  EyeIcon,
  CogIcon
} from '@heroicons/react/24/outline';
import useAppStore from '../stores/appStore';
import { apiService } from '../services/api';
import { DocumentType, OutputFormat, ProcessingStatus } from '../types';

const ProcessingJobCard = ({ job, onDownload, onView, onConfigure }) => {
  const getStatusIcon = () => {
    switch (job.status) {
      case ProcessingStatus.COMPLETED:
        return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
      case ProcessingStatus.ERROR:
        return <ExclamationTriangleIcon className="w-5 h-5 text-red-500" />;
      case ProcessingStatus.PROCESSING:
        return <ClockIcon className="w-5 h-5 text-blue-500 animate-spin" />;
      default:
        return <ClockIcon className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusColor = () => {
    switch (job.status) {
      case ProcessingStatus.COMPLETED:
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case ProcessingStatus.ERROR:
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      case ProcessingStatus.PROCESSING:
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200';
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2">
            {getStatusIcon()}
            <h3 className="text-sm font-medium text-gray-900 dark:text-white">
              {job.filename}
            </h3>
          </div>
          
          <div className="mt-2 space-y-1">
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Type: {job.documentType} | Format: {job.outputFormat || 'XML'}
            </p>
            <div className="flex items-center space-x-2">
              <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor()}`}>
                {job.status}
              </span>
              {job.progress > 0 && job.status === ProcessingStatus.PROCESSING && (
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  {job.progress}%
                </span>
              )}
            </div>
          </div>

          {job.status === ProcessingStatus.PROCESSING && (
            <div className="mt-2">
              <div className="w-full bg-gray-200 rounded-full h-2 dark:bg-gray-700">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${job.progress || 0}%` }}
                />
              </div>
            </div>
          )}
        </div>

        <div className="flex space-x-2 ml-4">
          {job.status === ProcessingStatus.COMPLETED && (
            <>
              <button
                onClick={() => onView(job)}
                className="p-1.5 text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-200"
                title="View output"
              >
                <EyeIcon className="w-4 h-4" />
              </button>
              <button
                onClick={() => onDownload(job)}
                className="p-1.5 text-green-600 hover:text-green-800 dark:text-green-400 dark:hover:text-green-200"
                title="Download"
              >
                <ArrowDownTrayIcon className="w-4 h-4" />
              </button>
            </>
          )}
          <button
            onClick={() => onConfigure(job)}
            className="p-1.5 text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200"
            title="Configure"
          >
            <CogIcon className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export const ProcessingCenter = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const {
    processingConfig,
    setProcessingConfig,
    processingJobs,
    addProcessingJob,
    updateProcessingJob,
    customers,
    addNotification
  } = useAppStore();

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    setIsUploading(true);
    setUploadProgress(0);

    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      const response = await uploadFiles(acceptedFiles, processingConfig);
      
      clearInterval(progressInterval);
      setUploadProgress(100);

      // Add jobs to store
      acceptedFiles.forEach((file, index) => {
        const job = {
          id: Date.now() + index,
          filename: file.name,
          documentType: processingConfig.documentType,
          outputFormat: processingConfig.outputFormat,
          status: ProcessingStatus.PROCESSING,
          progress: 0,
          createdAt: new Date().toISOString()
        };
        
        addProcessingJob(job);

        // Simulate processing
        setTimeout(() => {
          updateProcessingJob(job.id, {
            status: ProcessingStatus.COMPLETED,
            progress: 100,
            outputFiles: [`${file.name}.${processingConfig.outputFormat}`]
          });
        }, 2000 + (index * 1000));
      });

      addNotification({
        type: 'success',
        message: `${acceptedFiles.length} file(s) uploaded and processing started`
      });

    } catch (error) {
      console.error('Upload failed:', error);
      addNotification({
        type: 'error',
        message: 'Upload failed. Please try again.'
      });
    } finally {
      setTimeout(() => {
        setIsUploading(false);
        setUploadProgress(0);
      }, 1000);
    }
  }, [processingConfig, addProcessingJob, updateProcessingJob, addNotification]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.edi', '.txt'],
      'application/octet-stream': ['.edi']
    },
    multiple: true
  });

  const handleDownload = (job) => {
    // Simulate download
    addNotification({
      type: 'info',
      message: `Downloading ${job.filename}...`
    });
  };

  const handleView = (job) => {
    // Simulate view
    addNotification({
      type: 'info',
      message: `Opening ${job.filename} for preview...`
    });
  };

  const handleConfigure = (job) => {
    // Simulate configure
    addNotification({
      type: 'info',
      message: `Opening configuration for ${job.filename}...`
    });
  };

  const stats = {
    total: processingJobs.length,
    completed: processingJobs.filter(j => j.status === ProcessingStatus.COMPLETED).length,
    processing: processingJobs.filter(j => j.status === ProcessingStatus.PROCESSING).length,
    errors: processingJobs.filter(j => j.status === ProcessingStatus.ERROR).length
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Processing Center
        </h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Upload and process EDIFACT files
        </p>
      </div>

      {/* Configuration Panel */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
          Processing Configuration
        </h2>
        
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Document Type
            </label>
            <select
              value={processingConfig.documentType}
              onChange={(e) => setProcessingConfig({ documentType: e.target.value })}
              className="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            >
              <option value={DocumentType.ORDERS}>ORDERS - Purchase Orders</option>
              <option value={DocumentType.INVOIC}>INVOIC - Invoices</option>
              <option value={DocumentType.DESADV}>DESADV - Dispatch Advice</option>
              <option value={DocumentType.ORDRSP}>ORDRSP - Order Response</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Customer (Optional)
            </label>
            <select
              value={processingConfig.customerId || ''}
              onChange={(e) => setProcessingConfig({ customerId: e.target.value || null })}
              className="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            >
              <option value="">All Customers</option>
              {customers.map((customer) => (
                <option key={customer.id} value={customer.id}>
                  {customer.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Output Format
            </label>
            <select
              value={processingConfig.outputFormat}
              onChange={(e) => setProcessingConfig({ outputFormat: e.target.value })}
              className="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            >
              <option value={OutputFormat.XML}>XML</option>
              <option value={OutputFormat.JSON}>JSON</option>
              <option value={OutputFormat.CSV}>CSV</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Batch Size
            </label>
            <input
              type="number"
              value={processingConfig.batchSize}
              onChange={(e) => setProcessingConfig({ batchSize: parseInt(e.target.value) })}
              min="1"
              max="100"
              className="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
            />
          </div>
        </div>
      </div>

      {/* Upload Area */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors cursor-pointer ${
            isDragActive
              ? 'border-blue-400 bg-blue-50 dark:bg-blue-900/20'
              : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
          }`}
        >
          <input {...getInputProps()} />
          
          {isUploading ? (
            <div className="space-y-4">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto" />
              <div>
                <p className="text-lg font-medium text-gray-900 dark:text-white">
                  Uploading files...
                </p>
                <div className="mt-2 w-full bg-gray-200 rounded-full h-2 dark:bg-gray-700">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${uploadProgress}%` }}
                  />
                </div>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                  {uploadProgress}% complete
                </p>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <CloudArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
              <div>
                <p className="text-lg font-medium text-gray-900 dark:text-white">
                  {isDragActive ? 'Drop files here' : 'Drag & drop EDIFACT files'}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  or click to browse (.edi, .txt files)
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-4">
        <div className="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <DocumentTextIcon className="h-6 w-6 text-blue-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                    Total Files
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900 dark:text-white">
                    {stats.total}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CheckCircleIcon className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                    Completed
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900 dark:text-white">
                    {stats.completed}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ClockIcon className="h-6 w-6 text-yellow-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                    Processing
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900 dark:text-white">
                    {stats.processing}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ExclamationTriangleIcon className="h-6 w-6 text-red-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                    Errors
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900 dark:text-white">
                    {stats.errors}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Processing Jobs */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white">
            Processing Jobs ({processingJobs.length})
          </h3>
          
          {processingJobs.length === 0 ? (
            <div className="text-center py-12">
              <DocumentTextIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">
                No processing jobs
              </h3>
              <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                Upload EDIFACT files to start processing.
              </p>
            </div>
          ) : (
            <div className="mt-5 space-y-3">
              {processingJobs
                .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
                .map((job) => (
                  <ProcessingJobCard
                    key={job.id}
                    job={job}
                    onDownload={handleDownload}
                    onView={handleView}
                    onConfigure={handleConfigure}
                  />
                ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

