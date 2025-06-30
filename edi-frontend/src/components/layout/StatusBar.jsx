import React, { useEffect, useState } from 'react';
import useAppStore from '../../stores/appStore';

export const StatusBar = () => {
  const { 
    systemStatus, 
    statistics, 
    processingJobs,
    preferences 
  } = useAppStore();
  
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const activeJobs = processingJobs.filter(job => 
    job.status === 'processing' || job.status === 'pending'
  ).length;

  const getSystemStatusText = () => {
    switch (systemStatus) {
      case 'operational': return 'System Operational';
      case 'warning': return 'System Warning';
      case 'error': return 'System Error';
      default: return 'System Status Unknown';
    }
  };

  const getSystemStatusColor = () => {
    switch (systemStatus) {
      case 'operational': return 'text-green-600 dark:text-green-400';
      case 'warning': return 'text-yellow-600 dark:text-yellow-400';
      case 'error': return 'text-red-600 dark:text-red-400';
      default: return 'text-gray-600 dark:text-gray-400';
    }
  };

  return (
    <div className="bg-gray-100 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 px-6 py-2">
      <div className="flex items-center justify-between text-xs text-gray-600 dark:text-gray-400">
        {/* Left side - System status */}
        <div className="flex items-center space-x-4">
          <span className={getSystemStatusColor()}>
            {getSystemStatusText()}
          </span>
          
          {activeJobs > 0 && (
            <span className="text-blue-600 dark:text-blue-400">
              {activeJobs} job{activeJobs !== 1 ? 's' : ''} processing
            </span>
          )}
          
          <span>
            Processed: {statistics.totalProcessed} | 
            Success: {statistics.successfulProcessed} | 
            Errors: {statistics.errorCount}
          </span>
        </div>

        {/* Right side - Time and settings */}
        <div className="flex items-center space-x-4">
          {preferences.autoRefresh && (
            <span className="text-green-600 dark:text-green-400">
              Auto-refresh: {preferences.refreshInterval / 1000}s
            </span>
          )}
          
          <span>
            {currentTime.toLocaleTimeString()}
          </span>
        </div>
      </div>
    </div>
  );
};

