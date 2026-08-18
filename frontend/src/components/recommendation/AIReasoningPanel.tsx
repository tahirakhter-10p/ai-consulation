import AutoAwesomeRoundedIcon from '@mui/icons-material/AutoAwesomeRounded'
import { Box, Stack, Typography } from '@mui/material'

interface AIReasoningPanelProps {
  reasoning: string
}

export function AIReasoningPanel({ reasoning }: AIReasoningPanelProps) {
  return (
    <Box
      sx={{
        height: '100%',
        p: 3,
        border: '1px solid',
        borderColor: 'divider',
        borderLeft: '3px solid',
        borderLeftColor: 'primary.main',
        borderRadius: 1,
        bgcolor: '#f8fbfe',
      }}
    >
      <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
        <AutoAwesomeRoundedIcon color="primary" />
        <Typography variant="h6" component="h2" fontWeight={800}>AI Reasoning</Typography>
      </Stack>
      <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.75, whiteSpace: 'pre-wrap' }}>
        {reasoning}
      </Typography>
    </Box>
  )
}
