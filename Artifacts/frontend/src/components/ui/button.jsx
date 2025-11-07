import React from 'react';

const variantClasses = {
  default: 'bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white',
  destructive: 'bg-red-600 hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600 text-white',
  outline: 'border border-gray-300 dark:border-[#2a2a2a] bg-transparent hover:bg-gray-50 dark:hover:bg-[#1a1a1a] text-gray-900 dark:text-[#e5e5e5]',
  ghost: 'hover:bg-gray-100 dark:hover:bg-[#1a1a1a] text-gray-900 dark:text-[#e5e5e5]',
  secondary: 'bg-gray-200 dark:bg-[#1a1a1a] hover:bg-gray-300 dark:hover:bg-[#2a2a2a] text-gray-900 dark:text-[#e5e5e5]',
};

const sizeClasses = {
  default: 'h-10 px-4 py-2',
  sm: 'h-9 px-3 text-sm',
  lg: 'h-11 px-8',
  icon: 'h-10 w-10',
};

export const Button = ({ 
  children, 
  variant = 'default', 
  size = 'default',
  className = '', 
  disabled = false,
  onClick,
  type = 'button',
  ...props 
}) => (
  <button
    type={type}
    onClick={onClick}
    disabled={disabled}
    className={`
      inline-flex items-center justify-center rounded-md text-sm font-medium 
      ring-offset-white dark:ring-offset-[#0f0f0f] 
      transition-colors focus-visible:outline-none focus-visible:ring-2 
      focus-visible:ring-gray-950 dark:focus-visible:ring-gray-300 
      focus-visible:ring-offset-2 
      disabled:pointer-events-none disabled:opacity-50
      ${variantClasses[variant]} ${sizeClasses[size]} ${className}
    `}
    {...props}
  >
    {children}
  </button>
);

