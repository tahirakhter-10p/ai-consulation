import RefreshRoundedIcon from '@mui/icons-material/RefreshRounded'
import { Alert, AlertTitle, Button } from '@mui/material'

interface ErrorMessageProps {
  message: string
  title?: string
  onRetry?: () => void
}

export function ErrorMessage({ message, title = 'Unable to load data', onRetry }: ErrorMessageProps) {
  return (
    <Alert
      severity="error"
      action={
        onRetry ? (
          <Button color="inherit" size="small" startIcon={<RefreshRoundedIcon />} onClick={onRetry}>
            Retry
          </Button>
        ) : undefined
      }
      sx={{ border: '1px solid', borderColor: 'error.light' }}
    >
      <AlertTitle>{title}</AlertTitle>
      {message}
    </Alert>
  )
}
