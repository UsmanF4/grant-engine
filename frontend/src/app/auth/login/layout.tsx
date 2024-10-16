import React, { ReactNode } from 'react'

interface LayoutProps {
  readonly children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  return (
    <main>
      <div className="container relative h-screen flex-col items-center justify-center md:grid lg:max-w-none lg:grid-cols-2 lg:px-0">
        <div className="flex h-full lg:p-8">{children}</div>
        <div className="relative hidden h-full flex-col bg-muted p-10 text-white lg:flex">
          <div className="absolute inset-0 bg-zinc-900" />
          <div className="relative z-20 flex items-center text-lg font-medium">
            Document Verification App by Grant Engine
          </div>
          <div className="relative z-20 mt-auto">
            <blockquote className="space-y-2">
              <p className="text-lg">
                This tool is intented to help you verify documents and information
                provided by applicants. It is a great tool to help you make informed
                decisions.
              </p>
            </blockquote>
          </div>
        </div>
      </div>
    </main>
  )
}
