import { useState, type ReactNode } from 'react'
import { runStage } from '../lib/api'
import type { StageResult } from '../lib/StageResult'
import ErrorMessage from './ErrorMessage'

interface StageRunnerProps {
  stage: number
  children?: ReactNode
}

export default function StageRunner({ stage, children }: StageRunnerProps) {
  const [result, setResult] = useState<StageResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handle = async () => {
    try {
      setError(null)
      setResult(await runStage(stage))
    } catch (e) {
      const message = e instanceof Error ? e.message : 'Unknown error'
      setError(message)
    }
  }

  return (
    <div className="p-2 border rounded mb-2">
      <h2 className="font-bold">Stage {stage}</h2>
      <div className="mb-2">
        <button className="bg-blue-500 text-white px-2 py-1" onClick={handle}>
          Run
        </button>
        {children}
      </div>
      <ErrorMessage message={error} />
      {result && (
        <pre className="mt-2 bg-gray-100 p-2 text-sm">
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  )
}
