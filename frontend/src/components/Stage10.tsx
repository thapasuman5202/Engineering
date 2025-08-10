import { useState } from 'react'
import { getStagePath, postStagePath } from '../lib/api'

export default function Stage10() {
  const [resilience, setResilience] = useState<any>(null)
  const [revenueRes, setRevenueRes] = useState<any>(null)
  const [input, setInput] = useState('')

  const fetchResilience = async () => setResilience(await getStagePath(10, 'resilience'))
  const sendRevenue = async () => {
    setRevenueRes(await postStagePath(10, 'revenue', { value: input }))
    setInput('')
  }

  return (
    <div className="p-2 border rounded mb-2">
      <h2 className="font-bold">Stage 10</h2>
      <div className="flex space-x-2 mb-2">
        <button className="bg-blue-500 text-white px-2 py-1" onClick={fetchResilience}>Get Resilience</button>
        <input className="border p-1 flex-1" value={input} onChange={e => setInput(e.target.value)} />
        <button className="bg-green-500 text-white px-2 py-1" onClick={sendRevenue}>Send Revenue</button>
      </div>
      {resilience && <pre className="mt-2 bg-gray-100 p-2 text-sm">{JSON.stringify(resilience, null, 2)}</pre>}
      {revenueRes && <pre className="mt-2 bg-gray-100 p-2 text-sm">{JSON.stringify(revenueRes, null, 2)}</pre>}
    </div>
  )
}
