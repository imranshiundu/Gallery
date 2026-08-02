import React, { useState, useEffect } from 'react'

export default function EntryScreen({ onEnter }) {
  const [exiting, setExiting] = useState(false)
  const [revealed, setRevealed] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => setRevealed(true), 100)
    return () => clearTimeout(timer)
  }, [])

  const handleEnter = () => {
    setExiting(true)
    setTimeout(() => onEnter(), 900)
  }

  return (
    <div className={`entry-screen ${exiting ? 'fade-out' : ''} ${revealed ? 'revealed' : ''}`}>
      <div className="entry-bg">
        <div className="entry-gradient"></div>
        <div className="entry-particles" aria-hidden="true">
          {[...Array(24)].map((_, i) => (
            <span key={i} className="particle" style={{ 
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 10}s`,
              animationDuration: `${8 + Math.random() * 6}s`
            }} />
          ))}
        </div>
      </div>

      <div className="entry-content">
        <div className="entry-badge">Virtual Exhibition</div>
        
        <h1 className="entry-title">
          <span className="title-line">gallery</span>
        </h1>
        
        <p className="entry-tagline">
          Curated contemporary works in an immersive 3D space. Eleven paintings and sculptures, guided audio, interactive navigation.
        </p>

        <div className="entry-features">
          <div className="feature">
            <svg className="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
              <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
              <line x1="12" y1="22.08" x2="12" y2="12" />
            </svg>
            <span>11 Paintings & Sculptures</span>
          </div>
          <div className="feature">
            <svg className="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <circle cx="12" cy="12" r="10" />
              <path d="M12 6v6l4 2" />
            </svg>
            <span>Guided Audio Tour</span>
          </div>
          <div className="feature">
            <svg className="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
              <circle cx="12" cy="13" r="4" />
            </svg>
            <span>Interactive Navigation</span>
          </div>
        </div>

        <button className="entry-button" onClick={handleEnter} aria-label="Enter the exhibition">
          <span className="button-text">Enter Exhibition</span>
          <svg className="button-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>

        <div className="entry-footer">
          <p>Navigate with arrows, swipe, or dots · Audio toggle top right</p>
          <p className="credit">Built with React Three Fiber & Vite</p>
        </div>
      </div>

      <div className="entry-scroll-hint" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M12 5v14M19 12l-7 7-7-7" />
        </svg>
      </div>
    </div>
  )
}