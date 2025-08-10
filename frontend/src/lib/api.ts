const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function runStage(stage: number) {
  const res = await fetch(`${API_BASE}/stage${stage}`)
  if (!res.ok) throw new Error('request failed')
  return res.json()
}
