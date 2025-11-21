export enum AppState {
  RUNNING = 'running',
  STOPPED = 'stopped',
  PARTIALLY_HEALTHY = 'partially_healthy',
  ERROR = 'error',
  UNKNOWN = 'unknown',
}

export enum ContainerState {
  RUNNING = 'running',
  EXITED = 'exited',
  PAUSED = 'paused',
  RESTARTING = 'restarting',
  DEAD = 'dead',
  CREATED = 'created',
  REMOVING = 'removing',
}

export interface PortMapping {
  host_port: number
  container_port: number
  protocol: string
}

export interface VolumeInfo {
  name: string
  source: string
  destination: string
  mode: string
  size_mb?: number
}

export interface ServiceInfo {
  name: string
  image: string
  container_id?: string
  state: ContainerState
  ports: PortMapping[]
  volumes: VolumeInfo[]
  environment: Record<string, string>
  cpu_percent: number
  memory_mb: number
  memory_limit_mb?: number
  health_status?: string
}

export interface ComposeApp {
  id: string
  name: string
  path: string
  compose_file: string
  state: AppState
  services: ServiceInfo[]
  networks: string[]
  volumes: string[]
  created_at?: string
  updated_at?: string
  auto_start: boolean
  cpu_percent: number
  memory_mb: number
}

export interface ResourceUsage {
  cpu_percent: number
  memory_mb: number
  memory_percent: number
  disk_read_mb: number
  disk_write_mb: number
  network_rx_mb: number
  network_tx_mb: number
}

export interface SystemInfo {
  cpu: {
    count: number
    percent: number
  }
  memory: {
    total_mb: number
    available_mb: number
    used_mb: number
    percent: number
  }
  disk: {
    total_gb: number
    used_gb: number
    free_gb: number
    percent: number
  }
  platform: string
}

export interface DockerInfo {
  version: {
    Version: string
    ApiVersion: string
    GitCommit: string
  }
  info: {
    containers: number
    images: number
    server_version: string
    operating_system: string
    architecture: string
    memory_total: number
    cpus: number
  }
}

export interface LogEntry {
  timestamp: string
  service: string
  message: string
  stream: string
}
