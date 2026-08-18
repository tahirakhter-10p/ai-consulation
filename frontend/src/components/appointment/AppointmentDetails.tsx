import CalendarMonthOutlinedIcon from '@mui/icons-material/CalendarMonthOutlined'
import CheckCircleRoundedIcon from '@mui/icons-material/CheckCircleRounded'
import LocationOnOutlinedIcon from '@mui/icons-material/LocationOnOutlined'
import MedicalServicesOutlinedIcon from '@mui/icons-material/MedicalServicesOutlined'
import AccessTimeOutlinedIcon from '@mui/icons-material/AccessTimeOutlined'
import PaymentsOutlinedIcon from '@mui/icons-material/PaymentsOutlined'
import { Box, Card, CardContent, Divider, Grid2 as Grid, Stack, Typography } from '@mui/material'

import type { Appointment } from '../../types/appointment'
import type { RecommendedTreatment } from '../../types/recommendation'
import { StatusChip } from '../consultation/StatusChip'

interface AppointmentDetailsProps {
  appointment: Appointment
  treatment?: RecommendedTreatment
}

export function AppointmentDetails({ appointment, treatment }: AppointmentDetailsProps) {
  const scheduledAt = new Date(appointment.appointment_datetime)
  const formattedDate = Number.isNaN(scheduledAt.getTime())
    ? appointment.appointment_datetime
    : new Intl.DateTimeFormat(undefined, {
        dateStyle: 'long',
        timeStyle: 'short',
      }).format(scheduledAt)

  const estimatedCost = appointment.price
    ? `$${Number(appointment.price).toLocaleString()}`
    : treatment?.price_min && treatment.price_max
      ? `$${Number(treatment.price_min).toLocaleString()}–$${Number(treatment.price_max).toLocaleString()}`
      : 'Not specified'
  const details = [
    { label: 'Treatment', value: appointment.treatment, icon: <MedicalServicesOutlinedIcon /> },
    { label: 'Specialty', value: appointment.specialty ?? 'Not specified', icon: <MedicalServicesOutlinedIcon /> },
    { label: 'Target area', value: appointment.default_target_area ?? 'Not specified', icon: <MedicalServicesOutlinedIcon /> },
    {
      label: 'Duration',
      value: appointment.duration_minutes ? `${appointment.duration_minutes} minutes` : 'Not specified',
      icon: <AccessTimeOutlinedIcon />,
    },
    { label: 'Estimated cost', value: estimatedCost, icon: <PaymentsOutlinedIcon /> },
    { label: 'Date and time', value: formattedDate, icon: <CalendarMonthOutlinedIcon /> },
    { label: 'Location', value: appointment.location, icon: <LocationOnOutlinedIcon /> },
  ]

  return (
    <Card>
      <CardContent sx={{ p: { xs: 3, md: 4 }, '&:last-child': { pb: { xs: 3, md: 4 } } }}>
        <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between" gap={2}>
          <Stack direction="row" spacing={1.5} alignItems="center">
            <CheckCircleRoundedIcon color="success" sx={{ fontSize: 38 }} />
            <Box>
              <Typography variant="h5" component="h2" fontWeight={800}>Appointment Booked</Typography>
              <Typography variant="body2" color="text.secondary">Your appointment details are confirmed.</Typography>
            </Box>
          </Stack>
          <StatusChip status="Booked" />
        </Stack>
        <Divider sx={{ my: 3 }} />
        <Grid container spacing={3}>
          {details.map((detail) => (
            <Grid key={detail.label} size={{ xs: 12, sm: 6, md: 4 }}>
              <Stack direction="row" spacing={1.5} alignItems="flex-start">
                <Box sx={{ color: 'primary.main', mt: 0.25 }}>{detail.icon}</Box>
                <Box>
                  <Typography variant="caption" color="text.secondary">{detail.label.toUpperCase()}</Typography>
                  <Typography fontWeight={750} sx={{ mt: 0.25 }}>{detail.value}</Typography>
                </Box>
              </Stack>
            </Grid>
          ))}
        </Grid>
        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 3 }}>
          Appointment ID: {appointment.id}
        </Typography>
      </CardContent>
    </Card>
  )
}
