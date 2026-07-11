import React, { createContext, useContext, useState, useCallback, useRef, useEffect } from 'react'

const AudioContext = createContext(null)

export function AudioProvider({ children }) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [isLoaded, setIsLoaded] = useState(false)
  const audioRef = useRef(null)
  const audioContextRef = useRef(null)

  useEffect(() => {
    const audio = new Audio()
    audio.loop = true
    audio.volume = 0.15
    audio.preload = 'auto'
    audioRef.current = audio

    return () => {
      if (audioRef.current) {
        audioRef.current.pause()
        audioRef.current = null
      }
    }
  }, [])

  const toggle = useCallback(async () => {
    if (!audioRef.current) return

    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)()
    }

    if (audioContextRef.current.state === 'suspended') {
      await audioContextRef.current.resume()
    }

    if (isPlaying) {
      audioRef.current.pause()
      setIsPlaying(false)
    } else {
      try {
        await audioRef.current.play()
        setIsPlaying(true)
      } catch (err) {
        console.log('Audio playback failed:', err)
      }
    }
  }, [isPlaying])

  const loadTrack = useCallback((src) => {
    if (audioRef.current) {
      audioRef.current.src = src
      audioRef.current.load()
      setIsLoaded(true)
    }
  }, [])

  return (
    <AudioContext.Provider value={{ isPlaying, isLoaded, toggle, loadTrack }}>
      {children}
    </AudioContext.Provider>
  )
}

export function useAudio() {
  const context = useContext(AudioContext)
  if (!context) {
    throw new Error('useAudio must be used within an AudioProvider')
  }
  return context
}
