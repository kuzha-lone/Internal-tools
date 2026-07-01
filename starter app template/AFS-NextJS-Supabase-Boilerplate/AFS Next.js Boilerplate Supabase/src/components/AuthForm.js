'use client'
import { useState } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { signIn } from '@/lib/auth-client'

export default function AuthForm() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleGoogleAuth = async () => {
    setLoading(true)
    setError('')
    try {
      await signIn.social({ provider: 'google', callbackURL: '/app' })
    } catch (err) {
      setError(err.message || 'Failed to sign in')
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex">
      <div className="hidden lg:flex lg:w-1/2 gradient-dark relative overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute top-20 right-20 w-72 h-72 bg-white/5 rounded-full blur-3xl animate-float"></div>
          <div className="absolute bottom-20 left-20 w-96 h-96 bg-gray-500/10 rounded-full blur-3xl animate-float animation-delay-300"></div>
        </div>
        <div className="relative z-10 flex flex-col justify-center px-12 xl:px-16">
          <div className="mb-8">
            <div className="flex items-center space-x-3 mb-8">
              <div className="w-12 h-12 rounded-xl bg-white flex items-center justify-center shadow-lg">
                <span className="text-black font-bold text-xl">S</span>
              </div>
              <span className="text-2xl font-bold text-white">Starter App</span>
            </div>
            <h1 className="text-4xl xl:text-5xl font-bold text-white mb-4 leading-tight">
              welcome to<br /><span className="text-gray-400">Starter App</span>
            </h1>
            <p className="text-xl text-gray-400">Sign in to access your dashboard.</p>
          </div>
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center p-6 md:p-12 animated-gradient-bg">
        <div className="w-full max-w-md">
          <div className="lg:hidden flex items-center justify-center space-x-3 mb-8">
            <div className="w-10 h-10 rounded-xl bg-black flex items-center justify-center shadow-lg">
              <span className="text-white font-bold text-lg">S</span>
            </div>
            <span className="text-xl font-bold text-gray-900">Starter App</span>
          </div>

          <div className="glass-card rounded-2xl p-6 md:p-8 shadow-glass-lg">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold mb-2 text-gray-900">welcome</h2>
              <p className="text-gray-500">sign in to continue</p>
            </div>

            <Button className="w-full py-6 rounded-xl text-base" onClick={handleGoogleAuth} disabled={loading}>
              <svg className="w-5 h-5 mr-3" viewBox="0 0 24 24">
                <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              {loading ? 'Signing in...' : 'Continue with Google'}
            </Button>

            {error && (
              <div className="mt-6 p-4 bg-red-50/80 border border-red-100 rounded-xl">
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}
          </div>

          <div className="mt-6 text-center">
            <Link href="/">
              <span className="text-sm text-gray-500 hover:text-gray-700 cursor-pointer">← back to home</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
