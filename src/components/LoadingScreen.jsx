import React, { useState, useEffect, useRef } from 'react'
import { useProgress } from '@react-three/drei'

const STATUS = [
  { at: 0, text: 'Unlocking the doors…' },
  { at: 22, text: 'Hanging the paintings…' },
  { at: 45, text: 'Polishing the floors…' },
  { at: 68, text: 'Focusing the spotlights…' },
  { at: 88, text: 'Tuning the ambience…' },
]

export default function LoadingScreen({ onComplete }) {
  const { progress, total } = useProgress()
  const [displayed, setDisplayed] = useState(0)
  const [fadeOut, setFadeOut] = useState(false)
  const [visible, setVisible] = useState(true)
  const doneRef = useRef(false)
  const mountedAt = useRef(Date.now())

  useEffect(() => {
    let raf
    const tick = () => {
      setDisplayed((prev) => {
        const target = doneRef.current ? 100 : Math.min(progress, 100)
        return prev + (target - prev) * 0.12
      })
      raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [progress])

  useEffect(() => {
    const interval = setInterval(() => {
      const elapsed = Date.now() - mountedAt.current
      const ready = total === 0 || progress >= 100

      if (!doneRef.current && ready && elapsed >= 1600) {
        doneRef.current = true
        clearInterval(interval)
        setTimeout(() => setFadeOut(true), 350)
        setTimeout(() => {
          setVisible(false)
          onComplete()
        }, 1150)
      }
    }, 200)

    return () => clearInterval(interval)
  }, [progress, total, onComplete])

  if (!visible) return null

  const pct = Math.round(displayed)
  const status = [...STATUS].reverse().find((s) => pct >= s.at) || STATUS[0]
  const circumference = 2 * Math.PI * 54

  return (
    <div className={`loading-screen ${fadeOut ? 'fade-out' : ''}`}>
      <div className="loading-ring-wrap">
        <svg className="loading-ring" viewBox="0 0 120 120" aria-hidden="true">
          <circle className="ring-track" cx="60" cy="60" r="54" />
          <circle
            className="ring-fill"
            cx="60"
            cy="60"
            r="54"
            strokeDasharray={circumference}
            strokeDashoffset={circumference * (1 - displayed / 100)}
          />
        </svg>
        <div className="loading-count">
          {pct}
          <span>%</span>
        </div>
      </div>

      <div className="loading-title">gallery</div>

      <div className="loading-status" key={status.at}>
        {pct >= 100 ? 'Welcome' : status.text}
      </div>

      <div className="loading-bar-container">
        <div className="loading-bar" style={{ width: `${Math.min(displayed, 100)}%` }} />
      </div>
    </div>
  )
}
