import { Play, Square, RotateCw, PackageCheck, FolderOpen, Activity } from 'lucide-react'
import { ComposeApp, AppState } from '@/types'
import { getStateBadgeClass, formatPercentage } from '@/lib/utils'
import { useState } from 'react'

interface AppCardProps {
  app: ComposeApp
  onAction: (appId: string, action: string) => void
}

export function AppCard({ app, onAction }: AppCardProps) {
  const [actionLoading, setActionLoading] = useState<string | null>(null)

  const handleAction = async (action: string) => {
    setActionLoading(action)
    try {
      await onAction(app.id, action)
    } finally {
      setActionLoading(null)
    }
  }

  const runningServices = app.services.filter(s => s.state === 'running').length
  const totalServices = app.services.length

  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-800 hover:border-gray-700 transition-colors">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-white mb-1">{app.name}</h3>
          <p className="text-sm text-gray-500 flex items-center">
            <FolderOpen className="w-3 h-3 mr-1" />
            {app.path}
          </p>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getStateBadgeClass(app.state)}`}>
          {app.state.replace('_', ' ').toUpperCase()}
        </span>
      </div>

      {/* Services Info */}
      <div className="mb-4 space-y-2">
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-400">Services</span>
          <span className="text-white font-medium">
            {runningServices} / {totalServices} running
          </span>
        </div>

        {app.state === AppState.RUNNING && (
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-400">Resources</span>
            <div className="flex items-center space-x-3">
              <span className="text-blue-400">
                <Activity className="w-3 h-3 inline mr-1" />
                CPU: {formatPercentage(app.cpu_percent)}
              </span>
              <span className="text-green-400">
                RAM: {app.memory_mb.toFixed(0)} MB
              </span>
            </div>
          </div>
        )}

        {/* Service List */}
        <div className="mt-3 space-y-1">
          {app.services.map((service) => (
            <div
              key={service.name}
              className="flex items-center justify-between text-xs bg-gray-800/50 px-3 py-2 rounded"
            >
              <span className="text-gray-300">{service.name}</span>
              <span className={`px-2 py-0.5 rounded text-xs ${getStateBadgeClass(service.state)}`}>
                {service.state}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center space-x-2">
        {app.state !== AppState.RUNNING && (
          <button
            onClick={() => handleAction('start')}
            disabled={actionLoading === 'start'}
            className="flex-1 flex items-center justify-center space-x-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white px-4 py-2 rounded-lg transition-colors text-sm"
          >
            {actionLoading === 'start' ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Starting...</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                <span>Start</span>
              </>
            )}
          </button>
        )}

        {app.state === AppState.RUNNING && (
          <>
            <button
              onClick={() => handleAction('restart')}
              disabled={!!actionLoading}
              className="flex-1 flex items-center justify-center space-x-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white px-4 py-2 rounded-lg transition-colors text-sm"
            >
              {actionLoading === 'restart' ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Restarting...</span>
                </>
              ) : (
                <>
                  <RotateCw className="w-4 h-4" />
                  <span>Restart</span>
                </>
              )}
            </button>

            <button
              onClick={() => handleAction('stop')}
              disabled={!!actionLoading}
              className="flex-1 flex items-center justify-center space-x-2 bg-red-600 hover:bg-red-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white px-4 py-2 rounded-lg transition-colors text-sm"
            >
              {actionLoading === 'stop' ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Stopping...</span>
                </>
              ) : (
                <>
                  <Square className="w-4 h-4" />
                  <span>Stop</span>
                </>
              )}
            </button>
          </>
        )}

        <button
          onClick={() => handleAction('rebuild')}
          disabled={!!actionLoading}
          className="flex items-center justify-center bg-gray-700 hover:bg-gray-600 disabled:bg-gray-800 disabled:cursor-not-allowed text-white px-4 py-2 rounded-lg transition-colors text-sm"
          title="Rebuild"
        >
          {actionLoading === 'rebuild' ? (
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
          ) : (
            <PackageCheck className="w-4 h-4" />
          )}
        </button>
      </div>
    </div>
  )
}
