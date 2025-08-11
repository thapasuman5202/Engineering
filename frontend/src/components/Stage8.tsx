import { useState } from 'react'
import { getStagePath, postStagePath } from '../lib/api'
import ErrorMessage from './ErrorMessage'

interface PlanData {
  tasks: string[]
}

interface TelemetryData {
  count: number
}

export default function Stage8() {
  const [plan, setPlan] = useState<PlanData | null>(null)
  const [telemetry, setTelemetry] = useState<TelemetryData | null>(null)
  const [input, setInput] = useState('')
  const [error, setError] = useState<string | null>(null)

  const fetchPlan = async () => {
    try {
      setError(null)
      const res = await getStagePath<PlanData>(8, 'plan')
      setPlan(res.data)
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error'
      setError(message)
    }
  }
  const sendTelemetry = async () => {
    try {
      setError(null)
      const res = await postStagePath<TelemetryData>(8, 'telemetry', { message: input })
      setTelemetry(res.data)
      setInput('')
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error'
      setError(message)
    }
  }

  return (
    <div className="p-2 border rounded mb-2">
      <h2 className="font-bold">Stage 8</h2>
      <div className="flex space-x-2 mb-2">
        <button className="bg-blue-500 text-white px-2 py-1" onClick={fetchPlan}>Get Plan</button>
        <input className="border p-1 flex-1" value={input} onChange={e => setInput(e.target.value)} />
        <button className="bg-green-500 text-white px-2 py-1" onClick={sendTelemetry}>Send Telemetry</button>
      </div>
      <ErrorMessage message={error} />
      {plan && (
        <pre className="mt-2 bg-gray-100 p-2 text-sm">
          {JSON.stringify(plan, null, 2)}
        </pre>
      )}
      {telemetry && (
          <pre className="mt-2 bg-gray-100 p-2 text-sm">
            {JSON.stringify(telemetry, null, 2)}
          </pre>
      )}
    </div>
  )
}
