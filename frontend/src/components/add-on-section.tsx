"use client";

import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Sparkles, Plus, Coffee, Cake, Salad, Soup } from "lucide-react";

interface AddOnSectionProps {
    onAddOn: (category: string) => Promise<void>;
    isLoading?: boolean;
}

const QUICK_CATEGORIES = [
    { id: "飲料", label: "飲料", icon: Coffee },
    { id: "甜點", label: "甜點", icon: Cake },
    { id: "配菜", label: "配菜", icon: Salad },
    { id: "湯品", label: "湯品", icon: Soup },
];

export function AddOnSection({ onAddOn, isLoading = false }: AddOnSectionProps) {
    const [customCategory, setCustomCategory] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleQuickAdd = async (category: string) => {
        setIsSubmitting(true);
        try {
            await onAddOn(category);
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleCustomAdd = async () => {
        if (!customCategory.trim()) return;

        setIsSubmitting(true);
        try {
            await onAddOn(customCategory.trim());
            setCustomCategory("");
        } finally {
            setIsSubmitting(false);
        }
    };

    const disabled = isLoading || isSubmitting;

    return (
        <Card className="mb-6 bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20">
            <div className="p-4">
                <div className="flex items-center gap-2 mb-3">
                    <Sparkles className="w-5 h-5 text-primary" />
                    <h3 className="font-semibold text-foreground">我想加點</h3>
                </div>

                {/* 快選按鈕 */}
                <div className="flex flex-wrap gap-2 mb-3">
                    {QUICK_CATEGORIES.map(({ id, label, icon: Icon }) => (
                        <Button
                            key={id}
                            variant="outline"
                            size="sm"
                            onClick={() => handleQuickAdd(id)}
                            disabled={disabled}
                            className="gap-1"
                        >
                            <Icon className="w-4 h-4" />
                            {label}
                        </Button>
                    ))}
                </div>

                {/* 自訂輸入 */}
                <div className="flex gap-2">
                    <Input
                        placeholder="或輸入想要的類別（如：開胃菜、小菜）..."
                        value={customCategory}
                        onChange={(e) => setCustomCategory(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !disabled) {
                                handleCustomAdd();
                            }
                        }}
                        disabled={disabled}
                        className="flex-1"
                    />
                    <Button
                        onClick={handleCustomAdd}
                        disabled={disabled || !customCategory.trim()}
                        size="icon"
                    >
                        <Plus className="w-4 h-4" />
                    </Button>
                </div>
            </div>
        </Card>
    );
}
