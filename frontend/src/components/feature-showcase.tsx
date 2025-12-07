import { Target, DollarSign, Shield } from "lucide-react";
import { motion } from "framer-motion";

export function FeatureShowcase() {
  const features = [
    {
      icon: Target,
      title: "精準避雷",
      description: "分析數千則真實評論，幫你過濾掉過譽的網紅店與地雷菜色。"
    },
    {
      icon: DollarSign,
      title: "預算控制",
      description: "無論是月底吃土還是慶祝大餐，精準控制每人預算，不超支。"
    },
    {
      icon: Shield,
      title: "飲食客製",
      description: "不吃牛？香菜過敏？長輩要軟爛？AI 幫你把關所有細節。"
    }
  ];

  return (
    <div className="space-y-4">
      {features.map((feature, index) => {
        const Icon = feature.icon;
        return (
          <motion.div 
            key={index} 
            className="flex gap-4 items-start"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary flex-shrink-0">
              <Icon className="w-5 h-5" />
            </div>
            <div className="space-y-1">
              <h3 className="font-semibold text-foreground">{feature.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {feature.description}
              </p>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
