import PersonSearchRoundedIcon from '@mui/icons-material/PersonSearchRounded'
import { Card, CardContent, Stack, Typography } from '@mui/material'

interface PatientSummaryCardProps {
  summary: string
}

export function PatientSummaryCard({ summary }: PatientSummaryCardProps) {
  return (
    <Card sx={{ height: '100%' }}>
      <CardContent sx={{ p: 3, '&:last-child': { pb: 3 } }}>
        <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
          <PersonSearchRoundedIcon color="primary" />
          <Typography variant="h6" component="h2" fontWeight={800}>Patient Summary</Typography>
        </Stack>
        <Typography color="text.secondary" sx={{ lineHeight: 1.75, whiteSpace: 'pre-wrap' }}>
          {summary}
        </Typography>
      </CardContent>
    </Card>
  )
}
