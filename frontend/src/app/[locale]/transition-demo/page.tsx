"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  SlideInUp,
  FadeIn,
  ScaleIn,
  StaggerContainer,
  StaggerItem,
} from "@/components/page-transition";
import {
  ArrowLeft,
  Sparkles,
  Zap,
  Heart,
  Star,
  Coffee,
  Utensils,
} from "lucide-react";

/**
 * Transition Demo Page
 *
 * This page demonstrates all available transition animations
 * and serves as a testing ground for the animation system.
 */

export default function TransitionDemoPage() {
  const [showMore, setShowMore] = useState(false);

  const demoCards = [
    { id: 1, title: "Slide In Up", icon: Sparkles, color: "text-primary" },
    { id: 2, title: "Fade In", icon: Zap, color: "text-accent" },
    { id: 3, title: "Scale In", icon: Heart, color: "text-destructive" },
    { id: 4, title: "Stagger", icon: Star, color: "text-warning" },
  ];

  const staggerItems = [
    { id: 1, icon: Coffee, label: "First Item" },
    { id: 2, icon: Utensils, label: "Second Item" },
    { id: 3, icon: Heart, label: "Third Item" },
    { id: 4, icon: Star, label: "Fourth Item" },
  ];

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <FadeIn>
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-4xl font-bold text-foreground mb-2">
                Page Transition Demo
              </h1>
              <p className="text-muted-foreground">
                Testing ground for all animation components
              </p>
            </div>
            <Link href="/">
              <Button variant="outline">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back Home
              </Button>
            </Link>
          </div>
        </FadeIn>

        {/* Navigation Demo */}
        <SlideInUp delay={0.1}>
          <Card className="p-6 bg-gradient-to-br from-primary/5 to-accent/5">
            <h2 className="text-2xl font-bold mb-4">Page Navigation</h2>
            <p className="text-muted-foreground mb-4">
              Test page transitions by navigating between routes. Notice the
              direction-aware animations.
            </p>
            <div className="flex gap-2 flex-wrap">
              <Link href="/">
                <Button variant="outline">Home</Button>
              </Link>
              <Link href="/input">
                <Button variant="outline">Input</Button>
              </Link>
              <Link href="/recommendation">
                <Button variant="outline">Recommendation</Button>
              </Link>
              <Link href="/menu">
                <Button variant="outline">Menu</Button>
              </Link>
            </div>
          </Card>
        </SlideInUp>

        {/* Animation Components Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {demoCards.map((card, index) => (
            <SlideInUp key={card.id} delay={0.2 + index * 0.1}>
              <Card className="p-6 hover:shadow-lg transition-shadow">
                <div className="flex items-center gap-3 mb-2">
                  <card.icon className={`w-6 h-6 ${card.color}`} />
                  <h3 className="text-xl font-bold">{card.title}</h3>
                </div>
                <p className="text-sm text-muted-foreground">
                  Animation component demo #{card.id}
                </p>
              </Card>
            </SlideInUp>
          ))}
        </div>

        {/* FadeIn Demo */}
        <FadeIn delay={0.5} duration={0.5}>
          <Card className="p-6 border-accent">
            <Badge className="mb-3">FadeIn Component</Badge>
            <h3 className="text-xl font-bold mb-2">Smooth Fade Animation</h3>
            <p className="text-muted-foreground">
              This card uses a custom fade duration of 500ms with a delay of
              500ms.
            </p>
          </Card>
        </FadeIn>

        {/* ScaleIn Demo */}
        <ScaleIn delay={0.6}>
          <Card className="p-6 border-secondary">
            <Badge className="mb-3" variant="neutral">
              ScaleIn Component
            </Badge>
            <h3 className="text-xl font-bold mb-2">Scale Animation</h3>
            <p className="text-muted-foreground">
              This card scales up from 95% to 100% for emphasis.
            </p>
          </Card>
        </ScaleIn>

        {/* Stagger Demo */}
        <Card className="p-6">
          <h3 className="text-xl font-bold mb-4">Stagger Animation</h3>
          <p className="text-muted-foreground mb-4">
            Items animate sequentially with a stagger delay
          </p>
          <StaggerContainer staggerDelay={0.15}>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {staggerItems.map((item) => (
                <StaggerItem key={item.id}>
                  <Card className="p-4 text-center hover:bg-accent/5 transition-colors">
                    <item.icon className="w-8 h-8 mx-auto mb-2 text-primary" />
                    <p className="text-sm font-medium">{item.label}</p>
                  </Card>
                </StaggerItem>
              ))}
            </div>
          </StaggerContainer>
        </Card>

        {/* Conditional Rendering Demo */}
        <Card className="p-6">
          <h3 className="text-xl font-bold mb-4">
            Conditional Rendering Animation
          </h3>
          <p className="text-muted-foreground mb-4">
            Toggle to see enter/exit animations
          </p>
          <Button onClick={() => setShowMore(!showMore)} className="mb-4">
            {showMore ? "Hide" : "Show"} Extra Content
          </Button>

          {showMore && (
            <SlideInUp>
              <Card className="p-4 bg-primary/5 border-primary">
                <p className="text-sm">
                  This content slides up when shown and fades out when hidden.
                  Perfect for progressive disclosure patterns.
                </p>
              </Card>
            </SlideInUp>
          )}
        </Card>

        {/* Accessibility Notice */}
        <FadeIn delay={0.8}>
          <Card className="p-6 bg-success/5 border-success">
            <h3 className="text-xl font-bold mb-2 flex items-center gap-2">
              <Sparkles className="w-5 h-5" />
              Accessibility First
            </h3>
            <p className="text-muted-foreground">
              All animations respect the{" "}
              <code className="px-2 py-1 bg-muted rounded">
                prefers-reduced-motion
              </code>{" "}
              setting. Enable reduced motion in your system settings to see
              simplified animations.
            </p>
          </Card>
        </FadeIn>

        {/* Technical Info */}
        <Card className="p-6 bg-muted/30">
          <h3 className="text-xl font-bold mb-4">Technical Details</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Animation Library:</span>
              <span className="font-mono font-medium">Framer Motion</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Base Duration:</span>
              <span className="font-mono font-medium">300ms</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Easing:</span>
              <span className="font-mono font-medium text-xs">
                cubic-bezier(0.4, 0, 0.2, 1)
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">GPU Accelerated:</span>
              <span className="font-medium">✓ Yes</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">
                Reduced Motion Support:
              </span>
              <span className="font-medium">✓ Yes</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
