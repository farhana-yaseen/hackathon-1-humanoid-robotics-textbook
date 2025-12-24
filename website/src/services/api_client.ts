// API client for the Humanoid Robotics Textbook Platform

// Base API configuration
const API_BASE_URL = "http://localhost:8001/api/v1";

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
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // Create an AbortController for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 35000); // 35 seconds timeout

    try {
      // Use the correct backend endpoint that we implemented
      const response = await fetch(`http://localhost:8001/api/v1/translation/chapters/${request.chapter_id}/translate`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
          chapter_id: request.chapter_id,
          target_language: request.target_language || 'ur', // Use lowercase 'ur' as expected by backend
          user_session_id: request.user_session_id
        }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        if (response.status === 408) {
          throw new Error('Translation request timed out. Please try again.');
        } else {
          throw new Error(`Translation API error: ${response.status} ${response.statusText}`);
        }
      }

      const result = await response.json();

      // Return in the expected format
      return {
        translated_content: result.translated_content,
        chapter_id: request.chapter_id,
        target_language: request.target_language || 'ur',
        cached: false
      };
    } catch (error) {
      clearTimeout(timeoutId);

      if (error instanceof Error && error.name === 'AbortError') {
        throw new Error('Translation request timed out. Please try again.');
      }

      throw error;
    }
  }

  async translateText(request: TranslateTextRequest): Promise<TranslateTextResponse> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 35000); // 35 seconds timeout

    try {
      const response = await fetch(`${this.baseUrl}/text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: request.text,
          target_language: request.target_language || 'Urdu'
        }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        if (response.status === 408) {
          throw new Error('Translation request timed out. Please try again.');
        } else {
          throw new Error(`Translation API error: ${response.status} ${response.statusText}`);
        }
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);

      if (error instanceof Error && error.name === 'AbortError') {
        throw new Error('Translation request timed out. Please try again.');
      }

      throw error;
    }
  }

  async translateChatbotResponse(request: TranslateTextRequest): Promise<TranslateTextResponse> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 35000); // 35 seconds timeout

    try {
      const response = await fetch(`${this.baseUrl}/chatbot-response`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: request.text,
          target_language: request.target_language || 'Urdu'
        }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        if (response.status === 408) {
          throw new Error('Translation request timed out. Please try again.');
        } else {
          throw new Error(`Translation API error: ${response.status} ${response.statusText}`);
        }
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);

      if (error instanceof Error && error.name === 'AbortError') {
        throw new Error('Translation request timed out. Please try again.');
      }

      throw error;
    }
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