import { Chip } from '@mui/material'

import type { ConsultationStatus } from '../../types/consultation'

const statusColors: Record<ConsultationStatus, { background: string; color: string }> = {
  Pending: { background: '#f1f3f5', color: '#4f5864' },
  Booked: { background: '#e5f0ff', color: '#075ca8' },
  Completed: { background: '#e8f5ee', color: '#26734d' },
}

interface StatusChipProps {
  status: ConsultationStatus
}

export function StatusChip({ status }: StatusChipProps) {
  const colors = statusColors[status]

  return (
    <Chip
      label={status}
      size="small"
      sx={{ bgcolor: colors.background, color: colors.color, fontWeight: 700, minWidth: 78 }}
    />
  )
}
