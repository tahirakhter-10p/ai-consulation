import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { alpha, createTheme, ThemeProvider } from '@mui/material/styles'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'

import App from './App'

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: 1, refetchOnWindowFocus: false } },
})
const theme = createTheme({
  palette: {
    primary: { main: '#0876d1', dark: '#055da7', light: '#e8f3fc' },
    background: { default: '#f5f7fa', paper: '#ffffff' },
    text: { primary: '#17191d', secondary: '#68717d' },
    divider: '#e4e8ed',
  },
  shape: { borderRadius: 10 },
  typography: {
    fontFamily: 'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    button: { textTransform: 'none', fontWeight: 700 },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          border: '1px solid #e4e8ed',
          boxShadow: '0 6px 20px rgba(23, 25, 29, 0.04)',
        },
      },
    },
    MuiButton: {
      defaultProps: { disableElevation: true },
      styleOverrides: { root: { minHeight: 42, borderRadius: 8 } },
    },
    MuiListItemButton: {
      styleOverrides: { root: { minHeight: 46, borderRadius: 7 } },
    },
    MuiDialog: {
      styleOverrides: {
        paper: { boxShadow: `0 24px 80px ${alpha('#17191d', 0.18)}` },
      },
    },
  },
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider theme={theme}>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </QueryClientProvider>
    </ThemeProvider>
  </StrictMode>,
)
