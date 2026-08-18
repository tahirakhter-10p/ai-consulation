import { Box, CircularProgress, Typography } from '@mui/material'

interface LoadingSpinnerProps {
  label?: string
}

export function LoadingSpinner({ label = 'Loading dashboard…' }: LoadingSpinnerProps) {
  return (
    <Box
      role="status"
      sx={{
        minHeight: 220,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 2,
      }}
    >
      <CircularProgress size={34} thickness={4} />
      <Typography color="text.secondary">{label}</Typography>
    </Box>
  )
}
