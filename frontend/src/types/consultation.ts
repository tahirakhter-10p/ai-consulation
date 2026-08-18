export type ConsultationStatus = 'Pending' | 'Booked' | 'Completed'

export interface Consultation {
  id: string
  patient_name: string
  primary_concern: string
  status: ConsultationStatus
}

export interface ConsultationListItem extends Consultation {
  recommended_procedure: string
}

export interface ConsultationListParams {
  search?: string
  status?: ConsultationStatus
}

export interface CreateConsultationRequest {
  patient_name: string
  primary_concern: string
}

export type MessageRole = 'user' | 'assistant'

export interface ConsultationMessage {
  role: MessageRole
  content: string
}

export interface MessageExchange {
  user_message: ConsultationMessage
  assistant_message: ConsultationMessage
}
