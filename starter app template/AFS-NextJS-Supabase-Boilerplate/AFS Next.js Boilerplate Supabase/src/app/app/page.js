'use client'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useSession } from '@/lib/auth-client'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Button } from '@/components/ui/button'
import AccountSettings from '@/components/AccountSettings'

export default function AppPage() {
  const { data: session, isPending } = useSession()
  const router = useRouter()

  useEffect(() => {
    if (!isPending && !session) {
      router.push('/auth')
    }
  }, [isPending, session, router])

  if (isPending) {
    return (
      <div className="min-h-screen bg-white gradient-mesh">
        <div className="container mx-auto px-4 py-8">
          <div className="animate-pulse space-y-6">
            <div className="h-8 bg-gray-200/60 rounded-xl w-1/4"></div>
            <div className="h-64 bg-gray-200/60 rounded-2xl"></div>
          </div>
        </div>
      </div>
    )
  }

  if (!session) return null

  const user = session.user

  return (
    <div className="min-h-screen bg-white gradient-mesh">
      <header className="glass-nav sticky top-0 z-40">
        <div className="container mx-auto px-4 md:px-6">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-black flex items-center justify-center shadow-lg">
                <span className="text-white font-bold text-lg">S</span>
              </div>
              <span className="text-xl font-bold hidden sm:block">Starter App</span>
            </Link>
            <div className="flex items-center space-x-4">
              <span className="hidden md:block text-sm text-gray-500">
                welcome, <span className="font-medium text-gray-900">{user.name || user.email}</span>
              </span>
              <div className="w-10 h-10 rounded-full bg-black flex items-center justify-center overflow-hidden">
                {user.image ? (
                  <img src={user.image} alt="" className="w-full h-full object-cover" />
                ) : (
                  <span className="text-white font-semibold">{(user.name || user.email || 'U')[0].toUpperCase()}</span>
                )}
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 md:px-6 py-8">
        <div className="mb-8">
          <h1 className="text-2xl md:text-3xl font-bold mb-2">Dashboard</h1>
          <p className="text-gray-500">Manage your account and build your app</p>
        </div>

        <Tabs defaultValue="app" className="w-full">
          <TabsList className="grid w-full grid-cols-2 max-w-md mb-8">
            <TabsTrigger value="app">My App</TabsTrigger>
            <TabsTrigger value="account">Account</TabsTrigger>
          </TabsList>

          <TabsContent value="app">
            <Card className="min-h-[400px]">
              <CardHeader>
                <CardTitle>Build Your App</CardTitle>
                <CardDescription>This is your blank canvas.</CardDescription>
              </CardHeader>
              <CardContent className="flex flex-col items-center justify-center py-12 text-center">
                <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mb-6">
                  <span className="text-4xl">✨</span>
                </div>
                <h3 className="text-xl font-semibold mb-3">Ready to build?</h3>
                <p className="text-gray-500 max-w-md mb-6">
                  Edit <code className="bg-gray-100 px-2 py-1 rounded">src/app/app/page.js</code> to add your features.
                </p>
                <div className="flex gap-3">
                  <Button>Add Component</Button>
                  <Link href="/"><Button variant="outline">View Landing</Button></Link>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="account">
            <AccountSettings />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
