import React, { createContext, useContext, useEffect } from 'react';
import useAppStore from '../../stores/appStore';
import { Theme } from '../../types';

const ThemeContext = createContext();

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

export const ThemeProvider = ({ children }) => {
  const { theme, setTheme } = useAppStore();

  useEffect(() => {
    const root = window.document.documentElement;
    
    const applyTheme = (themeName) => {
      root.classList.remove('light', 'dark');
      root.classList.add(themeName);
    };

    if (theme === Theme.SYSTEM) {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches 
        ? Theme.DARK 
        : Theme.LIGHT;
      applyTheme(systemTheme);
    } else {
      applyTheme(theme);
    }

    // Listen for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = (e) => {
      if (theme === Theme.SYSTEM) {
        applyTheme(e.matches ? Theme.DARK : Theme.LIGHT);
      }
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [theme]);

  const toggleTheme = () => {
    const themes = [Theme.LIGHT, Theme.DARK, Theme.SYSTEM];
    const currentIndex = themes.indexOf(theme);
    const nextIndex = (currentIndex + 1) % themes.length;
    setTheme(themes[nextIndex]);
  };

  const value = {
    theme,
    setTheme,
    toggleTheme,
    isDark: theme === Theme.DARK || (theme === Theme.SYSTEM && window.matchMedia('(prefers-color-scheme: dark)').matches)
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

