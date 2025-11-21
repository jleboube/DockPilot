import { Container, Server, RefreshCw } from 'lucide-react'
import { DockerInfo } from '@/types'

interface HeaderProps {
  dockerInfo: DockerInfo | null
  onDiscover: () => void
}

export function Header({ dockerInfo, onDiscover }: HeaderProps) {
  return (
    <header className="bg-gray-900 border-b border-gray-800">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-primary-600 p-2 rounded-lg">
              <Container className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">DockPilot</h1>
              <p className="text-sm text-gray-400">Docker Compose Management</p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {dockerInfo && (
              <div className="flex items-center space-x-2 text-sm">
                <Server className="w-4 h-4 text-green-400" />
                <span className="text-gray-300">
                  Docker {dockerInfo.info.server_version}
                </span>
                <span className="text-gray-600">|</span>
                <span className="text-gray-400">
                  {dockerInfo.info.containers} containers
                </span>
                <span className="text-gray-600">|</span>
                <span className="text-gray-400">
                  {dockerInfo.info.images} images
                </span>
              </div>
            )}

            <button
              onClick={onDiscover}
              className="flex items-center space-x-2 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Discover Apps</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
