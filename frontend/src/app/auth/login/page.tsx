"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/authStore";
import { api } from "@/lib/api";
import { Mail, Lock, Eye, EyeOff, Loader2, AlertCircle, ArrowRight } from "lucide-react";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuthStore();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPw, setShowPw] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await api.login(email, password);
      login(res.user, res.access_token);
      router.push("/summarize");
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  const inputStyle: React.CSSProperties = {
    flex: 1, border: "none", outline: "none", fontSize: "0.9375rem", backgroundColor: "transparent", color: "var(--text-primary)", fontFamily: "var(--font-sans)",
  };
  const fieldStyle: React.CSSProperties = {
    display: "flex", alignItems: "center", gap: "10px", padding: "12px 16px", borderRadius: "var(--radius-md)", border: "1px solid var(--border-default)", backgroundColor: "var(--bg-input)", transition: "border-color 0.2s",
  };

  return (
    <div style={{ maxWidth: "420px", margin: "0 auto", padding: "60px 24px" }}>
      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} style={{ textAlign: "center", marginBottom: "36px" }}>
        <h1 style={{ fontFamily: "var(--font-serif)", fontSize: "2rem", marginBottom: "8px" }}>Welcome back</h1>
        <p style={{ color: "var(--text-tertiary)", fontSize: "0.9375rem" }}>Sign in to your Briefly account</p>
      </motion.div>

      <motion.form initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
        {error && (
          <div style={{ display: "flex", alignItems: "center", gap: "8px", padding: "10px 14px", borderRadius: "var(--radius-md)", backgroundColor: "rgba(220,38,38,0.08)", color: "var(--accent-error)", fontSize: "0.8125rem" }}>
            <AlertCircle size={14} /> {error}
          </div>
        )}

        <div>
          <label style={{ fontSize: "0.8125rem", fontWeight: 500, color: "var(--text-secondary)", display: "block", marginBottom: "6px" }}>Email</label>
          <div style={fieldStyle}>
            <Mail size={16} style={{ color: "var(--text-muted)", flexShrink: 0 }} />
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required style={inputStyle} />
          </div>
        </div>

        <div>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
            <label style={{ fontSize: "0.8125rem", fontWeight: 500, color: "var(--text-secondary)" }}>Password</label>
            <Link href="/auth/forgot-password" style={{ fontSize: "0.8125rem", color: "var(--accent-primary)", textDecoration: "none" }}>Forgot?</Link>
          </div>
          <div style={fieldStyle}>
            <Lock size={16} style={{ color: "var(--text-muted)", flexShrink: 0 }} />
            <input type={showPw ? "text" : "password"} value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" required minLength={8} style={inputStyle} />
            <button type="button" onClick={() => setShowPw(!showPw)} style={{ background: "none", border: "none", cursor: "pointer", color: "var(--text-muted)", padding: 0 }}>
              {showPw ? <EyeOff size={16} /> : <Eye size={16} />}
            </button>
          </div>
        </div>

        <button type="submit" disabled={loading} style={{
          display: "flex", alignItems: "center", justifyContent: "center", gap: "8px", padding: "14px", borderRadius: "var(--radius-md)", border: "none",
          backgroundColor: "var(--accent-primary)", color: "#fff", fontSize: "0.9375rem", fontWeight: 600, cursor: loading ? "not-allowed" : "pointer",
          opacity: loading ? 0.7 : 1, transition: "all 0.2s ease", marginTop: "4px",
        }}>
          {loading ? <Loader2 size={16} style={{ animation: "spin 1s linear infinite" }} /> : <><span>Sign In</span><ArrowRight size={16} /></>}
        </button>

        <p style={{ textAlign: "center", fontSize: "0.875rem", color: "var(--text-tertiary)", marginTop: "8px" }}>
          Don&apos;t have an account?{" "}
          <Link href="/auth/signup" style={{ color: "var(--accent-primary)", textDecoration: "none", fontWeight: 500 }}>Sign up</Link>
        </p>
      </motion.form>
    </div>
  );
}
