"use client";

import { useSession, signIn, signOut } from "next-auth/react";
import { Button } from "@/components/ui/button";
import { LogIn, LogOut, User } from "lucide-react";

export default function LoginButton() {
    const { data: session } = useSession();

    if (session) {
        return (
            <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                    {session.user?.image ? (
                        // eslint-disable-next-line @next/next/no-img-element
                        <img src={session.user.image} alt={session.user.name || "User"} className="w-8 h-8 rounded-full" />
                    ) : (
                        <User className="w-8 h-8 p-1 bg-secondary rounded-full" />
                    )}
                    <span className="text-sm font-medium hidden sm:inline-block">{session.user?.name}</span>
                </div>
                <Button variant="outline" size="sm" onClick={() => signOut()}>
                    <LogOut className="w-4 h-4 mr-2" />
                    登出
                </Button>
            </div>
        );
    }

    return (
        <Button variant="primary" size="sm" onClick={() => signIn("google")}>
            <LogIn className="w-4 h-4 mr-2" />
            Google 登入
        </Button>
    );
}
