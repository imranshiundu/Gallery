import React, { useState, useEffect } from 'react'
import artworksData from '../data/artworks.json'

export default function InfoPanel() {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isVisible, setIsVisible] = useState(true)
  const [opacity, setOpacity] = useState(1)

  useEffect(() => {
    const handleNavChange = (e) => {
      setOpacity(0)
      setTimeout(() => {
        setCurrentIndex(e.detail.index)
        setOpacity(1)
      }, 150)
    }
    window.addEventListener('gallery-nav-change', handleNavChange)
    return () => window.removeEventListener('gallery-nav-change', handleNavChange)
  }, [])

  const artwork = currentIndex > 0 ? artworksData[currentIndex - 1] : null

  if (!artwork) return null

  return (
    <div 
      className={`info-panel ${!isVisible ? 'hidden' : ''}`}
      style={{ opacity, transition: 'opacity 200ms ease-out' }}
    >
      <div className="artwork-title">{artwork.title}</div>
      <div className="artwork-artist">{artwork.artist}</div>
      <div className="artwork-meta">
        {artwork.frame && <span className="frame-type">{artwork.frame} frame</span>}
      </div>
      <div className="artwork-description">{artwork.description}</div>
    </div>
  )
}
