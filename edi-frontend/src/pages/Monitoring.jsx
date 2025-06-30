import React from 'react';
import { 
  ChartBarIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  EyeIcon
} from '@heroicons/react/24/outline';

const MetricCard = ({ title, value, change, icon: Icon, color = 'blue' }) => {
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

const LogEntry = ({ timestamp, level, message, details }) => {
  const getLevelColor = () => {
    switch (level) {
      case 'error': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      case 'warning': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      case 'info': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'success': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200';
    }
  };

  return (
    <div className="flex items-start space-x-3 py-3 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
      <div className="flex-shrink-0">
        <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getLevelColor()}`}>
          {level}
        </span>
      </div>
      <div className="min-w-0 flex-1">
        <p className="text-sm text-gray-900 dark:text-white">
          {message}
        </p>
        {details && (
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
            {details}
          </p>
        )}
        <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
          {new Date(timestamp).toLocaleString()}
        </p>
      </div>
    </div>
  );
};

export const Monitoring = () => {
  // Sample monitoring data
  const metrics = {
    totalProcessed: 1247,
    successRate: 98.5,
    averageProcessingTime: 2.3,
    activeConnections: 12,
    errorRate: 1.5,
    queueSize: 3
  };

  const recentLogs = [
    {
      id: 1,
      timestamp: '2024-01-15T14:30:00Z',
      level: 'success',
      message: 'ORDERS document processed successfully',
      details: 'File: sample_orders.edi | Output: sample_orders.xml | Duration: 1.2s'
    },
    {
      id: 2,
      timestamp: '2024-01-15T14:28:00Z',
      level: 'info',
      message: 'New processing job started',
      details: 'Job ID: 12847 | Document Type: INVOIC | Customer: ACME Corp'
    },
    {
      id: 3,
      timestamp: '2024-01-15T14:25:00Z',
      level: 'warning',
      message: 'High queue size detected',
      details: 'Current queue size: 15 jobs | Threshold: 10 jobs'
    },
    {
      id: 4,
      timestamp: '2024-01-15T14:20:00Z',
      level: 'error',
      message: 'Failed to parse EDIFACT file',
      details: 'File: invalid_format.edi | Error: Invalid segment structure at line 23'
    },
    {
      id: 5,
      timestamp: '2024-01-15T14:15:00Z',
      level: 'info',
      message: 'System health check completed',
      details: 'All services operational | Response time: 45ms'
    }
  ];

  const systemStatus = [
    { name: 'API Server', status: 'healthy', uptime: '99.9%', responseTime: '45ms' },
    { name: 'Database', status: 'healthy', uptime: '100%', responseTime: '12ms' },
    { name: 'EDIFACT Parser', status: 'healthy', uptime: '99.8%', responseTime: '230ms' },
    { name: 'XML Generator', status: 'healthy', uptime: '99.9%', responseTime: '180ms' },
    { name: 'File Storage', status: 'warning', uptime: '98.5%', responseTime: '95ms' }
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'warning': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      case 'error': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200';
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          System Monitoring
        </h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Real-time monitoring and system health overview
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <MetricCard
          title="Total Processed"
          value={metrics.totalProcessed.toLocaleString()}
          icon={ChartBarIcon}
          color="blue"
          change={{ type: 'increase', value: '+12%' }}
        />
        <MetricCard
          title="Success Rate"
          value={`${metrics.successRate}%`}
          icon={CheckCircleIcon}
          color="green"
          change={{ type: 'increase', value: '+0.3%' }}
        />
        <MetricCard
          title="Avg Processing Time"
          value={`${metrics.averageProcessingTime}s`}
          icon={ClockIcon}
          color="yellow"
          change={{ type: 'decrease', value: '-0.2s' }}
        />
        <MetricCard
          title="Active Connections"
          value={metrics.activeConnections}
          icon={EyeIcon}
          color="blue"
        />
        <MetricCard
          title="Error Rate"
          value={`${metrics.errorRate}%`}
          icon={ExclamationTriangleIcon}
          color="red"
          change={{ type: 'decrease', value: '-0.1%' }}
        />
        <MetricCard
          title="Queue Size"
          value={metrics.queueSize}
          icon={ClockIcon}
          color="yellow"
        />
      </div>

      {/* System Status and Logs */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        {/* System Status */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white">
              System Status
            </h3>
            <div className="mt-5">
              <div className="space-y-4">
                {systemStatus.map((service, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <span className="text-sm font-medium text-gray-900 dark:text-white">
                        {service.name}
                      </span>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(service.status)}`}>
                        {service.status}
                      </span>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-gray-900 dark:text-white">
                        {service.uptime}
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400">
                        {service.responseTime}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Recent Logs */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex items-center justify-between">
              <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white">
                Recent Logs
              </h3>
              <button className="text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-200">
                View All
              </button>
            </div>
            <div className="mt-5">
              <div className="space-y-0">
                {recentLogs.map((log) => (
                  <LogEntry key={log.id} {...log} />
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Performance Chart Placeholder */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
          Performance Trends
        </h3>
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-8 text-center">
          <ChartBarIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Performance charts will be available in the next version.
          </p>
          <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
            Features: Real-time graphs, historical data, and trend analysis.
          </p>
        </div>
      </div>

      {/* Alerts and Notifications */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
          Active Alerts
        </h3>
        <div className="space-y-3">
          <div className="flex items-center p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-md">
            <ExclamationTriangleIcon className="h-5 w-5 text-yellow-600 dark:text-yellow-400 mr-3" />
            <div className="flex-1">
              <p className="text-sm font-medium text-yellow-800 dark:text-yellow-200">
                High Queue Size
              </p>
              <p className="text-xs text-yellow-700 dark:text-yellow-300">
                Processing queue has 15 pending jobs (threshold: 10)
              </p>
            </div>
            <button className="text-xs text-yellow-600 hover:text-yellow-800 dark:text-yellow-400 dark:hover:text-yellow-200">
              Dismiss
            </button>
          </div>
          
          <div className="flex items-center p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-md">
            <ClockIcon className="h-5 w-5 text-blue-600 dark:text-blue-400 mr-3" />
            <div className="flex-1">
              <p className="text-sm font-medium text-blue-800 dark:text-blue-200">
                Scheduled Maintenance
              </p>
              <p className="text-xs text-blue-700 dark:text-blue-300">
                System maintenance scheduled for tonight at 2:00 AM
              </p>
            </div>
            <button className="text-xs text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-200">
              Details
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

