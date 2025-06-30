import React, { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  DocumentTextIcon,
  UsersIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import { apiService } from '../services/api';
import useAppStore from '../stores/appStore';

const StatCard = ({ title, value, icon: Icon, color = 'blue', change = null }) => {
  const colorClasses = {
    blue: 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400',
    green: 'bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400',
    yellow: 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-600 dark:text-yellow-400',
    red: 'bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400',
  };

  return (
    <div className="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className={`p-3 rounded-md ${colorClasses[color]}`}>
              <Icon className="h-6 w-6" />
            </div>
          </div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                {title}
              </dt>
              <dd className="flex items-baseline">
                <div className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {value}
                </div>
                {change && (
                  <div className={`ml-2 flex items-baseline text-sm font-semibold ${
                    change.type === 'increase' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {change.value}
                  </div>
                )}
              </dd>
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
};

const ActivityItem = ({ title, description, time, status }) => {
  const statusColors = {
    success: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    warning: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    info: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  };

  return (
    <div className="flex items-start space-x-3 py-3">
      <div className="flex-shrink-0">
        <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${statusColors[status]}`}>
          {status}
        </span>
      </div>
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium text-gray-900 dark:text-white">
          {title}
        </p>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          {description}
        </p>
        <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
          {time}
        </p>
      </div>
    </div>
  );
};

export const Dashboard = () => {
  const { 
    setDashboardData, 
    setSystemStatus, 
    setDocumentTypes, 
    setCustomers,
    addNotification 
  } = useAppStore();

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['dashboard'],
    queryFn: getDashboardData,
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  useEffect(() => {
    if (data) {
      setDashboardData(data);
      setSystemStatus(data.systemStatus);
      setDocumentTypes(data.documentTypes);
      setCustomers(data.customers);
    }
  }, [data, setDashboardData, setSystemStatus, setDocumentTypes, setCustomers]);

  useEffect(() => {
    if (error) {
      addNotification({
        type: 'error',
        message: 'Failed to load dashboard data. Please check your connection.',
        duration: 5000
      });
    }
  }, [error, addNotification]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const stats = data?.statistics || {
    totalProcessed: 0,
    successfulProcessed: 0,
    errorCount: 0,
    processingCount: 0
  };

  const recentActivity = [
    {
      title: 'ORDERS document processed',
      description: 'sample_orders.edi converted to XML successfully',
      time: '2 minutes ago',
      status: 'success'
    },
    {
      title: 'New customer added',
      description: 'ACME Corporation configured with GLN 3700123456789',
      time: '15 minutes ago',
      status: 'info'
    },
    {
      title: 'System health check',
      description: 'All services operational',
      time: '30 minutes ago',
      status: 'success'
    },
    {
      title: 'Configuration updated',
      description: 'INVOIC document type settings modified',
      time: '1 hour ago',
      status: 'info'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Dashboard
        </h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Overview of your EDI processing system
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Document Types"
          value={data?.documentTypes?.length || 0}
          icon={DocumentTextIcon}
          color="blue"
        />
        <StatCard
          title="Customers"
          value={data?.customers?.length || 0}
          icon={UsersIcon}
          color="green"
        />
        <StatCard
          title="Total Processed"
          value={stats.totalProcessed}
          icon={ChartBarIcon}
          color="blue"
        />
        <StatCard
          title="Success Rate"
          value={stats.totalProcessed > 0 ? 
            `${Math.round((stats.successfulProcessed / stats.totalProcessed) * 100)}%` : 
            '0%'
          }
          icon={CheckCircleIcon}
          color="green"
        />
      </div>

      {/* System Status */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
        <StatCard
          title="Processing Queue"
          value={stats.processingCount}
          icon={ClockIcon}
          color="yellow"
        />
        <StatCard
          title="Successful"
          value={stats.successfulProcessed}
          icon={CheckCircleIcon}
          color="green"
        />
        <StatCard
          title="Errors"
          value={stats.errorCount}
          icon={ExclamationTriangleIcon}
          color="red"
        />
      </div>

      {/* Recent Activity and System Health */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        {/* Recent Activity */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white">
              Recent Activity
            </h3>
            <div className="mt-5">
              <div className="flow-root">
                <ul className="-my-3 divide-y divide-gray-200 dark:divide-gray-700">
                  {recentActivity.map((activity, index) => (
                    <li key={index}>
                      <ActivityItem {...activity} />
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* System Health */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white">
              System Health
            </h3>
            <div className="mt-5 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500 dark:text-gray-400">API Status</span>
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                  data?.health?.status === 'healthy' 
                    ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                    : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                }`}>
                  {data?.health?.status === 'healthy' ? 'Healthy' : 'Error'}
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500 dark:text-gray-400">Database</span>
                <span className="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                  Connected
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500 dark:text-gray-400">EDIFACT Parser</span>
                <span className="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                  Available
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500 dark:text-gray-400">XML Generator</span>
                <span className="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                  Available
                </span>
              </div>

              <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                <button
                  onClick={() => refetch()}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium py-2 px-4 rounded-md transition-colors"
                >
                  Refresh Status
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

