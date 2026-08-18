import { Navigate, Route, Routes } from 'react-router-dom'

import { AppLayout } from '../layouts/AppLayout'
import { AppointmentPage } from '../pages/AppointmentPage'
import { ConsultationDetailPage } from '../pages/ConsultationDetailPage'
import { ConsultationListPage } from '../pages/ConsultationListPage'
import { DashboardPage } from '../pages/DashboardPage'
import { RecommendationPage } from '../pages/RecommendationPage'

export function AppRoutes() {
  return (
    <AppLayout>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/consultations" element={<ConsultationListPage />} />
        <Route path="/consultations/:id" element={<ConsultationDetailPage />} />
        <Route path="/consultations/:id/recommendation" element={<RecommendationPage />} />
        <Route path="/consultations/:id/appointment" element={<AppointmentPage />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </AppLayout>
  )
}
