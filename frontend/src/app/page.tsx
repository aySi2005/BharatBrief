"use client";

import { Poppins } from "next/font/google";


import Link from "next/link";
import {
  ArrowRight,
  BarChart3,
  BookOpenText,
  BrainCircuit,
  CheckCircle2,
  FileText,
  Globe2,
  Search,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800", "900"],
});

const highlights = [
  { label: "Documents Processed", value: "10K+", icon: FileText },
  { label: "Key Claims Verifiable", value: "95%", icon: CheckCircle2 },
  { label: "Input Formats", value: "4", icon: BookOpenText },
  { label: "Information Access", value: "24/7", icon: Globe2 },
];

const services = [
  {
    title: "Text Summarization",
    text: "Paste an article, report, or any long text and convert it into a clean summary.",
    icon: FileText,
    accent: "#4F46E5",
    soft: "rgba(79, 70, 229, 0.12)",
  },
  {
    title: "Web Article Summary",
    text: "Enter a URL and extract the essential information from the page in seconds.",
    icon: Globe2,
    accent: "#0E8F67",
    soft: "rgba(14, 143, 103, 0.12)",
  },
  {
    title: "Document Summary",
    text: "Upload PDF, DOCX, or TXT files and get a concise, structured brief.",
    icon: BookOpenText,
    accent: "#F59E0B",
    soft: "rgba(245, 158, 11, 0.12)",
  },
  {
    title: "Source Verification",
    text: "Check whether summary claims are supported by the original source content.",
    icon: ShieldCheck,
    accent: "#DC2626",
    soft: "rgba(220, 38, 38, 0.12)",
  },
];

const categories = [
  { title: "Global Affairs", text: "International relations, diplomacy, and geopolitical updates." },
  { title: "Business & Economy", text: "Financial reports, markets, and corporate developments." },
  { title: "Technology & AI", text: "Research, breakthroughs, and digital innovation updates." },
  { title: "Policy & Security", text: "Government strategy, security, and public policy analysis." },
  { title: "Research & Education", text: "Academic insights, reports, and thought leadership." },
  { title: "General Documents", text: "Any document content that needs better clarity and understanding." },
];

const steps = [
  { number: "01", title: "Input", text: "Paste text, add a URL, or upload a document." },
  { number: "02", title: "AI Analysis", text: "Our system reads, extracts, and summarizes core meaning." },
  { number: "03", title: "Results", text: "Receive a reliable brief with verification indicators." },
];

const trustPoints = [
  { title: "Smart AI", text: "Fine-tuned summarization for clearer, faster understanding." },
  { title: "Source Verification", text: "Claims are checked against the original text for reliability." },
  { title: "Analytics", text: "Measure sentiment, readability, and confidence signals." },
  { title: "Multiple Formats", text: "Works with text, URLs, PDFs, and DOCX files." },
];

export default function Page() {
  return (
    <main
  className={poppins.className}
  style={{
    minHeight: "100vh",
    background: "var(--bg-primary)",
  color: "var(--text-primary)",
  }}
>
      <section
        style={{
          position: "relative",
          overflow: "hidden",
          backgroundImage:
            "linear-gradient(135deg, rgba(9, 27, 42, 0.7), rgba(12, 61, 87, 0.38)), url('https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=1600&q=80')",
          backgroundSize: "cover",
          backgroundPosition: "center",
          boxShadow: "inset 0 0 0 1px rgba(255,255,255,0.08)",
        }}
      >
        <div
          style={{
            maxWidth: "1320px",
            margin: "0 auto",
            padding: "32px 24px 64px",
            position: "relative",
          }}
        >
          <div
            className="hero-grid"
            style={{
              display: "grid",
              gridTemplateColumns: "1.2fr 0.8fr",
              gap: "28px",
              paddingTop: "36px",
              alignItems: "center",
            }}
          >
            <div>
              <p
                style={{
                  margin: 0,
                  color: "#f4f8fb",
                  fontSize: "0.9rem",
                  letterSpacing: "0.18em",
                  fontWeight: 700,
                  textTransform: "uppercase",
                }}
              >
                SUMMARIZE • UNDERSTAND • VERIFY
              </p>

              <h1
                style={{
                  margin: "26px 0 18px",
                  fontSize: "clamp(3.4rem, 5vw, 7rem)",
                  lineHeight: 0.96,
                  letterSpacing: "-0.065em",
                  fontWeight: 700,
                  color: "#ffffff",
                }}
              >
                Read less.
                <br />
                <span
                  style={{
                    background: "linear-gradient(90deg, #ffb347 0%, #ff7b54 45%, #eb4d4b 100%)",
                    WebkitBackgroundClip: "text",
                    backgroundClip: "text",
                    color: "transparent",
                  }}
                >
                  Know more.
                </span>
              </h1>

              <p
                style={{
                  margin: 0,
                  color: "rgba(255,255,255,0.86)",
                  maxWidth: "620px",
                  fontSize: "1.2rem",
                  lineHeight: 1.6,
                }}
              >
                Turn complex information into clear, trustworthy briefs with BharatBrief.
              </p>

              <div style={{ marginTop: "28px", display: "flex", gap: "14px", flexWrap: "wrap" }}>
                <Link
                  href="/summarize"
                  style={{
                    display: "inline-flex",
                    alignItems: "center",
                    justifyContent: "center",
                    gap: "10px",
                    padding: "16px 28px",
                    borderRadius: "18px",
                    background: "linear-gradient(135deg, #ff5c5c, #e92a4a)",
                    color: "#ffffff",
                    textDecoration: "none",
                    fontWeight: 800,
                    boxShadow: "0 18px 32px rgba(233, 42, 74, 0.35)",
                  }}
                >
                  Start Summarizing
                  <ArrowRight size={18} />
                </Link>
              </div>
            </div>

            <div
              style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                position: "relative",
              }}
            >
              <div
                style={{
                  width: "100%",
                  maxWidth: "420px",
                  background: "rgba(12, 38, 61, 0.34)",
                  border: "1px solid rgba(255,255,255,0.24)",
                  borderRadius: "26px",
                  padding: "20px",
                  backdropFilter: "blur(8px)",
                  boxShadow: "0 30px 60px rgba(10, 26, 36, 0.25)",
                }}
              >
                <div
                  style={{
                    background: "rgba(255,255,255,0.12)",
                    border: "1px solid rgba(255,255,255,0.2)",
                    borderRadius: "18px",
                    padding: "18px",
                    color: "#ffffff",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      gap: "12px",
                      marginBottom: "16px",
                    }}
                  >
                    <div style={{ fontSize: "0.72rem", textTransform: "uppercase", letterSpacing: "0.12em", opacity: 0.8 }}>
                      Digital India
                    </div>
                    <div style={{ fontSize: "0.72rem", fontWeight: 700, opacity: 0.9 }}>AI</div>
                  </div>

                  <div
                    style={{
                      display: "flex",
                      justifyContent: "center",
                      alignItems: "center",
                      height: "160px",
                      borderRadius: "18px",
                      background:
                        "linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.02)), url('https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=900&q=80')",
                      backgroundSize: "cover",
                      backgroundPosition: "center",
                      border: "1px solid rgba(255,255,255,0.18)",
                    }}
                  >
                    <div
                      style={{
                        width: "120px",
                        height: "120px",
                        borderRadius: "50%",
                        background: "radial-gradient(circle at center, #f7f7f7 0%, rgba(255,255,255,0.2) 35%, transparent 75%)",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        border: "1px solid rgba(255,255,255,0.18)",
                        boxShadow: "0 10px 24px rgba(0,0,0,0.2)",
                      }}
                    >
                      <div
                        style={{
                          fontSize: "3rem",
                          fontWeight: 900,
                          color: "#ffffff",
                          textShadow: "0 6px 18px rgba(0,0,0,0.35)",
                        }}
                      >
                        ☼
                      </div>
                    </div>
                  </div>

                  <div style={{ marginTop: "18px", display: "grid", gap: "10px" }}>
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                        background: "rgba(255,255,255,0.08)",
                        border: "1px solid rgba(255,255,255,0.14)",
                        borderRadius: "12px",
                        padding: "10px 12px",
                      }}
                    >
                      <span style={{ fontSize: "0.8rem", opacity: 0.86 }}>AI Summary</span>
                      <span style={{ fontSize: "0.8rem", fontWeight: 700 }}>92%</span>
                    </div>
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                        background: "rgba(255,255,255,0.08)",
                        border: "1px solid rgba(255,255,255,0.14)",
                        borderRadius: "12px",
                        padding: "10px 12px",
                      }}
                    >
                      <span style={{ fontSize: "0.8rem", opacity: 0.86 }}>Verifiable Claims</span>
                      <span style={{ fontSize: "0.8rem", fontWeight: 700 }}>95%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div
            style={{
              maxWidth: "1180px",
              margin: "40px auto 0",
              background: "rgba(255,255,255,0.9)",
              border: "1px solid rgba(16, 41, 61, 0.06)",
              borderRadius: "26px",
              boxShadow: "0 24px 48px rgba(11, 33, 52, 0.12)",
              padding: "18px 20px",
            }}
          >
            <div
              className="quick-input-grid"
              style={{
                display: "grid",
                gridTemplateColumns: "1.6fr 0.8fr 0.8fr 0.8fr 0.8fr",
                gap: "14px",
                alignItems: "center",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "12px",
                  background: "#f3f7fb",
                  borderRadius: "16px",
                  padding: "14px 16px",
                  border: "1px solid #e2ebf5",
                }}
              >
                <Search size={20} color="#0d2d3c" />
                <input
                  placeholder="Paste text, enter an article URL, or upload a document"
                  style={{
                    flex: 1,
                    border: "none",
                    background: "transparent",
                    outline: "none",
                    color: "var(--text-primary)",
                    fontSize: "1rem",
                  }}
                />
              </div>

              <button
                style={{
                  border: "none",
                  borderRadius: "16px",
                  fontWeight: 800,
                  padding: "16px 18px",
                  background: "linear-gradient(135deg, #ff5c5c, #e92a4a)",
                  color: "#fff",
                  boxShadow: "0 14px 24px rgba(233, 42, 74, 0.24)",
                  cursor: "pointer",
                }}
              >
                Summarize
              </button>

              <button
                style={{
                  border: "1px solid #d8e0eb",
                  borderRadius: "16px",
                  fontWeight: 700,
                  padding: "16px 18px",
                  background: "var(--bg-secondary)",
                  color: "var(--text-primary)",
                  cursor: "pointer",
                }}
              >
                Text Summary
              </button>

              <button
                style={{
                  border: "1px solid #d8e0eb",
                  borderRadius: "16px",
                  fontWeight: 700,
                  padding: "16px 18px",
                  background: "var(--bg-secondary)",
                  color: "var(--text-primary)",
                  cursor: "pointer",
                }}
              >
                Web URL
              </button>

              <button
                style={{
                  border: "1px solid #d8e0eb",
                  borderRadius: "16px",
                  fontWeight: 700,
                  padding: "16px 18px",
                  background: "var(--bg-secondary)",
                  color: "var(--text-primary)",
                  cursor: "pointer",
                }}
              >
                PDF / DOCX
              </button>
            </div>
          </div>
        </div>
      </section>

      <section style={{ maxWidth: "1320px", margin: "0 auto", padding: "26px 24px 18px" }}>
        <div
          className="highlights-grid"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
            gap: "18px",
            background: "rgba(255,255,255,0.75)",
            border: "1px solid rgba(17, 53, 79, 0.08)",
            borderRadius: "22px",
            padding: "18px",
          }}
        >
          {highlights.map((item) => {
            const Icon = item.icon;
            return (
              <div
                key={item.label}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "14px",
                  background: "#f7f9fb",
                  borderRadius: "18px",
                  padding: "18px 16px",
                  border: "1px solid #edf2f6",
                }}
              >
                <div
                  style={{
                    width: "42px",
                    height: "42px",
                    borderRadius: "12px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    background: "rgba(77, 101, 138, 0.1)",
                    color: "#315b7a",
                  }}
                >
                  <Icon size={18} />
                </div>
                <div>
                  <div style={{ fontSize: "1.9rem", fontWeight: 900, lineHeight: 1, color: "#17324d" }}>{item.value}</div>
                  <div style={{ marginTop: "6px", fontSize: "0.9rem", color: "#4f687d" }}>{item.label}</div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <section style={{ maxWidth: "1320px", margin: "0 auto", padding: "54px 24px 10px" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            marginBottom: "24px",
            gap: "16px",
            flexWrap: "wrap",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
            <div
              style={{
                width: "42px",
                height: "4px",
                borderRadius: "999px",
                background: "linear-gradient(90deg, #ff5c5c, #0f9f6c)",
              }}
            />
            <h2
              style={{
                margin: 0,
                fontSize: "clamp(2rem, 4vw, 2.8rem)",
                color: "var(--text-primary)",
                letterSpacing: "-0.04em",
                fontWeight: 700,
              }}
            >
              Our Services
            </h2>
          </div>
          <Link
            href="#services"
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "8px",
              color: "var(--text-primary)",
              textDecoration: "none",
              fontWeight: 700,
            }}
          >
            Explore All Services
            <ArrowRight size={16} />
          </Link>
        </div>

        <div
          id="services"
          className="services-grid"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
            gap: "18px",
          }}
        >
          {services.map((service) => {
            const Icon = service.icon;
            return (
              <div
                key={service.title}
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: "18px",
                  background: service.soft,
                  border: "1px solid rgba(17, 53, 79, 0.08)",
                  borderRadius: "26px",
                  padding: "24px 20px",
                  boxShadow: "0 16px 26px rgba(16, 41, 61, 0.04)",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    gap: "16px",
                  }}
                >
                  <div
                    style={{
                      width: "48px",
                      height: "48px",
                      borderRadius: "14px",
                      background: service.accent,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      color: "#fff",
                    }}
                  >
                    <Icon size={22} />
                  </div>
                  <ArrowRight size={18} color={service.accent} />
                </div>

                <div>
                  <h3 style={{ margin: 0, fontSize: "1.4rem", color: "var(--text-primary)" }}>{service.title}</h3>
                  <p style={{ margin: "12px 0 0", color: "var(--text-secondary)", lineHeight: 1.7 }}>{service.text}</p>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <section style={{ maxWidth: "1320px", margin: "0 auto", padding: "62px 24px 18px" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            marginBottom: "24px",
            gap: "16px",
            flexWrap: "wrap",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
            <div
              style={{
                width: "42px",
                height: "4px",
                borderRadius: "999px",
                background: "linear-gradient(90deg, #ff5c5c, #0f9f6c)",
              }}
            />
            <h2
              style={{
                margin: 0,
                fontSize: "clamp(2rem, 4vw, 2.8rem)",
                color: "var(--text-primary)",
                letterSpacing: "-0.04em",
              }}
            >
              Information Categories
            </h2>
          </div>
          <Link
            href="#categories"
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "8px",
              color: "var(--text-primary)",
              textDecoration: "none",
              fontWeight: 700,
            }}
          >
            View All Categories
            <ArrowRight size={16} />
          </Link>
        </div>

        <div
          id="categories"
          className="categories-grid"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
            gap: "18px",
          }}
        >
          {categories.map((category, index) => (
            <div
              key={category.title}
              style={{
                background: "var(--bg-secondary)",
                border: "1px solid #e5edf4",
                borderRadius: "22px",
                padding: "24px 20px",
                boxShadow: "0 16px 26px rgba(16, 41, 61, 0.03)",
              }}
            >
              <div
                style={{
                  width: "44px",
                  height: "44px",
                  borderRadius: "14px",
                  background: ["#e2ebff", "#e5f9f0", "#fff0d9", "#ffe4e6", "#f0ebff", "#edf6ff"][index % 6],
                  color: "var(--text-primary)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontWeight: 900,
                  fontSize: "1.2rem",
                }}
              >
                {category.title.charAt(0)}
              </div>
              <h3 style={{ margin: "18px 0 10px", fontSize: "1.35rem", color: "var(--text-primary)" }}>{category.title}</h3>
              <p style={{ margin: 0, color: "var(--text-secondary)", lineHeight: 1.7 }}>{category.text}</p>
            </div>
          ))}
        </div>
      </section>

      <section style={{ maxWidth: "1320px", margin: "0 auto", padding: "64px 24px 18px" }}>
        <div style={{ textAlign: "center", marginBottom: "30px" }}>
          <h2 style={{ margin: 0, fontSize: "clamp(2rem, 4vw, 2.8rem)", color: "var(--text-primary)", letterSpacing: "-0.04em" }}>
            How It Works
          </h2>
        </div>

        <div
          className="steps-grid"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
            gap: "18px",
          }}
        >
          {steps.map((step) => (
            <div
              key={step.number}
              style={{
                background: "var(--bg-secondary)",
                border: "1px solid #e5edf4",
                borderRadius: "24px",
                padding: "28px 22px",
                boxShadow: "0 16px 26px rgba(16, 41, 61, 0.03)",
              }}
            >
              <div style={{ color: "#ff6659", fontSize: "0.82rem", fontWeight: 800, letterSpacing: "0.12em", marginBottom: "14px" }}>
                {step.number}
              </div>
              <h3 style={{ margin: 0, fontSize: "1.6rem", color: "var(--text-primary)" }}>{step.title}</h3>
              <p style={{ margin: "12px 0 0", color: "var(--text-secondary)", lineHeight: 1.7 }}>{step.text}</p>
            </div>
          ))}
        </div>
      </section>

      <section style={{ maxWidth: "1320px", margin: "0 auto", padding: "64px 24px 18px" }}>
        <div style={{ textAlign: "center", marginBottom: "30px" }}>
          <h2 style={{ margin: 0, fontSize: "clamp(2rem, 4vw, 2.8rem)", color: "var(--text-primary)", letterSpacing: "-0.04em" }}>
            Why BharatBrief
          </h2>
        </div>

        <div
          className="trust-grid"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
            gap: "18px",
          }}
        >
          {trustPoints.map((item) => (
            <div
              key={item.title}
              style={{
                background: "#f7f9fc",
                border: "1px solid #e3eaef",
                borderRadius: "24px",
                padding: "24px 20px",
                boxShadow: "0 16px 24px rgba(16, 41, 61, 0.02)",
              }}
            >
              <div
                style={{
                  width: "48px",
                  height: "48px",
                  borderRadius: "14px",
                  background: "linear-gradient(135deg, #dfe9ff, #edf6ff)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "var(--text-primary)",
                }}
              >
                <Sparkles size={20} />
              </div>
              <h3 style={{ margin: "18px 0 10px", fontSize: "1.45rem", color: "var(--text-primary)" }}>{item.title}</h3>
              <p style={{ margin: 0, color: "var(--text-secondary)", lineHeight: 1.7 }}>{item.text}</p>
            </div>
          ))}
        </div>
      </section>

      <section style={{ maxWidth: "1320px", margin: "0 auto", padding: "64px 24px 24px" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: "20px",
            flexWrap: "wrap",
            background: "linear-gradient(135deg, #f03856, #153f5f)",
            borderRadius: "28px",
            padding: "34px 30px",
            boxShadow: "0 26px 38px rgba(127, 58, 68, 0.18)",
            color: "#fff",
          }}
        >
          <div style={{ maxWidth: "720px" }}>
            <h2 style={{ margin: 0, fontSize: "clamp(2rem, 4vw, 2.8rem)", color: "#fff", letterSpacing: "-0.04em" }}>
              More than a summary. A trustworthy brief.
            </h2>
            <p style={{ margin: "14px 0 0", color: "rgba(225, 209, 149, 0.82)", fontSize: "1.06rem", lineHeight: 1.7 }}>
              BharatBrief combines summarization with source-grounded verification for a more informed India.
            </p>
          </div>

          <Link
            href="/summarize"
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "10px",
              padding: "18px 26px",
              borderRadius: "18px",
              background: "linear-gradient(135deg, #ff5c5c, #e92a4a)",
              color: "#fff",
              textDecoration: "none",
              fontWeight: 800,
              boxShadow: "0 18px 28px rgba(233, 42, 74, 0.28)",
            }}
          >
            Try BharatBrief
            <ArrowRight size={18} />
          </Link>
        </div>
      </section>

      <footer
  style={{
    background: "#0b3b67",
    color: "#ffffff",
    borderTop: "4px solid #f39a23",
    marginTop: "30px",
  }}
>
  <div
    className="footer-grid"
    style={{
      maxWidth: "1450px",
      margin: "0 auto",
      padding: "35px 45px 28px",
      display: "grid",
      gridTemplateColumns: "1fr 1.5fr 1fr 1.3fr",
      gap: "35px",
      alignItems: "center",
    }}
  >

    {/* YOUR NAME */}
    <div>
      <div
        style={{
          fontSize: "30px",
          fontStyle: "italic",
          fontWeight: 400,
          color: "#f39a23",
        }}
      >
        Ayush{" "}
        <span style={{ color: "#159447" }}>
          Singh
        </span>
      </div>
    </div>

    {/* PROJECT */}
    <div style={{ textAlign: "center" }}>
      <div
        style={{
          fontSize: "20px",
          fontWeight: 800,
          marginBottom: "8px",
        }}
      >
        BharatBrief
      </div>

      <div
        style={{
          fontSize: "13px",
          lineHeight: 1.8,
          color: "#e4eef5",
        }}
      >
        AI-powered information summarization and verification.
        <br />
        Inspired by Digital India and a more connected world.
      </div>
    </div>

    {/* DIGITAL INDIA */}
    <div style={{ textAlign: "center" }}>
      <div
        style={{
          fontSize: "25px",
          fontWeight: 800,
          fontStyle: "italic",
        }}
      >
        <span style={{ color: "#f39a23" }}>
          Digital
        </span>{" "}
        <span style={{ color: "#159447" }}>
          India
        </span>
      </div>

      <div
        style={{
          marginTop: "3px",
          fontSize: "11px",
          color: "#ffffff",
        }}
      >
        Power To Empower
      </div>
    </div>

    {/* GOVERNMENT OF INDIA */}
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: "12px",
      }}
    >
      <div
        style={{
          fontSize: "36px",
          color: "#ffffff",
        }}
      >
        ☸
      </div>

      <div>
        <div
          style={{
            fontSize: "20px",
            color: "#f39a23",
            fontWeight: 500,
          }}
        >
          भारत सरकार
        </div>

        <div
          style={{
            fontSize: "17px",
            color: "#ffffff",
          }}
        >
          Government{" "}
          <span style={{ color: "#159447" }}>
            of India
          </span>
        </div>
      </div>
    </div>

  </div>

  {/* BOTTOM BAR */}
  <div
    style={{
      borderTop: "1px solid rgba(255,255,255,0.18)",
      padding: "15px 30px",
      textAlign: "center",
      color: "#d5e2eb",
      fontSize: "12px",
    }}
  >
    © 2026 BharatBrief &nbsp; • &nbsp;
    AI-Powered Information Intelligence
    &nbsp; • &nbsp;
    Made in India
  </div>
</footer>
      <style jsx global>{`
        * { box-sizing: border-box; }
        html, body {
          margin: 0;
          padding: 0;
          width: 100%;
          overflow-x: hidden;
        }

        @media (max-width: 1100px) {
          .hero-grid {
            grid-template-columns: 1fr 0.9fr !important;
          }

          .quick-input-grid {
            grid-template-columns: 1.5fr 1fr 1fr 1fr !important;
          }

          .quick-input-grid > div:first-child {
            grid-column: 1 / -1;
          }

          .highlights-grid,
          .services-grid,
          .trust-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
          }

          .categories-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
          }

          .steps-grid {
            grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
          }

          .footer-grid {
            grid-template-columns: 1fr 1.5fr 1fr !important;
          }

          .footer-grid > div:last-child {
            grid-column: 1 / -1;
          }
        }

        @media (max-width: 800px) {
          .hero-grid {
            grid-template-columns: 1fr !important;
            gap: 36px !important;
          }

          .hero-grid > div:last-child {
            max-width: 520px;
            width: 100%;
            margin: 0 auto;
          }

          .quick-input-grid {
            grid-template-columns: 1fr 1fr !important;
          }

          .quick-input-grid > div:first-child {
            grid-column: 1 / -1;
          }

          .highlights-grid,
          .services-grid,
          .categories-grid,
          .trust-grid {
            grid-template-columns: 1fr 1fr !important;
          }

          .steps-grid {
            grid-template-columns: 1fr !important;
          }

          .footer-grid {
            grid-template-columns: 1fr 1fr !important;
            gap: 24px !important;
          }

          .footer-grid > div:last-child {
            grid-column: 1 / -1;
          }
        }

        @media (max-width: 600px) {
          .hero-grid {
            gap: 28px !important;
            padding-top: 16px !important;
          }

          .hero-grid h1 {
            font-size: clamp(2.7rem, 14vw, 4.2rem) !important;
          }

          .hero-grid p {
            font-size: 1rem !important;
          }

          .hero-grid a {
            width: 100%;
          }

          .quick-input-grid,
          .highlights-grid,
          .services-grid,
          .categories-grid,
          .steps-grid,
          .trust-grid,
          .footer-grid {
            grid-template-columns: 1fr !important;
          }

          .quick-input-grid {
            gap: 10px !important;
          }

          .quick-input-grid > div:first-child {
            grid-column: auto;
          }

          .quick-input-grid button {
            width: 100%;
          }

          .highlights-grid {
            gap: 12px !important;
          }

          .services-grid,
          .categories-grid,
          .steps-grid,
          .trust-grid {
            gap: 14px !important;
          }

          .footer-grid {
            text-align: center !important;
            padding: 28px 18px !important;
            gap: 24px !important;
          }

          .footer-grid > div {
            width: 100%;
            grid-column: auto !important;
          }

          section > div {
            max-width: 100%;
          }
        }

        @media (max-width: 420px) {
          .hero-grid h1 {
            letter-spacing: -0.055em !important;
          }

          .hero-grid p {
            line-height: 1.5 !important;
          }

          .hero-grid > div:last-child {
            max-width: 100%;
          }

          .highlights-grid > div {
            padding: 16px 14px !important;
          }

          .highlights-grid > div > div:last-child > div:first-child {
            font-size: 1.65rem !important;
          }
        }
      `}</style>
    </main>
  );
}
