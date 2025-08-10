import { useState } from 'react'
import { getStagePath, postStagePath } from '../lib/api'

export default function Stage9() {
  const [wellness, setWellness] = useState<any>(null)
  const [tuningRes, setTuningRes] = useState<any>(null)
  const [input, setInput] = useState('')

  const fetchWellness = async () => setWellness(await getStagePath(9, 'wellness'))
  const sendTuning = async () => {
    setTuningRes(await postStagePath(9, 'tuning', { value: input }))
    setInput('')
  }

  return (
    <div className="p-2 border rounded mb-2">
      <h2 className="font-bold">Stage 9</h2>
      <div className="flex space-x-2 mb-2">
        <button className="bg-blue-500 text-white px-2 py-1" onClick={fetchWellness}>Get Wellness</button>
        <input className="border p-1 flex-1" value={input} onChange={e => setInput(e.target.value)} />
        <button className="bg-green-500 text-white px-2 py-1" onClick={sendTuning}>Send Tuning</button>
      </div>
      {wellness && <pre className="mt-2 bg-gray-100 p-2 text-sm">{JSON.stringify(wellness, null, 2)}</pre>}
      {tuningRes && <pre className="mt-2 bg-gray-100 p-2 text-sm">{JSON.stringify(tuningRes, null, 2)}</pre>}
    </div>
  )
}
