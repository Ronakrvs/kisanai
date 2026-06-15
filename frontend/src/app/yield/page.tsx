"use client";

export const dynamic = "force-dynamic";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { getYieldPrediction } from "@/lib/api";
import { TrendingUp, Loader2 } from "lucide-react";
import { toast } from "sonner";

const INDIAN_STATES = [
  "Andhra Pradesh","Assam","Bihar","Chhattisgarh","Gujarat","Haryana",
  "Himachal Pradesh","Jharkhand","Karnataka","Kerala","Madhya Pradesh",
  "Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha",
  "Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura",
  "Uttar Pradesh","Uttarakhand","West Bengal",
];

const schema = z.object({
  state: z.string().min(1),
  district: z.string().min(1),
  crop: z.string().min(1),
  rainfall: z.coerce.number().min(0),
  temperature: z.coerce.number().min(-10).max(60),
  area: z.coerce.number().min(0.01),
  fertilizer_usage: z.coerce.number().min(0),
});

type FormData = z.infer<typeof schema>;

export default function YieldPage() {
  const [result, setResult] = useState<{ predicted_yield: string } | null>(null);
  const [loading, setLoading] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    setLoading(true);
    try {
      const res = await getYieldPrediction(data);
      setResult(res);
    } catch {
      toast.error("Prediction failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <TrendingUp className="text-purple-500" /> Crop Yield Prediction
        </h1>
        <p className="text-muted-foreground mt-1">Predict expected yield for your farm using AI.</p>
      </div>

      <Card>
        <CardContent className="pt-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-sm font-medium">State</label>
                <select
                  {...register("state")}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                >
                  <option value="">Select State</option>
                  {INDIAN_STATES.map((s) => <option key={s} value={s}>{s}</option>)}
                </select>
                {errors.state && <p className="text-xs text-destructive">Required</p>}
              </div>

              {[
                { name: "district" as const, label: "District", placeholder: "e.g. Pune", type: "text" },
                { name: "crop" as const, label: "Crop", placeholder: "e.g. Rice", type: "text" },
                { name: "rainfall" as const, label: "Annual Rainfall (mm)", placeholder: "e.g. 800", type: "number" },
                { name: "temperature" as const, label: "Avg Temperature (°C)", placeholder: "e.g. 28", type: "number" },
                { name: "area" as const, label: "Farm Area (hectares)", placeholder: "e.g. 2.5", type: "number" },
                { name: "fertilizer_usage" as const, label: "Fertilizer Used (kg/ha)", placeholder: "e.g. 120", type: "number" },
              ].map((f) => (
                <div key={f.name} className="space-y-1">
                  <label className="text-sm font-medium">{f.label}</label>
                  <Input {...register(f.name)} type={f.type} placeholder={f.placeholder} step="any" />
                  {errors[f.name] && <p className="text-xs text-destructive">{errors[f.name]?.message}</p>}
                </div>
              ))}
            </div>

            <Button type="submit" disabled={loading} className="w-full" size="lg">
              {loading ? <><Loader2 className="animate-spin h-4 w-4 mr-2" />Predicting...</> : "Predict Yield"}
            </Button>
          </form>
        </CardContent>
      </Card>

      {result && (
        <Card className="border-purple-300">
          <CardHeader>
            <CardTitle>Predicted Yield</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-4xl font-bold text-purple-600">{result.predicted_yield}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
