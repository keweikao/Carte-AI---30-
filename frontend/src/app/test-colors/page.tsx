"use client";

export default function TestColorsPage() {
    return (
        <div className="min-h-screen bg-background p-8 space-y-8">
            <h1 className="text-4xl font-bold text-foreground">Color System Test</h1>

            <div className="grid grid-cols-2 gap-4">
                {/* Primary */}
                <div className="space-y-2">
                    <div className="w-full h-32 bg-primary rounded-lg"></div>
                    <p className="text-sm font-mono">bg-primary</p>
                    <p className="text-xs text-muted-foreground">Should be Orange #F97316</p>
                </div>

                {/* Primary Text */}
                <div className="space-y-2">
                    <div className="w-full h-32 bg-background border-2 border-border rounded-lg flex items-center justify-center">
                        <p className="text-4xl font-bold text-primary">TEXT</p>
                    </div>
                    <p className="text-sm font-mono">text-primary</p>
                    <p className="text-xs text-muted-foreground">Should be Orange</p>
                </div>

                {/* Accent */}
                <div className="space-y-2">
                    <div className="w-full h-32 bg-accent rounded-lg"></div>
                    <p className="text-sm font-mono">bg-accent</p>
                    <p className="text-xs text-muted-foreground">Should be Orange (same as primary)</p>
                </div>

                {/* Success */}
                <div className="space-y-2">
                    <div className="w-full h-32 bg-success rounded-lg"></div>
                    <p className="text-sm font-mono">bg-success</p>
                    <p className="text-xs text-muted-foreground">Should be Green</p>
                </div>

                {/* Secondary */}
                <div className="space-y-2">
                    <div className="w-full h-32 bg-secondary rounded-lg border border-border"></div>
                    <p className="text-sm font-mono">bg-secondary</p>
                    <p className="text-xs text-muted-foreground">Should be Light Gray</p>
                </div>

                {/* Muted */}
                <div className="space-y-2">
                    <div className="w-full h-32 bg-muted rounded-lg"></div>
                    <p className="text-sm font-mono">bg-muted</p>
                    <p className="text-xs text-muted-foreground">Should be Light Gray</p>
                </div>
            </div>

            <div className="mt-8 p-6 bg-card rounded-lg border border-border">
                <h2 className="text-2xl font-bold text-foreground mb-4">Button Tests</h2>
                <div className="flex gap-4 flex-wrap">
                    <button className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90">
                        Primary Button
                    </button>
                    <button className="px-6 py-3 bg-secondary text-secondary-foreground rounded-lg hover:bg-secondary/80">
                        Secondary Button
                    </button>
                    <button className="px-6 py-3 bg-destructive text-destructive-foreground rounded-lg hover:bg-destructive/90">
                        Destructive Button
                    </button>
                </div>
            </div>

            <div className="p-6 bg-card rounded-lg border border-border">
                <h2 className="text-2xl font-bold text-foreground mb-4">CSS Variables</h2>
                <pre className="text-xs font-mono bg-muted p-4 rounded overflow-auto">
{`--primary: 24 95% 53% (Orange #F97316)
--accent: 24 95% 53% (Orange #F97316)
--success: 158 64% 52% (Green #10B981)
--background: 0 0% 98% (Very Light Gray #FAFAFA)
--foreground: 215 28% 17% (Deep Charcoal #1F2937)`}
                </pre>
            </div>
        </div>
    );
}
