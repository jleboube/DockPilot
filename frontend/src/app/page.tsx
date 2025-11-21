'use client'

import { useEffect, useState } from 'react'
import { AppDashboard } from '@/components/AppDashboard'
import { SystemStats } from '@/components/SystemStats'
import { Header } from '@/components/Header'
import { ComposeApp, SystemInfo, DockerInfo } from '@/types'
import { apiClient } from '@/lib/api'

export default function Home() {
  const [apps, setApps] = useState<ComposeApp[]>([])
  const [systemInfo, setSystemInfo] = useState<SystemInfo | null>(null)
  const [dockerInfo, setDockerInfo] = useState<DockerInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadData()
    const interval = setInterval(loadData, 5000) // Refresh every 5 seconds
    return () => clearInterval(interval)
  }, [])

  async function loadData() {
    try {
      const [appsData, sysInfo, dockInfo] = await Promise.all([
        apiClient.getApps(),
        apiClient.getSystemInfo(),
        apiClient.getDockerInfo(),
      ])

      setApps(appsData)
      setSystemInfo(sysInfo)
      setDockerInfo(dockInfo)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  async function handleDiscoverApps() {
    try {
      setLoading(true)
      await apiClient.discoverApps()
      await loadData()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to discover apps')
    } finally {
      setLoading(false)
    }
  }

  async function handleAppAction(appId: string, action: string) {
    try {
      await apiClient.performAction(appId, action)
      await loadData()
    } catch (err) {
      setError(err instanceof Error ? err.message : `Failed to ${action} app`)
    }
  }

  if (loading && apps.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading DockPilot...</p>
        </div>
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-gray-950">
      <Header dockerInfo={dockerInfo} onDiscover={handleDiscoverApps} />

      <div className="container mx-auto px-4 py-6 space-y-6">
        {error && (
          <div className="bg-red-900/20 border border-red-500 text-red-300 px-4 py-3 rounded">
            {error}
          </div>
        )}

        <SystemStats systemInfo={systemInfo} />

        <AppDashboard
          apps={apps}
          onAction={handleAppAction}
          loading={loading}
        />
      </div>
    </main>
  )
}
