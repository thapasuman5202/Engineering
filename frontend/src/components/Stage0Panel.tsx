import { useState } from 'react'
import {
  buildStage0Context,
  validateGeometry,
  uploadBoundary,
  getStage0Context,
  counterfactualStage0,
  resolveStage0,
} from '../lib/api'
import ErrorMessage from './ErrorMessage'

export default function Stage0Panel() {
  const [siteName, setSiteName] = useState('')
  const [lat, setLat] = useState('')
  const [lon, setLon] = useState('')
  const [radius, setRadius] = useState('500')
  const [boundary, setBoundary] = useState('')
  const [brief, setBrief] = useState('')
  const [online, setOnline] = useState(false)
  const [scenarios, setScenarios] = useState<string[]>(['baseline'])

  const [context, setContext] = useState<any | null>(null)
  const [contextId, setContextId] = useState('')
  const [output, setOutput] = useState<any | null>(null)
  const [error, setError] = useState<string | null>(null)

  const toggleScenario = (s: string) => {
    setScenarios(prev =>
      prev.includes(s) ? prev.filter(x => x !== s) : [...prev, s]
    )
  }

  const validate = async () => {
    try {
      setError(null)
      const gj = JSON.parse(boundary)
      setOutput(await validateGeometry(gj))
    } catch (e) {
      setError('invalid geojson')
    }
  }

  const upload = async (files: FileList | null) => {
    if (!files || files.length === 0) return
    try {
      const res = await uploadBoundary(files[0])
      setBoundary(JSON.stringify(res.boundary_geojson, null, 2))
    } catch (e) {
      setError('upload failed')
    }
  }

  const build = async () => {
    try {
      setError(null)
      const req: any = {
        site_name: siteName,
        brief,
        online,
        scenarios,
      }
      if (boundary.trim()) req.boundary_geojson = JSON.parse(boundary)
      else {
        req.lat = parseFloat(lat)
        req.lon = parseFloat(lon)
        req.radius_m = parseInt(radius)
      }
      const res = await buildStage0Context(req)
      setContext(res)
      setContextId(res.context_id)
    } catch (e) {
      setError('build failed')
    }
  }

  const counterfactual = async () => {
    if (!contextId) return
    try {
      setOutput(await counterfactualStage0(contextId, { greenspace_pct: 0.1 }))
    } catch (e) {
      setError('counterfactual failed')
    }
  }

  const resolve = async () => {
    if (!contextId) return
    try {
      const res = await resolveStage0(contextId, {
        constraints: ['manual override'],
      })
      setContext(res)
    } catch (e) {
      setError('resolve failed')
    }
  }

  const copyId = async () => {
    if (contextId) await navigator.clipboard.writeText(contextId)
  }

  const loadContext = async () => {
    if (!contextId) return
    setContext(await getStage0Context(contextId))
  }

  return (
    <div className="p-2 border rounded mb-2">
      <h2 className="font-bold mb-2">Stage 0 (Ultra)</h2>
      <div className="space-y-2">
        <input
          className="border p-1 w-full"
          placeholder="Site Name"
          value={siteName}
          onChange={e => setSiteName(e.target.value)}
        />
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
          <input
            className="border p-1 w-24"
            placeholder="radius m"
            value={radius}
            onChange={e => setRadius(e.target.value)}
          />
        </div>
        <textarea
          className="border p-1 w-full h-24"
          placeholder="boundary geojson"
          value={boundary}
          onChange={e => setBoundary(e.target.value)}
        />
        <input type="file" onChange={e => upload(e.target.files)} />
        <input
          className="border p-1 w-full"
          placeholder="brief"
          value={brief}
          onChange={e => setBrief(e.target.value)}
        />
        <div className="flex space-x-2 items-center">
          <label>
            <input
              type="checkbox"
              checked={scenarios.includes('baseline')}
              onChange={() => toggleScenario('baseline')}
            />{' '}
            Baseline
          </label>
          <label>
            <input
              type="checkbox"
              checked={scenarios.includes('RCP4.5')}
              onChange={() => toggleScenario('RCP4.5')}
            />{' '}
            RCP4.5
          </label>
          <label>
            <input
              type="checkbox"
              checked={scenarios.includes('RCP8.5')}
              onChange={() => toggleScenario('RCP8.5')}
            />{' '}
            RCP8.5
          </label>
          <label className="ml-4">
            <input
              type="checkbox"
              checked={online}
              onChange={e => setOnline(e.target.checked)}
            />{' '}
            online
          </label>
        </div>
        <div className="flex space-x-2">
          <button className="bg-blue-500 text-white px-2" onClick={validate}>
            Validate Geometry
          </button>
          <button className="bg-blue-500 text-white px-2" onClick={build}>
            Build Context
          </button>
          <button className="bg-blue-500 text-white px-2" onClick={counterfactual}>
            Counterfactual (+greenspace)
          </button>
          <button className="bg-blue-500 text-white px-2" onClick={resolve}>
            Resolve
          </button>
        </div>
        {context && (
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <span className="font-mono text-sm">{context.context_id}</span>
              <button className="bg-gray-200 px-1" onClick={copyId}>
                copy
              </button>
              <button className="bg-gray-200 px-1" onClick={loadContext}>
                refresh
              </button>
            </div>
            <div className="flex space-x-2">
              {Object.entries(context.risk_scores).map(([k, v]) => (
                <span key={k} className="px-2 py-1 bg-gray-100 text-xs">
                  {k}:{v as number}
                </span>
              ))}
            </div>
            <pre className="bg-gray-100 p-2 text-xs overflow-auto h-64">
              {JSON.stringify(context, null, 2)}
            </pre>
          </div>
        )}
        {output && (
          <pre className="bg-gray-100 p-2 text-xs overflow-auto h-40">
            {JSON.stringify(output, null, 2)}
          </pre>
        )}
        <ErrorMessage message={error} />
      </div>
    </div>
  )
}
