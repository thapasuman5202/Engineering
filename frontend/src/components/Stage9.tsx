import { useState } from 'react'
import { getStagePath, postStagePath } from '../lib/api'
import type { StageResult } from '../lib/StageResult'
import ErrorMessage from './ErrorMessage'

export default function Stage9() {
  const [wellness, setWellness] = useState<StageResult | null>(null)
  const [tuningRes, setTuningRes] = useState<StageResult | null>(null)
  const [input, setInput] = useState('')
  const [error, setError] = useState<string | null>(null)

  const fetchWellness = async () => {
    try {
      setError(null)
      setWellness(await getStagePath<StageResult>(9, 'wellness'))
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error'
      setError(message)
    }
  }
  const sendTuning = async () => {
    try {
      setError(null)
      setTuningRes(await postStagePath<StageResult>(9, 'tuning', { value: input }))
      setInput('')
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error'
      setError(message)
    }
  }

  return (
    <div className="p-2 border rounded mb-2">
      <h2 className="font-bold">Stage 9</h2>
      <div className="flex space-x-2 mb-2">
        <button className="bg-blue-500 text-white px-2 py-1" onClick={fetchWellness}>Get Wellness</button>
        <input className="border p-1 flex-1" value={input} onChange={e => setInput(e.target.value)} />
        <button className="bg-green-500 text-white px-2 py-1" onClick={sendTuning}>Send Tuning</button>
      </div>
      <ErrorMessage message={error} />
      {wellness && <pre className="mt-2 bg-gray-100 p-2 text-sm">{JSON.stringify(wellness, null, 2)}</pre>}
      {tuningRes && <pre className="mt-2 bg-gray-100 p-2 text-sm">{JSON.stringify(tuningRes, null, 2)}</pre>}
    </div>
  )
}
