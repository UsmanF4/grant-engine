import { NextAuthConfig } from 'next-auth'

declare module 'next-auth' {
  interface User {
    accessToken: string
    refreshToken: string
    expiresAt: number
  }
}
import CredentialProvider from 'next-auth/providers/credentials'

const authConfig = {
  providers: [
    CredentialProvider({
      credentials: {
        email: {
          type: 'email'
        },
        password: {
          type: 'password'
        }
      },
      authorize: async (credentials, _req) => {
        console.log('original request:', _req)
        try {
          const response = await fetch(
            'https://api.aiathenalytics.com/api/v1/user/login',
            {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                email: credentials?.email,
                password: credentials?.password,
                remember_me: true
              })
            }
          )

          if (!response.ok) {
            console.error('Failed to log in:', response.status, response.statusText)
            return null
          }

          const tokens = await response.json()

          // Create a mock user object with tokens
          const user = {
            id: tokens.access_token, // You might use a different value here if available
            name: credentials?.email, // or another identifier from your backend
            email: credentials?.email,
            accessToken: tokens.access_token,
            refreshToken: tokens.refresh_token,
            expiresAt: tokens.expires_at
          }

          return user // Return the user object to be used in the session
        } catch (error) {
          console.error('Error in authorize:', error)
          return null
        }
      }
    })
  ],
  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60, // 30 days
    updateAge: 24 * 60 * 60 // 24 hours
  },
  callbacks: {
    async jwt({ token, user }) {
      //Store USER ROLES HERE
      if (user) {
        token.accessToken = user.accessToken
        token.refreshToken = user.refreshToken
        token.expiresAt = user.expiresAt
      }
      return token
    },
    async session({ session, token }) {
      // Add token fields to the session
      session.accessToken = token.accessToken as string
      session.refreshToken = token.refreshToken
      session.expiresAt = token.expiresAt
      return session
    }
  },
  pages: {
    signIn: '/auth/login', //sigin page,
    error: '/auth/error' //error pageu
  },
  debug: true
} satisfies NextAuthConfig

export default authConfig
