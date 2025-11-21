import axios from 'axios'
import { ComposeApp, SystemInfo, DockerInfo, ResourceUsage, LogEntry } from '@/types'

// Use relative URL if in browser, otherwise use env variable or default
const getApiBaseUrl = () => {
  if (typeof window !== 'undefined') {
    // Client-side: use current hostname with backend port
    const protocol = window.location.protocol
    const hostname = window.location.hostname
    return `${protocol}//${hostname}:48391`
  }
  // Server-side: use env variable or docker service name
  return process.env.NEXT_PUBLIC_API_URL || 'http://backend:8000'
}

const API_BASE_URL = getApiBaseUrl()

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const apiClient = {
  // Apps
  async getApps(): Promise<ComposeApp[]> {
    const response = await api.get('/api/apps/')
    return response.data
  },

  async getApp(appId: string): Promise<ComposeApp> {
    const response = await api.get(`/api/apps/${appId}`)
    return response.data
  },

  async discoverApps(searchPaths?: string[]): Promise<{ apps: ComposeApp[]; count: number }> {
    const response = await api.post('/api/apps/discover', { search_paths: searchPaths })
    return response.data
  },

  async performAction(appId: string, action: string): Promise<{ status: string; message: string }> {
    const response = await api.post(`/api/apps/${appId}/action`, { action })
    return response.data
  },

  async getAppStats(appId: string): Promise<{ app_id: string; app_name: string; stats: Array<{ service: string; stats: ResourceUsage }> }> {
    const response = await api.get(`/api/apps/${appId}/stats`)
    return response.data
  },

  async getAppLogs(appId: string, tail: number = 100): Promise<{ status: string; logs?: string }> {
    const response = await api.get(`/api/apps/${appId}/logs`, { params: { tail } })
    return response.data
  },

  // Docker
  async getDockerInfo(): Promise<DockerInfo> {
    const response = await api.get('/api/docker/info')
    return response.data
  },

  async getDockerStatus(): Promise<{ available: boolean; status: string }> {
    const response = await api.get('/api/docker/status')
    return response.data
  },

  // System
  async getSystemInfo(): Promise<SystemInfo> {
    const response = await api.get('/api/system/info')
    return response.data
  },

  async getOpenPorts(): Promise<{ ports: number[]; count: number }> {
    const response = await api.get('/api/system/ports')
    return response.data
  },

  // Logs
  async getContainerLogs(containerId: string, tail: number = 100): Promise<LogEntry[]> {
    const response = await api.get(`/api/logs/container/${containerId}`, { params: { tail } })
    return response.data
  },

  // Health
  async healthCheck(): Promise<{ status: string; version: string }> {
    const response = await api.get('/health')
    return response.data
  },
}

export default api
