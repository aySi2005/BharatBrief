/** API client for communicating with the FastAPI backend. */

const API_BASE = process.env.NEXT_PUBLIC_API_URL 
  ? `${process.env.NEXT_PUBLIC_API_URL}/api` 
  : "http://localhost:8000/api";

export type SupportedLanguage = "english" | "hindi" | "french" | "spanish" | "arabic";

export interface SummarizeTextPayload {
  text: string;
  length: "short" | "medium" | "detailed";
  bullet_mode: boolean;
  target_language: SupportedLanguage;
  external_fact_check: boolean;
}

export interface SummarizeMultiTextPayload {
  documents: string[];
  length: "short" | "medium" | "detailed";
  bullet_mode: boolean;
  target_language: SupportedLanguage;
  external_fact_check: boolean;
}

export interface SummarizeURLPayload {
  url: string;
  length: "short" | "medium" | "detailed";
  bullet_mode: boolean;
  target_language: SupportedLanguage;
  external_fact_check: boolean;
}

export interface SummaryAnalytics {
  sentiment: string;
  sentiment_score: number;
  keywords: string[];
  readability_score: number;
  original_word_count: number;
  summary_word_count: number;
  reading_time_saved: number;
  confidence_score: number;
}

export interface ClaimVerification {
  text: string;
  status: string;
  support_score: number;
  evidence: string;
  external_verified?: boolean;
  external_provider?: string | null;
  external_match_score?: number | null;
  external_evidence?: string | null;
}

export interface SummaryVerification {
  supported_claims: number;
  unsupported_claims: number;
  reliability_score: number;
  claims: ClaimVerification[];
  external_fact_check_enabled?: boolean;
}

export interface ArticleMetadata {
  title: string | null;
  author: string | null;
  publish_date: string | null;
  source_url: string | null;
}

export interface SummarizeResponse {
  id: string | null;
  summary: string;
  headline: string | null;
  key_points: string[];
  bullet_summary: string | null;
  analytics: SummaryAnalytics;
  verification: SummaryVerification | null;
  metadata: ArticleMetadata | null;
  created_at: string | null;
}

export interface HistoryItem {
  id: string;
  title: string | null;
  summary_text: string;
  source_type: string;
  source_url: string | null;
  summary_length: string;
  original_word_count: number | null;
  is_favorite: boolean;
  created_at: string;
}

export interface HistoryListResponse {
  items: HistoryItem[];
  total: number;
  page: number;
  per_page: number;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    email: string;
    name: string;
    avatar_url: string | null;
  };
}

class APIError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  
  const { headers, ...restOptions } = options;
  
  const res = await fetch(url, {
    ...restOptions,
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    let message = body.detail;
    if (Array.isArray(message)) {
      message = message.map((m: any) => `${m.loc.join('.')}: ${m.msg}`).join(', ');
    }
    throw new APIError(message || "Request failed", res.status);
  }

  return res.json();
}

export const api = {
  // Summarize
  summarizeText: (data: SummarizeTextPayload, token?: string | null) =>
    request<SummarizeResponse>("/summarize/text", {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      body: JSON.stringify(data),
    }),

  summarizeMulti: (data: SummarizeMultiTextPayload, token?: string | null) =>
    request<SummarizeResponse>("/summarize/multi", {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      body: JSON.stringify(data),
    }),

  summarizeURL: (data: SummarizeURLPayload, token?: string | null) =>
    request<SummarizeResponse>("/summarize/url", {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      body: JSON.stringify(data),
    }),

  summarizeFile: (file: File, length: string, bulletMode: boolean, targetLanguage: SupportedLanguage, token?: string | null) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("length", length);
    formData.append("bullet_mode", String(bulletMode));
    formData.append("target_language", targetLanguage);
    
    const headers: Record<string, string> = {};
    if (token) headers["Authorization"] = `Bearer ${token}`;

    return fetch(`${API_BASE}/summarize/file`, {
      method: "POST",
      headers,
      body: formData,
    }).then(async (res) => {
      if (!res.ok) {
        const body = await res.json().catch(() => ({ detail: res.statusText }));
        throw new APIError(body.detail || "Upload failed", res.status);
      }
      return res.json() as Promise<SummarizeResponse>;
    });
  },

  // Auth
  signup: (name: string, email: string, password: string) =>
    request<AuthResponse>("/auth/signup", {
      method: "POST",
      body: JSON.stringify({ name, email, password }),
    }),

  login: (email: string, password: string) =>
    request<AuthResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  forgotPassword: (email: string) =>
    request<{ message: string }>("/auth/forgot-password", {
      method: "POST",
      body: JSON.stringify({ email }),
    }),

  // History
  getHistory: (token: string, page = 1, search = "", favoritesOnly = false) =>
    request<HistoryListResponse>(
      `/history?token=${token}&page=${page}&search=${encodeURIComponent(search)}&favorites_only=${favoritesOnly}`
    ),

  deleteHistory: (token: string, id: string) =>
    request<{ message: string }>(`/history/${id}?token=${token}`, {
      method: "DELETE",
    }),

  toggleFavorite: (token: string, id: string) =>
    request<{ is_favorite: boolean }>(`/history/${id}/favorite?token=${token}`, {
      method: "PATCH",
    }),

  // Health
  health: () => request<{ status: string; model_loaded: boolean }>("/health"),
};
