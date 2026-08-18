import { apiClient } from './axios'
import type { APIResponse } from '../types/api'
import type {
  Consultation,
  ConsultationListItem,
  ConsultationListParams,
  ConsultationMessage,
  CreateConsultationRequest,
  MessageExchange,
} from '../types/consultation'

export async function getConsultations(
  params: ConsultationListParams = {},
): Promise<ConsultationListItem[]> {
  const response = await apiClient.get<APIResponse<ConsultationListItem[]>>('/consultations', {
    params,
  })
  return response.data.data
}

export async function createConsultation(
  payload: CreateConsultationRequest,
): Promise<Consultation> {
  const response = await apiClient.post<APIResponse<Consultation>>('/consultations', payload)
  return response.data.data
}

export async function getConsultation(consultationId: string): Promise<Consultation> {
  const response = await apiClient.get<APIResponse<Consultation>>(
    `/consultations/${consultationId}`,
  )
  return response.data.data
}

export async function getConsultationMessages(
  consultationId: string,
): Promise<ConsultationMessage[]> {
  const response = await apiClient.get<APIResponse<ConsultationMessage[]>>(
    `/consultations/${consultationId}/messages`,
  )
  return response.data.data
}

export async function sendConsultationMessage(
  consultationId: string,
  message: string,
): Promise<MessageExchange> {
  const response = await apiClient.post<APIResponse<MessageExchange>>(
    `/consultations/${consultationId}/messages`,
    { message },
    { timeout: 120_000 },
  )
  return response.data.data
}
