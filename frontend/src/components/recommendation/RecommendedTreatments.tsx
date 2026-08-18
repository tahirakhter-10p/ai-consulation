import CheckCircleRoundedIcon from '@mui/icons-material/CheckCircleRounded'
import AccessTimeOutlinedIcon from '@mui/icons-material/AccessTimeOutlined'
import LocationOnOutlinedIcon from '@mui/icons-material/LocationOnOutlined'
import MedicalServicesOutlinedIcon from '@mui/icons-material/MedicalServicesOutlined'
import PaymentsOutlinedIcon from '@mui/icons-material/PaymentsOutlined'
import { Card, CardActionArea, CardContent, Chip, Grid2 as Grid, Stack, Typography } from '@mui/material'

import type { RecommendedTreatment } from '../../types/recommendation'

interface RecommendedTreatmentsProps {
  treatments: RecommendedTreatment[]
  selectedTreatmentKey: string
  onSelect: (treatment: RecommendedTreatment) => void
}

export function RecommendedTreatments({
  treatments,
  selectedTreatmentKey,
  onSelect,
}: RecommendedTreatmentsProps) {
  return (
    <section aria-labelledby="recommended-treatments-title">
      <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
        <MedicalServicesOutlinedIcon color="primary" />
        <Typography id="recommended-treatments-title" variant="h6" component="h2" fontWeight={800}>
          Recommended Treatments
        </Typography>
      </Stack>
      <Grid container spacing={2}>
        {treatments.map((treatment, index) => {
          const treatmentKey = treatment.treatment_id ?? treatment.name
          const selected = selectedTreatmentKey === treatmentKey
          const price = treatment.price
            ? `$${Number(treatment.price).toLocaleString()}`
            : treatment.price_min && treatment.price_max
              ? `$${Number(treatment.price_min).toLocaleString()}–$${Number(treatment.price_max).toLocaleString()}`
              : 'Not specified'

          return (
          <Grid key={treatmentKey} size={{ xs: 12, md: 6 }}>
            <Card
              sx={{
                height: '100%',
                border: '2px solid',
                borderColor: selected ? 'primary.main' : 'divider',
                bgcolor: selected ? '#f5faff' : 'background.paper',
              }}
            >
              <CardActionArea
                onClick={() => onSelect(treatment)}
                aria-pressed={selected}
                sx={{ height: '100%', alignItems: 'stretch' }}
              >
                <CardContent sx={{ p: 2.5 }}>
                  <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <Typography variant="overline" color="primary.main" fontWeight={800}>
                      Recommendation {index + 1}
                    </Typography>
                    {selected && (
                      <Stack direction="row" spacing={0.5} alignItems="center" color="primary.main">
                        <CheckCircleRoundedIcon fontSize="small" />
                        <Typography variant="caption" fontWeight={800}>Selected</Typography>
                      </Stack>
                    )}
                  </Stack>
                <Typography variant="h6" component="h3" fontWeight={800} sx={{ mt: 0.25 }}>
                  {treatment.name}
                </Typography>
                {treatment.specialty && (
                  <Chip label={treatment.specialty} size="small" color="primary" variant="outlined" sx={{ mt: 1 }} />
                )}
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1.25, lineHeight: 1.7 }}>
                  {treatment.description}
                </Typography>
                <Grid container spacing={1.5} sx={{ mt: 1.5 }}>
                  <Grid size={{ xs: 6 }}>
                    <Stack direction="row" spacing={0.75} alignItems="center">
                      <PaymentsOutlinedIcon fontSize="small" color="action" />
                      <Typography variant="body2" fontWeight={700}>{price}</Typography>
                    </Stack>
                  </Grid>
                  <Grid size={{ xs: 6 }}>
                    <Stack direction="row" spacing={0.75} alignItems="center">
                      <AccessTimeOutlinedIcon fontSize="small" color="action" />
                      <Typography variant="body2" fontWeight={700}>
                        {treatment.duration_minutes ? `${treatment.duration_minutes} min` : 'Not specified'}
                      </Typography>
                    </Stack>
                  </Grid>
                  {treatment.location && (
                    <Grid size={{ xs: 12 }}>
                      <Stack direction="row" spacing={0.75} alignItems="center">
                        <LocationOnOutlinedIcon fontSize="small" color="action" />
                        <Typography variant="body2">{treatment.location}</Typography>
                      </Stack>
                    </Grid>
                  )}
                  {treatment.default_target_area && (
                    <Grid size={{ xs: 12 }}>
                      <Typography variant="caption" color="text.secondary">TARGET AREA</Typography>
                      <Typography variant="body2" fontWeight={700}>{treatment.default_target_area}</Typography>
                    </Grid>
                  )}
                </Grid>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
          )
        })}
      </Grid>
    </section>
  )
}
