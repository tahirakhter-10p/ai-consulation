import AddRoundedIcon from '@mui/icons-material/AddRounded'
import ArrowForwardRoundedIcon from '@mui/icons-material/ArrowForwardRounded'
import CalendarMonthOutlinedIcon from '@mui/icons-material/CalendarMonthOutlined'
import DashboardRoundedIcon from '@mui/icons-material/DashboardRounded'
import ForumOutlinedIcon from '@mui/icons-material/ForumOutlined'
import SwapHorizRoundedIcon from '@mui/icons-material/SwapHorizRounded'
import PaymentsOutlinedIcon from '@mui/icons-material/PaymentsOutlined'
import { Box, Button, Card, CardContent, Grid2 as Grid, Skeleton, Stack, Typography } from '@mui/material'
import { useQuery } from '@tanstack/react-query'
import { Link as RouterLink } from 'react-router-dom'

import { getDashboardStatistics } from '../api/dashboard'
import { ErrorMessage } from '../components/common/ErrorMessage'
import { StatisticsCard } from '../components/dashboard/StatisticsCard'
import { DashboardDemoSections } from '../components/dashboard/DashboardDemoSections'
import { dashboardDemoData } from '../components/dashboard/demoData'
import { getErrorMessage } from '../utils/apiError'

const metricCards = [
  {
    key: 'total_consultations' as const,
    label: 'Total Consultations',
    icon: <ForumOutlinedIcon />,
    accentColor: '#0876d1',
    iconBackground: '#e7f3fd',
  },
  {
    key: 'booked_appointments' as const,
    label: 'Booked Appointments',
    icon: <CalendarMonthOutlinedIcon />,
    accentColor: '#0876d1',
    iconBackground: '#e7f3fd',
  },
  {
    key: 'conversion_rate' as const,
    label: 'Conversion Rate',
    icon: <SwapHorizRoundedIcon />,
    accentColor: '#0876d1',
    iconBackground: '#e7f3fd',
  },
]

function DashboardLoadingState() {
  return (
    <Grid container spacing={2.25} aria-label="Loading dashboard statistics">
      {metricCards.map((metric) => (
        <Grid key={metric.key} size={{ xs: 12, sm: 6, lg: 3 }}>
          <Card sx={{ minHeight: 158 }}>
            <CardContent sx={{ p: 3 }}>
              <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                <Box sx={{ width: '68%' }}>
                  <Skeleton width="82%" height={20} />
                  <Skeleton width="58%" height={60} sx={{ mt: 1 }} />
                </Box>
                <Skeleton variant="rounded" width={44} height={44} />
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      ))}
      <Grid size={{ xs: 12, sm: 6, lg: 3 }}>
        <Card sx={{ minHeight: 158 }}>
          <CardContent sx={{ p: 3 }}>
            <Skeleton width="72%" height={20} />
            <Skeleton width="52%" height={60} sx={{ mt: 1 }} />
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  )
}

export function DashboardPage() {
  const dashboardQuery = useQuery({
    queryKey: ['dashboard'],
    queryFn: getDashboardStatistics,
  })
  const monthlyRevenue = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: dashboardDemoData.monthlyRevenue.currency,
    notation: 'compact',
    maximumFractionDigits: 1,
  }).format(dashboardDemoData.monthlyRevenue.amount)

  return (
    <Box sx={{ maxWidth: 1180, mx: 'auto', pt: { xs: 3, md: 4.5 }, pb: 5 }}>
      <Stack
        direction={{ xs: 'column', md: 'row' }}
        alignItems={{ xs: 'flex-start', md: 'center' }}
        justifyContent="space-between"
        gap={3}
        sx={{ mb: { xs: 3, md: 4 } }}
      >
        <Stack direction="row" spacing={1.75} alignItems="flex-start">
          <Box
            sx={{
              width: 44,
              height: 44,
              display: 'grid',
              placeItems: 'center',
              borderRadius: 2,
              bgcolor: 'primary.light',
              color: 'primary.main',
              flexShrink: 0,
            }}
          >
            <DashboardRoundedIcon />
          </Box>
          <Box>
            <Typography
              variant="h4"
              component="h1"
              fontWeight={800}
              letterSpacing="-0.04em"
              sx={{ fontSize: { xs: '2rem', md: '2.2rem' } }}
            >
              Overview
            </Typography>
            <Typography color="text.secondary" sx={{ mt: 0.6, maxWidth: 550 }}>
              Monitor consultation activity and appointment conversion at a glance.
            </Typography>
          </Box>
        </Stack>

        <Stack
          direction={{ xs: 'column', sm: 'row' }}
          spacing={1.25}
          sx={{ width: { xs: '100%', md: 'auto' } }}
        >
          <Button
            component={RouterLink}
            to="/consultations"
            variant="outlined"
            endIcon={<ArrowForwardRoundedIcon />}
          >
            Consultation Records
          </Button>
          <Button
            component={RouterLink}
            to="/dashboard?newConsult=true"
            variant="contained"
            startIcon={<AddRoundedIcon />}
          >
            New Consult
          </Button>
        </Stack>
      </Stack>

      {dashboardQuery.isPending && <DashboardLoadingState />}

      {dashboardQuery.isError && (
        <ErrorMessage
          title="Dashboard unavailable"
          message={getErrorMessage(dashboardQuery.error)}
          onRetry={() => void dashboardQuery.refetch()}
        />
      )}

      {dashboardQuery.data && (
        <Grid container spacing={2.25} aria-label="Dashboard statistics">
          {metricCards.map((metric) => {
            const rawValue = dashboardQuery.data[metric.key]
            const value = metric.key === 'conversion_rate'
              ? `${rawValue.toLocaleString(undefined, { maximumFractionDigits: 2 })}%`
              : rawValue.toLocaleString()

            return (
              <Grid key={metric.key} size={{ xs: 12, sm: 6, lg: 3 }}>
                <StatisticsCard {...metric} value={value} />
              </Grid>
            )
          })}
          <Grid size={{ xs: 12, sm: 6, lg: 3 }}>
            <Card sx={{ height: '100%', minHeight: 158, borderRadius: 2.25, bgcolor: 'primary.main', color: 'common.white' }}>
              <CardContent sx={{ p: 3, '&:last-child': { pb: 3 } }}>
                <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                  <Box>
                    <Typography variant="caption" fontWeight={800} sx={{ letterSpacing: '0.075em', opacity: 0.8 }}>
                      MONTHLY REVENUE
                    </Typography>
                    <Typography variant="h4" fontWeight={800} sx={{ mt: 1.5 }}>{monthlyRevenue}</Typography>
                  </Box>
                  <Box sx={{ width: 44, height: 44, borderRadius: 2, bgcolor: 'rgba(255,255,255,0.16)', display: 'grid', placeItems: 'center' }}>
                    <PaymentsOutlinedIcon />
                  </Box>
                </Stack>
                <Typography variant="caption" sx={{ display: 'block', mt: 2, opacity: 0.8 }}>
                  {dashboardDemoData.monthlyRevenue.comparisonLabel}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      <DashboardDemoSections />
    </Box>
  )
}
