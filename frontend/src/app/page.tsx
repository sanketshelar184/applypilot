"use client";
import { AlertTriangle } from "lucide-react";
import { Dashboard } from "@/components/Dashboard";
import { DashboardSkeleton } from "@/components/DashboardSkeleton";
import { useTelegramAuth } from "@/hooks/useTelegramAuth";

export default function Home() {
  const { loading, dashboard, error, reload } = useTelegramAuth();
  if (loading) return <DashboardSkeleton/>;
  if (error || !dashboard) return <main className="flex min-h-screen items-center justify-center p-6"><div className="max-w-sm rounded-xl border border-red-200 bg-white p-6 text-center"><AlertTriangle className="mx-auto text-red-500"/><h1 className="mt-3 font-semibold">Secure sign-in required</h1><p className="mt-2 text-sm text-slate-600">{error}</p></div></main>;
  return <Dashboard data={dashboard} onRefresh={reload}/>;
}

