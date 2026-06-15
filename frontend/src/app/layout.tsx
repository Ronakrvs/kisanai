import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/layout/Navbar";
import { Toaster } from "sonner";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "KisanAI - AI Farming Assistant",
  description: "Multilingual AI assistant for Indian farmers — disease detection, fertilizer advice, yield prediction, and more.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Navbar />
        <main className="container mx-auto px-4 py-6">{children}</main>
        <Toaster richColors position="top-right" />
      </body>
    </html>
  );
}
