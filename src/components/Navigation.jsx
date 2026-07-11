import React, { useState, useCallback, useEffect, useRef } from 'react'
import { cameraWaypoints } from './Gallery'

export default function Navigation() {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [showHint, setShowHint] = useState(true)

  useEffect(() => {
    const handleNavChange = (e) => {
      setCurrentIndex(e.detail.index)
    }
    window.addEventListener('gallery-nav-change', handleNavChange)
    return () => window.removeEventListener('gallery-nav-change', handleNavChange)
  }, [])

  const goToNext = useCallback(() => {
    if (currentIndex < cameraWaypoints.length - 1) {
      window.dispatchEvent(new CustomEvent('gallery-set-index', { 
        detail: { index: currentIndex + 1 } 
      }))
      setShowHint(false)
    }
  }, [currentIndex])

  const goToPrev = useCallback(() => {
    if (currentIndex > 0) {
      window.dispatchEvent(new CustomEvent('gallery-set-index', { 
        detail: { index: currentIndex - 1 } 
      }))
      setShowHint(false)
    }
  }, [currentIndex])

  const goToIndex = useCallback((index) => {
    window.dispatchEvent(new CustomEvent('gallery-set-index', { 
      detail: { index } 
    }))
    setShowHint(false)
  }, [])

  useEffect(() => {
    const timer = setTimeout(() => setShowHint(false), 5000)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="nav-container">
      <button 
        className="nav-button" 
        onClick={goToPrev}
        disabled={currentIndex === 0}
        aria-label="Previous artwork"
      >
        <svg viewBox="0 0 24 24">
          <polyline points="15,18 9,12 15,6" />
        </svg>
      </button>
      
      <div className="nav-dots">
        {cameraWaypoints.map((_, index) => (
          <button
            key={index}
            className={`nav-dot ${index === currentIndex ? 'active' : ''}`}
            onClick={() => goToIndex(index)}
            aria-label={`Go to artwork ${index + 1}`}
          />
        ))}
      </div>

      <button 
        className="nav-button" 
        onClick={goToNext}
        disabled={currentIndex === cameraWaypoints.length - 1}
        aria-label="Next artwork"
      >
        <svg viewBox="0 0 24 24">
          <polyline points="9,6 15,12 9,18" />
        </svg>
      </button>

      {showHint && (
        <div className="swipe-hint">
          Swipe or tap arrows to navigate
        </div>
      )}
    </div>
  )
}
