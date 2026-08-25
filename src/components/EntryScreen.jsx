import React, { useState, useEffect } from 'react'
import { useAudio } from '../hooks/useAudio'

const THUMBS = Array.from({ length: 11 }, (_, i) => `/textures/paintings/painting_${String(i + 1).padStart(2, '0')}.jpg`)

export default function EntryScreen({ onEnter }) {
  const [exiting, setExiting] = useState(false)
  const [revealed, setRevealed] = useState(false)
  const { start } = useAudio()

  useEffect(() => {
    const timer = setTimeout(() => setRevealed(true), 100)
    return () => clearTimeout(timer)
  }, [])

  const handleEnter = () => {
    start()
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

      <div className="entry-marquee" aria-hidden="true">
        <div className="marquee-track">
          {[...THUMBS, ...THUMBS].map((src, i) => (
            <figure className={`marquee-card ${i % 3 === 0 ? 'tilt-l' : i % 3 === 1 ? 'tilt-r' : ''}`} key={i}>
              <img src={src} alt="" loading="eager" draggable="false" />
            </figure>
          ))}
        </div>
        <div className="marquee-fade marquee-fade-l"></div>
        <div className="marquee-fade marquee-fade-r"></div>
      </div>

      <div className="entry-content">
        <div className="entry-badge">Virtual Exhibition</div>

        <h1 className="entry-title">
          <span className="title-line">gallery</span>
        </h1>

        <p className="entry-tagline">
          Curated contemporary works in an immersive 3D space.
          Eleven paintings and sculptures, guided ambience, cinematic navigation.
        </p>

        <div className="entry-features">
          <div className="feature">
            <svg className="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
              <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
              <line x1="12" y1="22.08" x2="12" y2="12" />
            </svg>
            <span>11 Framed Works</span>
          </div>
          <div className="feature">
            <svg className="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M9 18V5l12-2v13" />
              <circle cx="6" cy="18" r="3" />
              <circle cx="18" cy="16" r="3" />
            </svg>
            <span>Generative Ambience</span>
          </div>
          <div className="feature">
            <svg className="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
              <circle cx="12" cy="13" r="4" />
            </svg>
            <span>Cinematic Tour</span>
          </div>
        </div>

        <button className="entry-button" onClick={handleEnter} aria-label="Enter the exhibition">
          <span className="button-text">Enter Exhibition</span>
          <svg className="button-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>

        <div className="entry-footer">
          <p className="key-hints">
            <kbd>←</kbd><kbd>→</kbd> or swipe to wander
            <span className="dot-sep">·</span>sound toggles top right
          </p>
          <p className="credit">Built with React Three Fiber &amp; Vite</p>
        </div>
      </div>
    </div>
  )
}
