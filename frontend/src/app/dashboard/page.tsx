'use client'

import { useSession } from 'next-auth/react'
const Page = () => {
  const { data: session } = useSession()
  console.log(session)

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <header className="mb-6 bg-white p-4 shadow">
        <h1 className="text-2xl font-bold">Dashboard</h1>
      </header>
      <main>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          <div className="rounded-lg bg-white p-6 shadow">
            <h2 className="mb-2 text-xl font-semibold">Card 1</h2>
            <p className="text-gray-700">Content for card 1.</p>
          </div>
          <div className="rounded-lg bg-white p-6 shadow">
            <h2 className="mb-2 text-xl font-semibold">Card 2</h2>
            <p className="text-gray-700">Content for card 2.</p>
          </div>
          <div className="rounded-lg bg-white p-6 shadow">
            <h2 className="mb-2 text-xl font-semibold">Card 3</h2>
            <p className="text-gray-700">Content for card 3.</p>
          </div>
        </div>
      </main>
    </div>
  )
}

export default Page
