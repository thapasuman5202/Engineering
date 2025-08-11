import type { StageResult } from './StageResult'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init)
  if (!res.ok) throw new Error('request failed')
  return res.json()
}

export async function runStage<T = unknown>(stage: number): Promise<StageResult<T>> {
  return fetchJson(`${API_BASE}/stage${stage}`)
}

export async function getStagePath<T = unknown>(
  stage: number,
  path: string
): Promise<StageResult<T>> {
  return fetchJson(`${API_BASE}/stage${stage}/${path}`)
}

export async function postStagePath<T = unknown>(
  stage: number,
  path: string,
  data: unknown
): Promise<StageResult<T>> {
  return fetchJson(`${API_BASE}/stage${stage}/${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
}
