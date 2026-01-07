const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:3001"

interface ApiResponse<T = any> {
  success: boolean
  data: T
}

export const predictSingle = async (sequence: string, model: string): Promise<ApiResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/predictions/single`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ sequence, model }),
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.message || `Prediction failed: ${response.statusText}`)
  }

  const data = await response.json()
  return data
}

export const predictBatch = async (sequences: string[], model: string): Promise<ApiResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/predictions/batch`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ sequences, model }),
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.message || `Batch prediction failed: ${response.statusText}`)
  }

  const data = await response.json()
  return data
}

export const analyzeFeatures = async (sequence: string): Promise<ApiResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/analysis/features`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ sequence }),
  })

  if (!response.ok) {
    throw new Error("Feature analysis failed")
  }

  return response.json()
}

export const getHistory = async (limit = 20): Promise<ApiResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/history?limit=${limit}`)

  if (!response.ok) {
    throw new Error("Failed to fetch history")
  }

  return response.json()
}

export const getStats = async (): Promise<ApiResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/history/stats`)

  if (!response.ok) {
    throw new Error("Failed to fetch stats")
  }

  return response.json()
}
