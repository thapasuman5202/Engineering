import type { StageResult } from './StageResult'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function fetchJson<T>(
  input: RequestInfo | URL,
  init?: RequestInit
): Promise<T> {
  const res = await fetch(input, init)
  if (!res.ok) {
    const message = await res.text()
    throw new Error(`${res.status}: ${message}`)
  }
  return res.json() as Promise<T>
}

export function runStage(stage: number): Promise<StageResult> {
  return fetchJson<StageResult>(`${API_BASE}/stage${stage}`)
}

export function getStagePath(stage: number, path: string): Promise<StageResult> {
  return fetchJson<StageResult>(`${API_BASE}/stage${stage}/${path}`)
}

export function postStagePath(
  stage: number,
  path: string,
  data: unknown
): Promise<StageResult> {
  return fetchJson<StageResult>(`${API_BASE}/stage${stage}/${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
}
