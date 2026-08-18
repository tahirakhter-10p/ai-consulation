import { Box, CssBaseline, Toolbar } from '@mui/material'
import { type PropsWithChildren, useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

import { Header } from '../components/common/Header'
import { Sidebar, sidebarWidth } from '../components/common/Sidebar'
import { NewConsultDialog } from '../components/consultation/NewConsultDialog'

export function AppLayout({ children }: PropsWithChildren) {
  const [mobileOpen, setMobileOpen] = useState(false)
  const [newConsultOpen, setNewConsultOpen] = useState(false)
  const location = useLocation()
  const navigate = useNavigate()

  useEffect(() => {
    if (new URLSearchParams(location.search).get('newConsult') === 'true') {
      setNewConsultOpen(true)
    }
  }, [location.search])

  function closeNewConsult() {
    setNewConsultOpen(false)
    const search = new URLSearchParams(location.search)
    if (search.has('newConsult')) {
      search.delete('newConsult')
      navigate({ pathname: location.pathname, search: search.toString() }, { replace: true })
    }
  }

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
      <CssBaseline />
      <Header onMenuClick={() => setMobileOpen(true)} />
      <Sidebar
        mobileOpen={mobileOpen}
        onMobileClose={() => setMobileOpen(false)}
        onNewConsult={() => setNewConsultOpen(true)}
      />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          width: { sm: `calc(100% - ${sidebarWidth}px)` },
          minWidth: 0,
          px: { xs: 2, sm: 3, lg: 4.5 },
          pb: 5,
        }}
      >
        <Toolbar sx={{ display: { xs: 'block', sm: 'none' } }} />
        {children}
      </Box>
      <NewConsultDialog open={newConsultOpen} onClose={closeNewConsult} />
    </Box>
  )
}
