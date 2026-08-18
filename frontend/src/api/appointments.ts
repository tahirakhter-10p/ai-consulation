import { apiClient } from './axios'
import type { APIResponse } from '../types/api'
import type {
  Appointment,
  AppointmentBookedResponse,
  CreateAppointmentRequest,
} from '../types/appointment'

export async function getAppointmentForConsultation(
  consultationId: string,
): Promise<Appointment | null> {
  const response = await apiClient.get<APIResponse<Appointment[]>>('/appointments')
  return response.data.data.find((appointment) => appointment.consultation_id === consultationId) ?? null
}

export async function bookAppointment(
  consultationId: string,
  payload: CreateAppointmentRequest,
): Promise<AppointmentBookedResponse> {
  const response = await apiClient.post<APIResponse<AppointmentBookedResponse>>(
    `/consultations/${consultationId}/appointment`,
    payload,
  )
  return response.data.data
}
