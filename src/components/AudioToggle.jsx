import React from 'react'
import { useAudio } from '../hooks/useAudio'

export default function AudioToggle() {
  const { isPlaying, toggle } = useAudio()

  return (
    <button 
      className="audio-toggle" 
      onClick={toggle}
      aria-label={isPlaying ? 'Mute audio' : 'Play audio'}
    >
      {isPlaying ? (
        <svg viewBox="0 0 24 24">
          <polygon points="11,5 6,9 2,9 2,15 6,15 11,19" fill="currentColor" stroke="none" />
          <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07" />
        </svg>
      ) : (
        <svg viewBox="0 0 24 24">
          <polygon points="11,5 6,9 2,9 2,15 6,15 11,19" fill="currentColor" stroke="none" />
          <line x1="23" y1="9" x2="17" y2="15" />
          <line x1="17" y1="9" x2="23" y2="15" />
        </svg>
      )}
    </button>
  )
}
