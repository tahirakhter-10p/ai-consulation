import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen, waitFor } from '@testing-library/react'
import { StrictMode } from 'react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { ConsultationDetailPage } from '../../src/pages/ConsultationDetailPage'
import type { MessageExchange } from '../../src/types/consultation'

const consultationApi = vi.hoisted(() => ({
  getConsultation: vi.fn(),
  getConsultationMessages: vi.fn(),
  sendConsultationMessage: vi.fn(),
}))

vi.mock('../../src/api/consultations', () => consultationApi)

function renderPage(initialState?: { initializeMessage: string }) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  })

  return render(
    <StrictMode>
      <QueryClientProvider client={queryClient}>
        <MemoryRouter
          initialEntries={[
            {
              pathname: '/consultations/consultation-1',
              state: initialState,
            },
          ]}
        >
          <Routes>
            <Route path="/consultations/:id" element={<ConsultationDetailPage />} />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>
    </StrictMode>,
  )
}

describe('ConsultationDetailPage', () => {
  beforeEach(() => {
    consultationApi.getConsultation.mockResolvedValue({
      id: 'consultation-1',
      patient_name: 'Ada Lovelace',
      primary_concern: 'Headache',
      status: 'Pending',
    })
    consultationApi.getConsultationMessages.mockResolvedValue([])
    consultationApi.sendConsultationMessage.mockReset()
  })

  it('releases the chat input after the automatic first AI response completes', async () => {
    let resolveExchange!: (exchange: MessageExchange) => void
    consultationApi.sendConsultationMessage.mockReturnValue(
      new Promise<MessageExchange>((resolve) => {
        resolveExchange = resolve
      }),
    )
    renderPage({ initializeMessage: 'Headache' })

    expect(await screen.findByText('AI is thinking…')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Sending message' })).toBeDisabled()
    expect(consultationApi.sendConsultationMessage).toHaveBeenCalledOnce()

    resolveExchange({
      user_message: { role: 'user', content: 'Headache' },
      assistant_message: { role: 'assistant', content: 'How long have you had it?' },
    })

    expect(await screen.findByText('How long have you had it?')).toBeInTheDocument()
    await waitFor(() => {
      expect(screen.queryByText('AI is thinking…')).not.toBeInTheDocument()
      expect(screen.getByRole('button', { name: 'Send message' })).toBeEnabled()
      expect(screen.getByLabelText('Consultation message')).toBeEnabled()
    })
    expect(consultationApi.sendConsultationMessage).toHaveBeenCalledOnce()
  })

  it('releases the chat input when the automatic first message fails', async () => {
    consultationApi.sendConsultationMessage.mockRejectedValue(new Error('Request failed'))
    renderPage({ initializeMessage: 'Headache' })

    expect(await screen.findByText(/your message was not sent/i)).toBeInTheDocument()
    await waitFor(() => {
      expect(screen.queryByText('AI is thinking…')).not.toBeInTheDocument()
      expect(screen.getByRole('button', { name: 'Send message' })).toBeEnabled()
      expect(screen.getByLabelText('Consultation message')).toBeEnabled()
    })
    expect(consultationApi.sendConsultationMessage).toHaveBeenCalledOnce()
  })
})
