export interface RecommendedTreatment {
  treatment_id: string | null
  name: string
  specialty: string | null
  description: string
  price: string | null
  price_min: string | null
  price_max: string | null
  duration_minutes: number | null
  location: string | null
  default_target_area: string | null
  priority: number | null
}

export interface Recommendation {
  patient_summary: string
  recommended_treatments: RecommendedTreatment[]
  ai_reasoning: string | null
}
