import ArrowForwardRoundedIcon from '@mui/icons-material/ArrowForwardRounded'
import {
  Avatar,
  Box,
  Card,
  CardContent,
  IconButton,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material'
import { useNavigate } from 'react-router-dom'

import type { ConsultationListItem } from '../../types/consultation'
import { StatusChip } from './StatusChip'

interface ConsultationTableProps {
  consultations: ConsultationListItem[]
}

function initials(name: string) {
  return name
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join('')
}

export function ConsultationTable({ consultations }: ConsultationTableProps) {
  const navigate = useNavigate()
  const openConsultation = (id: string) => navigate(`/consultations/${id}`)

  return (
    <>
      <TableContainer component={Card} sx={{ display: { xs: 'none', md: 'block' } }}>
        <Table aria-label="Consultation records">
          <TableHead>
            <TableRow>
              <TableCell>Patient Name</TableCell>
              <TableCell>Primary Concern</TableCell>
              <TableCell>Recommended Procedure</TableCell>
              <TableCell>Status</TableCell>
              <TableCell align="right" aria-label="Open consultation" />
            </TableRow>
          </TableHead>
          <TableBody>
            {consultations.map((consultation) => (
              <TableRow
                hover
                key={consultation.id}
                tabIndex={0}
                onClick={() => openConsultation(consultation.id)}
                onKeyDown={(event) => {
                  if (event.key === 'Enter' || event.key === ' ') openConsultation(consultation.id)
                }}
                sx={{ cursor: 'pointer', '&:last-child td': { borderBottom: 0 } }}
              >
                <TableCell>
                  <Stack direction="row" alignItems="center" spacing={1.5}>
                    <Avatar sx={{ width: 34, height: 34, fontSize: 13, bgcolor: 'primary.light', color: 'primary.dark' }}>
                      {initials(consultation.patient_name)}
                    </Avatar>
                    <Typography variant="body2" fontWeight={700}>{consultation.patient_name}</Typography>
                  </Stack>
                </TableCell>
                <TableCell sx={{ maxWidth: 260 }}>
                  <Typography variant="body2" noWrap title={consultation.primary_concern}>
                    {consultation.primary_concern}
                  </Typography>
                </TableCell>
                <TableCell sx={{ maxWidth: 260 }}>
                  <Typography variant="body2">{consultation.recommended_procedure}</Typography>
                </TableCell>
                <TableCell><StatusChip status={consultation.status} /></TableCell>
                <TableCell align="right">
                  <IconButton aria-label={`Open consultation for ${consultation.patient_name}`} size="small">
                    <ArrowForwardRoundedIcon fontSize="small" />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Stack spacing={2} sx={{ display: { xs: 'flex', md: 'none' } }}>
        {consultations.map((consultation) => (
          <Card key={consultation.id}>
            <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
              <Stack direction="row" justifyContent="space-between" alignItems="flex-start" gap={2}>
                <Stack direction="row" spacing={1.5} alignItems="center" minWidth={0}>
                  <Avatar sx={{ width: 38, height: 38, fontSize: 13, bgcolor: 'primary.light', color: 'primary.dark' }}>
                    {initials(consultation.patient_name)}
                  </Avatar>
                  <Box minWidth={0}>
                    <Typography fontWeight={750} noWrap>{consultation.patient_name}</Typography>
                    <StatusChip status={consultation.status} />
                  </Box>
                </Stack>
                <IconButton
                  aria-label={`Open consultation for ${consultation.patient_name}`}
                  onClick={() => openConsultation(consultation.id)}
                  color="primary"
                >
                  <ArrowForwardRoundedIcon />
                </IconButton>
              </Stack>
              <Box sx={{ mt: 2.5 }}>
                <Typography variant="caption" color="text.secondary">PRIMARY CONCERN</Typography>
                <Typography variant="body2" sx={{ mt: 0.5 }}>{consultation.primary_concern}</Typography>
              </Box>
              <Box sx={{ mt: 2 }}>
                <Typography variant="caption" color="text.secondary">RECOMMENDED PROCEDURE</Typography>
                <Typography variant="body2" sx={{ mt: 0.5 }}>{consultation.recommended_procedure}</Typography>
              </Box>
            </CardContent>
          </Card>
        ))}
      </Stack>
    </>
  )
}
