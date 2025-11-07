import React, { useState, createContext, useContext } from 'react';

const TabsContext = createContext(null);

export const Tabs = ({ defaultValue, children, className = '', value, onValueChange }) => {
  const [internalValue, setInternalValue] = useState(defaultValue);
  const controlled = value !== undefined;
  const currentValue = controlled ? value : internalValue;
  const setValue = controlled ? onValueChange : setInternalValue;

  return (
    <TabsContext.Provider value={{ value: currentValue, setValue }}>
      <div className={className}>
        {children}
      </div>
    </TabsContext.Provider>
  );
};

export const TabsList = ({ children, className = '' }) => {
  return (
    <div className={`inline-flex h-10 items-center justify-center rounded-md bg-gray-100 dark:bg-[#1f1f1f] p-1 text-gray-500 dark:text-[#a0a0a0] ${className}`}>
      {children}
    </div>
  );
};

export const TabsTrigger = ({ value, children, className = '' }) => {
  const context = useContext(TabsContext);
  if (!context) throw new Error('TabsTrigger must be used within Tabs');

  const isActive = context.value === value;

  return (
    <button
      onClick={() => context.setValue(value)}
      className={`inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-white dark:ring-offset-[#0f0f0f] transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-950 dark:focus-visible:ring-gray-300 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 ${
        isActive
          ? 'bg-white dark:bg-[#2a2a2a] text-gray-900 dark:text-[#e5e5e5] shadow-sm'
          : 'text-gray-500 dark:text-[#a0a0a0] hover:text-gray-900 dark:hover:text-[#e5e5e5]'
      } ${className}`}
    >
      {children}
    </button>
  );
};

export const TabsContent = ({ value, children, className = '' }) => {
  const context = useContext(TabsContext);
  if (!context) throw new Error('TabsContent must be used within Tabs');

  if (context.value !== value) return null;

  return (
    <div className={`mt-2 ring-offset-white dark:ring-offset-[#0f0f0f] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-950 dark:focus-visible:ring-gray-300 focus-visible:ring-offset-2 ${className}`}>
      {children}
    </div>
  );
};

