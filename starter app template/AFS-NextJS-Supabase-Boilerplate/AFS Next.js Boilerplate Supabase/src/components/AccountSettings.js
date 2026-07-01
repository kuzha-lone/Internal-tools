'use client'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Switch } from '@/components/ui/switch'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useSession, signOut } from '@/lib/auth-client'
import { getUserProfile, updateUserProfile } from '@/lib/supabase'

export default function AccountSettings() {
  const { data: session, isPending } = useSession()
  const [profile, setProfile] = useState(null)
  const [username, setUsername] = useState('')
  const [theme, setTheme] = useState('light')
  const [notifications, setNotifications] = useState(true)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')
  const router = useRouter()

  useEffect(() => {
    if (session?.user) {
      loadProfile()
    }
  }, [session])

  const loadProfile = async () => {
    try {
      const p = await getUserProfile(session.user.id)
      if (p) {
        setProfile(p)
        setUsername(p.username || session.user.name || '')
        setTheme(p.theme || 'light')
        setNotifications(p.notifications !== false)
      } else {
        setUsername(session.user.name || session.user.email?.split('@')[0] || '')
      }
    } catch (err) {
      console.error(err)
    }
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      await updateUserProfile(session.user.id, { username, theme, notifications })
      setMessage('Settings saved!')
      setTimeout(() => setMessage(''), 3000)
    } catch (err) {
      setMessage('Error saving settings')
    } finally {
      setSaving(false)
    }
  }

  const handleSignOut = async () => {
    await signOut()
    router.push('/')
  }

  if (isPending) {
    return <div className="h-32 bg-gray-100/60 animate-pulse rounded-2xl"></div>
  }

  if (!session?.user) return null

  const user = session.user

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center space-x-4">
            <div className="w-16 h-16 rounded-2xl bg-black flex items-center justify-center shadow-lg overflow-hidden">
              {user.image ? (
                <img src={user.image} alt="" className="w-full h-full object-cover" />
              ) : (
                <span className="text-white font-bold text-2xl">{(user.name || user.email || 'U')[0].toUpperCase()}</span>
              )}
            </div>
            <div>
              <CardTitle className="text-xl">{username || user.name}</CardTitle>
              <CardDescription>{user.email}</CardDescription>
            </div>
          </div>
        </CardHeader>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Settings</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">Display Name</label>
            <Input value={username} onChange={(e) => setUsername(e.target.value)} className="rounded-xl" />
          </div>

          <div className="flex items-center justify-between p-4 glass-subtle rounded-xl">
            <div>
              <div className="font-medium">Dark Mode</div>
              <div className="text-sm text-gray-500">Toggle dark theme</div>
            </div>
            <Switch checked={theme === 'dark'} onCheckedChange={(c) => setTheme(c ? 'dark' : 'light')} />
          </div>

          <div className="flex items-center justify-between p-4 glass-subtle rounded-xl">
            <div>
              <div className="font-medium">Notifications</div>
              <div className="text-sm text-gray-500">Email notifications</div>
            </div>
            <Switch checked={notifications} onCheckedChange={setNotifications} />
          </div>

          <Button onClick={handleSave} disabled={saving} className="rounded-xl">
            {saving ? 'Saving...' : 'Save Changes'}
          </Button>

          {message && <p className="text-sm text-green-600">{message}</p>}
        </CardContent>
      </Card>

      <Card className="border-red-200/60">
        <CardHeader>
          <CardTitle className="text-red-600">Danger Zone</CardTitle>
        </CardHeader>
        <CardContent>
          <Button variant="outline" onClick={handleSignOut} className="rounded-xl border-red-200 text-red-600 hover:bg-red-50">
            Sign Out
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
