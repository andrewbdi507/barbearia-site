/** API Client — complete typed wrapper for all backend endpoints */

const API = `${import.meta.env.VITE_API_URL || ""}/api/v1`;

// ---- Helpers ----

async function request<T>(url: string, options: RequestInit = {}): Promise<T> {
  const token = sessionStorage.getItem("access_token");
  const res = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });
  if (!res.ok) {
    if (res.status === 401) {
      sessionStorage.removeItem("access_token");
      window.location.href = "/login";
      throw new Error("Sessão expirada");
    }
    const err = await res.json().catch(() => ({ message: res.statusText }));
    throw new Error(err.message || err.detail || "Erro de API");
  }
  return res.json();
}

// ---- Auth ----

export interface LoginRequest { email: string; password: string; tenant_id?: string }
export interface LoginResponse { access_token: string; token_type: string; expires_in: number; user: { id: string; email: string; name: string } }
export interface RegisterRequest { email: string; password: string; name: string; tenant_id: string }
export interface RegisterResponse { id: string; email: string; name: string; message: string }

export const authAPI = {
  login: (data: LoginRequest) => request<LoginResponse>(`${API}/auth/login`, { method: "POST", body: JSON.stringify(data) }),
  register: (data: RegisterRequest) => request<RegisterResponse>(`${API}/auth/register`, { method: "POST", body: JSON.stringify(data) }),
  me: () => request<{ user_id: string; tenant_id: string; email: string; name: string; role: string }>(`${API}/auth/me`),
  logout: () => request(`${API}/auth/logout`, { method: "POST" }).finally(() => { sessionStorage.removeItem("access_token"); window.location.href = "/login"; }),
};

// ---- Types ----

export interface DashboardKPI { revenue_today: number; bookings_confirmed: number; bookings_completed: number; bookings_cancelled: number; occupancy_pct: number; avg_rating: number; active_staff: number; total_customers: number; total_reviews: number }
export interface TimelineItem { time: string; customer: string; service: string; status: string }
export interface ServiceDTO { id: string; name: string; description: string; price_cents: number; duration_minutes: number; is_active: boolean }
export interface StaffDTO { id: string; professional_name: string; photo_url: string | null; specialties: string[] }
export interface CustomerDTO { id: string; name: string; phone: string; email: string }

// ---- APIs ----

export const adminAPI = {
  getDashboard: () => request<{ kpis: DashboardKPI; today_timeline: TimelineItem[] }>(`${API}/admin/dashboard`),
};

export const servicesAPI = {
  list: () => request<ServiceDTO[]>(`${API}/scheduling/services`),
  create: (d: Partial<ServiceDTO>) => request<ServiceDTO>(`${API}/scheduling/services`, { method: "POST", body: JSON.stringify(d) }),
  update: (id: string, d: Partial<ServiceDTO>) => request<ServiceDTO>(`${API}/scheduling/services/${id}`, { method: "PATCH", body: JSON.stringify(d) }),
  delete: (id: string) => request(`${API}/scheduling/services/${id}`, { method: "DELETE" }),
};

export const staffAPI = { list: () => request<StaffDTO[]>(`${API}/staff`) };
export const customersAPI = { list: () => request<CustomerDTO[]>(`${API}/customers`) };

export const schedulingAPI = {
  list: (date?: string) => request<{ id: string; customer_name: string; service_name: string; booking_time: string; status: string }[]>(`${API}/scheduling/bookings${date ? `?date=${date}` : ""}`),
  create: (d: Record<string, unknown>) => request(`${API}/scheduling/bookings`, { method: "POST", body: JSON.stringify(d) }),
};

export const siteAPI = { get: (subdomain: string) => request<{ tenant: { name: string }; branding: Record<string, string>; services: unknown[] }>(`${API}/site?subdomain=${subdomain}`) };

// ---- AI Agents ----

export interface AgentHealthResponse { agents: Record<string, { status: string; agent?: string; latency_ms?: number; error?: string }>; total: number; healthy: number }

export const agentsAPI = {
  health: () => request<AgentHealthResponse>(`${API}/agents/health`),
  status: (agentId: string) => request(`${API}/agents/${agentId}/status`),
  andExecute: (input: Record<string, unknown>) => request(`${API}/agents/and/execute`, { method: "POST", body: JSON.stringify({ input }) }),
  hermesPlan: (goal: string, constraints?: Record<string, unknown>) => request(`${API}/agents/hermes/plan`, { method: "POST", body: JSON.stringify({ goal, constraints }) }),
  evolverOptimize: (target: string, metrics: Record<string, number>) => request(`${API}/agents/evolver/optimize`, { method: "POST", body: JSON.stringify({ target, metrics }) }),
  genericOrchestrate: (tasks: Record<string, unknown>[]) => request(`${API}/agents/generic/orchestrate`, { method: "POST", body: JSON.stringify({ tasks }) }),
  claudeMemRetrieve: (userId: string, query?: string) => request(`${API}/agents/claude-mem/retrieve`, { method: "POST", body: JSON.stringify({ user_id: userId, query }) }),
  runWorkflow: (workflow: { name: string; steps: Record<string, unknown>[] }) => request(`${API}/agents/workflow`, { method: "POST", body: JSON.stringify(workflow) }),
};

// ---- Plans & Billing ----

export interface PlanDTO {
  id: string;
  name: string;
  slug: string;
  tier: string;
  description: string | null;
  price_monthly: number;
  price_yearly: number;
  limits: Record<string, unknown>;
  features: string[];
  themes: string[];
  ai_tokens: number | null;
  max_concurrent_users: number | null;
  is_active: boolean;
  is_public: boolean;
  sort_order: number;
}

export interface PlanUsageDTO {
  tenant_id: string;
  month: string;
  bookings_count: number;
  ai_tokens_used: number;
  limits: Record<string, unknown>;
}

export interface CheckLimitDTO {
  resource: string;
  current: number;
  max_allowed: number;
  remaining: number;
  exceeded: boolean;
}

export interface TenantMeDTO {
  id: string;
  subdomain: string;
  name: string;
  slug: string;
  status: string;
  plan_id: string | null;
  owner_id: string | null;
  trial_ends_at: string | null;
  settings: Record<string, unknown> | null;
  branding: Record<string, unknown> | null;
  created_at: string;
}

export const planAPI = {
  list: () => request<{ plans: PlanDTO[] }>(`${API}/plans`),
  listAll: () => request<{ plans: PlanDTO[] }>(`${API}/plans/all`),
  get: (id: string) => request<PlanDTO>(`${API}/plans/${id}`),
  getUsage: (id: string) => request<PlanUsageDTO>(`${API}/plans/${id}/usage`),
  checkLimit: (id: string, resource: string) => request<CheckLimitDTO>(`${API}/plans/${id}/check-limit/${resource}`),
};

export const tenantAPI = {
  me: () => request<TenantMeDTO>(`${API}/tenants/me`),
  updateMe: (data: Record<string, unknown>) => request<TenantMeDTO>(`${API}/tenants/me`, { method: "PATCH", body: JSON.stringify(data) }),
  getSubscription: () => request<{ id: string; plan_id: string; status: string; trial_ends_at: string | null }>(`${API}/tenants/me/subscription`),
};
