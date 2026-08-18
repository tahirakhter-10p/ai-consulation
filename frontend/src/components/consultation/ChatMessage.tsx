import AutoAwesomeRoundedIcon from '@mui/icons-material/AutoAwesomeRounded'
import PersonRoundedIcon from '@mui/icons-material/PersonRounded'
import { Avatar, Box, Paper, Stack, Typography } from '@mui/material'

import type { ConsultationMessage } from '../../types/consultation'

interface ChatMessageProps {
  message: ConsultationMessage
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user'

  return (
    <Stack
      direction={isUser ? 'row-reverse' : 'row'}
      alignItems="flex-start"
      spacing={1.5}
      sx={{ alignSelf: isUser ? 'flex-end' : 'flex-start', maxWidth: { xs: '94%', md: '78%' } }}
    >
      <Avatar
        sx={{
          width: 34,
          height: 34,
          mt: 0.25,
          bgcolor: isUser ? 'common.black' : 'primary.main',
          color: 'common.white',
        }}
      >
        {isUser ? <PersonRoundedIcon fontSize="small" /> : <AutoAwesomeRoundedIcon fontSize="small" />}
      </Avatar>
      <Paper
        elevation={0}
        sx={{
          px: 2.25,
          py: 1.75,
          border: '1px solid',
          borderColor: isUser ? '#d8dce2' : 'divider',
          borderLeftColor: isUser ? '#d8dce2' : 'primary.main',
          borderLeftWidth: isUser ? 1 : 3,
          bgcolor: isUser ? '#eef0f3' : 'background.paper',
          borderRadius: isUser ? '14px 4px 14px 14px' : '4px 14px 14px 14px',
        }}
      >
        <Box>
          <Typography variant="caption" color="text.secondary" fontWeight={700}>
            {isUser ? 'You' : 'AI Assistant'}
          </Typography>
          <Typography
            variant="body2"
            sx={{ mt: 0.5, whiteSpace: 'pre-wrap', overflowWrap: 'anywhere', lineHeight: 1.65 }}
          >
            {message.content}
          </Typography>
        </Box>
      </Paper>
    </Stack>
  )
}
