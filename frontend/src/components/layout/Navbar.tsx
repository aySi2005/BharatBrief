"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ThemeToggle } from "./ThemeToggle";
import { useAuthStore } from "@/store/authStore";
import {
  FileText,
  History,
  LogIn,
  LogOut,
  Menu,
  X,
  User,
} from "lucide-react";

const navLinks = [
  { href: "/summarize", label: "Summarize", icon: FileText },
  { href: "/history", label: "History", icon: History },
];

export function Navbar() {
  const pathname = usePathname();
  const { isAuthenticated, user, logout } = useAuthStore();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const isLanding = pathname === "/";

  return (
    <header
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        zIndex: 100,
        backdropFilter: scrolled ? "blur(16px)" : "none",
        backgroundColor: scrolled
          ? "color-mix(in srgb, var(--bg-primary) 85%, transparent)"
          : "transparent",
        borderBottom: scrolled
          ? "1px solid var(--border-subtle)"
          : "1px solid transparent",
        transition: "all 0.3s ease",
      }}
    >
      <nav
        style={{
          maxWidth: "1280px",
          margin: "0 auto",
          padding: "0 24px",
          height: "64px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        {/* Logo */}
        <Link
          href="/"
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            textDecoration: "none",
          }}
        >
          <span
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "1.5rem",
              color: "var(--text-primary)",
              letterSpacing: "-0.02em",
            }}
          >
            BharatBrief
          </span>
          
        </Link>

        {/* Desktop Nav */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
          }}
          className="hide-mobile"
        >
          {navLinks.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "6px",
                  padding: "8px 14px",
                  borderRadius: "var(--radius-md)",
                  fontSize: "0.875rem",
                  fontWeight: 500,
                  color: isActive
                    ? "var(--accent-primary)"
                    : "var(--text-tertiary)",
                  backgroundColor: isActive
                    ? "var(--accent-primary-light)"
                    : "transparent",
                  textDecoration: "none",
                  transition: "all 0.2s ease",
                }}
              >
                <link.icon size={16} />
                {link.label}
              </Link>
            );
          })}
        </div>

        {/* Right side */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
          }}
        >
          <ThemeToggle />

          {isAuthenticated ? (
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "8px",
              }}
              className="hide-mobile"
            >
              <span
                style={{
                  fontSize: "0.875rem",
                  color: "var(--text-tertiary)",
                }}
              >
                {user?.name}
              </span>
              <button
                onClick={logout}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "6px",
                  padding: "8px 14px",
                  borderRadius: "var(--radius-md)",
                  fontSize: "0.875rem",
                  fontWeight: 500,
                  color: "var(--text-tertiary)",
                  background: "none",
                  border: "1px solid var(--border-default)",
                  cursor: "pointer",
                  transition: "all 0.2s ease",
                }}
              >
                <LogOut size={14} />
                Logout
              </button>
            </div>
          ) : (
            <Link
              href="/auth/login"
              style={{
                display: "flex",
                alignItems: "center",
                gap: "6px",
                padding: "8px 18px",
                borderRadius: "var(--radius-md)",
                fontSize: "0.875rem",
                fontWeight: 600,
                color: "var(--text-inverse)",
                backgroundColor: "var(--accent-primary)",
                textDecoration: "none",
                transition: "all 0.2s ease",
              }}
              className="hide-mobile"
            >
              <LogIn size={14} />
              Sign In
            </Link>
          )}

          {/* Mobile menu toggle */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            style={{
              display: "none",
              padding: "8px",
              background: "none",
              border: "none",
              cursor: "pointer",
              color: "var(--text-primary)",
            }}
            className="show-mobile"
          >
            {mobileOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </nav>

      {/* Mobile Menu */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            style={{
              backgroundColor: "var(--bg-primary)",
              borderTop: "1px solid var(--border-subtle)",
              padding: "16px 24px",
            }}
            className="show-mobile"
          >
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileOpen(false)}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  padding: "12px 0",
                  fontSize: "1rem",
                  color: "var(--text-secondary)",
                  textDecoration: "none",
                  borderBottom: "1px solid var(--border-subtle)",
                }}
              >
                <link.icon size={18} />
                {link.label}
              </Link>
            ))}
            {!isAuthenticated && (
              <Link
                href="/auth/login"
                onClick={() => setMobileOpen(false)}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  padding: "12px 0",
                  fontSize: "1rem",
                  color: "var(--accent-primary)",
                  textDecoration: "none",
                }}
              >
                <LogIn size={18} />
                Sign In
              </Link>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Responsive styles */}
      <style jsx global>{`
        @media (min-width: 768px) {
          .show-mobile {
            display: none !important;
          }
        }
        @media (max-width: 767px) {
          .hide-mobile {
            display: none !important;
          }
          .show-mobile {
            display: flex !important;
          }
        }
      `}</style>
    </header>
  );
}
