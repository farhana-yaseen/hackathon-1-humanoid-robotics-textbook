// API client for the Humanoid Robotics Textbook Platform
import { useAuth } from '../contexts/AuthContext';

// Base API configuration
const API_BASE_URL = "http://localhost:8000/api/v1";

// API Client interface
interface TranslationRequest {
  chapter_id: string;
  target_language?: string;
  user_session_id?: string;
}

interface TranslateTextRequest {
  text: string;
  target_language?: string;
}

interface TranslationResponse {
  translated_content: string;
  chapter_id: string;
  target_language: string;
  cached: boolean;
}

interface TranslateTextResponse {
  translated_text: string;
  target_language: string;
}

interface RAGQueryRequest {
  query: string;
  session_id?: string;
}

interface RAGQueryResponse {
  response: string;
  session_id: string;
  selection_context_active: boolean;
}

interface CreateSessionRequest {
  user_id?: string;
}

interface SessionResponse {
  session_id: string;
  user_id?: string;
}

// API Client class
class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  // Translation API methods
  async translateChapter(request: TranslationRequest): Promise<TranslationResponse> {
    const response = await fetch(`${this.baseUrl}/translation/chapters/${request.chapter_id}/translate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        chapter_id: request.chapter_id,
        target_language: request.target_language || 'Urdu',
        user_session_id: request.user_session_id
      })
    });

    if (!response.ok) {
      throw new Error(`Translation API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async translateText(request: TranslateTextRequest): Promise<TranslateTextResponse> {
    const response = await fetch(`${this.baseUrl}/translation/text`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: request.text,
        target_language: request.target_language || 'Urdu'
      })
    });

    if (!response.ok) {
      throw new Error(`Translation API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async translateChatbotResponse(request: TranslateTextRequest): Promise<TranslateTextResponse> {
    const response = await fetch(`${this.baseUrl}/translation/chatbot-response`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: request.text,
        target_language: request.target_language || 'Urdu'
      })
    });

    if (!response.ok) {
      throw new Error(`Translation API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // RAG API methods
  async createRAGSession(request: CreateSessionRequest): Promise<SessionResponse> {
    const response = await fetch(`${this.baseUrl}/rag/sessions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: request.user_id
      })
    });

    if (!response.ok) {
      throw new Error(`RAG Session API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async queryRAG(request: RAGQueryRequest): Promise<RAGQueryResponse> {
    const response = await fetch(`${this.baseUrl}/rag/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: request.query,
        session_id: request.session_id
      })
    });

    if (!response.ok) {
      throw new Error(`RAG Query API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async setSelectionContext(sessionId: string, selectedText: string): Promise<any> {
    const response = await fetch(`${this.baseUrl}/rag/selection-context`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        selected_text: selectedText,
        session_id: sessionId
      })
    });

    if (!response.ok) {
      throw new Error(`RAG Selection Context API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async clearSelectionContext(sessionId: string): Promise<SessionResponse> {
    const response = await fetch(`${this.baseUrl}/rag/clear-selection`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        session_id: sessionId
      })
    });

    if (!response.ok) {
      throw new Error(`RAG Clear Selection API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }
}

// Create and export a singleton instance
export const apiClient = new ApiClient();

// Export types
export type {
  TranslationRequest,
  TranslateTextRequest,
  TranslationResponse,
  TranslateTextResponse,
  RAGQueryRequest,
  RAGQueryResponse,
  CreateSessionRequest,
  SessionResponse
};