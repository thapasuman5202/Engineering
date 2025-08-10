import { useState } from 'react'
import { runStage } from '../lib/api'
import ErrorMessage from './ErrorMessage'

export default function Stage1() {
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const handle = async () => {
    try {
      setError(null)
      setResult(await runStage(1))
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error'
      setError(message)
    }
  }
  return (
    <div className="p-2 border rounded mb-2">
      <h2 className="font-bold">Stage 1</h2>
      <button className="bg-blue-500 text-white px-2 py-1" onClick={handle}>Run</button>
      <ErrorMessage message={error} />
      {result && <pre className="mt-2 bg-gray-100 p-2 text-sm">{JSON.stringify(result,null,2)}</pre>}
    </div>
  )
}
