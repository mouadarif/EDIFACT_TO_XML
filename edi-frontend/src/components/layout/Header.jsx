import React from 'react';
import { 
  MagnifyingGlassIcon,
  BellIcon,
  SunIcon,
  MoonIcon,
  ComputerDesktopIcon,
  UserCircleIcon
} from '@heroicons/react/24/outline';
import { useTheme } from '../providers/ThemeProvider';
import useAppStore from '../../stores/appStore';
import { Theme } from '../../types';

export const Header = () => {
  const { theme, toggleTheme } = useTheme();
  const { 
    searchQuery, 
    setSearchQuery, 
    notifications, 
    clearNotifications,
    systemStatus 
  } = useAppStore();

  const getThemeIcon = () => {
    switch (theme) {
      case Theme.LIGHT: return SunIcon;
      case Theme.DARK: return MoonIcon;
      case Theme.SYSTEM: return ComputerDesktopIcon;
      default: return SunIcon;
    }
  };

  const ThemeIcon = getThemeIcon();
  const unreadNotifications = notifications.filter(n => !n.read).length;

  return (
    <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Search */}
        <div className="flex-1 max-w-lg">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white dark:bg-gray-700 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-sm"
              placeholder="Search documents, customers, or jobs..."
            />
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center space-x-4">
          {/* System Status */}
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${
              systemStatus === 'operational' ? 'bg-green-500' :
              systemStatus === 'warning' ? 'bg-yellow-500' :
              systemStatus === 'error' ? 'bg-red-500' : 'bg-gray-500'
            }`} />
            <span className="text-sm text-gray-600 dark:text-gray-300 hidden sm:inline">
              {systemStatus === 'operational' ? 'System Online' :
               systemStatus === 'warning' ? 'System Warning' :
               systemStatus === 'error' ? 'System Error' : 'System Unknown'}
            </span>
          </div>

          {/* Theme Toggle */}
          <button
            onClick={toggleTheme}
            className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-700 rounded-md transition-colors"
            title={`Current theme: ${theme}`}
          >
            <ThemeIcon className="h-5 w-5" />
          </button>

          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => {
                if (unreadNotifications > 0) {
                  clearNotifications();
                }
              }}
              className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-700 rounded-md transition-colors relative"
            >
              <BellIcon className="h-5 w-5" />
              {unreadNotifications > 0 && (
                <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                  {unreadNotifications > 9 ? '9+' : unreadNotifications}
                </span>
              )}
            </button>
          </div>

          {/* User Menu */}
          <div className="relative">
            <button className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-700 rounded-md transition-colors">
              <UserCircleIcon className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Notifications Panel */}
      {notifications.length > 0 && (
        <div className="mt-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-md p-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-blue-800 dark:text-blue-200">
              Recent Notifications ({notifications.length})
            </h3>
            <button
              onClick={clearNotifications}
              className="text-xs text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-200"
            >
              Clear All
            </button>
          </div>
          <div className="mt-2 space-y-1">
            {notifications.slice(0, 3).map((notification) => (
              <div
                key={notification.id}
                className={`text-sm ${
                  notification.type === 'error' 
                    ? 'text-red-700 dark:text-red-300'
                    : notification.type === 'warning'
                    ? 'text-yellow-700 dark:text-yellow-300'
                    : notification.type === 'success'
                    ? 'text-green-700 dark:text-green-300'
                    : 'text-blue-700 dark:text-blue-300'
                }`}
              >
                {notification.message}
              </div>
            ))}
            {notifications.length > 3 && (
              <div className="text-xs text-blue-600 dark:text-blue-400">
                +{notifications.length - 3} more notifications
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
};

