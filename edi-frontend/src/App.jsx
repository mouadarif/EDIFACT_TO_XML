import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider } from './components/providers/ThemeProvider';
import { AppShell } from './components/layout/AppShell';
import { Dashboard } from './pages/Dashboard';
import { ConfigurationHub } from './pages/ConfigurationHub';
import { ProcessingCenter } from './pages/ProcessingCenter';
import { Settings } from './pages/Settings';
import './App.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <Router>
          <AppShell>
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/configuration" element={<ConfigurationHub />} />
              <Route path="/processing" element={<ProcessingCenter />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </AppShell>
        </Router>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;

