import React from 'react';

interface LoadingSpinnerProps {
  progress?: number;
  message?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ progress, message }) => {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <div className="relative">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500"></div>
        {progress !== undefined && (
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-sm font-medium text-blue-600">{progress}%</span>
          </div>
        )}
      </div>

      {message && (
        <p className="mt-4 text-sm text-gray-600 text-center">{message}</p>
      )}

      {progress !== undefined && (
        <div className="w-64 bg-gray-200 rounded-full h-2 mt-4">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all duration-300 ease-out"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      )}
    </div>
  );
};

export default LoadingSpinner;