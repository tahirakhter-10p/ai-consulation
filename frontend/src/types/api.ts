export interface APIResponse<Data> {
  success: boolean
  message: string
  data: Data
}

export interface APIErrorDetail {
  field: string
  message: string
}

export interface APIError {
  success: false
  message: string
  errors: APIErrorDetail[]
}
