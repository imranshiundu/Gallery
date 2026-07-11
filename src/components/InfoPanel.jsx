import React, { useState, useEffect } from 'react'
import artworksData from '../data/artworks.json'

export default function InfoPanel() {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isVisible, setIsVisible] = useState(true)

  useEffect(() => {
    const handleNavChange = (e) => {
      setCurrentIndex(e.detail.index)
    }
    window.addEventListener('gallery-nav-change', handleNavChange)
    return () => window.removeEventListener('gallery-nav-change', handleNavChange)
  }, [])

  const artwork = artworksData[currentIndex]

  if (!artwork) return null

  return (
    <div className={`info-panel ${!isVisible ? 'hidden' : ''}`}>
      <div className="artwork-title">{artwork.title}</div>
      <div className="artwork-artist">{artwork.artist}</div>
      <div className="artwork-description">{artwork.description}</div>
    </div>
  )
}
