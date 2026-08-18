import axios from 'axios'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { getErrorMessage } from '../../src/utils/apiError'

describe('getErrorMessage', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('returns the API message for an Axios error response', () => {
    const error = { response: { data: { message: 'Consultation not found' } } }
    vi.spyOn(axios, 'isAxiosError').mockReturnValue(true)

    expect(getErrorMessage(error)).toBe('Consultation not found')
  })

  it('returns a connection message when an Axios response has no API message', () => {
    vi.spyOn(axios, 'isAxiosError').mockReturnValue(true)

    expect(getErrorMessage(new Error('Network error'))).toBe(
      'Unable to connect to the server. Please try again.',
    )
  })

  it('returns a generic message for non-Axios errors', () => {
    vi.spyOn(axios, 'isAxiosError').mockReturnValue(false)

    expect(getErrorMessage(new Error('Unexpected'))).toBe(
      'Something went wrong. Please try again.',
    )
  })
})
