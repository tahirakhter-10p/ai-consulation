import { Box, Card, CardContent, Stack, Typography } from '@mui/material'
import type { ReactNode } from 'react'

interface StatisticsCardProps {
  label: string
  value: string
  icon: ReactNode
  accentColor: string
  iconBackground: string
}

export function StatisticsCard({
  label,
  value,
  icon,
  accentColor,
  iconBackground,
}: StatisticsCardProps) {
  return (
    <Card
      sx={{
        height: '100%',
        minHeight: 158,
        borderRadius: 2.25,
        borderColor: '#dfe5ed',
        boxShadow: '0 7px 20px rgba(32, 51, 74, 0.055)',
        transition: 'transform 180ms ease, box-shadow 180ms ease',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: '0 11px 26px rgba(32, 51, 74, 0.09)',
        },
      }}
    >
      <CardContent sx={{ p: 3, '&:last-child': { pb: 3 } }}>
        <Stack direction="row" alignItems="flex-start" justifyContent="space-between" spacing={2}>
          <Box>
            <Typography
              variant="caption"
              color="text.secondary"
              fontWeight={800}
              sx={{ letterSpacing: '0.075em', textTransform: 'uppercase' }}
            >
              {label}
            </Typography>
            <Typography
              variant="h2"
              component="p"
              fontWeight={800}
              letterSpacing="-0.055em"
              sx={{ mt: 1.5, fontSize: { xs: '2.55rem', sm: '2.9rem' }, lineHeight: 1 }}
            >
              {value}
            </Typography>
          </Box>
          <Box
            sx={{
              width: 44,
              height: 44,
              borderRadius: 2,
              bgcolor: iconBackground,
              color: accentColor,
              display: 'grid',
              placeItems: 'center',
              flexShrink: 0,
              '& .MuiSvgIcon-root': { fontSize: 22 },
            }}
          >
            {icon}
          </Box>
        </Stack>
      </CardContent>
    </Card>
  )
}
