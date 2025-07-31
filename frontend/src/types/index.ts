export interface APIResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
}

export interface DocumentSummary {
  id: string;
  filename: string;
  summary: string;
  file_size: number;
  page_count: number;
  upload_date: string;
  metadata?: any;
}

export interface DocumentHistory {
  id: string;
  filename: string;
  summary: string;
  upload_date: string;
  file_size: number;
  page_count: number;
}

export interface UploadResponse {
  id: string;
  filename: string;
  summary: string;
  file_size: number;
  page_count: number;
  upload_date: string;
  metadata: any;
}

export interface HistoryResponse {
  documents: DocumentHistory[];
}

export interface UploadState {
  isUploading: boolean;
  progress: number;
  error: string | null;
  result: DocumentSummary | null;
}