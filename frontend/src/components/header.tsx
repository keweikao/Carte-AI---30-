import { useState } from "react";
import { useSession, signIn, signOut } from "next-auth/react";
import { LogOut, Sparkles } from "lucide-react";
import Link from "next/link";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { PricingModal } from "@/components/pricing-modal";

export function Header() {
  const { data: session, status } = useSession();
  const [showPricingModal, setShowPricingModal] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between px-4">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
          <Image
            src="/icon_banner.png"
            alt="Carte AI 點餐助手"
            width={180}
            height={40}
            className="h-10 w-auto object-contain"
            priority
          />
        </Link>

        {/* Auth Section */}
        <div className="flex items-center gap-4">
          {/* Upgrade Button - Visible when logged in */}
          {session && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowPricingModal(true)}
              className="hidden sm:flex gap-2 border-primary/20 hover:bg-primary/5 text-primary"
            >
              <Sparkles className="w-4 h-4" />
              升級方案
            </Button>
          )}

          {status === "loading" ? (
            <div className="w-8 h-8 animate-pulse bg-muted rounded-full"></div>
          ) : session ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-10 w-10 rounded-full">
                  <Avatar className="h-10 w-10">
                    <AvatarImage src={session.user?.image || ""} alt={session.user?.name || ""} />
                    <AvatarFallback className="bg-primary text-primary-foreground">
                      {session.user?.name?.[0]?.toUpperCase() || "U"}
                    </AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end" forceMount>
                <DropdownMenuLabel className="font-normal">
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium leading-none">{session.user?.name}</p>
                    <p className="text-xs leading-none text-muted-foreground">
                      {session.user?.email}
                    </p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                {/* Mobile Upgrade Button in Menu */}
                <DropdownMenuItem onClick={() => setShowPricingModal(true)} className="sm:hidden text-primary focus:text-primary">
                  <Sparkles className="mr-2 h-4 w-4" />
                  <span>升級方案</span>
                </DropdownMenuItem>
                <DropdownMenuSeparator className="sm:hidden" />
                <DropdownMenuItem onClick={() => signOut()}>
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>登出</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <Button onClick={() => signIn("google")}>登入</Button>
          )}
        </div>
      </div>

      <PricingModal
        isOpen={showPricingModal}
        onClose={() => setShowPricingModal(false)}
        currentCredits={0}
      />
    </header>
  );
}
