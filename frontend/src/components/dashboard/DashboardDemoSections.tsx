import AssignmentTurnedInOutlinedIcon from '@mui/icons-material/AssignmentTurnedInOutlined'
import AutoGraphRoundedIcon from '@mui/icons-material/AutoGraphRounded'
import CalendarMonthOutlinedIcon from '@mui/icons-material/CalendarMonthOutlined'
import ChevronRightRoundedIcon from '@mui/icons-material/ChevronRightRounded'
import DescriptionOutlinedIcon from '@mui/icons-material/DescriptionOutlined'
import ForumOutlinedIcon from '@mui/icons-material/ForumOutlined'
import HistoryRoundedIcon from '@mui/icons-material/HistoryRounded'
import NoteAltOutlinedIcon from '@mui/icons-material/NoteAltOutlined'
import PersonAddAltOutlinedIcon from '@mui/icons-material/PersonAddAltOutlined'
import {
  Avatar,
  Box,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid2 as Grid,
  Stack,
  Typography,
} from '@mui/material'
import type { ReactNode } from 'react'

import { dashboardDemoData, type ActivityKind } from './demoData'

const activityIcons: Record<ActivityKind, ReactNode> = {
  consultation: <ForumOutlinedIcon fontSize="small" />,
  appointment: <CalendarMonthOutlinedIcon fontSize="small" />,
  report: <DescriptionOutlinedIcon fontSize="small" />,
  intake: <PersonAddAltOutlinedIcon fontSize="small" />,
  note: <NoteAltOutlinedIcon fontSize="small" />,
}

export function DashboardDemoSections() {
  const maxConsultations = Math.max(
    ...dashboardDemoData.consultationTrends.map((item) => item.consultations),
  )

  return (
    <Grid container spacing={2.25} sx={{ mt: 0.25 }}>
      <Grid size={{ xs: 12, lg: 8 }}>
        <Stack spacing={2.25}>
          <Card>
            <CardContent sx={{ p: 2.75, '&:last-child': { pb: 2.75 } }}>
              <Stack direction="row" alignItems="center" justifyContent="space-between" spacing={2}>
                <Stack direction="row" alignItems="center" spacing={1}>
                  <AutoGraphRoundedIcon color="primary" />
                  <Typography variant="subtitle1" component="h2" fontWeight={800}>
                    Consultation Trends
                  </Typography>
                </Stack>
                <Chip label="Last 7 Days · Demo" size="small" variant="outlined" />
              </Stack>
              <Divider sx={{ my: 2 }} />

              <Box
                role="img"
                aria-label="Demo consultation activity for the last seven days"
                sx={{
                  height: 220,
                  display: 'flex',
                  alignItems: 'flex-end',
                  gap: { xs: 1, sm: 2 },
                  px: { xs: 1, sm: 2 },
                  pt: 2,
                  borderRadius: 2,
                  backgroundImage: 'linear-gradient(to top, #e7ebf0 1px, transparent 1px)',
                  backgroundSize: '100% 25%',
                }}
              >
                {dashboardDemoData.consultationTrends.map((trend) => (
                  <Stack
                    key={trend.day}
                    alignItems="center"
                    justifyContent="flex-end"
                    spacing={1}
                    sx={{ height: '100%', flex: 1, minWidth: 0 }}
                  >
                    <Typography variant="caption" fontWeight={800} color="text.secondary">
                      {trend.consultations}
                    </Typography>
                    <Box
                      title={`${trend.day}: ${trend.consultations} consultations`}
                      sx={{
                        width: '100%',
                        maxWidth: 52,
                        minHeight: 12,
                        height: `${Math.max((trend.consultations / maxConsultations) * 145, 12)}px`,
                        borderRadius: '6px 6px 2px 2px',
                        bgcolor: trend.highlighted ? 'primary.main' : '#bed8f5',
                        transition: 'height 200ms ease',
                      }}
                    />
                    <Typography variant="caption" color="text.secondary">{trend.day}</Typography>
                  </Stack>
                ))}
              </Box>
            </CardContent>
          </Card>

          <Card>
            <CardContent sx={{ p: 2.75, '&:last-child': { pb: 2.75 } }}>
              <Stack direction="row" alignItems="center" justifyContent="space-between" spacing={2}>
                <Stack direction="row" alignItems="center" spacing={1}>
                  <AssignmentTurnedInOutlinedIcon color="primary" />
                  <Typography variant="subtitle1" component="h2" fontWeight={800}>
                    Pending Clinical Reviews
                  </Typography>
                </Stack>
                <Chip
                  label={`${dashboardDemoData.pendingClinicalReviews.length} Demo Records`}
                  size="small"
                  sx={{ bgcolor: '#fff1ed', color: '#b54726', fontWeight: 800 }}
                />
              </Stack>
              <Divider sx={{ my: 2 }} />
              <Stack spacing={1.25}>
                {dashboardDemoData.pendingClinicalReviews.map((review) => (
                  <Stack
                    key={review.id}
                    direction="row"
                    alignItems="center"
                    spacing={1.5}
                    sx={{ p: 1.5, border: '1px solid', borderColor: 'divider', borderRadius: 2, bgcolor: '#fafbfd' }}
                  >
                    <Avatar sx={{ width: 38, height: 38, bgcolor: '#e6ebf5', color: '#52647a', fontSize: '0.8rem', fontWeight: 800 }}>
                      {review.initials}
                    </Avatar>
                    <Box sx={{ minWidth: 0, flex: 1 }}>
                      <Typography variant="body2" fontWeight={800}>
                        {review.patientName} · {review.specialty}
                      </Typography>
                      <Typography variant="caption" color="text.secondary" noWrap>
                        {review.summary}
                      </Typography>
                    </Box>
                    <ChevronRightRoundedIcon color="primary" />
                  </Stack>
                ))}
              </Stack>
            </CardContent>
          </Card>
        </Stack>
      </Grid>

      <Grid size={{ xs: 12, lg: 4 }}>
        <Card>
          <CardContent sx={{ p: 2.75, '&:last-child': { pb: 2.75 } }}>
            <Stack direction="row" alignItems="center" justifyContent="space-between" spacing={2}>
              <Stack direction="row" alignItems="center" spacing={1}>
                <HistoryRoundedIcon color="primary" />
                <Typography variant="subtitle1" component="h2" fontWeight={800}>
                  Recent Activity
                </Typography>
              </Stack>
              <Chip label="Demo" size="small" variant="outlined" />
            </Stack>
            <Divider sx={{ my: 2 }} />
            <Stack component="ol" sx={{ m: 0, p: 0, listStyle: 'none' }}>
              {dashboardDemoData.recentActivity.map((activity, index) => (
                <Stack
                  component="li"
                  key={activity.id}
                  direction="row"
                  alignItems="center"
                  spacing={1.5}
                  sx={{
                    py: 1.4,
                    borderBottom: index < dashboardDemoData.recentActivity.length - 1 ? '1px solid' : 0,
                    borderColor: 'divider',
                  }}
                >
                  <Box
                    sx={{
                      width: 40,
                      height: 40,
                      flexShrink: 0,
                      display: 'grid',
                      placeItems: 'center',
                      borderRadius: 2,
                      bgcolor: index % 2 === 0 ? 'primary.light' : '#edf1f6',
                      color: index % 2 === 0 ? 'primary.main' : 'text.secondary',
                    }}
                  >
                    {activityIcons[activity.kind]}
                  </Box>
                  <Box sx={{ minWidth: 0, flex: 1 }}>
                    <Typography variant="body2" fontWeight={750} noWrap>
                      {activity.title}
                    </Typography>
                    <Typography variant="caption" color="text.secondary" noWrap sx={{ display: 'block', mt: 0.25 }}>
                      {activity.subject}
                    </Typography>
                  </Box>
                  <Typography
                    variant="caption"
                    color="text.secondary"
                    sx={{ flexShrink: 0, alignSelf: 'flex-start', pt: 0.25, whiteSpace: 'nowrap' }}
                  >
                    {activity.occurredAt}
                  </Typography>
                </Stack>
              ))}
            </Stack>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  )
}
