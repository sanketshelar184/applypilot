"use client";
import { ArrowRight, BriefcaseBusiness, FileText, Plus, Sparkles, Target, WalletCards } from "lucide-react";
import { createResume } from "@/lib/api";
import type { Dashboard as DashboardType } from "@/types/api";

export function Dashboard({ data, onRefresh }: { data: DashboardType; onRefresh: () => Promise<void> }) {
  const startResume = async () => {
    try {
      const { default: WebApp } = await import("@twa-dev/sdk");
      WebApp.HapticFeedback.impactOccurred("light");
      await createResume();
      await onRefresh();
    } catch (error) {
      const message = error instanceof Error ? error.message : "Could not create resume";
      const { default: WebApp } = await import("@twa-dev/sdk");
      WebApp.showAlert(message);
    }
  };
  const stats = [{label:"Resumes",value:data.resume_count,icon:FileText},{label:"Job matches",value:data.job_match_count,icon:Target},{label:"Applications",value:data.application_count,icon:BriefcaseBusiness},{label:"Credits",value:data.remaining_credits,icon:WalletCards}];
  return <main className="mx-auto min-h-screen max-w-5xl px-4 pb-24 pt-5 sm:px-6">
    <header className="flex items-center justify-between"><div><p className="text-sm text-slate-500">Welcome back</p><h1 className="text-2xl font-bold tracking-tight">{data.first_name}</h1></div><span className="rounded-full bg-brand-pale px-3 py-1.5 text-xs font-semibold uppercase tracking-wide text-brand-dark">{data.current_plan} plan</span></header>
    <section className="mt-6 rounded-2xl bg-ink p-5 text-white shadow-soft sm:flex sm:items-center sm:justify-between"><div><div className="mb-2 flex items-center gap-2 text-sm font-medium text-blue-200"><Sparkles size={16}/>Your next opportunity starts here</div><h2 className="max-w-xl text-xl font-semibold">Build a focused, ATS-friendly resume in minutes.</h2><p className="mt-2 text-sm text-slate-300">We’ll guide you section by section. You stay in control of every detail.</p></div><button onClick={startResume} className="mt-5 flex w-full items-center justify-center gap-2 rounded-lg bg-brand px-4 py-3 text-sm font-semibold transition hover:bg-brand-dark sm:mt-0 sm:w-auto"><Plus size={18}/>Create Resume</button></section>
    <section className="mt-6 grid grid-cols-2 gap-3 md:grid-cols-4">{stats.map(({label,value,icon:Icon})=><div key={label} className="rounded-xl border border-slate-200 bg-white p-4"><Icon className="mb-3 text-brand" size={20}/><div className="text-2xl font-bold">{value}</div><div className="text-xs text-slate-500">{label}</div></div>)}</section>
    <section className="mt-7"><div className="mb-3 flex items-center justify-between"><h2 className="text-base font-semibold">Recent resumes</h2>{data.recent_resumes.length>0&&<button className="flex items-center gap-1 text-sm font-medium text-brand">View all <ArrowRight size={15}/></button>}</div>
      {data.recent_resumes.length===0?<div className="rounded-xl border border-dashed border-slate-300 bg-white px-5 py-10 text-center"><FileText className="mx-auto text-slate-400" size={30}/><h3 className="mt-3 font-semibold">You haven&apos;t created a resume yet.</h3><p className="mx-auto mt-1 max-w-sm text-sm text-slate-500">Create your master resume once, then tailor versions for every job.</p><button onClick={startResume} className="mt-5 rounded-lg bg-brand px-4 py-2.5 text-sm font-semibold text-white">Create Resume</button></div>:<div className="space-y-2">{data.recent_resumes.map(r=><article key={r.id} className="flex items-center justify-between rounded-xl border border-slate-200 bg-white p-4"><div><h3 className="font-medium">{r.title}</h3><p className="text-xs text-slate-500">{r.target_role??"Add a target role"} · {r.status}</p></div><ArrowRight size={18} className="text-slate-400"/></article>)}</div>}
    </section>
  </main>;
}
