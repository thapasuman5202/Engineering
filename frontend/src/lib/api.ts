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

// Stage 0 ultra endpoints -------------------------------------------------

export interface Stage0Request {
  location: { lat: number; lon: number }
  climate_scenario?: string
  lineage?: unknown
}

export interface BuildContextResponse {
  context_id: string
  context: unknown
}

export interface ValidateContextResponse {
  valid: boolean
  errors?: string[]
}

export interface UploadContextResponse {
  uploaded: boolean
}

export interface ResolveResponse {
  result: string
}

export interface CounterfactualResponse {
  description: string
}

export interface PolicyWatchResponse {
  status: string
}

export async function buildStage0Context(
  req: Stage0Request
): Promise<BuildContextResponse> {
  return fetchJson(`${API_BASE}/stage0/context/build`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  })
}

export async function validateStage0Context(
  context: unknown
): Promise<ValidateContextResponse> {
  return fetchJson(`${API_BASE}/stage0/context/validate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ context }),
  })
}

export async function uploadStage0Context(
  context_id: string
): Promise<UploadContextResponse> {
  return fetchJson(`${API_BASE}/stage0/context/upload`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ context_id }),
  })
}

export async function getStage0Context(context_id: string): Promise<unknown> {
  return fetchJson(`${API_BASE}/stage0/context/${context_id}`)
}

export async function listStage0Sources(): Promise<string[]> {
  return fetchJson(`${API_BASE}/stage0/sources`)
}

export async function resolveStage0(query: string): Promise<ResolveResponse> {
  return fetchJson(`${API_BASE}/stage0/resolve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  })
}

export async function counterfactualStage0(
  scenario: string
): Promise<CounterfactualResponse> {
  return fetchJson(`${API_BASE}/stage0/counterfactual`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ scenario }),
  })
}

export async function policyWatchStage0(
  policy_id: string
): Promise<PolicyWatchResponse> {
  return fetchJson(`${API_BASE}/stage0/policy/watch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ policy_id }),
  })
}
