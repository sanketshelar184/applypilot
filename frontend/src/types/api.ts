export type User = { id: string; first_name: string; last_name: string | null; username: string | null; language_code: string | null; subscription_status: string };
export type Resume = { id: string; title: string; target_role: string | null; status: string; updated_at: string };
export type Dashboard = { first_name: string; resume_count: number; job_match_count: number; application_count: number; remaining_credits: number; current_plan: string; recent_resumes: Resume[] };
export type AuthResponse = { access_token: string; token_type: "bearer"; user: User };

