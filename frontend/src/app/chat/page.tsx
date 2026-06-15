"use client";

export const dynamic = "force-dynamic";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { sendChatMessage } from "@/lib/api";
import { Send, Loader2, Bot, User } from "lucide-react";
import { cn } from "@/lib/utils";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

const SUGGESTIONS = [
  "मेरी फसल की पत्तियां पीली हो रही हैं",
  "What fertilizer is best for wheat?",
  "कब सिंचाई करनी चाहिए?",
  "How to prevent tomato blight?",
];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "नमस्ते! मैं KisanAI हूं। आप मुझसे हिंदी या English में कृषि से जुड़े कोई भी सवाल पूछ सकते हैं। Hello! I'm KisanAI. Ask me anything about farming in Hindi or English.",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [lang, setLang] = useState<"hi" | "en">("hi");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async (text?: string) => {
    const msg = text || input.trim();
    if (!msg || loading) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: msg, timestamp: new Date() }]);
    setLoading(true);

    try {
      const res = await sendChatMessage(msg, lang);
      setMessages((prev) => [...prev, { role: "assistant", content: res.answer, timestamp: new Date() }]);
    } catch {
      setMessages((prev) => [...prev, {
        role: "assistant",
        content: "Sorry, I couldn't process your request. Please try again. / माफ करें, कृपया दोबारा कोशिश करें।",
        timestamp: new Date(),
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto flex flex-col h-[calc(100vh-8rem)]">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <Bot className="text-green-500" /> KisanAI Chatbot
          </h1>
          <p className="text-sm text-muted-foreground">Ask in Hindi or English</p>
        </div>
        <div className="flex rounded-lg border overflow-hidden">
          {(["hi", "en"] as const).map((l) => (
            <button
              key={l}
              onClick={() => setLang(l)}
              className={cn(
                "px-3 py-1 text-sm font-medium transition-colors",
                lang === l ? "bg-primary text-primary-foreground" : "hover:bg-muted"
              )}
            >
              {l === "hi" ? "हिंदी" : "English"}
            </button>
          ))}
        </div>
      </div>

      {/* Messages */}
      <Card className="flex-1 overflow-hidden">
        <CardContent className="h-full overflow-y-auto p-4 space-y-4">
          {messages.map((m, i) => (
            <div key={i} className={cn("flex gap-3", m.role === "user" ? "flex-row-reverse" : "flex-row")}>
              <div className={cn("rounded-full p-1.5 h-8 w-8 flex items-center justify-center flex-shrink-0",
                m.role === "assistant" ? "bg-primary text-primary-foreground" : "bg-secondary"
              )}>
                {m.role === "assistant" ? <Bot className="h-4 w-4" /> : <User className="h-4 w-4" />}
              </div>
              <div className={cn("rounded-lg px-4 py-2 max-w-[80%] text-sm",
                m.role === "assistant" ? "bg-muted" : "bg-primary text-primary-foreground"
              )}>
                {m.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex gap-3">
              <div className="rounded-full p-1.5 h-8 w-8 flex items-center justify-center bg-primary text-primary-foreground">
                <Bot className="h-4 w-4" />
              </div>
              <div className="bg-muted rounded-lg px-4 py-3">
                <Loader2 className="h-4 w-4 animate-spin" />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </CardContent>
      </Card>

      {/* Suggestions */}
      <div className="flex gap-2 mt-3 overflow-x-auto pb-1">
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            onClick={() => send(s)}
            className="whitespace-nowrap text-xs px-3 py-1.5 rounded-full border hover:bg-muted transition-colors flex-shrink-0"
          >
            {s}
          </button>
        ))}
      </div>

      {/* Input */}
      <div className="flex gap-2 mt-2">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && send()}
          placeholder={lang === "hi" ? "अपना सवाल यहां लिखें..." : "Type your question..."}
          disabled={loading}
          className="flex-1"
        />
        <Button onClick={() => send()} disabled={loading || !input.trim()} size="icon">
          <Send className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
