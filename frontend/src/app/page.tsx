import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Bug, FlaskConical, TrendingUp, CloudSun, MessageCircle, Leaf } from "lucide-react";

const features = [
  {
    icon: Bug,
    title: "Crop Disease Detection",
    description: "Upload a photo of your crop and get instant AI-powered disease diagnosis with treatment advice.",
    href: "/disease-detection",
    color: "text-red-500",
  },
  {
    icon: FlaskConical,
    title: "Fertilizer Recommendation",
    description: "Get personalized NPK fertilizer recommendations based on your soil conditions and crop type.",
    href: "/fertilizer",
    color: "text-blue-500",
  },
  {
    icon: TrendingUp,
    title: "Yield Prediction",
    description: "Predict crop yield using historical data, weather patterns, and soil metrics.",
    href: "/yield",
    color: "text-purple-500",
  },
  {
    icon: CloudSun,
    title: "Weather Advice",
    description: "Receive smart farming advice based on real-time and 7-day weather forecasts.",
    href: "/weather",
    color: "text-yellow-500",
  },
  {
    icon: MessageCircle,
    title: "AI Farmer Chatbot",
    description: "Ask questions in Hindi or English. Get expert advice on farming 24/7.",
    href: "/chat",
    color: "text-green-500",
  },
];

export default function HomePage() {
  return (
    <div className="space-y-12">
      {/* Hero */}
      <section className="text-center py-16 space-y-6">
        <div className="flex justify-center">
          <div className="rounded-full bg-primary/10 p-4">
            <Leaf className="h-12 w-12 text-primary" />
          </div>
        </div>
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
          KisanAI
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          AI-powered farming assistant for Indian farmers. Detect diseases, get fertilizer advice,
          predict yield, and chat in Hindi or English — all free.
        </p>
        <div className="flex flex-wrap gap-3 justify-center">
          <Link href="/disease-detection">
            <Button size="lg">Detect Disease</Button>
          </Link>
          <Link href="/chat">
            <Button size="lg" variant="outline">Chat with AI (हिंदी)</Button>
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold text-center">What can KisanAI do?</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <Link key={feature.href} href={feature.href}>
                <Card className="h-full hover:shadow-md transition-shadow cursor-pointer">
                  <CardHeader>
                    <Icon className={`h-8 w-8 ${feature.color}`} />
                    <CardTitle className="text-lg">{feature.title}</CardTitle>
                    <CardDescription>{feature.description}</CardDescription>
                  </CardHeader>
                </Card>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4 py-8">
        {[
          { label: "Crops Supported", value: "50+" },
          { label: "Diseases Detected", value: "38+" },
          { label: "Languages", value: "2" },
          { label: "Cost to Farmers", value: "₹0" },
        ].map((stat) => (
          <div key={stat.label} className="text-center p-4 rounded-lg border">
            <p className="text-3xl font-bold text-primary">{stat.value}</p>
            <p className="text-sm text-muted-foreground mt-1">{stat.label}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
