import { apiClient } from './axios'
import type { APIResponse } from '../types/api'
import type { DashboardStatistics } from '../types/dashboard'

export async function getDashboardStatistics(): Promise<DashboardStatistics> {
  const response = await apiClient.get<APIResponse<DashboardStatistics>>('/dashboard')
  return response.data.data
}
