import { ComposeApp } from '@/types'
import { AppCard } from './AppCard'
import { Package } from 'lucide-react'

interface AppDashboardProps {
  apps: ComposeApp[]
  onAction: (appId: string, action: string) => void
  loading: boolean
}

export function AppDashboard({ apps, onAction, loading }: AppDashboardProps) {
  if (loading && apps.length === 0) {
    return (
      <div className="space-y-4">
        <h2 className="text-xl font-semibold text-white">Applications</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-gray-900 rounded-lg p-6 border border-gray-800 animate-pulse">
              <div className="space-y-4">
                <div className="h-6 bg-gray-800 rounded w-1/3"></div>
                <div className="h-4 bg-gray-800 rounded w-2/3"></div>
                <div className="h-20 bg-gray-800 rounded"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (apps.length === 0) {
    return (
      <div className="bg-gray-900 rounded-lg p-12 border border-gray-800 text-center">
        <Package className="w-16 h-16 text-gray-600 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-300 mb-2">No Applications Found</h3>
        <p className="text-gray-500 mb-6">
          Click "Discover Apps" to scan for Docker Compose applications
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-white">
          Applications <span className="text-gray-500">({apps.length})</span>
        </h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {apps.map((app) => (
          <AppCard key={app.id} app={app} onAction={onAction} />
        ))}
      </div>
    </div>
  )
}
