import React, { useState, useEffect } from 'react'
import artworksData from '../data/artworks.json'
import { cameraWaypoints } from '../data/cameraWaypoints'

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

  const wp = cameraWaypoints[currentIndex]
  if (!wp || wp.type === 'overview') return null

  const item = wp.type === 'sculpture'
    ? { title: wp.title, artist: wp.artist, description: wp.description, kind: 'Sculpture' }
    : (() => {
        const a = artworksData[currentIndex - 1]
        return a ? { ...a, kind: 'Painting' } : null
      })()

  if (!item) return null

  return (
    <div
      className={`info-panel ${!isVisible ? 'hidden' : ''}`}
      style={{ opacity, transition: 'opacity 200ms ease-out' }}
    >
      <div className="artwork-title">{item.title}</div>
      <div className="artwork-artist">{item.artist}</div>
      <div className="artwork-meta">
        <span className="frame-type">{item.kind}{item.frame ? ` · ${item.frame} frame` : ''}</span>
      </div>
      <div className="artwork-description">{item.description}</div>
    </div>
  )
}
