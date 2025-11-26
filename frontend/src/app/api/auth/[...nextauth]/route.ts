import NextAuth from "next-auth"
import GoogleProvider from "next-auth/providers/google"

const handler = NextAuth({
    providers: [
        GoogleProvider({
            clientId: process.env.GOOGLE_CLIENT_ID ?? "",
            clientSecret: process.env.GOOGLE_CLIENT_SECRET ?? "",
            authorization: {
                params: {
                    access_type: "offline",
                    response_type: "code"
                }
            }
        }),
    ],
    callbacks: {
        async jwt({ token, account }) {
            // Persist the id_token to the token right after signin
            if (account) {
                token.id_token = account.id_token
            }
            return token
        },
        async session({ session, token }) {
            // Send properties to the client
            // @ts-expect-error - id_token is not in the default session type
            session.id_token = token.id_token
            return session
        }
    },
    secret: process.env.NEXTAUTH_SECRET,
})

export { handler as GET, handler as POST }
