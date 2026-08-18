import AddRoundedIcon from '@mui/icons-material/AddRounded'
import ArchiveOutlinedIcon from '@mui/icons-material/ArchiveOutlined'
import AutoAwesomeOutlinedIcon from '@mui/icons-material/AutoAwesomeOutlined'
import DashboardOutlinedIcon from '@mui/icons-material/DashboardOutlined'
import ForumOutlinedIcon from '@mui/icons-material/ForumOutlined'
import HelpOutlineRoundedIcon from '@mui/icons-material/HelpOutlineRounded'
import LogoutRoundedIcon from '@mui/icons-material/LogoutRounded'
import MedicalServicesRoundedIcon from '@mui/icons-material/MedicalServicesRounded'
import PeopleAltOutlinedIcon from '@mui/icons-material/PeopleAltOutlined'
import {
  Box,
  Button,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
} from '@mui/material'
import { NavLink } from 'react-router-dom'

export const sidebarWidth = 232

interface SidebarProps {
  mobileOpen: boolean
  onMobileClose: () => void
  onNewConsult: () => void
}

const navigation = [
  { label: 'Dashboard', path: '/dashboard', icon: <DashboardOutlinedIcon /> },
  { label: 'Consultation Records', path: '/consultations', icon: <ForumOutlinedIcon /> },
]

const visualNavigation = [
  { label: 'Patients', icon: <PeopleAltOutlinedIcon /> },
  { label: 'AI Insights', icon: <AutoAwesomeOutlinedIcon /> },
  { label: 'Archive', icon: <ArchiveOutlinedIcon /> },
]

const utilityNavigation = [
  { label: 'Support', icon: <HelpOutlineRoundedIcon /> },
  { label: 'Sign Out', icon: <LogoutRoundedIcon /> },
]

export function Sidebar({ mobileOpen, onMobileClose, onNewConsult }: SidebarProps) {
  const content = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column', px: 2, py: 2.5 }}>
      <Box sx={{ px: 0.75, mb: 3.5 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.25 }}>
          <Box
            sx={{
              width: 38,
              height: 38,
              display: 'grid',
              placeItems: 'center',
              borderRadius: 2,
              bgcolor: 'primary.main',
              color: 'common.white',
              boxShadow: '0 6px 16px rgba(8, 118, 209, 0.2)',
            }}
          >
            <MedicalServicesRoundedIcon fontSize="small" />
          </Box>
          <Box>
            <Typography variant="subtitle1" fontWeight={850} color="primary.main" letterSpacing="-0.03em">
              AI Consult
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: -0.25, fontSize: '0.64rem', letterSpacing: '0.055em' }}>
              CLINICAL INTELLIGENCE
            </Typography>
          </Box>
        </Box>
      </Box>

      <Button
        variant="contained"
        color="inherit"
        startIcon={<AddRoundedIcon />}
        onClick={() => {
          onNewConsult()
          onMobileClose()
        }}
        fullWidth
        sx={{ mb: 3.25, bgcolor: 'common.black', color: 'common.white', '&:hover': { bgcolor: '#20242b' } }}
      >
        New Consult
      </Button>

      <Typography variant="caption" color="text.secondary" fontWeight={800} sx={{ px: 1.25, mb: 1, letterSpacing: '0.08em' }}>
        WORKSPACE
      </Typography>
      <List aria-label="Application navigation" disablePadding>
        {navigation.map((item) => (
          <ListItemButton
            key={item.path}
            component={NavLink}
            to={item.path}
            end={item.path === '/dashboard'}
            onClick={onMobileClose}
            sx={{
              mb: 0.75,
              px: 1.25,
              color: 'text.secondary',
              '&.active': {
                bgcolor: 'primary.main',
                color: 'common.white',
                '& .MuiListItemIcon-root': { color: 'inherit' },
                '&:hover': { bgcolor: 'primary.dark' },
              },
              '&:hover': { bgcolor: '#eaf3fb', color: 'text.primary' },
            }}
          >
            <ListItemIcon sx={{ minWidth: 40 }}>{item.icon}</ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItemButton>
        ))}
        {visualNavigation.map((item) => (
          <ListItemButton
            key={item.label}
            aria-disabled="true"
            onClick={(event) => event.preventDefault()}
            sx={{
              mb: 0.75,
              px: 1.25,
              color: 'text.secondary',
              cursor: 'default',
              '&:hover': { bgcolor: 'transparent', color: 'text.secondary' },
            }}
          >
            <ListItemIcon sx={{ minWidth: 40, color: 'inherit' }}>{item.icon}</ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItemButton>
        ))}
      </List>

      <Box sx={{ flexGrow: 1 }} />
      <List aria-label="Utility navigation" disablePadding>
        {utilityNavigation.map((item) => (
          <ListItemButton
            key={item.label}
            aria-disabled="true"
            onClick={(event) => event.preventDefault()}
            sx={{
              mb: 0.25,
              px: 1.25,
              color: 'text.secondary',
              cursor: 'default',
              '&:hover': { bgcolor: 'transparent', color: 'text.secondary' },
            }}
          >
            <ListItemIcon sx={{ minWidth: 40, color: 'inherit' }}>{item.icon}</ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItemButton>
        ))}
      </List>
    </Box>
  )

  return (
    <Box component="nav" sx={{ width: { sm: sidebarWidth }, flexShrink: { sm: 0 } }}>
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={onMobileClose}
        ModalProps={{ keepMounted: true }}
        sx={{
          display: { xs: 'block', sm: 'none' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: sidebarWidth },
        }}
      >
        {content}
      </Drawer>
      <Drawer
        variant="permanent"
        open
        sx={{
          display: { xs: 'none', sm: 'block' },
          '& .MuiDrawer-paper': {
            boxSizing: 'border-box',
            width: sidebarWidth,
            borderRightColor: 'divider',
            bgcolor: '#fbfcfe',
          },
        }}
      >
        {content}
      </Drawer>
    </Box>
  )
}
