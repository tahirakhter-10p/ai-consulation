import axios from 'axios'

import { apiClient } from './axios'
import type { APIResponse } from '../types/api'
import type { Recommendation } from '../types/recommendation'

export async function getRecommendation(consultationId: string): Promise<Recommendation | null> {
  try {
    const response = await apiClient.get<APIResponse<Recommendation>>(
      `/consultations/${consultationId}/recommendation`,
    )
    return response.data.data
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 404) return null
    throw error
  }
}

export async function generateRecommendation(consultationId: string): Promise<Recommendation> {
  const response = await apiClient.post<APIResponse<Recommendation>>(
    `/consultations/${consultationId}/recommendation`,
    undefined,
    { timeout: 180_000 },
  )
  return response.data.data
}
