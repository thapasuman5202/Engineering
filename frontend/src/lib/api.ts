const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function runStage(stage: number) {
  const res = await fetch(`${API_BASE}/stage${stage}`)
  if (!res.ok) throw new Error('request failed')
  return res.json()
}

export async function getStagePath(stage: number, path: string) {
  const res = await fetch(`${API_BASE}/stage${stage}/${path}`)
  if (!res.ok) throw new Error('request failed')
  return res.json()
}

export async function postStagePath(stage: number, path: string, data: any) {
  const res = await fetch(`${API_BASE}/stage${stage}/${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error('request failed')
  return res.json()
}
