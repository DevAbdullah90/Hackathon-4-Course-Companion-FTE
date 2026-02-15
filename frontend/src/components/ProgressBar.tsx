import React from 'react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface ProgressBarProps {
  value: number;
  max?: number;
  className?: string;
  indicatorClassName?: string;
}

const ProgressBar: React.FC<ProgressBarProps> = ({ 
  value, 
  max = 100, 
  className,
  indicatorClassName 
}) => {
  const percentage = Math.min(Math.max(0, (value / max) * 100), 100);

  return (
    <div className={cn("w-full bg-secondary h-2 rounded-full overflow-hidden", className)}>
      <div 
        className={cn("bg-primary h-full transition-all duration-500", indicatorClassName)} 
        style={{ width: `${percentage}%` }}
      />
    </div>
  );
};

export default ProgressBar;
