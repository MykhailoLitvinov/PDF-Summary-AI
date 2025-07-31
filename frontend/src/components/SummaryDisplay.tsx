import React from 'react';
import { DocumentSummary } from '../types';
import { FileText, Calendar, HardDrive, Hash } from 'lucide-react';

interface SummaryDisplayProps {
  document: DocumentSummary;
}

const SummaryDisplay: React.FC<SummaryDisplayProps> = ({ document }) => {
  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleString('en-US');
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="border-b border-gray-200 pb-4 mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Processing Result</h2>

        <div className="flex flex-wrap gap-4 text-sm text-gray-600">
          <div className="flex items-center">
            <FileText className="h-4 w-4 mr-1" />
            <span>{document.filename}</span>
          </div>

          <div className="flex items-center">
            <HardDrive className="h-4 w-4 mr-1" />
            <span>{formatFileSize(document.file_size)}</span>
          </div>

          <div className="flex items-center">
            <Hash className="h-4 w-4 mr-1" />
            <span>{document.page_count} pages</span>
          </div>

          <div className="flex items-center">
            <Calendar className="h-4 w-4 mr-1" />
            <span>{formatDate(document.upload_date)}</span>
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-3">Document Summary</h3>
        <div className="prose max-w-none">
          <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
            <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
              {document.summary}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SummaryDisplay;