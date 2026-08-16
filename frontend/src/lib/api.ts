import type { AuthResponse, Dashboard } from "@/types/api";

const configuredApiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const normalizedApiUrl = configuredApiUrl.replace(/\/$/, "");
const API_URL = normalizedApiUrl.endsWith("/api/v1")
  ? normalizedApiUrl
  : `${normalizedApiUrl}/api/v1`;
const TOKEN_KEY = "applypilot_session";

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = typeof window === "undefined" ? null : sessionStorage.getItem(TOKEN_KEY);
  const response = await fetch(`${API_URL}${path}`, { ...init, headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}), ...init.headers } });
  if (!response.ok) { const body = await response.json().catch(() => null); throw new Error(body?.detail ?? "Something went wrong. Please try again."); }
  return response.json() as Promise<T>;
}

export async function authenticate(initData: string): Promise<AuthResponse> {
  const auth = await request<AuthResponse>("/auth/telegram", { method: "POST", body: JSON.stringify({ init_data: initData }) });
  sessionStorage.setItem(TOKEN_KEY, auth.access_token);
  return auth;
}
export const getDashboard = () => request<Dashboard>("/dashboard");
export const createResume = () => request("/resumes", { method: "POST", body: JSON.stringify({ title: "My Resume" }) });
