import React from 'react';

export const Textarea = ({ 
  className = '', 
  placeholder,
  value,
  onChange,
  rows = 4,
  ...props 
}) => (
  <textarea
    placeholder={placeholder}
    value={value}
    onChange={onChange}
    rows={rows}
    className={`
      flex min-h-[80px] w-full rounded-md border border-gray-300 dark:border-[#2a2a2a]
      bg-white dark:bg-[#1a1a1a] px-3 py-2 text-sm
      ring-offset-white dark:ring-offset-[#0f0f0f]
      placeholder:text-gray-500 dark:placeholder:text-[#6a6a6a]
      focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-950 
      dark:focus-visible:ring-gray-300 focus-visible:ring-offset-2
      disabled:cursor-not-allowed disabled:opacity-50
      text-gray-900 dark:text-[#e5e5e5]
      ${className}
    `}
    {...props}
  />
);

