import MenuRoundedIcon from '@mui/icons-material/MenuRounded'
import { AppBar, IconButton, Toolbar, Typography } from '@mui/material'
import { useLocation } from 'react-router-dom'

interface HeaderProps {
  onMenuClick: () => void
}

function getPageTitle(pathname: string) {
  if (pathname === '/dashboard') return 'Overview'
  if (pathname === '/consultations') return 'Consultation Records'
  if (pathname.endsWith('/recommendation')) return 'Consultation Recommendation'
  if (pathname.endsWith('/appointment')) return 'Appointment Booking'
  if (pathname.startsWith('/consultations/')) return 'Consultation Detail'
  return 'AI Consultation Platform'
}

export function Header({ onMenuClick }: HeaderProps) {
  const location = useLocation()

  return (
    <AppBar
      position="fixed"
      color="inherit"
      elevation={0}
      sx={{
        display: { xs: 'block', sm: 'none' },
        borderBottom: '1px solid',
        borderColor: 'divider',
        width: '100%',
      }}
    >
      <Toolbar sx={{ minHeight: { xs: 64, md: 72 } }}>
        <IconButton
          edge="start"
          aria-label="Open navigation"
          onClick={onMenuClick}
          sx={{ mr: 1.5 }}
        >
          <MenuRoundedIcon />
        </IconButton>
        <Typography variant="h5" component="p" fontWeight={750} letterSpacing="-0.025em">
          {getPageTitle(location.pathname)}
        </Typography>
      </Toolbar>
    </AppBar>
  )
}
