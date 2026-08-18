import type { ConsultationStatus } from './consultation'

export interface CreateAppointmentRequest {
  treatment_id?: string
  treatment?: string
  appointment_datetime: string
  location: string
}

export interface AppointmentBookedResponse {
  appointment_id: string
  consultation_id: string
  treatment_id: string
  treatment: string
  specialty: string
  treatment_description: string
  default_target_area: string | null
  appointment_datetime: string
  location: string
  price: string | null
  duration_minutes: number | null
  status: ConsultationStatus
}

export interface Appointment {
  id: string
  consultation_id: string
  treatment_id: string | null
  treatment: string
  specialty: string | null
  appointment_datetime: string
  location: string
  treatment_description: string | null
  default_target_area: string | null
  price: string | null
  duration_minutes: number | null
}
