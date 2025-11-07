import React from 'react';

export const Progress = ({ value, className = '', max = 100 }) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);
  
  return (
    <div className={`w-full bg-gray-200 dark:bg-[#2a2a2a] rounded-full h-2 overflow-hidden ${className}`}>
      <div
        className="h-full bg-blue-600 dark:bg-blue-500 transition-all duration-300 ease-in-out rounded-full"
        style={{ width: `${percentage}%` }}
      />
    </div>
  );
};
