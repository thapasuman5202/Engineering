import { useState } from 'react'
import { getStagePath, postStagePath } from '../lib/api'
import type { StageResult } from '../lib/StageResult'
import ErrorMessage from './ErrorMessage'

export default function Stage8() {
  const [plan, setPlan] = useState<StageResult | null>(null)
  const [telemetryRes, setTelemetryRes] = useState<StageResult | null>(null)
  const [input, setInput] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [isFetchingPlan, setIsFetchingPlan] = useState(false)
  const [isSendingTelemetry, setIsSendingTelemetry] = useState(false)

  const withLoading = async <T,>(
    action: () => Promise<T>,
    setLoading: (flag: boolean) => void
  ) => {
    try {
      setError(null)
      setLoading(true)
      return await action()
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error'
      setError(message)
      return null
    } finally {
      setLoading(false)
    }
  }

  const fetchPlan = async () => {
    const res = await withLoading(() => getStagePath(8, 'plan'), setIsFetchingPlan)
    if (res) setPlan(res)
  }

  const sendTelemetry = async () => {
    const res = await withLoading(
      () => postStagePath(8, 'telemetry', { message: input }),
      setIsSendingTelemetry
    )
    if (res) {
      setTelemetryRes(res)
      setInput('')
    }
  }

  return (
    <div className="p-2 border rounded mb-2">
      <h2 className="font-bold">Stage 8</h2>
      <div className="flex space-x-2 mb-2">
        <button
          className="bg-blue-500 text-white px-2 py-1 disabled:opacity-50"
          onClick={fetchPlan}
          disabled={isFetchingPlan}
        >
          {isFetchingPlan ? 'Fetching...' : 'Get Plan'}
        </button>
        <input
          className="border p-1 flex-1"
          value={input}
          onChange={e => setInput(e.target.value)}
        />
        <button
          className="bg-green-500 text-white px-2 py-1 disabled:opacity-50"
          onClick={sendTelemetry}
          disabled={isSendingTelemetry}
        >
          {isSendingTelemetry ? 'Sending...' : 'Send Telemetry'}
        </button>
      </div>
      <ErrorMessage message={error} />
      {plan && <pre className="mt-2 bg-gray-100 p-2 text-sm">{JSON.stringify(plan, null, 2)}</pre>}
      {telemetryRes && <pre className="mt-2 bg-gray-100 p-2 text-sm">{JSON.stringify(telemetryRes, null, 2)}</pre>}
    </div>
  )
}
