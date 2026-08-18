import ArrowBackRoundedIcon from '@mui/icons-material/ArrowBackRounded'
import AutoAwesomeRoundedIcon from '@mui/icons-material/AutoAwesomeRounded'
import CalendarMonthOutlinedIcon from '@mui/icons-material/CalendarMonthOutlined'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Alert, Box, Button, Card, CircularProgress, Grid2 as Grid, Stack, Typography } from '@mui/material'
import { useEffect, useRef, useState } from 'react'
import { Link as RouterLink, Navigate, useLocation, useNavigate, useParams } from 'react-router-dom'

import { getConsultation } from '../api/consultations'
import { generateRecommendation, getRecommendation } from '../api/recommendations'
import { EmptyState } from '../components/common/EmptyState'
import { ErrorMessage } from '../components/common/ErrorMessage'
import { LoadingSpinner } from '../components/common/LoadingSpinner'
import { StatusChip } from '../components/consultation/StatusChip'
import { AIReasoningPanel } from '../components/recommendation/AIReasoningPanel'
import { PatientSummaryCard } from '../components/recommendation/PatientSummaryCard'
import { RecommendedTreatments } from '../components/recommendation/RecommendedTreatments'
import type { Recommendation } from '../types/recommendation'
import { getErrorMessage } from '../utils/apiError'

export function RecommendationPage() {
  const { id } = useParams<{ id: string }>()
  const location = useLocation()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const automaticGenerationStartedRef = useRef(false)
  const [selectedTreatmentKey, setSelectedTreatmentKey] = useState('')

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

  const generateMutation = useMutation({
    mutationFn: () => generateRecommendation(id!),
    onSuccess: (recommendation) => {
      queryClient.setQueryData<Recommendation>(['recommendation', id], recommendation)
      void queryClient.invalidateQueries({ queryKey: ['consultations'] })
    },
  })

  const autoGenerate = (location.state as { autoGenerate?: boolean } | null)?.autoGenerate
  useEffect(() => {
    if (
      !autoGenerate
      || recommendationQuery.data !== null
      || automaticGenerationStartedRef.current
    ) return

    automaticGenerationStartedRef.current = true
    navigate(location.pathname, { replace: true, state: null })
    generateMutation.mutate()
  }, [autoGenerate, generateMutation, location.pathname, navigate, recommendationQuery.data])

  if (!id) {
    return (
      <Box sx={{ pt: 5 }}>
        <ErrorMessage title="Invalid consultation" message="No consultation ID was provided." />
      </Box>
    )
  }

  if (consultationQuery.data?.status === 'Booked') {
    return <Navigate to={`/consultations/${id}/appointment`} replace />
  }

  const recommendation = recommendationQuery.data
  const displayedTreatments = recommendation?.recommended_treatments.slice(0, 2) ?? []
  const effectiveSelectedTreatmentKey = selectedTreatmentKey
    || displayedTreatments[0]?.treatment_id
    || displayedTreatments[0]?.name
    || ''

  return (
    <Box sx={{ maxWidth: 1100, mx: 'auto', pt: { xs: 3, md: 4 }, pb: 4 }}>
      <Button
        component={RouterLink}
        to={`/consultations/${id}`}
        color="inherit"
        startIcon={<ArrowBackRoundedIcon />}
        sx={{ mb: 2 }}
      >
        Back to Consultation
      </Button>

      {consultationQuery.isPending && <LoadingSpinner label="Loading consultation…" />}
      {consultationQuery.isError && (
        <ErrorMessage
          title="Consultation unavailable"
          message={getErrorMessage(consultationQuery.error)}
          onRetry={() => void consultationQuery.refetch()}
        />
      )}

      {consultationQuery.data && (
        <>
          <Card sx={{ mb: 3 }}>
            <Stack
              direction={{ xs: 'column', sm: 'row' }}
              alignItems={{ xs: 'flex-start', sm: 'center' }}
              justifyContent="space-between"
              gap={2}
              sx={{ p: 3 }}
            >
              <Box>
                <Typography variant="overline" color="primary.main" fontWeight={800}>
                  Consultation Recommendation
                </Typography>
                <Stack direction="row" spacing={1.5} alignItems="center" flexWrap="wrap" useFlexGap>
                  <Typography variant="h4" component="h1" fontWeight={800} letterSpacing="-0.035em">
                    {consultationQuery.data.patient_name}
                  </Typography>
                  <StatusChip status={consultationQuery.data.status} />
                </Stack>
                <Typography color="text.secondary" sx={{ mt: 1 }}>
                  <Box component="span" color="text.primary" fontWeight={700}>Primary concern: </Box>
                  {consultationQuery.data.primary_concern}
                </Typography>
              </Box>
              {recommendation && (
                <Button
                  component={RouterLink}
                  to={`/consultations/${id}/appointment`}
                  state={{ selectedTreatmentKey: effectiveSelectedTreatmentKey }}
                  variant="contained"
                  color="inherit"
                  startIcon={<CalendarMonthOutlinedIcon />}
                  sx={{ bgcolor: 'common.black', color: 'common.white', '&:hover': { bgcolor: '#20242b' } }}
                >
                  Book Appointment
                </Button>
              )}
            </Stack>
          </Card>

          {recommendationQuery.isPending && <LoadingSpinner label="Loading recommendation…" />}

          {recommendationQuery.isError && (
            <ErrorMessage
              title="Recommendation unavailable"
              message={getErrorMessage(recommendationQuery.error)}
              onRetry={() => void recommendationQuery.refetch()}
            />
          )}

          {recommendation === null && (
            <Card>
              <EmptyState
                title="No recommendation has been generated yet"
                description="Generate a structured recommendation from the saved consultation conversation."
              />
              <Stack alignItems="center" sx={{ px: 3, pb: 4 }}>
                {generateMutation.isError && (
                  <Alert severity="error" sx={{ width: '100%', maxWidth: 600, mb: 2 }}>
                    {getErrorMessage(generateMutation.error)}
                  </Alert>
                )}
                <Button
                  variant="contained"
                  startIcon={
                    generateMutation.isPending
                      ? <CircularProgress size={18} color="inherit" />
                      : <AutoAwesomeRoundedIcon />
                  }
                  disabled={generateMutation.isPending}
                  onClick={() => generateMutation.mutate()}
                >
                  {generateMutation.isPending ? 'Generating recommendation…' : 'Generate Recommendation'}
                </Button>
              </Stack>
            </Card>
          )}

          {recommendation && (
            <Stack spacing={3}>
              <Grid container spacing={2.5}>
                <Grid size={{ xs: 12, md: recommendation.ai_reasoning ? 7 : 12 }}>
                  <PatientSummaryCard summary={recommendation.patient_summary} />
                </Grid>
                {recommendation.ai_reasoning && (
                  <Grid size={{ xs: 12, md: 5 }}>
                    <AIReasoningPanel reasoning={recommendation.ai_reasoning} />
                  </Grid>
                )}
              </Grid>
              <RecommendedTreatments
                treatments={displayedTreatments}
                selectedTreatmentKey={effectiveSelectedTreatmentKey}
                onSelect={(treatment) => setSelectedTreatmentKey(treatment.treatment_id ?? treatment.name)}
              />
              <Card sx={{ p: 3, textAlign: 'center', bgcolor: '#f8f9fb' }}>
                <Typography variant="h6" fontWeight={800}>Next Step</Typography>
                <Typography color="text.secondary" sx={{ mt: 0.5, mb: 2 }}>
                  Review the recommendation, then continue when you are ready to arrange an appointment.
                </Typography>
                <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent="center" spacing={1.5}>
                  <Button component={RouterLink} to={`/consultations/${id}`} variant="outlined" color="inherit">
                    Return to Consultation
                  </Button>
                  <Button
                    component={RouterLink}
                    to={`/consultations/${id}/appointment`}
                    state={{ selectedTreatmentKey: effectiveSelectedTreatmentKey }}
                    variant="contained"
                    color="inherit"
                    startIcon={<CalendarMonthOutlinedIcon />}
                    sx={{ bgcolor: 'common.black', color: 'common.white', '&:hover': { bgcolor: '#20242b' } }}
                  >
                    Book Appointment
                  </Button>
                </Stack>
              </Card>
            </Stack>
          )}
        </>
      )}
    </Box>
  )
}
