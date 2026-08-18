import { useMutation, useQueryClient } from '@tanstack/react-query'
import {
  Alert,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Stack,
  TextField,
  Typography,
} from '@mui/material'
import { type FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { createConsultation } from '../../api/consultations'
import type { ConsultationMessage } from '../../types/consultation'
import { getErrorMessage } from '../../utils/apiError'

interface NewConsultDialogProps {
  open: boolean
  onClose: () => void
}

export function NewConsultDialog({ open, onClose }: NewConsultDialogProps) {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [patientName, setPatientName] = useState('')
  const [primaryConcern, setPrimaryConcern] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const mutation = useMutation({
    mutationFn: createConsultation,
    onSuccess: (consultation) => {
      queryClient.setQueryData(['consultation', consultation.id], consultation)
      queryClient.setQueryData<ConsultationMessage[]>(['consultation-messages', consultation.id], [])
      void queryClient.invalidateQueries({ queryKey: ['dashboard'] })
      void queryClient.invalidateQueries({ queryKey: ['consultations'] })
      handleClose()
      navigate(`/consultations/${consultation.id}`, {
        state: { initializeMessage: consultation.primary_concern },
      })
    },
  })

  function handleClose() {
    setPatientName('')
    setPrimaryConcern('')
    setSubmitted(false)
    mutation.reset()
    onClose()
  }

  const nameError = submitted && patientName.trim().length === 0
  const concernError = submitted && primaryConcern.trim().length === 0

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSubmitted(true)

    if (!patientName.trim() || !primaryConcern.trim()) return

    mutation.mutate({
      patient_name: patientName.trim(),
      primary_concern: primaryConcern.trim(),
    })
  }

  return (
    <Dialog open={open} onClose={mutation.isPending ? undefined : handleClose} fullWidth maxWidth="sm">
      <DialogTitle sx={{ pb: 1 }}>New Consultation</DialogTitle>
      <DialogContent>
        <Typography color="text.secondary" sx={{ mb: 3 }}>
          Enter the patient details to begin an AI-assisted consultation.
        </Typography>
        <Stack component="form" id="new-consult-form" spacing={2.5} onSubmit={handleSubmit} noValidate>
          {mutation.isError && <Alert severity="error">{getErrorMessage(mutation.error)}</Alert>}
          <TextField
            label="Patient name"
            value={patientName}
            onChange={(event) => setPatientName(event.target.value)}
            error={nameError}
            helperText={nameError ? 'Patient name is required.' : ' '}
            autoFocus
            disabled={mutation.isPending}
            inputProps={{ maxLength: 255 }}
          />
          <TextField
            label="Primary concern"
            value={primaryConcern}
            onChange={(event) => setPrimaryConcern(event.target.value)}
            error={concernError}
            helperText={concernError ? 'Primary concern is required.' : ' '}
            multiline
            minRows={3}
            disabled={mutation.isPending}
          />
        </Stack>
      </DialogContent>
      <DialogActions sx={{ px: 3, pb: 3 }}>
        <Button onClick={handleClose} disabled={mutation.isPending} color="inherit">
          Cancel
        </Button>
        <Button type="submit" form="new-consult-form" variant="contained" disabled={mutation.isPending}>
          {mutation.isPending ? 'Creating…' : 'Start Consultation'}
        </Button>
      </DialogActions>
    </Dialog>
  )
}
