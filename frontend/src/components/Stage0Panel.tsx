import { useState } from 'react'
import ErrorMessage from './ErrorMessage'
import {
  buildStage0Context,
  validateStage0Context,
  uploadStage0Context,
  getStage0Context,
  listStage0Sources,
  resolveStage0,
  counterfactualStage0,
  policyWatchStage0,
} from '../lib/api'

export default function Stage0Panel() {
  const [lat, setLat] = useState('')
  const [lon, setLon] = useState('')
  const [contextId, setContextId] = useState('')
  const [context, setContext] = useState<unknown | null>(null)
  const [output, setOutput] = useState<unknown | null>(null)

  const [query, setQuery] = useState('')
  const [scenario, setScenario] = useState('')
  const [policy, setPolicy] = useState('')

  const [error, setError] = useState<string | null>(null)

  const build = async () => {
    try {
      setError(null)
      const res = await buildStage0Context({
        location: { lat: parseFloat(lat), lon: parseFloat(lon) },
      })
      setContextId(res.context_id)
      setContext(res.context)
      setOutput(res)
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error'
      setError(message)
    }
  }

  const validate = async () => {
    try {
      if (!context) return
      setError(null)
      setOutput(await validateStage0Context(context))
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error'
      setError(message)
    }
  }

  const upload = async () => {
    try {
      if (!contextId) return
      setError(null)
      setOutput(await uploadStage0Context(contextId))
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error'
      setError(message)
    }
  }

  const fetchCtx = async () => {
    try {
      if (!contextId) return
      setError(null)
      const res = await getStage0Context(contextId)
      setContext(res)
      setOutput(res)
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error'
      setError(message)
    }
  }

  const sources = async () => {
    try {
      setError(null)
      setOutput(await listStage0Sources())
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error'
      setError(message)
    }
  }

  const resolve = async () => {
    try {
      setError(null)
      setOutput(await resolveStage0(query))
      setQuery('')
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error'
      setError(message)
    }
  }

  const counterfactual = async () => {
    try {
      setError(null)
      setOutput(await counterfactualStage0(scenario))
      setScenario('')
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error'
      setError(message)
    }
  }

  const policyWatch = async () => {
    try {
      setError(null)
      setOutput(await policyWatchStage0(policy))
      setPolicy('')
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error'
      setError(message)
    }
  }

  return (
    <div className="p-2 border rounded mb-2">
      <h2 className="font-bold">Stage 0 (Ultra)</h2>
      <div className="space-y-2">
        <div className="flex space-x-2">
          <input
            className="border p-1 w-24"
            placeholder="lat"
            value={lat}
            onChange={e => setLat(e.target.value)}
          />
          <input
            className="border p-1 w-24"
            placeholder="lon"
            value={lon}
            onChange={e => setLon(e.target.value)}
          />
          <button className="bg-blue-500 text-white px-2 py-1" onClick={build}>
            Build Context
          </button>
          <button
            className="bg-blue-500 text-white px-2 py-1"
            onClick={validate}
          >
            Validate
          </button>
          <button
            className="bg-blue-500 text-white px-2 py-1"
            onClick={upload}
          >
            Upload
          </button>
        </div>
        <div className="flex space-x-2">
          <input
            className="border p-1 flex-1"
            placeholder="context id"
            value={contextId}
            onChange={e => setContextId(e.target.value)}
          />
          <button
            className="bg-blue-500 text-white px-2 py-1"
            onClick={fetchCtx}
          >
            Get Context
          </button>
          <button
            className="bg-blue-500 text-white px-2 py-1"
            onClick={sources}
          >
            List Sources
          </button>
        </div>
        <div className="flex space-x-2">
          <input
            className="border p-1 flex-1"
            placeholder="query"
            value={query}
            onChange={e => setQuery(e.target.value)}
          />
          <button className="bg-blue-500 text-white px-2 py-1" onClick={resolve}>
            Resolve
          </button>
        </div>
        <div className="flex space-x-2">
          <input
            className="border p-1 flex-1"
            placeholder="scenario"
            value={scenario}
            onChange={e => setScenario(e.target.value)}
          />
          <button
            className="bg-blue-500 text-white px-2 py-1"
            onClick={counterfactual}
          >
            Counterfactual
          </button>
        </div>
        <div className="flex space-x-2">
          <input
            className="border p-1 flex-1"
            placeholder="policy id"
            value={policy}
            onChange={e => setPolicy(e.target.value)}
          />
          <button
            className="bg-blue-500 text-white px-2 py-1"
            onClick={policyWatch}
          >
            Policy Watch
          </button>
        </div>
        <ErrorMessage message={error} />
        {context && (
          <pre className="mt-2 bg-gray-100 p-2 text-sm">
            {JSON.stringify(context, null, 2)}
          </pre>
        )}
        {output && (
          <pre className="mt-2 bg-gray-100 p-2 text-sm">
            {JSON.stringify(output, null, 2)}
          </pre>
        )}
      </div>
    </div>
  )
}

