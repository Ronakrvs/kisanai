"use client";

export const dynamic = "force-dynamic";

import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { detectDisease } from "@/lib/api";
import { Upload, Loader2, Bug, AlertCircle } from "lucide-react";
import { toast } from "sonner";
import Image from "next/image";

interface DiseaseResult {
  crop: string;
  disease: string;
  confidence: number;
  cause: string;
  treatment: string;
  prevention: string;
}

export default function DiseaseDetectionPage() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<DiseaseResult | null>(null);
  const [loading, setLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = (f: File) => {
    if (!f.type.startsWith("image/")) {
      toast.error("Please upload an image file");
      return;
    }
    if (f.size > 10 * 1024 * 1024) {
      toast.error("Image must be under 10MB");
      return;
    }
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setResult(null);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  };

  const analyze = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const data = await detectDisease(file);
      setResult(data);
    } catch {
      toast.error("Analysis failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const confidenceColor = (c: number) =>
    c >= 80 ? "bg-green-100 text-green-800" : c >= 60 ? "bg-yellow-100 text-yellow-800" : "bg-red-100 text-red-800";

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <Bug className="text-red-500" /> Crop Disease Detection
        </h1>
        <p className="text-muted-foreground mt-1">Upload a photo of your crop leaf to detect diseases instantly.</p>
      </div>

      {/* Upload Area */}
      <Card
        className="border-2 border-dashed cursor-pointer hover:border-primary transition-colors"
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        onClick={() => inputRef.current?.click()}
      >
        <CardContent className="flex flex-col items-center justify-center py-12 gap-3">
          <input
            ref={inputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
          />
          {preview ? (
            <div className="relative w-64 h-48">
              <Image src={preview} alt="Crop preview" fill className="object-contain rounded" />
            </div>
          ) : (
            <>
              <Upload className="h-12 w-12 text-muted-foreground" />
              <p className="text-muted-foreground text-center">
                Drag & drop or click to upload<br />
                <span className="text-sm">JPG, PNG, WebP — max 10MB</span>
              </p>
            </>
          )}
        </CardContent>
      </Card>

      {file && (
        <Button onClick={analyze} disabled={loading} className="w-full" size="lg">
          {loading ? <><Loader2 className="animate-spin h-4 w-4 mr-2" /> Analyzing...</> : "Analyze Disease"}
        </Button>
      )}

      {/* Results */}
      {result && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span className="capitalize">{result.disease}</span>
              <Badge className={confidenceColor(result.confidence)}>
                {result.confidence}% confidence
              </Badge>
            </CardTitle>
            <p className="text-sm text-muted-foreground capitalize">Crop: {result.crop}</p>
          </CardHeader>
          <CardContent className="space-y-4">
            {[
              { label: "Cause", value: result.cause, icon: AlertCircle },
              { label: "Treatment", value: result.treatment, icon: null },
              { label: "Prevention", value: result.prevention, icon: null },
            ].map(({ label, value }) => (
              <div key={label}>
                <p className="font-semibold text-sm">{label}</p>
                <p className="text-muted-foreground text-sm mt-1">{value}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
