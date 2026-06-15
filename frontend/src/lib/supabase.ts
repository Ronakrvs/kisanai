"use client";

import { createClient, SupabaseClient } from "@supabase/supabase-js";

let _client: SupabaseClient | null = null;

export function getSupabase(): SupabaseClient {
  if (!_client) {
    const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? "";
    const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? "";
    _client = createClient(url || "https://placeholder.supabase.co", key || "placeholder");
  }
  return _client;
}

export const supabase = {
  auth: {
    getSession: () => getSupabase().auth.getSession(),
    signInWithOtp: (opts: Parameters<SupabaseClient["auth"]["signInWithOtp"]>[0]) =>
      getSupabase().auth.signInWithOtp(opts),
    verifyOtp: (opts: Parameters<SupabaseClient["auth"]["verifyOtp"]>[0]) =>
      getSupabase().auth.verifyOtp(opts),
    signInWithOAuth: (opts: Parameters<SupabaseClient["auth"]["signInWithOAuth"]>[0]) =>
      getSupabase().auth.signInWithOAuth(opts),
  },
};
