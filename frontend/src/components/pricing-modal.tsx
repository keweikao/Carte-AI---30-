"use client";

import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Check, Zap, Crown, Calendar } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

interface PricingModalProps {
    isOpen: boolean;
    onClose: () => void;
    currentCredits: number;
}

export function PricingModal({ isOpen, onClose, currentCredits }: PricingModalProps) {
    const [selectedPlan, setSelectedPlan] = useState<'single' | 'monthly' | 'yearly'>('monthly');

    const plans = [
        {
            id: 'single',
            title: '單次使用',
            price: 'NT$ 30',
            period: '/ 次',
            description: '臨時需要？隨買隨用',
            features: ['獲得 1 次完整推薦', '無使用期限', '包含視覺菜單解析'],
            icon: Zap,
            highlight: false
        },
        {
            id: 'monthly',
            title: '月費訂閱',
            price: 'NT$ 90',
            period: '/ 月',
            description: '最受歡迎！適合愛嚐鮮的你',
            features: ['無限次使用推薦', '優先使用新功能', '隨時可取消'],
            icon: Calendar,
            highlight: true
        },
        {
            id: 'yearly',
            title: '年費訂閱',
            price: 'NT$ 890',
            period: '/ 年',
            description: '超值優惠！約 2 個月免費',
            features: ['包含所有月費功能', '專屬 VIP 客服', '支持我們持續開發'],
            icon: Crown,
            highlight: false
        }
    ];

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[900px] bg-background">
                <DialogHeader className="text-center pb-6">
                    <DialogTitle className="text-3xl font-bold font-display mb-2">
                        升級您的用餐體驗
                    </DialogTitle>
                    <DialogDescription className="text-lg">
                        您的免費額度已用完（剩餘 {currentCredits} 次）。<br />
                        選擇適合您的方案，繼續探索美食！
                    </DialogDescription>
                </DialogHeader>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    {plans.map((plan) => (
                        <Card
                            key={plan.id}
                            className={`relative p-6 cursor-pointer transition-all hover:shadow-lg border-2 ${selectedPlan === plan.id
                                ? 'border-primary bg-primary/5 shadow-md'
                                : 'border-border hover:border-primary/50'
                                }`}
                            onClick={() => setSelectedPlan(plan.id as 'single' | 'monthly' | 'yearly')}
                        >
                            {plan.highlight && (
                                <Badge className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-3 py-1">
                                    最熱門
                                </Badge>
                            )}

                            <div className="flex justify-between items-start mb-4">
                                <div className={`p-3 rounded-full ${selectedPlan === plan.id ? 'bg-primary/20 text-primary' : 'bg-secondary text-muted-foreground'}`}>
                                    <plan.icon className="w-6 h-6" />
                                </div>
                                {selectedPlan === plan.id && <Check className="w-6 h-6 text-primary" />}
                            </div>

                            <h3 className="text-xl font-bold mb-1">{plan.title}</h3>
                            <p className="text-sm text-muted-foreground mb-4">{plan.description}</p>

                            <div className="flex items-baseline mb-6">
                                <span className="text-3xl font-bold font-mono">{plan.price}</span>
                                <span className="text-muted-foreground ml-1">{plan.period}</span>
                            </div>

                            <ul className="space-y-3 mb-6">
                                {plan.features.map((feature, idx) => (
                                    <li key={idx} className="flex items-center text-sm">
                                        <Check className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" />
                                        {feature}
                                    </li>
                                ))}
                            </ul>
                        </Card>
                    ))}
                </div>

                <DialogFooter className="flex-col sm:flex-row gap-3 sm:justify-center">
                    <Button variant="outline" onClick={onClose} className="w-full sm:w-auto">
                        稍後再說
                    </Button>
                    <Button className="w-full sm:w-auto min-w-[200px] bg-primary text-primary-foreground hover:bg-primary/90">
                        前往付款 ({plans.find(p => p.id === selectedPlan)?.price})
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
