import AccessTimeOutlinedIcon from '@mui/icons-material/AccessTimeOutlined'
import CalendarMonthOutlinedIcon from '@mui/icons-material/CalendarMonthOutlined'
import LocationOnOutlinedIcon from '@mui/icons-material/LocationOnOutlined'
import PaymentsOutlinedIcon from '@mui/icons-material/PaymentsOutlined'
import {
  Alert,
  Box,
  Button,
  Chip,
  CircularProgress,
  Divider,
  Grid2 as Grid,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from '@mui/material'
import { type FormEvent, useMemo, useState } from 'react'

import type { CreateAppointmentRequest } from '../../types/appointment'
import type { RecommendedTreatment } from '../../types/recommendation'

interface AppointmentFormProps {
  treatments: RecommendedTreatment[]
  initialTreatmentKey?: string
  isSubmitting: boolean
  submissionError?: string
  onSubmit: (appointment: CreateAppointmentRequest) => void
}

function treatmentKey(treatment: RecommendedTreatment) {
  return treatment.treatment_id ?? treatment.name
}

function treatmentPrice(treatment: RecommendedTreatment) {
  if (treatment.price) return `$${Number(treatment.price).toLocaleString()}`
  if (treatment.price_min && treatment.price_max) {
    return `$${Number(treatment.price_min).toLocaleString()}–$${Number(treatment.price_max).toLocaleString()}`
  }
  return 'Not specified'
}

export function AppointmentForm({
  treatments,
  initialTreatmentKey,
  isSubmitting,
  submissionError,
  onSubmit,
}: AppointmentFormProps) {
  const initialTreatment = treatments.find((item) => treatmentKey(item) === initialTreatmentKey)
    ?? treatments[0]
  const [selectedKey, setSelectedKey] = useState(initialTreatment ? treatmentKey(initialTreatment) : '')
  const [appointmentDate, setAppointmentDate] = useState('')
  const [appointmentTime, setAppointmentTime] = useState('')
  const [location, setLocation] = useState(initialTreatment?.location ?? '')
  const [submitted, setSubmitted] = useState(false)
  const selectedTreatment = useMemo(
    () => treatments.find((item) => treatmentKey(item) === selectedKey),
    [selectedKey, treatments],
  )

  const treatmentError = submitted && !selectedTreatment
  const dateError = submitted && appointmentDate.length === 0
  const timeError = submitted && appointmentTime.length === 0
  const locationError = submitted && location.trim().length === 0

  function selectTreatment(key: string) {
    setSelectedKey(key)
    const treatment = treatments.find((item) => treatmentKey(item) === key)
    if (treatment?.location) setLocation(treatment.location)
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSubmitted(true)

    if (!selectedTreatment || !appointmentDate || !appointmentTime || !location.trim() || isSubmitting) return

    const appointmentDatetime = new Date(`${appointmentDate}T${appointmentTime}`)
    if (Number.isNaN(appointmentDatetime.getTime())) return

    onSubmit({
      ...(selectedTreatment.treatment_id
        ? { treatment_id: selectedTreatment.treatment_id }
        : { treatment: selectedTreatment.name }),
      appointment_datetime: appointmentDatetime.toISOString(),
      location: location.trim(),
    })
  }

  return (
    <Stack component="form" spacing={3} onSubmit={handleSubmit} noValidate>
      {submissionError && <Alert severity="error">{submissionError}</Alert>}

      <TextField
        select
        label="Primary treatment"
        value={selectedKey}
        onChange={(event) => selectTreatment(event.target.value)}
        error={treatmentError}
        helperText={treatmentError ? 'Select a recommended treatment.' : 'Choose from the AI recommendation.'}
        disabled={isSubmitting}
      >
        {treatments.map((treatment) => (
          <MenuItem key={treatmentKey(treatment)} value={treatmentKey(treatment)}>
            {treatment.name}
          </MenuItem>
        ))}
      </TextField>

      {selectedTreatment && (
        <Box sx={{ border: '1px solid', borderColor: 'divider', borderRadius: 2, p: 2.5, bgcolor: '#f8fafc' }}>
          <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between" gap={1}>
            <Box>
              <Typography variant="h6" fontWeight={800}>{selectedTreatment.name}</Typography>
              {selectedTreatment.specialty && (
                <Chip label={selectedTreatment.specialty} size="small" color="primary" variant="outlined" sx={{ mt: 0.75 }} />
              )}
            </Box>
            <Typography variant="h6" fontWeight={800}>{treatmentPrice(selectedTreatment)}</Typography>
          </Stack>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1.5 }}>
            {selectedTreatment.description}
          </Typography>
          <Divider sx={{ my: 2 }} />
          <Grid container spacing={2}>
            <Grid size={{ xs: 12, sm: 4 }}>
              <Stack direction="row" spacing={1} alignItems="center">
                <AccessTimeOutlinedIcon color="action" />
                <Box>
                  <Typography variant="caption" color="text.secondary">DURATION</Typography>
                  <Typography variant="body2" fontWeight={700}>
                    {selectedTreatment.duration_minutes ? `${selectedTreatment.duration_minutes} min` : 'Not specified'}
                  </Typography>
                </Box>
              </Stack>
            </Grid>
            <Grid size={{ xs: 12, sm: 4 }}>
              <Stack direction="row" spacing={1} alignItems="center">
                <PaymentsOutlinedIcon color="action" />
                <Box>
                  <Typography variant="caption" color="text.secondary">ESTIMATED COST</Typography>
                  <Typography variant="body2" fontWeight={700}>{treatmentPrice(selectedTreatment)}</Typography>
                </Box>
              </Stack>
            </Grid>
            <Grid size={{ xs: 12, sm: 4 }}>
              <Stack direction="row" spacing={1} alignItems="center">
                <LocationOnOutlinedIcon color="action" />
                <Box>
                  <Typography variant="caption" color="text.secondary">TARGET AREA</Typography>
                  <Typography variant="body2" fontWeight={700}>
                    {selectedTreatment.default_target_area ?? 'Not specified'}
                  </Typography>
                </Box>
              </Stack>
            </Grid>
          </Grid>
        </Box>
      )}

      <Grid container spacing={2}>
        <Grid size={{ xs: 12, sm: 6 }}>
          <TextField
            fullWidth
            label="Appointment date"
            type="date"
            value={appointmentDate}
            onChange={(event) => setAppointmentDate(event.target.value)}
            error={dateError}
            helperText={dateError ? 'Appointment date is required.' : ' '}
            disabled={isSubmitting}
            slotProps={{ inputLabel: { shrink: true } }}
          />
        </Grid>
        <Grid size={{ xs: 12, sm: 6 }}>
          <TextField
            fullWidth
            label="Appointment time"
            type="time"
            value={appointmentTime}
            onChange={(event) => setAppointmentTime(event.target.value)}
            error={timeError}
            helperText={timeError ? 'Appointment time is required.' : ' '}
            disabled={isSubmitting}
            slotProps={{ inputLabel: { shrink: true } }}
          />
        </Grid>
      </Grid>

      <TextField
        label="Clinic location"
        value={location}
        onChange={(event) => setLocation(event.target.value)}
        error={locationError}
        helperText={locationError ? 'Location is required.' : 'Pre-filled from the treatment catalog.'}
        disabled={isSubmitting}
        inputProps={{ maxLength: 255 }}
      />

      <Button
        type="submit"
        variant="contained"
        color="inherit"
        size="large"
        disabled={isSubmitting || !selectedTreatment}
        startIcon={isSubmitting ? <CircularProgress size={18} color="inherit" /> : <CalendarMonthOutlinedIcon />}
        sx={{ alignSelf: { xs: 'stretch', sm: 'flex-start' }, bgcolor: 'common.black', color: 'common.white', '&:hover': { bgcolor: '#20242b' } }}
      >
        {isSubmitting ? 'Booking appointment…' : 'Confirm Appointment'}
      </Button>
    </Stack>
  )
}
