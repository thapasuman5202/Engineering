import React from 'react'

interface ErrorMessageProps {
  message: string | null
}

export default function ErrorMessage({ message }: ErrorMessageProps) {
  if (!message) return null
  return (
    <div className="mt-2 bg-red-100 text-red-800 p-2 text-sm rounded">
      {message}
    </div>
  )
}
