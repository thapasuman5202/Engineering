import { useState } from 'react'
import { getStagePath, postStagePath } from '../lib/api'

export default function Stage11() {
  const [match, setMatch] = useState<any>(null)
  const [salvageRes, setSalvageRes] = useState<any>(null)
  const [input, setInput] = useState('')

  const fetchMatch = async () => setMatch(await getStagePath(11, 'match'))
  const sendSalvage = async () => {
    setSalvageRes(await postStagePath(11, 'salvage', { item: input }))
    setInput('')
  }

  return (
    <div className="p-2 border rounded mb-2">
      <h2 className="font-bold">Stage 11</h2>
      <div className="flex space-x-2 mb-2">
        <button className="bg-blue-500 text-white px-2 py-1" onClick={fetchMatch}>Get Match</button>
        <input className="border p-1 flex-1" value={input} onChange={e => setInput(e.target.value)} />
        <button className="bg-green-500 text-white px-2 py-1" onClick={sendSalvage}>Send Salvage</button>
      </div>
      {match && <pre className="mt-2 bg-gray-100 p-2 text-sm">{JSON.stringify(match, null, 2)}</pre>}
      {salvageRes && <pre className="mt-2 bg-gray-100 p-2 text-sm">{JSON.stringify(salvageRes, null, 2)}</pre>}
    </div>
  )
}
