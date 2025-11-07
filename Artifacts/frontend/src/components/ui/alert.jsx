import React from 'react';
import { AlertTriangle, Info, CheckCircle, XCircle } from 'lucide-react';

const iconMap = {
  default: Info,
  destructive: AlertTriangle,
  success: CheckCircle,
  warning: AlertTriangle,
};

export const Alert = ({ children, className = '', variant = 'default' }) => {
  const Icon = iconMap[variant] || iconMap.default;
  
  const variantStyles = {
    default: 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800 text-blue-900 dark:text-blue-200',
    destructive: 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800 text-red-900 dark:text-red-200',
    success: 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800 text-green-900 dark:text-green-200',
    warning: 'bg-orange-50 dark:bg-orange-900/20 border-orange-200 dark:border-orange-800 text-orange-900 dark:text-orange-200',
  };

  return (
    <div className={`relative w-full rounded-lg border p-4 ${variantStyles[variant]} ${className}`}>
      <div className="flex gap-3">
        <Icon className="h-4 w-4 mt-0.5 flex-shrink-0" />
        <div className="flex-1">
          {children}
        </div>
      </div>
    </div>
  );
};

export const AlertDescription = ({ children, className = '' }) => {
  return (
    <div className={`text-sm ${className}`}>
      {children}
    </div>
  );
};

export const AlertTitle = ({ children, className = '' }) => {
  return (
    <h5 className={`mb-1 font-medium leading-none tracking-tight ${className}`}>
      {children}
    </h5>
  );
};

