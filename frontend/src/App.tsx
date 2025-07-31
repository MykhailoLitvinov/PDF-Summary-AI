import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import LoadingSpinner from './components/LoadingSpinner';
import SummaryDisplay from './components/SummaryDisplay';
import HistoryList from './components/HistoryList';
import { apiService } from './services/apiService';
import { DocumentSummary, DocumentHistory, UploadState } from './types';
import { AlertCircle, RefreshCw, Zap } from 'lucide-react';

function App() {
  const [uploadState, setUploadState] = useState<UploadState>({
    isUploading: false,
    progress: 0,
    error: null,
    result: null
  });

  const [history, setHistory] = useState<DocumentHistory[]>([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [isBackendAvailable, setIsBackendAvailable] = useState<boolean | null>(null);

  // Check backend availability on load
  useEffect(() => {
    checkBackendHealth();
    loadHistory();
  }, []);

  const checkBackendHealth = async () => {
    try {
      const isAvailable = await apiService.healthCheck();
      setIsBackendAvailable(isAvailable);
    } catch (error) {
      setIsBackendAvailable(false);
    }
  };

  const loadHistory = async () => {
    setIsLoadingHistory(true);
    try {
      const historyData = await apiService.getHistory();
      setHistory(historyData.documents);
    } catch (error) {
      console.error('Failed to load history:', error);
    } finally {
      setIsLoadingHistory(false);
    }
  };

  const handleFileSelect = async (file: File) => {
    setUploadState({
      isUploading: true,
      progress: 0,
      error: null,
      result: null
    });

    try {
      const result = await apiService.uploadPDF(file, (progress) => {
        setUploadState(prev => ({ ...prev, progress }));
      });

      setUploadState({
        isUploading: false,
        progress: 100,
        error: null,
        result: result
      });

      // Refresh history after successful upload
      await loadHistory();

    } catch (error: any) {
      setUploadState({
        isUploading: false,
        progress: 0,
        error: error.message || 'File processing error',
        result: null
      });
    }
  };

  const resetUpload = () => {
    setUploadState({
      isUploading: false,
      progress: 0,
      error: null,
      result: null
    });
  };

  // Show error if backend is unavailable
  if (isBackendAvailable === false) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md mx-auto text-center p-6">
          <AlertCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Backend Unavailable</h2>
          <p className="text-gray-600 mb-4">
            Failed to connect to the server. Make sure the backend is running on port 8000.
          </p>
          <button
            onClick={checkBackendHealth}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors flex items-center mx-auto"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex items-center">
            <Zap className="h-8 w-8 text-blue-500 mr-3" />
            <div>
              <h1 className="text-3xl font-bold text-gray-800">PDF Summary AI</h1>
              <p className="text-gray-600">Quick summary generation for PDF documents</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Upload */}
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4">Upload Document</h2>

              {!uploadState.result ? (
                <>
                  <FileUpload
                    onFileSelect={handleFileSelect}
                    isUploading={uploadState.isUploading}
                    error={uploadState.error}
                  />

                  {uploadState.isUploading && (
                    <div className="mt-6">
                      <LoadingSpinner
                        progress={uploadState.progress}
                        message="Document processing may take a few minutes..."
                      />
                    </div>
                  )}
                </>
              ) : (
                <div className="text-center py-4">
                  <div className="text-green-600 mb-4">
                    <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                      ✓
                    </div>
                    <p className="text-lg font-medium">Document successfully processed!</p>
                  </div>

                  <button
                    onClick={resetUpload}
                    className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors"
                  >
                    Upload Another File
                  </button>
                </div>
              )}
            </div>

            {/* History */}
            <div>
              {isLoadingHistory ? (
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <LoadingSpinner message="Loading history..." />
                </div>
              ) : (
                <HistoryList documents={history} />
              )}
            </div>
          </div>

          {/* Right Column - Result */}
          <div>
            {uploadState.result && (
              <SummaryDisplay document={uploadState.result} />
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;