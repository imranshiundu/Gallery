import React, { useState, useEffect } from 'react'

export default function LoadingScreen({ onComplete }) {
  const [progress, setProgress] = useState(0)
  const [visible, setVisible] = useState(true)
  const [fadeOut, setFadeOut] = useState(false)

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval)
          setTimeout(() => {
            setFadeOut(true)
            setTimeout(() => {
              setVisible(false)
              onComplete()
            }, 800)
          }, 300)
          return 100
        }
        return prev + Math.random() * 15 + 5
      })
    }, 100)

    return () => clearInterval(interval)
  }, [onComplete])

  if (!visible) return null

  return (
    <div className={`loading-screen ${fadeOut ? 'fade-out' : ''}`}>
      <div className="loading-title">Gallery</div>
      <div className="loading-bar-container">
        <div 
          className="loading-bar" 
          style={{ width: `${Math.min(progress, 100)}%` }}
        />
      </div>
      <div className="loading-text">
        {progress < 100 ? 'Loading exhibition...' : 'Welcome'}
      </div>
    </div>
  )
}
