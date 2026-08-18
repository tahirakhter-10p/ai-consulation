import axios from 'axios'

import type { APIError } from '../types/api'

export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError<APIError>(error)) {
    return error.response?.data?.message ?? 'Unable to connect to the server. Please try again.'
  }

  return 'Something went wrong. Please try again.'
}
