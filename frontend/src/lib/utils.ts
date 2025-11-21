import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatBytes(bytes: number, decimals = 2): string {
  if (bytes === 0) return '0 Bytes'

  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']

  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}

export function formatPercentage(value: number, decimals = 1): string {
  return `${value.toFixed(decimals)}%`
}

export function getStateColor(state: string): string {
  switch (state.toLowerCase()) {
    case 'running':
      return 'text-green-400'
    case 'stopped':
    case 'exited':
      return 'text-gray-400'
    case 'partially_healthy':
      return 'text-yellow-400'
    case 'error':
    case 'dead':
      return 'text-red-400'
    case 'restarting':
      return 'text-blue-400'
    default:
      return 'text-gray-500'
  }
}

export function getStateBadgeClass(state: string): string {
  switch (state.toLowerCase()) {
    case 'running':
      return 'bg-green-900/30 text-green-400 border-green-500/30'
    case 'stopped':
    case 'exited':
      return 'bg-gray-900/30 text-gray-400 border-gray-500/30'
    case 'partially_healthy':
      return 'bg-yellow-900/30 text-yellow-400 border-yellow-500/30'
    case 'error':
    case 'dead':
      return 'bg-red-900/30 text-red-400 border-red-500/30'
    case 'restarting':
      return 'bg-blue-900/30 text-blue-400 border-blue-500/30'
    default:
      return 'bg-gray-900/30 text-gray-500 border-gray-500/30'
  }
}
