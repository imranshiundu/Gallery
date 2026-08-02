import React, { useState } from 'react'

export default function EntryScreen({ onEnter }) {
  const [exiting, setExiting] = useState(false)

  const handleEnter = () => {
    setExiting(true)
    setTimeout(() => onEnter(), 800)
  }

  return (
    <div className={`entry-screen ${exiting ? 'fade-out' : ''}`}>
      <button className="entry-button" onClick={handleEnter}>
        Enter Exhibition
      </button>
    </div>
  )
}
