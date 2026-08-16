export function DashboardSkeleton() { return <div className="mx-auto max-w-5xl animate-pulse p-5"><div className="mb-7 h-8 w-52 rounded bg-slate-200"/><div className="grid grid-cols-2 gap-3 md:grid-cols-4">{[1,2,3,4].map(i=><div key={i} className="h-24 rounded-xl bg-white"/>)}</div><div className="mt-7 h-48 rounded-xl bg-white"/></div>; }

