import React, { useState } from 'react'

export default function EntryScreen({ onEnter }) {
  const [exiting, setExiting] = useState(false)

  const handleEnter = () => {
    setExiting(true)
    setTimeout(() => onEnter(), 800)
  }

  return (
    <div className={`entry-screen ${exiting ? 'fade-out' : ''}`}>
      <div className="entry-content">
        <div className="entry-subtitle">Virtual Exhibition</div>
        <h1 className="entry-title">Gallery</h1>
        <p className="entry-description">
          Step inside and explore this month's curated collection of contemporary art.
        </p>
        <button className="entry-button" onClick={handleEnter}>
          Enter Exhibition
        </button>
      </div>
      <div className="entry-footer">
        <span>Touch or click to navigate</span>
      </div>
    </div>
  )
}
