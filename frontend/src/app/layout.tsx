import type { Metadata } from "next";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "Briefly — Read less. Know more.",
    description:
        "AI-powered news article summarization. Transform long-form articles into concise, accurate summaries using our fine-tuned T5 model trained on CNN/DailyMail.",
          keywords: [
              "AI summarizer",
                  "news summarizer",
                      "article summary",
                          "text summarization",
                              "NLP",
                                  "T5 model",
                                    ],
                                      openGraph: {
                                          title: "Briefly — Read less. Know more.",
                                              description:
                                                    "AI-powered news article summarization platform.",
                                                        type: "website",
                                                          },
                                                          };

                                                          export default function RootLayout({
                                                            children,
                                                            }: Readonly<{
                                                              children: React.ReactNode;
                                                              }>) {
                                                                return (
                                                                    <html lang="en" suppressHydrationWarning>
                                                                          <head>
                                                                                  <link
                                                                                            href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap"
                                                                                                      rel="stylesheet"
                                                                                                              />
                                                                                                                      <link
                                                                                                                                href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&f[]=general-sans@400,500,600,700&display=swap"
                                                                                                                                          rel="stylesheet"
                                                                                                                                                  />
                                                                                                                                                        </head>
                                                                                                                                                              <body>
                                                                                                                                                                      <Providers>
                                                                                                                                                                                <Navbar />
                                                                                                                                                                                          <main style={{ minHeight: "100vh", paddingTop: "64px" }}>
                                                                                                                                                                                                      {children}
                                                                                                                                                                                                                </main>
                                                                                                                                                                                                                        </Providers>
                                                                                                                                                                                                                              </body>
                                                                                                                                                                                                                                  </html>
                                                                                                                                                                                                                                    );
                                                                                                                                                                                                                                    }