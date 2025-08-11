import type { StageResult } from './StageResult'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function runStage(stage: number): Promise<StageResult> {
  const res = await fetch(`${API_BASE}/stage${stage}`)
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`)
  return res.json()
}

export async function getStagePath<T = unknown>(stage: number, path: string): Promise<StageResult<T>> {
  const res = await fetch(`${API_BASE}/stage${stage}/${path}`)
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`)
  return res.json()
}

export async function postStagePath<T = unknown>(stage: number, path: string, data: unknown): Promise<StageResult<T>> {
  const res = await fetch(`${API_BASE}/stage${stage}/${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`)
  return res.json()
}
