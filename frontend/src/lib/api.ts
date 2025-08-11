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

export async function getStagePath<T = unknown>(stage: number, path: string): Promise<StageResult<T>> {
  return fetchJson(`${API_BASE}/stage${stage}/${path}`)
}

export async function postStagePath<T = unknown>(stage: number, path: string, data: unknown): Promise<StageResult<T>> {
  return fetchJson(`${API_BASE}/stage${stage}/${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
}

// Stage 0 ultra endpoints -------------------------------------------------

export interface Stage0Request {
  site_name: string
  lat?: number
  lon?: number
  radius_m?: number
  boundary_geojson?: unknown
  brief?: string
  online?: boolean
  scenarios?: string[]
}

export async function buildStage0Context(req: Stage0Request): Promise<any> {
  return fetchJson(`${API_BASE}/stage0/context/build`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  })
}

export async function validateGeometry(boundary_geojson: unknown): Promise<any> {
  return fetchJson(`${API_BASE}/stage0/context/validate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ boundary_geojson }),
  })
}

export async function uploadBoundary(file: File): Promise<any> {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${API_BASE}/stage0/context/upload`, {
    method: 'POST',
    body: form,
  })
  if (!res.ok) throw new Error('upload failed')
  return res.json()
}

export async function getStage0Context(context_id: string): Promise<any> {
  return fetchJson(`${API_BASE}/stage0/context/${context_id}`)
}

export async function listStage0Sources(): Promise<any> {
  return fetchJson(`${API_BASE}/stage0/sources`)
}

export async function resolveStage0(context_id: string, patch: any): Promise<any> {
  return fetchJson(`${API_BASE}/stage0/resolve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ context_id, patch }),
  })
}

export async function counterfactualStage0(context_id: string, delta: any): Promise<any> {
  return fetchJson(`${API_BASE}/stage0/counterfactual`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ context_id, delta }),
  })
}

export async function policyWatchStage0(text?: string, url?: string): Promise<any> {
  return fetchJson(`${API_BASE}/stage0/policy/watch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, url }),
  })
}
