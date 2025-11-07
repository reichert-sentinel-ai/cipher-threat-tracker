import React from 'react';

export const Label = ({ children, className = '', htmlFor, ...props }) => (
  <label
    htmlFor={htmlFor}
    className={`
      text-sm font-medium leading-none peer-disabled:cursor-not-allowed 
      peer-disabled:opacity-70
      text-gray-900 dark:text-[#e5e5e5]
      ${className}
    `}
    {...props}
  >
    {children}
  </label>
);

