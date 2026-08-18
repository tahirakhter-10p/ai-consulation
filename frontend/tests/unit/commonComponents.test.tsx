import { Button } from '@mui/material'
import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

import { EmptyState } from '../../src/components/common/EmptyState'
import { ErrorMessage } from '../../src/components/common/ErrorMessage'
import { StatusChip } from '../../src/components/consultation/StatusChip'

describe('EmptyState', () => {
  it('renders its content and optional action', () => {
    render(
      <EmptyState
        title="No consultations"
        description="Start a consultation to see it here."
        action={<Button>Start consultation</Button>}
      />,
    )

    expect(screen.getByRole('heading', { name: 'No consultations' })).toBeInTheDocument()
    expect(screen.getByText('Start a consultation to see it here.')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Start consultation' })).toBeInTheDocument()
  })

  it('does not render an action container when no action is provided', () => {
    render(<EmptyState title="No results" description="Change the active filters." />)

    expect(screen.queryByRole('button')).not.toBeInTheDocument()
  })
})

describe('ErrorMessage', () => {
  it('uses the default title and invokes retry', () => {
    const onRetry = vi.fn()
    render(<ErrorMessage message="The request failed." onRetry={onRetry} />)

    expect(screen.getByText('Unable to load data')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: /retry/i }))
    expect(onRetry).toHaveBeenCalledOnce()
  })

  it('supports a custom title without a retry action', () => {
    render(<ErrorMessage title="Booking failed" message="Choose another time." />)

    expect(screen.getByText('Booking failed')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /retry/i })).not.toBeInTheDocument()
  })
})

describe('StatusChip', () => {
  it.each(['Pending', 'Booked', 'Completed'] as const)('renders the %s state', (status) => {
    render(<StatusChip status={status} />)

    expect(screen.getByText(status)).toBeInTheDocument()
  })
})
