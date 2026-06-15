"use client";

export const dynamic = "force-dynamic";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { getFertilizerRecommendation } from "@/lib/api";
import { FlaskConical, Loader2 } from "lucide-react";
import { toast } from "sonner";

const schema = z.object({
  crop: z.string().min(1, "Crop name required"),
  nitrogen: z.coerce.number().min(0).max(200),
  phosphorus: z.coerce.number().min(0).max(200),
  potassium: z.coerce.number().min(0).max(200),
  ph: z.coerce.number().min(0).max(14),
  temperature: z.coerce.number().min(-10).max(60),
  humidity: z.coerce.number().min(0).max(100),
  rainfall: z.coerce.number().min(0),
});

type FormData = z.infer<typeof schema>;

interface FertilizerResult {
  fertilizer: string;
  quantity: string;
  reason: string;
}

const fields = [
  { name: "crop" as const, label: "Crop Type", placeholder: "e.g. Wheat, Rice, Tomato", type: "text" },
  { name: "nitrogen" as const, label: "Nitrogen (N) kg/ha", placeholder: "0-200", type: "number" },
  { name: "phosphorus" as const, label: "Phosphorus (P) kg/ha", placeholder: "0-200", type: "number" },
  { name: "potassium" as const, label: "Potassium (K) kg/ha", placeholder: "0-200", type: "number" },
  { name: "ph" as const, label: "Soil pH", placeholder: "0-14", type: "number" },
  { name: "temperature" as const, label: "Temperature (°C)", placeholder: "e.g. 25", type: "number" },
  { name: "humidity" as const, label: "Humidity (%)", placeholder: "0-100", type: "number" },
  { name: "rainfall" as const, label: "Rainfall (mm)", placeholder: "e.g. 120", type: "number" },
];

export default function FertilizerPage() {
  const [result, setResult] = useState<FertilizerResult | null>(null);
  const [loading, setLoading] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    setLoading(true);
    try {
      const res = await getFertilizerRecommendation(data);
      setResult(res);
    } catch {
      toast.error("Failed to get recommendation. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <FlaskConical className="text-blue-500" /> Fertilizer Recommendation
        </h1>
        <p className="text-muted-foreground mt-1">Enter your soil and crop details to get NPK fertilizer advice.</p>
      </div>

      <Card>
        <CardContent className="pt-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {fields.map((f) => (
                <div key={f.name} className="space-y-1">
                  <label className="text-sm font-medium">{f.label}</label>
                  <Input
                    {...register(f.name)}
                    type={f.type}
                    placeholder={f.placeholder}
                    step={f.name === "ph" ? "0.1" : "1"}
                    className={errors[f.name] ? "border-destructive" : ""}
                  />
                  {errors[f.name] && (
                    <p className="text-xs text-destructive">{errors[f.name]?.message}</p>
                  )}
                </div>
              ))}
            </div>
            <Button type="submit" disabled={loading} className="w-full" size="lg">
              {loading ? <><Loader2 className="animate-spin h-4 w-4 mr-2" /> Analyzing...</> : "Get Recommendation"}
            </Button>
          </form>
        </CardContent>
      </Card>

      {result && (
        <Card className="border-primary">
          <CardHeader>
            <CardTitle className="text-primary">{result.fertilizer}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div>
              <p className="text-sm font-semibold">Recommended Quantity</p>
              <p className="text-2xl font-bold text-primary">{result.quantity}</p>
            </div>
            {result.reason && (
              <div>
                <p className="text-sm font-semibold">Why this fertilizer?</p>
                <p className="text-sm text-muted-foreground">{result.reason}</p>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
