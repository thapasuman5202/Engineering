import { useState } from 'react'
import { runStage } from '../lib/api'

export default function Stage7() {
  const [result, setResult] = useState<any>(null)
  const handle = async () => setResult(await runStage(7))
  return (
    <div className="p-2 border rounded mb-2">
      <h2 className="font-bold">Stage 7</h2>
      <button className="bg-blue-500 text-white px-2 py-1" onClick={handle}>Run</button>
      {result && <pre className="mt-2 bg-gray-100 p-2 text-sm">{JSON.stringify(result,null,2)}</pre>}
    </div>
  )
}
