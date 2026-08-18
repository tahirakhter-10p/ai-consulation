import SendRoundedIcon from '@mui/icons-material/SendRounded'
import { Box, CircularProgress, IconButton, TextField } from '@mui/material'
import { type FormEvent, useState } from 'react'

interface ChatInputProps {
  isSending: boolean
  onSend: (message: string) => Promise<boolean>
}

export function ChatInput({ isSending, onSend }: ChatInputProps) {
  const [message, setMessage] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const isEmpty = message.trim().length === 0

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSubmitted(true)
    if (isEmpty || isSending) return

    const sent = await onSend(message.trim())
    if (sent) {
      setMessage('')
      setSubmitted(false)
    }
  }

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
      <TextField
        fullWidth
        multiline
        maxRows={4}
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault()
            event.currentTarget.closest('form')?.requestSubmit()
          }
        }}
        placeholder="Ask the AI assistant about this consultation…"
        error={submitted && isEmpty}
        helperText={submitted && isEmpty ? 'Enter a message before sending.' : 'Press Enter to send · Shift+Enter for a new line'}
        disabled={isSending}
        slotProps={{ htmlInput: { 'aria-label': 'Consultation message' } }}
      />
      <IconButton
        type="submit"
        color="primary"
        disabled={isSending}
        aria-label={isSending ? 'Sending message' : 'Send message'}
        sx={{
          width: 48,
          height: 48,
          bgcolor: 'primary.main',
          color: 'common.white',
          '&:hover': { bgcolor: 'primary.dark' },
          '&.Mui-disabled': { bgcolor: 'action.disabledBackground' },
        }}
      >
        {isSending ? <CircularProgress size={22} color="inherit" /> : <SendRoundedIcon />}
      </IconButton>
    </Box>
  )
}
