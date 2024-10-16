// next-auth.d.ts
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import NextAuth from 'next-auth'

// Extend the built-in types for User
declare module 'next-auth' {
  interface User {
    access_token: string
    refresh_token: string
    expires_at: string
    roles: string[] // Array of roles for the user
  }

  interface Session {
    access_token: string
    refresh_token: string
    expires_at: string
    user: {
      name?: string | null
      email?: string | null
      image?: string | null
      roles: string[] // Array of roles for the user in the session
    }
  }
}

// Extend the built-in types for JWT
declare module 'next-auth/jwt' {
  interface JWT {
    access_token: string
    refresh_token: string
    expires_at: string
    roles: string[] // Array of roles for the JWT token
  }
}
