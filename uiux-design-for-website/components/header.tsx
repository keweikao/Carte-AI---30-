import { Button } from "@/components/ui/button"
import { Settings } from "lucide-react"

interface HeaderProps {
  title: string
}

export default function Header({ title }: HeaderProps) {
  return (
    <header className="border-b border-border bg-card sticky top-0 z-40">
      <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white text-sm font-bold">
            C
          </div>
          <h1 className="text-lg font-bold text-foreground">Carte</h1>
        </div>
        <span className="text-sm text-muted-foreground">{title}</span>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground hover:bg-secondary">
            <Settings className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </header>
  )
}
