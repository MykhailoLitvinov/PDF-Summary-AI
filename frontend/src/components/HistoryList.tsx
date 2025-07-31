import React from 'react';
import { DocumentHistory } from '../types';
import { Calendar, FileText, HardDrive, Hash } from 'lucide-react';

interface HistoryListProps {
  documents: DocumentHistory[];
}

const HistoryList: React.FC<HistoryListProps> = ({ documents }) => {
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

  if (documents.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Document History</h2>
        <p className="text-gray-500 text-center py-8">
          No processed documents yet
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4">
        Document History ({documents.length})
      </h2>

      <div className="space-y-4">
        {documents.map((doc) => (
          <div
            key={doc.id}
            className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-3">
              <div className="flex items-center mb-2 sm:mb-0">
                <FileText className="h-5 w-5 text-blue-500 mr-2 flex-shrink-0" />
                <h3 className="font-medium text-gray-800 truncate">{doc.filename}</h3>
              </div>

              <div className="flex flex-wrap gap-3 text-xs text-gray-500">
                <div className="flex items-center">
                  <HardDrive className="h-3 w-3 mr-1" />
                  <span>{formatFileSize(doc.file_size)}</span>
                </div>

                <div className="flex items-center">
                  <Hash className="h-3 w-3 mr-1" />
                  <span>{doc.page_count} pages</span>
                </div>

                <div className="flex items-center">
                  <Calendar className="h-3 w-3 mr-1" />
                  <span>{formatDate(doc.upload_date)}</span>
                </div>
              </div>
            </div>

            <div className="text-sm text-gray-600 bg-gray-50 rounded p-3">
              <p className="line-clamp-3">{doc.summary}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HistoryList;