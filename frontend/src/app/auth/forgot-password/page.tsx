"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { api } from "@/lib/api";
import { Mail, Loader2, AlertCircle, CheckCircle2, ArrowLeft } from "lucide-react";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await api.forgotPassword(email);
      setSent(true);
    } catch (err: any) {
      setError(err.message || "Failed to send reset email");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "420px", margin: "0 auto", padding: "60px 24px" }}>
      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} style={{ textAlign: "center", marginBottom: "36px" }}>
        <h1 style={{ fontFamily: "var(--font-serif)", fontSize: "2rem", marginBottom: "8px" }}>Reset password</h1>
        <p style={{ color: "var(--text-tertiary)", fontSize: "0.9375rem" }}>We&apos;ll send you a link to reset your password</p>
      </motion.div>

      {sent ? (
        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} style={{ textAlign: "center", padding: "32px", borderRadius: "var(--radius-lg)", border: "1px solid var(--border-subtle)", backgroundColor: "var(--bg-card)" }}>
          <CheckCircle2 size={40} style={{ color: "var(--accent-success)", marginBottom: "16px" }} />
          <h3 style={{ fontSize: "1.125rem", fontWeight: 600, marginBottom: "8px" }}>Check your email</h3>
          <p style={{ fontSize: "0.875rem", color: "var(--text-tertiary)", marginBottom: "20px" }}>If an account with {email} exists, we&apos;ve sent a reset link.</p>
          <Link href="/auth/login" style={{ display: "inline-flex", alignItems: "center", gap: "6px", fontSize: "0.875rem", color: "var(--accent-primary)", textDecoration: "none", fontWeight: 500 }}>
            <ArrowLeft size={14} /> Back to login
          </Link>
        </motion.div>
      ) : (
        <motion.form initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          {error && (
            <div style={{ display: "flex", alignItems: "center", gap: "8px", padding: "10px 14px", borderRadius: "var(--radius-md)", backgroundColor: "rgba(220,38,38,0.08)", color: "var(--accent-error)", fontSize: "0.8125rem" }}>
              <AlertCircle size={14} /> {error}
            </div>
          )}
          <div>
            <label style={{ fontSize: "0.8125rem", fontWeight: 500, color: "var(--text-secondary)", display: "block", marginBottom: "6px" }}>Email</label>
            <div style={{ display: "flex", alignItems: "center", gap: "10px", padding: "12px 16px", borderRadius: "var(--radius-md)", border: "1px solid var(--border-default)", backgroundColor: "var(--bg-input)" }}>
              <Mail size={16} style={{ color: "var(--text-muted)" }} />
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required style={{ flex: 1, border: "none", outline: "none", fontSize: "0.9375rem", backgroundColor: "transparent", color: "var(--text-primary)", fontFamily: "var(--font-sans)" }} />
            </div>
          </div>
          <button type="submit" disabled={loading} style={{
            display: "flex", alignItems: "center", justifyContent: "center", gap: "8px", padding: "14px", borderRadius: "var(--radius-md)", border: "none",
            backgroundColor: "var(--accent-primary)", color: "#fff", fontSize: "0.9375rem", fontWeight: 600, cursor: loading ? "not-allowed" : "pointer", opacity: loading ? 0.7 : 1,
          }}>
            {loading ? <Loader2 size={16} style={{ animation: "spin 1s linear infinite" }} /> : "Send Reset Link"}
          </button>
          <Link href="/auth/login" style={{ textAlign: "center", fontSize: "0.875rem", color: "var(--accent-primary)", textDecoration: "none", display: "flex", alignItems: "center", justifyContent: "center", gap: "6px" }}>
            <ArrowLeft size={14} /> Back to login
          </Link>
        </motion.form>
      )}
    </div>
  );
}
