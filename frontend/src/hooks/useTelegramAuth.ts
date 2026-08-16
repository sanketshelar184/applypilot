"use client";
import { useEffect, useState } from "react";
import WebApp from "@twa-dev/sdk";
import { authenticate, getDashboard } from "@/lib/api";
import type { Dashboard } from "@/types/api";

type State = { loading: boolean; dashboard: Dashboard | null; error: string | null };
export function useTelegramAuth() {
  const [state, setState] = useState<State>({ loading: true, dashboard: null, error: null });
  const reload = async () => { const dashboard = await getDashboard(); setState({ loading: false, dashboard, error: null }); };
  useEffect(() => {
    let active = true;
    (async () => {
      try {
        WebApp.ready(); WebApp.expand();
        if (!WebApp.initData) throw new Error("Open ApplyPilot from the Telegram bot to sign in securely.");
        await authenticate(WebApp.initData);
        const dashboard = await getDashboard();
        if (active) setState({ loading: false, dashboard, error: null });
      } catch (error) { if (active) setState({ loading: false, dashboard: null, error: error instanceof Error ? error.message : "Unable to sign in" }); }
    })();
    return () => { active = false; };
  }, []);
  return { ...state, reload };
}

