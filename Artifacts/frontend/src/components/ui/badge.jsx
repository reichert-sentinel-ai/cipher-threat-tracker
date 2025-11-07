import React from 'react';

const variantClasses = {
  destructive: 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300 border-red-200 dark:border-red-800',
  warning: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800',
  secondary: 'bg-gray-100 dark:bg-[#1a1a1a] text-gray-800 dark:text-[#a0a0a0] border-gray-200 dark:border-[#2a2a2a]',
  default: 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 border-blue-200 dark:border-blue-800',
  outline: 'bg-transparent text-gray-700 dark:text-[#a0a0a0] border-gray-300 dark:border-[#2a2a2a]',
};

export const Badge = ({ children, variant = 'default', className = '' }) => (
  <span
    className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${variantClasses[variant]} ${className}`}
  >
    {children}
  </span>
);

