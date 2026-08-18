import ArrowBackRoundedIcon from '@mui/icons-material/ArrowBackRounded'
import CalendarMonthOutlinedIcon from '@mui/icons-material/CalendarMonthOutlined'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Box, Button, Card, CardContent, Divider, Grid2 as Grid, Stack, Typography } from '@mui/material'
import { Link as RouterLink, useLocation, useParams } from 'react-router-dom'

import { bookAppointment, getAppointmentForConsultation } from '../api/appointments'
import { getConsultation } from '../api/consultations'
import { getRecommendation } from '../api/recommendations'
import { AppointmentForm } from '../components/appointment/AppointmentForm'
import { AppointmentDetails } from '../components/appointment/AppointmentDetails'
import { EmptyState } from '../components/common/EmptyState'
import { ErrorMessage } from '../components/common/ErrorMessage'
import { LoadingSpinner } from '../components/common/LoadingSpinner'
import { StatusChip } from '../components/consultation/StatusChip'
import type { CreateAppointmentRequest } from '../types/appointment'
import type { Consultation, ConsultationListItem } from '../types/consultation'
import { getErrorMessage } from '../utils/apiError'

export function AppointmentPage() {
  const { id } = useParams<{ id: string }>()
  const location = useLocation()
  const queryClient = useQueryClient()

  const consultationQuery = useQuery({
    queryKey: ['consultation', id],
    queryFn: () => getConsultation(id!),
    enabled: Boolean(id),
  })

  const recommendationQuery = useQuery({
    queryKey: ['recommendation', id],
    queryFn: () => getRecommendation(id!),
    enabled: Boolean(id),
  })

  const appointmentQuery = useQuery({
    queryKey: ['appointment', id],
    queryFn: () => getAppointmentForConsultation(id!),
    enabled: Boolean(id),
  })

  const appointmentMutation = useMutation({
    mutationFn: (appointment: CreateAppointmentRequest) => bookAppointment(id!, appointment),
    onSuccess: (appointmentResponse) => {
      queryClient.setQueryData(['appointment', id], {
        id: appointmentResponse.appointment_id,
        consultation_id: appointmentResponse.consultation_id,
        treatment_id: appointmentResponse.treatment_id,
        treatment: appointmentResponse.treatment,
        specialty: appointmentResponse.specialty,
        treatment_description: appointmentResponse.treatment_description,
        default_target_area: appointmentResponse.default_target_area,
        appointment_datetime: appointmentResponse.appointment_datetime,
        location: appointmentResponse.location,
        price: appointmentResponse.price,
        duration_minutes: appointmentResponse.duration_minutes,
      })
      queryClient.setQueryData<Consultation>(['consultation', id], (current) =>
        current ? { ...current, status: appointmentResponse.status } : current,
      )
      queryClient.setQueriesData<ConsultationListItem[]>(
        { queryKey: ['consultations'] },
        (current) => current?.map((item) =>
          item.id === id ? { ...item, status: appointmentResponse.status } : item,
        ),
      )

      window.setTimeout(() => {
        void queryClient.invalidateQueries({ queryKey: ['consultation', id] })
        void queryClient.invalidateQueries({ queryKey: ['consultations'] })
        void queryClient.invalidateQueries({ queryKey: ['dashboard'] })
        void queryClient.invalidateQueries({ queryKey: ['appointment', id] })
      }, 1_000)
    },
  })

  if (!id) {
    return (
      <Box sx={{ pt: 5 }}>
        <ErrorMessage title="Invalid consultation" message="No consultation ID was provided." />
      </Box>
    )
  }

  const consultation = consultationQuery.data
  const recommendation = recommendationQuery.data
  const appointment = appointmentQuery.data
  const recommendedTreatments = recommendation?.recommended_treatments.slice(0, 2) ?? []
  const selectedTreatmentKey = (location.state as { selectedTreatmentKey?: string } | null)
    ?.selectedTreatmentKey
  const appointmentTreatment = appointment
    ? recommendedTreatments.find((item) => (
        item.treatment_id === appointment.treatment_id || item.name === appointment.treatment
      ))
    : undefined
  const isAlreadyBooked = consultation?.status === 'Booked' && !appointment

  return (
    <Box sx={{ maxWidth: 1100, mx: 'auto', pt: { xs: 3, md: 4 }, pb: 4 }}>
      <Button
        component={RouterLink}
        to={consultation?.status === 'Booked' ? '/consultations' : `/consultations/${id}/recommendation`}
        color="inherit"
        startIcon={<ArrowBackRoundedIcon />}
        sx={{ mb: 2 }}
      >
        {consultation?.status === 'Booked' ? 'Back to Consultation Records' : 'Back to Recommendation'}
      </Button>

      {(consultationQuery.isPending || recommendationQuery.isPending || appointmentQuery.isPending) && (
        <LoadingSpinner label="Loading appointment details…" />
      )}

      {consultationQuery.isError && (
        <ErrorMessage
          title="Consultation unavailable"
          message={getErrorMessage(consultationQuery.error)}
          onRetry={() => void consultationQuery.refetch()}
        />
      )}

      {recommendationQuery.isError && (
        <ErrorMessage
          title="Recommendation unavailable"
          message={getErrorMessage(recommendationQuery.error)}
          onRetry={() => void recommendationQuery.refetch()}
        />
      )}

      {appointmentQuery.isError && (
        <ErrorMessage
          title="Appointment unavailable"
          message={getErrorMessage(appointmentQuery.error)}
          onRetry={() => void appointmentQuery.refetch()}
        />
      )}

      {consultation && recommendationQuery.isSuccess && appointmentQuery.isSuccess && (
        <>
          <Box sx={{ mb: 3 }}>
            <Typography variant="overline" color="primary.main" fontWeight={800}>
              Appointment Workflow
            </Typography>
            <Typography variant="h4" component="h1" fontWeight={800} letterSpacing="-0.04em">
              Appointment Booking
            </Typography>
            <Typography color="text.secondary" sx={{ mt: 0.75 }}>
              Configure appointment details for the recommended treatment.
            </Typography>
          </Box>

          {appointment ? (
            <Stack spacing={2.5}>
              <AppointmentDetails appointment={appointment} treatment={appointmentTreatment} />
              <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent="center" spacing={1.5}>
                <Button component={RouterLink} to="/consultations" variant="contained">
                  View Consultation Records
                </Button>
                <Button component={RouterLink} to="/dashboard" variant="outlined">
                  Back to Dashboard
                </Button>
              </Stack>
            </Stack>
          ) : isAlreadyBooked ? (
            <Card>
              <CardContent sx={{ p: { xs: 3, md: 5 }, textAlign: 'center', '&:last-child': { pb: { xs: 3, md: 5 } } }}>
                <CalendarMonthOutlinedIcon color="primary" sx={{ fontSize: 52 }} />
                <Typography variant="h5" component="h2" fontWeight={800} sx={{ mt: 2 }}>
                  This consultation is already booked
                </Typography>
                <Typography color="text.secondary" sx={{ mt: 1 }}>
                  The current workflow supports one appointment per consultation.
                </Typography>
                <Button component={RouterLink} to="/consultations" variant="contained" sx={{ mt: 3 }}>
                  Back to Consultation Records
                </Button>
              </CardContent>
            </Card>
          ) : recommendation === null || recommendedTreatments.length === 0 ? (
            <Card>
              <EmptyState
                title="Recommendation required"
                description="Generate a treatment recommendation before booking an appointment."
                action={(
                  <Button component={RouterLink} to={`/consultations/${id}/recommendation`} variant="contained">
                    Go to Recommendation
                  </Button>
                )}
              />
            </Card>
          ) : (
            <Grid container spacing={2.5} alignItems="flex-start">
              <Grid size={{ xs: 12, md: 8 }}>
                <Card>
                  <CardContent sx={{ p: { xs: 2.5, md: 3.5 }, '&:last-child': { pb: { xs: 2.5, md: 3.5 } } }}>
                    <Typography variant="h6" component="h2" fontWeight={800} sx={{ mb: 0.5 }}>
                      Appointment Details
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                      Select a treatment, date, time, and location.
                    </Typography>
                    <AppointmentForm
                      treatments={recommendedTreatments}
                      initialTreatmentKey={selectedTreatmentKey}
                      isSubmitting={appointmentMutation.isPending}
                      submissionError={
                        appointmentMutation.isError
                          ? getErrorMessage(appointmentMutation.error)
                          : undefined
                      }
                      onSubmit={(appointment) => appointmentMutation.mutate(appointment)}
                    />
                  </CardContent>
                </Card>
              </Grid>

              <Grid size={{ xs: 12, md: 4 }}>
                <Card>
                  <CardContent sx={{ p: 3, '&:last-child': { pb: 3 } }}>
                    <Typography variant="h6" component="h2" fontWeight={800}>Consultation</Typography>
                    <Divider sx={{ my: 2 }} />
                    <Typography variant="caption" color="text.secondary">PATIENT</Typography>
                    <Typography fontWeight={750}>{consultation.patient_name}</Typography>
                    <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2 }}>
                      PRIMARY CONCERN
                    </Typography>
                    <Typography variant="body2">{consultation.primary_concern}</Typography>
                    <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2, mb: 0.75 }}>
                      STATUS
                    </Typography>
                    <StatusChip status={consultation.status} />
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          )}
        </>
      )}
    </Box>
  )
}
