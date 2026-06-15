"use client";

export const dynamic = "force-dynamic";

import { useState } from "react";
import { supabase } from "@/lib/supabase";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Leaf, Loader2 } from "lucide-react";
import { toast } from "sonner";

type Mode = "phone" | "otp";

export default function AuthPage() {
  const [mode, setMode] = useState<Mode>("phone");
  const [phone, setPhone] = useState("");
  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);

  const sendOTP = async () => {
    if (!phone.match(/^\+91[0-9]{10}$/)) {
      toast.error("Enter valid phone: +91XXXXXXXXXX");
      return;
    }
    setLoading(true);
    const { error } = await supabase.auth.signInWithOtp({ phone });
    setLoading(false);
    if (error) { toast.error(error.message); return; }
    toast.success("OTP sent!");
    setMode("otp");
  };

  const verifyOTP = async () => {
    if (otp.length !== 6) { toast.error("Enter 6-digit OTP"); return; }
    setLoading(true);
    const { error } = await supabase.auth.verifyOtp({ phone, token: otp, type: "sms" });
    setLoading(false);
    if (error) { toast.error(error.message); return; }
    toast.success("Logged in!");
    window.location.href = "/";
  };

  const loginWithGoogle = async () => {
    await supabase.auth.signInWithOAuth({
      provider: "google",
      options: { redirectTo: `${window.location.origin}/` },
    });
  };

  return (
    <div className="max-w-sm mx-auto mt-16">
      <div className="text-center mb-8">
        <div className="flex justify-center mb-3">
          <div className="rounded-full bg-primary/10 p-3">
            <Leaf className="h-8 w-8 text-primary" />
          </div>
        </div>
        <h1 className="text-2xl font-bold">KisanAI Login</h1>
        <p className="text-muted-foreground text-sm">Login to save your history</p>
      </div>

      <Card>
        <CardHeader><CardTitle>Sign In</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          {mode === "phone" ? (
            <>
              <div className="space-y-1">
                <label className="text-sm font-medium">Phone Number</label>
                <Input
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="+91XXXXXXXXXX"
                  type="tel"
                />
              </div>
              <Button onClick={sendOTP} disabled={loading} className="w-full">
                {loading ? <Loader2 className="animate-spin h-4 w-4 mr-2" /> : null}
                Send OTP
              </Button>
            </>
          ) : (
            <>
              <p className="text-sm text-muted-foreground">OTP sent to {phone}</p>
              <div className="space-y-1">
                <label className="text-sm font-medium">Enter OTP</label>
                <Input
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  placeholder="6-digit code"
                  maxLength={6}
                  type="number"
                />
              </div>
              <Button onClick={verifyOTP} disabled={loading} className="w-full">
                {loading ? <Loader2 className="animate-spin h-4 w-4 mr-2" /> : null}
                Verify OTP
              </Button>
              <button onClick={() => setMode("phone")} className="text-sm text-muted-foreground hover:text-foreground w-full text-center">
                Change number
              </button>
            </>
          )}

          <div className="relative">
            <div className="absolute inset-0 flex items-center"><span className="w-full border-t" /></div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-card px-2 text-muted-foreground">Or</span>
            </div>
          </div>

          <Button variant="outline" onClick={loginWithGoogle} className="w-full">
            Continue with Google
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
