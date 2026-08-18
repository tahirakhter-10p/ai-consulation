import AssessmentRoundedIcon from '@mui/icons-material/AssessmentRounded'
import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { StatisticsCard } from '../../src/components/dashboard/StatisticsCard'

describe('StatisticsCard', () => {
  it('renders the supplied label, value, and icon', () => {
    render(
      <StatisticsCard
        label="Total consultations"
        value="24"
        icon={<AssessmentRoundedIcon data-testid="statistics-icon" />}
        accentColor="#075ca8"
        iconBackground="#e5f0ff"
      />,
    )

    expect(screen.getByText('Total consultations')).toBeInTheDocument()
    expect(screen.getByText('24')).toBeInTheDocument()
    expect(screen.getByTestId('statistics-icon')).toBeInTheDocument()
  })
})
