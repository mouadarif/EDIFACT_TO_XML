import React from 'react';
import { 
  CogIcon,
  BellIcon,
  ShieldCheckIcon,
  DatabaseIcon,
  CloudIcon,
  UserIcon
} from '@heroicons/react/24/outline';
import useAppStore from '../stores/appStore';
import { Theme } from '../types';

const SettingSection = ({ title, description, icon: Icon, children }) => (
  <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
    <div className="flex items-center mb-4">
      <div className="flex-shrink-0">
        <Icon className="h-6 w-6 text-blue-600 dark:text-blue-400" />
      </div>
      <div className="ml-3">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white">
          {title}
        </h3>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          {description}
        </p>
      </div>
    </div>
    <div className="space-y-4">
      {children}
    </div>
  </div>
);

const SettingItem = ({ label, description, children }) => (
  <div className="flex items-center justify-between">
    <div className="flex-1">
      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
        {label}
      </label>
      {description && (
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
          {description}
        </p>
      )}
    </div>
    <div className="ml-4">
      {children}
    </div>
  </div>
);

const Toggle = ({ checked, onChange, disabled = false }) => (
  <button
    type="button"
    onClick={() => !disabled && onChange(!checked)}
    disabled={disabled}
    className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
      checked ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-700'
    } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
  >
    <span
      className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
        checked ? 'translate-x-5' : 'translate-x-0'
      }`}
    />
  </button>
);

export const Settings = () => {
  const { 
    theme, 
    setTheme, 
    preferences, 
    setPreference,
    resetStore,
    addNotification 
  } = useAppStore();

  const handleSaveSettings = () => {
    addNotification({
      type: 'success',
      message: 'Settings saved successfully'
    });
  };

  const handleResetSettings = () => {
    if (window.confirm('Are you sure you want to reset all settings to default values?')) {
      resetStore();
      addNotification({
        type: 'info',
        message: 'Settings reset to default values'
      });
    }
  };

  const handleExportSettings = () => {
    const settings = {
      theme,
      preferences,
      exportedAt: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(settings, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'edi-settings.json';
    a.click();
    URL.revokeObjectURL(url);
    
    addNotification({
      type: 'success',
      message: 'Settings exported successfully'
    });
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Settings
        </h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Manage your application preferences and system configuration
        </p>
      </div>

      {/* General Settings */}
      <SettingSection
        title="General"
        description="Basic application settings and preferences"
        icon={CogIcon}
      >
        <SettingItem
          label="Theme"
          description="Choose your preferred color scheme"
        >
          <select
            value={theme}
            onChange={(e) => setTheme(e.target.value)}
            className="block w-32 border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white text-sm"
          >
            <option value={Theme.LIGHT}>Light</option>
            <option value={Theme.DARK}>Dark</option>
            <option value={Theme.SYSTEM}>System</option>
          </select>
        </SettingItem>

        <SettingItem
          label="Auto Refresh"
          description="Automatically refresh data every 30 seconds"
        >
          <Toggle
            checked={preferences.autoRefresh}
            onChange={(value) => setPreference('autoRefresh', value)}
          />
        </SettingItem>

        <SettingItem
          label="Compact View"
          description="Use a more compact layout to show more information"
        >
          <Toggle
            checked={preferences.compactView}
            onChange={(value) => setPreference('compactView', value)}
          />
        </SettingItem>

        <SettingItem
          label="Refresh Interval"
          description="How often to refresh data (in seconds)"
        >
          <select
            value={preferences.refreshInterval / 1000}
            onChange={(e) => setPreference('refreshInterval', parseInt(e.target.value) * 1000)}
            className="block w-24 border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white text-sm"
          >
            <option value="15">15s</option>
            <option value="30">30s</option>
            <option value="60">1m</option>
            <option value="300">5m</option>
          </select>
        </SettingItem>
      </SettingSection>

      {/* Processing Settings */}
      <SettingSection
        title="Processing"
        description="Default settings for file processing"
        icon={DatabaseIcon}
      >
        <SettingItem
          label="Default Output Format"
          description="Default format for processed files"
        >
          <select
            value={preferences.defaultOutputFormat}
            onChange={(e) => setPreference('defaultOutputFormat', e.target.value)}
            className="block w-24 border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white text-sm"
          >
            <option value="xml">XML</option>
            <option value="json">JSON</option>
            <option value="csv">CSV</option>
          </select>
        </SettingItem>

        <SettingItem
          label="Default Batch Size"
          description="Number of files to process in a single batch"
        >
          <input
            type="number"
            value={preferences.defaultBatchSize}
            onChange={(e) => setPreference('defaultBatchSize', parseInt(e.target.value))}
            min="1"
            max="100"
            className="block w-20 border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white text-sm"
          />
        </SettingItem>
      </SettingSection>

      {/* Notifications */}
      <SettingSection
        title="Notifications"
        description="Configure how you receive notifications"
        icon={BellIcon}
      >
        <SettingItem
          label="Show Notifications"
          description="Display notifications for system events"
        >
          <Toggle
            checked={preferences.showNotifications}
            onChange={(value) => setPreference('showNotifications', value)}
          />
        </SettingItem>

        <SettingItem
          label="Processing Notifications"
          description="Notify when file processing is complete"
        >
          <Toggle
            checked={true}
            onChange={() => {}}
            disabled
          />
        </SettingItem>

        <SettingItem
          label="Error Notifications"
          description="Notify when errors occur"
        >
          <Toggle
            checked={true}
            onChange={() => {}}
            disabled
          />
        </SettingItem>

        <SettingItem
          label="System Notifications"
          description="Notify about system status changes"
        >
          <Toggle
            checked={false}
            onChange={() => {}}
            disabled
          />
        </SettingItem>
      </SettingSection>

      {/* Security */}
      <SettingSection
        title="Security"
        description="Security and privacy settings"
        icon={ShieldCheckIcon}
      >
        <SettingItem
          label="Session Timeout"
          description="Automatically log out after inactivity"
        >
          <select
            defaultValue="60"
            className="block w-32 border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white text-sm"
            disabled
          >
            <option value="30">30 minutes</option>
            <option value="60">1 hour</option>
            <option value="240">4 hours</option>
            <option value="480">8 hours</option>
          </select>
        </SettingItem>

        <SettingItem
          label="Two-Factor Authentication"
          description="Add an extra layer of security to your account"
        >
          <Toggle
            checked={false}
            onChange={() => {}}
            disabled
          />
        </SettingItem>

        <SettingItem
          label="Audit Logging"
          description="Log all user actions for security auditing"
        >
          <Toggle
            checked={true}
            onChange={() => {}}
            disabled
          />
        </SettingItem>
      </SettingSection>

      {/* Data & Storage */}
      <SettingSection
        title="Data & Storage"
        description="Manage data retention and storage settings"
        icon={CloudIcon}
      >
        <SettingItem
          label="File Retention"
          description="How long to keep processed files"
        >
          <select
            defaultValue="30"
            className="block w-32 border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white text-sm"
            disabled
          >
            <option value="7">7 days</option>
            <option value="30">30 days</option>
            <option value="90">90 days</option>
            <option value="365">1 year</option>
          </select>
        </SettingItem>

        <SettingItem
          label="Auto Cleanup"
          description="Automatically delete old files"
        >
          <Toggle
            checked={true}
            onChange={() => {}}
            disabled
          />
        </SettingItem>

        <SettingItem
          label="Backup Settings"
          description="Automatically backup configuration"
        >
          <Toggle
            checked={false}
            onChange={() => {}}
            disabled
          />
        </SettingItem>
      </SettingSection>

      {/* Account */}
      <SettingSection
        title="Account"
        description="Account information and preferences"
        icon={UserIcon}
      >
        <SettingItem
          label="Username"
          description="Your account username"
        >
          <input
            type="text"
            defaultValue="admin"
            className="block w-32 border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white text-sm"
            disabled
          />
        </SettingItem>

        <SettingItem
          label="Email"
          description="Your email address for notifications"
        >
          <input
            type="email"
            defaultValue="admin@example.com"
            className="block w-48 border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white text-sm"
            disabled
          />
        </SettingItem>

        <SettingItem
          label="Language"
          description="Interface language"
        >
          <select
            defaultValue="en"
            className="block w-32 border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white text-sm"
            disabled
          >
            <option value="en">English</option>
            <option value="fr">Français</option>
            <option value="de">Deutsch</option>
            <option value="es">Español</option>
          </select>
        </SettingItem>
      </SettingSection>

      {/* Action Buttons */}
      <div className="flex justify-between">
        <div className="space-x-3">
          <button
            onClick={handleSaveSettings}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
          >
            Save Settings
          </button>
          <button
            onClick={handleExportSettings}
            className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
          >
            Export Settings
          </button>
        </div>
        <button
          onClick={handleResetSettings}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
        >
          Reset to Defaults
        </button>
      </div>
    </div>
  );
};

