import SearchRoundedIcon from '@mui/icons-material/SearchRounded'
import { useQuery } from '@tanstack/react-query'
import {
  Box,
  Button,
  Card,
  InputAdornment,
  LinearProgress,
  Stack,
  TextField,
  Typography,
} from '@mui/material'
import { useEffect, useState } from 'react'

import { getConsultations } from '../api/consultations'
import { EmptyState } from '../components/common/EmptyState'
import { ErrorMessage } from '../components/common/ErrorMessage'
import { LoadingSpinner } from '../components/common/LoadingSpinner'
import { ConsultationTable } from '../components/consultation/ConsultationTable'
import type { ConsultationStatus } from '../types/consultation'
import { getErrorMessage } from '../utils/apiError'

type StatusFilter = 'All' | ConsultationStatus

const statusFilters: StatusFilter[] = ['All', 'Pending', 'Booked', 'Completed']

export function ConsultationListPage() {
  const [search, setSearch] = useState('')
  const [debouncedSearch, setDebouncedSearch] = useState('')
  const [status, setStatus] = useState<StatusFilter>('All')

  useEffect(() => {
    const timer = window.setTimeout(() => setDebouncedSearch(search.trim()), 350)
    return () => window.clearTimeout(timer)
  }, [search])

  const consultationsQuery = useQuery({
    queryKey: ['consultations', { search: debouncedSearch, status }],
    queryFn: () =>
      getConsultations({
        search: debouncedSearch || undefined,
        status: status === 'All' ? undefined : status,
      }),
    placeholderData: (previousData) => previousData,
  })

  const hasFilters = Boolean(debouncedSearch) || status !== 'All'

  return (
    <Box sx={{ maxWidth: 1180, mx: 'auto', pt: { xs: 3, md: 5 } }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" fontWeight={800} letterSpacing="-0.04em">
          Consultation Records
        </Typography>
        <Typography color="text.secondary" sx={{ mt: 0.75 }}>
          Review and manage historical patient consultations and AI-assisted recommendations.
        </Typography>
      </Box>

      <Stack
        direction={{ xs: 'column', md: 'row' }}
        alignItems={{ xs: 'stretch', md: 'center' }}
        justifyContent="space-between"
        gap={2}
        sx={{ mb: 2.5 }}
      >
        <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap aria-label="Filter by status">
          {statusFilters.map((filter) => (
            <Button
              key={filter}
              size="small"
              variant={status === filter ? 'contained' : 'outlined'}
              color={status === filter ? 'inherit' : 'primary'}
              aria-pressed={status === filter}
              onClick={() => setStatus(filter)}
              sx={status === filter ? {
                bgcolor: 'common.black',
                color: 'common.white',
                '&:hover': { bgcolor: '#20242b' },
              } : undefined}
            >
              {filter}
            </Button>
          ))}
        </Stack>

        <TextField
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search patient name"
          aria-label="Search consultations by patient name"
          size="small"
          sx={{ width: { xs: '100%', md: 300 }, bgcolor: 'background.paper' }}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start"><SearchRoundedIcon fontSize="small" /></InputAdornment>
              ),
            },
          }}
        />
      </Stack>

      {consultationsQuery.isFetching && !consultationsQuery.isPending && (
        <LinearProgress aria-label="Updating consultation records" sx={{ mb: 1, borderRadius: 1 }} />
      )}

      {consultationsQuery.isPending && <LoadingSpinner label="Loading consultation records…" />}

      {consultationsQuery.isError && (
        <ErrorMessage
          title="Consultation records unavailable"
          message={getErrorMessage(consultationsQuery.error)}
          onRetry={() => void consultationsQuery.refetch()}
        />
      )}

      {consultationsQuery.data?.length === 0 && (
        <Card>
          <EmptyState
            title={hasFilters ? 'No matching consultations' : 'No consultations yet'}
            description={
              hasFilters
                ? 'Try a different patient name or status filter.'
                : 'Create a new consultation to begin the patient workflow.'
            }
          />
        </Card>
      )}

      {consultationsQuery.data && consultationsQuery.data.length > 0 && (
        <ConsultationTable consultations={consultationsQuery.data} />
      )}
    </Box>
  )
}
