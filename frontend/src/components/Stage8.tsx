import { useState } from 'react'
import { getStagePath, postStagePath } from '../lib/api'

interface PlanType {
  stage: number
  status: string
  data: {
    tasks: any[]
  }
}

interface TelemetryResponse {
  stage: number
  status: string
  data: {
    count: number
  }
}

export default function Stage8() {
  const [plan, setPlan] = useState<PlanType | null>(null)
  const [telemetryRes, setTelemetryRes] = useState<TelemetryResponse | null>(null)
  const [input, setInput] = useState('')

  const fetchPlan = async () => {
    const res = (await getStagePath(8, 'plan')) as PlanType
    setPlan(res)
  }
  const sendTelemetry = async () => {
    const res = (await postStagePath(8, 'telemetry', { message: input })) as TelemetryResponse
    setTelemetryRes(res)
    setInput('')
  }

  return (
    <div className="p-2 border rounded mb-2">
      <h2 className="font-bold">Stage 8</h2>
      <div className="flex space-x-2 mb-2">
        <button className="bg-blue-500 text-white px-2 py-1" onClick={fetchPlan}>Get Plan</button>
        <input className="border p-1 flex-1" value={input} onChange={e => setInput(e.target.value)} />
        <button className="bg-green-500 text-white px-2 py-1" onClick={sendTelemetry}>Send Telemetry</button>
      </div>
      {plan && <pre className="mt-2 bg-gray-100 p-2 text-sm">{JSON.stringify(plan, null, 2)}</pre>}
      {telemetryRes && <pre className="mt-2 bg-gray-100 p-2 text-sm">{JSON.stringify(telemetryRes, null, 2)}</pre>}
    </div>
  )
}
