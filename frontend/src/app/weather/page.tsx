"use client";

export const dynamic = "force-dynamic";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getWeatherAdvice } from "@/lib/api";
import { CloudSun, Loader2, MapPin } from "lucide-react";
import { toast } from "sonner";

interface WeatherData {
  location: { lat: number; lon: number };
  current: {
    temperature: number;
    humidity: number;
    rainfall: number;
    wind_speed: number;
  };
  advice: string[];
  forecast: Array<{ date: string; max_temp: number; min_temp: number; rainfall: number }>;
}

export default function WeatherPage() {
  const [data, setData] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchAdvice = () => {
    if (!navigator.geolocation) {
      toast.error("Geolocation not supported");
      return;
    }
    setLoading(true);
    navigator.geolocation.getCurrentPosition(
      async ({ coords }) => {
        try {
          const res = await getWeatherAdvice(coords.latitude, coords.longitude);
          setData(res);
        } catch {
          toast.error("Failed to fetch weather data");
        } finally {
          setLoading(false);
        }
      },
      () => {
        toast.error("Location access denied");
        setLoading(false);
      }
    );
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <CloudSun className="text-yellow-500" /> Weather-based Farming Advice
        </h1>
        <p className="text-muted-foreground mt-1">Get real-time farming advice based on your local weather.</p>
      </div>

      <Button onClick={fetchAdvice} disabled={loading} size="lg" className="w-full md:w-auto">
        {loading
          ? <><Loader2 className="animate-spin h-4 w-4 mr-2" />Fetching...</>
          : <><MapPin className="h-4 w-4 mr-2" />Use My Location</>
        }
      </Button>

      {data && (
        <div className="space-y-4">
          {/* Current */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {[
              { label: "Temperature", value: `${data.current.temperature}°C` },
              { label: "Humidity", value: `${data.current.humidity}%` },
              { label: "Rainfall", value: `${data.current.rainfall} mm` },
              { label: "Wind Speed", value: `${data.current.wind_speed} km/h` },
            ].map((m) => (
              <Card key={m.label}>
                <CardContent className="pt-4 pb-4 text-center">
                  <p className="text-2xl font-bold text-primary">{m.value}</p>
                  <p className="text-xs text-muted-foreground">{m.label}</p>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Advice */}
          <Card>
            <CardHeader><CardTitle>Farming Advice</CardTitle></CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {data.advice.map((a, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <span className="text-primary mt-0.5">•</span>
                    <span>{a}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Forecast */}
          <Card>
            <CardHeader><CardTitle>7-Day Forecast</CardTitle></CardHeader>
            <CardContent>
              <div className="space-y-2">
                {data.forecast.map((day) => (
                  <div key={day.date} className="flex justify-between items-center py-2 border-b last:border-0 text-sm">
                    <span className="font-medium">{day.date}</span>
                    <span>{day.min_temp}° – {day.max_temp}°C</span>
                    <span className="text-blue-500">{day.rainfall} mm</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
