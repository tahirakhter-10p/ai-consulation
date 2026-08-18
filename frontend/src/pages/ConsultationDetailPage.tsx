import ArrowBackRoundedIcon from '@mui/icons-material/ArrowBackRounded'
import AutoAwesomeRoundedIcon from '@mui/icons-material/AutoAwesomeRounded'
import SummarizeOutlinedIcon from '@mui/icons-material/SummarizeOutlined'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Alert, Box, Button, Card, Divider, Stack, Typography } from '@mui/material'
import { useCallback, useEffect, useRef, useState } from 'react'
import { Link as RouterLink, Navigate, useLocation, useNavigate, useParams } from 'react-router-dom'

import {
  getConsultation,
  getConsultationMessages,
  sendConsultationMessage,
} from '../api/consultations'
import { ErrorMessage } from '../components/common/ErrorMessage'
import { LoadingSpinner } from '../components/common/LoadingSpinner'
import { ChatInput } from '../components/consultation/ChatInput'
import { ChatMessage } from '../components/consultation/ChatMessage'
import { StatusChip } from '../components/consultation/StatusChip'
import type { ConsultationMessage } from '../types/consultation'
import { getErrorMessage } from '../utils/apiError'

export function ConsultationDetailPage() {
  const { id } = useParams<{ id: string }>()
  const location = useLocation()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const endOfConversationRef = useRef<HTMLDivElement>(null)
  const initializationStartedRef = useRef(false)
  const sendInFlightRef = useRef(false)
  const [isSendingMessage, setIsSendingMessage] = useState(false)

  const consultationQuery = useQuery({
    queryKey: ['consultation', id],
    queryFn: () => getConsultation(id!),
    enabled: Boolean(id),
    staleTime: 5_000,
    retry: 3,
    retryDelay: (attempt) => 300 * (attempt + 1),
  })

  const messagesQuery = useQuery({
    queryKey: ['consultation-messages', id],
    queryFn: () => getConsultationMessages(id!),
    enabled: Boolean(id),
    staleTime: 5_000,
    retry: 3,
    retryDelay: (attempt) => 300 * (attempt + 1),
  })

  const {
    mutateAsync: sendMessage,
    isError: isSendError,
    error: sendError,
  } = useMutation({
    mutationFn: (message: string) => sendConsultationMessage(id!, message),
    onSuccess: (exchange) => {
      queryClient.setQueryData<ConsultationMessage[]>(
        ['consultation-messages', id],
        (current = []) => [...current, exchange.user_message, exchange.assistant_message],
      )
    },
  })

  const messageCount = messagesQuery.data?.length ?? 0
  useEffect(() => {
    endOfConversationRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [isSendingMessage, messageCount])

  const handleSend = useCallback(async (message: string) => {
    if (sendInFlightRef.current) return false

    sendInFlightRef.current = true
    setIsSendingMessage(true)
    try {
      await sendMessage(message)
      return true
    } catch {
      return false
    } finally {
      sendInFlightRef.current = false
      setIsSendingMessage(false)
    }
  }, [sendMessage])

  const initializeMessage = (location.state as { initializeMessage?: string } | null)
    ?.initializeMessage

  useEffect(() => {
    if (
      !initializeMessage
      || messagesQuery.data?.length !== 0
      || initializationStartedRef.current
    ) return

    initializationStartedRef.current = true
    navigate(location.pathname, { replace: true, state: null })
    void handleSend(initializeMessage)
  }, [handleSend, initializeMessage, location.pathname, messagesQuery.data, navigate])

  if (!id) {
    return (
      <Box sx={{ pt: 5 }}>
        <ErrorMessage title="Invalid consultation" message="No consultation ID was provided." />
      </Box>
    )
  }

  if (consultationQuery.data?.status === 'Booked') {
    return <Navigate to={`/consultations/${id}/appointment`} replace />
  }

  return (
    <Box sx={{ maxWidth: 1100, mx: 'auto', pt: { xs: 3, md: 4 }, pb: 2 }}>
      <Button
        component={RouterLink}
        to="/consultations"
        color="inherit"
        startIcon={<ArrowBackRoundedIcon />}
        sx={{ mb: 2 }}
      >
        Back to Consultation Records
      </Button>

      {consultationQuery.isPending && <LoadingSpinner label="Loading consultation details…" />}

      {consultationQuery.isError && (
        <ErrorMessage
          title="Consultation unavailable"
          message={getErrorMessage(consultationQuery.error)}
          onRetry={() => void consultationQuery.refetch()}
        />
      )}

      {consultationQuery.data && (
        <>
          <Card sx={{ mb: 2.5 }}>
            <Stack
              direction={{ xs: 'column', sm: 'row' }}
              alignItems={{ xs: 'flex-start', sm: 'center' }}
              justifyContent="space-between"
              gap={2}
              sx={{ px: { xs: 2.5, md: 3 }, py: 2.5 }}
            >
              <Box>
                <Stack direction="row" alignItems="center" spacing={1.5} flexWrap="wrap" useFlexGap>
                  <Typography variant="h5" component="h1" fontWeight={800}>
                    {consultationQuery.data.patient_name}
                  </Typography>
                  <StatusChip status={consultationQuery.data.status} />
                </Stack>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                  <Box component="span" fontWeight={700} color="text.primary">Primary concern: </Box>
                  {consultationQuery.data.primary_concern}
                </Typography>
              </Box>
              <Stack direction={{ xs: 'column', sm: 'row' }} alignItems={{ xs: 'flex-start', sm: 'center' }} spacing={1.5}>
                <Stack direction="row" alignItems="center" spacing={1} color="primary.main">
                  <AutoAwesomeRoundedIcon fontSize="small" />
                  <Typography variant="body2" fontWeight={750}>AI Consultation</Typography>
                </Stack>
                <Button
                  component={RouterLink}
                  to={`/consultations/${id}/recommendation`}
                  state={{ autoGenerate: true }}
                  variant="outlined"
                  startIcon={<SummarizeOutlinedIcon />}
                >
                  Generate Recommendation
                </Button>
              </Stack>
            </Stack>
          </Card>

          <Card sx={{ overflow: 'hidden' }}>
            <Box sx={{ px: { xs: 2.5, md: 3 }, py: 2.25 }}>
              <Typography variant="h6" fontWeight={800}>Conversation</Typography>
              <Typography variant="body2" color="text.secondary">
                Messages are saved automatically and used as context by the AI assistant.
              </Typography>
            </Box>
            <Divider />

            <Box
              aria-live="polite"
              sx={{
                height: { xs: 280, sm: 430 },
                minHeight: { xs: 240, sm: 300 },
                overflowY: 'auto',
                px: { xs: 2, md: 3 },
                py: 3,
                bgcolor: '#f8f9fb',
              }}
            >
              {messagesQuery.isPending && <LoadingSpinner label="Loading conversation…" />}

              {messagesQuery.isError && (
                <ErrorMessage
                  title="Conversation unavailable"
                  message={getErrorMessage(messagesQuery.error)}
                  onRetry={() => void messagesQuery.refetch()}
                />
              )}

              {messagesQuery.data?.length === 0 && !isSendingMessage && (
                <Box
                  sx={{
                    minHeight: 240,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    textAlign: 'center',
                  }}
                >
                  <AutoAwesomeRoundedIcon color="primary" sx={{ fontSize: 36, mb: 1.5 }} />
                  <Typography variant="h6" fontWeight={750}>No messages yet</Typography>
                  <Typography color="text.secondary" sx={{ mt: 0.75 }}>
                    Start the consultation by sending a message below.
                  </Typography>
                </Box>
              )}

              {messagesQuery.data && (messagesQuery.data.length > 0 || isSendingMessage) && (
                <Stack spacing={2.5}>
                  {messagesQuery.data.map((message, index) => (
                    <ChatMessage key={`${message.role}-${index}`} message={message} />
                  ))}
                  {isSendingMessage && (
                    <Stack direction="row" spacing={1.5} alignItems="center" color="text.secondary">
                      <AutoAwesomeRoundedIcon color="primary" fontSize="small" />
                      <Typography variant="body2">AI is thinking…</Typography>
                    </Stack>
                  )}
                </Stack>
              )}
              <div ref={endOfConversationRef} />
            </Box>

            <Divider />
            <Box sx={{ p: { xs: 2, md: 2.5 }, bgcolor: 'background.paper' }}>
              {isSendError && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {getErrorMessage(sendError)} Your message was not sent. Please try again.
                </Alert>
              )}
              <ChatInput isSending={isSendingMessage} onSend={handleSend} />
              <Typography variant="caption" color="text.secondary" sx={{ display: 'block', textAlign: 'center', mt: 1 }}>
                AI can make mistakes. Verify important clinical information.
              </Typography>
            </Box>
          </Card>
        </>
      )}
    </Box>
  )
}
