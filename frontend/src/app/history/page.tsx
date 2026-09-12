"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useAuthStore } from "@/store/authStore";
import { api, type HistoryItem } from "@/lib/api";
import { formatTimeAgo, truncateText } from "@/lib/utils";
import { Search, Star, Trash2, Download, FileText, Link2, File, Clock, ChevronLeft, ChevronRight, Filter } from "lucide-react";

export default function HistoryPage() {
  const { isAuthenticated, token } = useAuthStore();
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [favOnly, setFavOnly] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isAuthenticated || !token) return;
    setLoading(true);
    api.getHistory(token, page, search, favOnly)
      .then((res) => { setItems(res.items); setTotal(res.total); })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [isAuthenticated, token, page, search, favOnly]);

  const handleDelete = async (id: string) => {
    if (!token) return;
    await api.deleteHistory(token, id);
    setItems((prev) => prev.filter((i) => i.id !== id));
    setTotal((t) => t - 1);
  };

  const handleFavorite = async (id: string) => {
    if (!token) return;
    const res = await api.toggleFavorite(token, id);
    setItems((prev) => prev.map((i) => i.id === id ? { ...i, is_favorite: res.is_favorite } : i));
  };

  const sourceIcon = (type: string) => {
    switch (type) { case "url": return <Link2 size={14} />; case "pdf": case "docx": case "txt": return <File size={14} />; default: return <FileText size={14} />; }
  };

  const totalPages = Math.ceil(total / 20);

  if (!isAuthenticated) {
    return (
      <div style={{ maxWidth: "1280px", margin: "0 auto", padding: "80px 24px", textAlign: "center" }}>
        <div style={{ width: "64px", height: "64px", borderRadius: "var(--radius-lg)", backgroundColor: "var(--bg-secondary)", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 20px" }}>
          <Clock size={28} style={{ color: "var(--text-muted)" }} />
        </div>
        <h2 style={{ fontFamily: "var(--font-serif)", fontSize: "1.5rem", marginBottom: "8px" }}>Sign in to view history</h2>
        <p style={{ color: "var(--text-tertiary)", fontSize: "0.9375rem" }}>Your past summaries will appear here after you log in.</p>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: "1280px", margin: "0 auto", padding: "32px 24px" }}>
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-heading-2" style={{ marginBottom: "4px" }}>History</h1>
        <p style={{ color: "var(--text-tertiary)", fontSize: "0.9375rem", marginBottom: "24px" }}>{total} summaries</p>
      </motion.div>

      {/* Search & Filter Bar */}
      <div style={{ display: "flex", gap: "12px", marginBottom: "24px", flexWrap: "wrap" }}>
        <div style={{ flex: 1, minWidth: "240px", display: "flex", alignItems: "center", gap: "8px", padding: "10px 14px", borderRadius: "var(--radius-md)", border: "1px solid var(--border-default)", backgroundColor: "var(--bg-card)" }}>
          <Search size={16} style={{ color: "var(--text-muted)" }} />
          <input type="text" value={search} onChange={(e) => { setSearch(e.target.value); setPage(1); }} placeholder="Search summaries..." style={{ flex: 1, border: "none", outline: "none", fontSize: "0.875rem", backgroundColor: "transparent", color: "var(--text-primary)", fontFamily: "var(--font-sans)" }} />
        </div>
        <button onClick={() => { setFavOnly(!favOnly); setPage(1); }} style={{
          display: "flex", alignItems: "center", gap: "6px", padding: "10px 16px", borderRadius: "var(--radius-md)", border: "1px solid var(--border-default)", fontSize: "0.8125rem", fontWeight: 500, cursor: "pointer",
          backgroundColor: favOnly ? "var(--accent-primary-light)" : "var(--bg-card)", color: favOnly ? "var(--accent-primary)" : "var(--text-tertiary)", transition: "all 0.2s ease",
        }}>
          <Star size={14} fill={favOnly ? "var(--accent-primary)" : "none"} /> Favorites
        </button>
      </div>

      {/* Results */}
      {loading ? (
        <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-shimmer" style={{ height: "100px", borderRadius: "var(--radius-md)" }} />
          ))}
        </div>
      ) : items.length === 0 ? (
        <div style={{ textAlign: "center", padding: "64px 24px" }}>
          <FileText size={40} style={{ color: "var(--text-muted)", marginBottom: "16px" }} />
          <h3 style={{ fontFamily: "var(--font-serif)", fontSize: "1.25rem", marginBottom: "8px" }}>No summaries yet</h3>
          <p style={{ color: "var(--text-muted)", fontSize: "0.875rem" }}>Your summarization history will appear here.</p>
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          {items.map((item, i) => (
            <motion.div key={item.id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.03 }} style={{
              padding: "16px 20px", borderRadius: "var(--radius-md)", border: "1px solid var(--border-subtle)", backgroundColor: "var(--bg-card)", display: "flex", gap: "16px", alignItems: "flex-start", transition: "all 0.2s ease",
            }}>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "6px" }}>
                  <span style={{ color: "var(--text-muted)" }}>{sourceIcon(item.source_type)}</span>
                  <span style={{ fontSize: "0.9375rem", fontWeight: 500, color: "var(--text-primary)" }}>{item.title || "Untitled"}</span>
                  <span style={{ fontSize: "0.75rem", color: "var(--text-muted)", padding: "2px 8px", borderRadius: "var(--radius-full)", backgroundColor: "var(--bg-secondary)" }}>{item.summary_length}</span>
                </div>
                <p style={{ fontSize: "0.8125rem", color: "var(--text-tertiary)", lineHeight: 1.5 }}>{truncateText(item.summary_text, 180)}</p>
                <div style={{ display: "flex", gap: "12px", marginTop: "8px", fontSize: "0.75rem", color: "var(--text-muted)" }}>
                  <span>{formatTimeAgo(item.created_at)}</span>
                  {item.original_word_count && <span>{item.original_word_count} words</span>}
                </div>
              </div>
              <div style={{ display: "flex", gap: "4px", flexShrink: 0 }}>
                <button onClick={() => handleFavorite(item.id)} style={{ padding: "8px", borderRadius: "var(--radius-sm)", border: "none", backgroundColor: "transparent", cursor: "pointer", color: item.is_favorite ? "#F59E0B" : "var(--text-muted)", transition: "color 0.2s" }}>
                  <Star size={16} fill={item.is_favorite ? "#F59E0B" : "none"} />
                </button>
                <button onClick={() => handleDelete(item.id)} style={{ padding: "8px", borderRadius: "var(--radius-sm)", border: "none", backgroundColor: "transparent", cursor: "pointer", color: "var(--text-muted)", transition: "color 0.2s" }}>
                  <Trash2 size={16} />
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div style={{ display: "flex", justifyContent: "center", gap: "8px", marginTop: "32px" }}>
          <button onClick={() => setPage(Math.max(1, page - 1))} disabled={page === 1} style={{ padding: "8px 12px", borderRadius: "var(--radius-md)", border: "1px solid var(--border-default)", backgroundColor: "var(--bg-card)", cursor: page === 1 ? "not-allowed" : "pointer", color: "var(--text-tertiary)", opacity: page === 1 ? 0.5 : 1 }}>
            <ChevronLeft size={16} />
          </button>
          <span style={{ display: "flex", alignItems: "center", fontSize: "0.875rem", color: "var(--text-tertiary)", padding: "0 12px" }}>Page {page} of {totalPages}</span>
          <button onClick={() => setPage(Math.min(totalPages, page + 1))} disabled={page === totalPages} style={{ padding: "8px 12px", borderRadius: "var(--radius-md)", border: "1px solid var(--border-default)", backgroundColor: "var(--bg-card)", cursor: page === totalPages ? "not-allowed" : "pointer", color: "var(--text-tertiary)", opacity: page === totalPages ? 0.5 : 1 }}>
            <ChevronRight size={16} />
          </button>
        </div>
      )}
    </div>
  );
}
