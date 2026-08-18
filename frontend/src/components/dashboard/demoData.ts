export interface MonthlyRevenueDemo {
  amount: number
  currency: 'USD'
  comparisonLabel: string
}

export interface ConsultationTrendDemo {
  day: string
  consultations: number
  highlighted?: boolean
}

export type ActivityKind = 'consultation' | 'appointment' | 'report' | 'intake' | 'note'

export interface RecentActivityDemo {
  id: string
  kind: ActivityKind
  title: string
  subject: string
  occurredAt: string
}

export interface ClinicalReviewDemo {
  id: string
  patientName: string
  specialty: string
  summary: string
  initials: string
}

export interface DashboardDemoData {
  monthlyRevenue: MonthlyRevenueDemo
  consultationTrends: ConsultationTrendDemo[]
  recentActivity: RecentActivityDemo[]
  pendingClinicalReviews: ClinicalReviewDemo[]
}

export const dashboardDemoData: DashboardDemoData = {
  monthlyRevenue: {
    amount: 124_500,
    currency: 'USD',
    comparisonLabel: 'Demo monthly total',
  },
  consultationTrends: [
    { day: 'Mon', consultations: 48 },
    { day: 'Tue', consultations: 76 },
    { day: 'Wed', consultations: 63 },
    { day: 'Thu', consultations: 102, highlighted: true },
    { day: 'Fri', consultations: 91, highlighted: true },
    { day: 'Sat', consultations: 116 },
    { day: 'Sun', consultations: 84 },
  ],
  recentActivity: [
    {
      id: 'activity-1',
      kind: 'consultation',
      title: 'Consultation completed',
      subject: 'Michael B.',
      occurredAt: '10 min ago',
    },
    {
      id: 'activity-2',
      kind: 'appointment',
      title: 'New appointment booked',
      subject: 'Sarah J.',
      occurredAt: '45 min ago',
    },
    {
      id: 'activity-3',
      kind: 'report',
      title: 'Diagnostic report generated',
      subject: 'Consultation record',
      occurredAt: '2 hours ago',
    },
    {
      id: 'activity-4',
      kind: 'intake',
      title: 'Patient intake submitted',
      subject: 'David W.',
      occurredAt: '3 hours ago',
    },
    {
      id: 'activity-5',
      kind: 'note',
      title: 'Clinical note updated',
      subject: 'Emma T.',
      occurredAt: 'Yesterday',
    },
  ],
  pendingClinicalReviews: [
    {
      id: 'review-1',
      patientName: 'John Doe',
      specialty: 'Cardiology',
      summary: 'AI detected minor anomalies in the latest ECG assessment.',
      initials: 'JD',
    },
    {
      id: 'review-2',
      patientName: 'Alice Smith',
      specialty: 'Neurology',
      summary: 'Preliminary assessment is ready for clinical sign-off.',
      initials: 'AS',
    },
  ],
}
