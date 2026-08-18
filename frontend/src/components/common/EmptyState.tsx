import SearchOffRoundedIcon from '@mui/icons-material/SearchOffRounded'
import { Box, Typography } from '@mui/material'
import type { ReactNode } from 'react'

interface EmptyStateProps {
  title: string
  description: string
  action?: ReactNode
}

export function EmptyState({ title, description, action }: EmptyStateProps) {
  return (
    <Box
      sx={{
        minHeight: 240,
        px: 3,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
      }}
    >
      <Box
        sx={{
          width: 48,
          height: 48,
          mb: 2,
          borderRadius: '50%',
          display: 'grid',
          placeItems: 'center',
          bgcolor: 'primary.light',
          color: 'primary.main',
        }}
      >
        <SearchOffRoundedIcon />
      </Box>
      <Typography variant="h6" fontWeight={750}>{title}</Typography>
      <Typography color="text.secondary" sx={{ mt: 0.75, maxWidth: 420 }}>
        {description}
      </Typography>
      {action && <Box sx={{ mt: 2.5 }}>{action}</Box>}
    </Box>
  )
}
