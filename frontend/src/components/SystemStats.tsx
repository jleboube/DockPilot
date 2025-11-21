import { Cpu, MemoryStick, HardDrive } from 'lucide-react'
import { SystemInfo } from '@/types'
import { formatPercentage } from '@/lib/utils'

interface SystemStatsProps {
  systemInfo: SystemInfo | null
}

export function SystemStats({ systemInfo }: SystemStatsProps) {
  if (!systemInfo) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="bg-gray-900 rounded-lg p-4 border border-gray-800 animate-pulse">
            <div className="h-16 bg-gray-800 rounded"></div>
          </div>
        ))}
      </div>
    )
  }

  const stats = [
    {
      icon: Cpu,
      label: 'CPU',
      value: formatPercentage(systemInfo.cpu.percent),
      subtext: `${systemInfo.cpu.count} cores`,
      color: 'text-blue-400',
      bgColor: 'bg-blue-900/20',
    },
    {
      icon: MemoryStick,
      label: 'Memory',
      value: formatPercentage(systemInfo.memory.percent),
      subtext: `${(systemInfo.memory.used_mb / 1024).toFixed(1)} GB / ${(systemInfo.memory.total_mb / 1024).toFixed(1)} GB`,
      color: 'text-green-400',
      bgColor: 'bg-green-900/20',
    },
    {
      icon: HardDrive,
      label: 'Disk',
      value: formatPercentage(systemInfo.disk.percent),
      subtext: `${systemInfo.disk.free_gb.toFixed(1)} GB free`,
      color: 'text-purple-400',
      bgColor: 'bg-purple-900/20',
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="bg-gray-900 rounded-lg p-4 border border-gray-800 hover:border-gray-700 transition-colors"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-2">
                <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                  <stat.icon className={`w-5 h-5 ${stat.color}`} />
                </div>
                <span className="text-gray-400 text-sm font-medium">{stat.label}</span>
              </div>
              <div className="ml-11">
                <p className={`text-2xl font-bold ${stat.color}`}>{stat.value}</p>
                <p className="text-sm text-gray-500 mt-1">{stat.subtext}</p>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
