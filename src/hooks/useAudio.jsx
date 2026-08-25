import React, { createContext, useContext, useState, useCallback, useRef, useEffect } from 'react'

const AudioContext = createContext(null)

const CHORDS = [
  [110.0, 164.81, 261.63, 329.63],
  [87.31, 130.81, 220.0, 349.23],
  [130.81, 196.0, 246.94, 392.0],
  [98.0, 146.83, 246.94, 293.66],
]

const BELLS = [523.25, 587.33, 659.25, 783.99, 880.0]

class GalleryAudioEngine {
  constructor() {
    this.ctx = null
    this.master = null
    this.wet = null
    this.filter = null
    this.chordTimer = null
    this.bellTimer = null
    this.running = false
    this.chordIndex = 0
    this.voices = []
  }

  _ensure() {
    if (this.ctx) return
    const AC = window.AudioContext || window.webkitAudioContext
    if (!AC) return
    const ctx = new AC()
    this.ctx = ctx

    this.master = ctx.createGain()
    this.master.gain.value = 0

    const comp = ctx.createDynamicsCompressor()
    comp.threshold.value = -24
    comp.ratio.value = 4
    this.master.connect(comp)
    comp.connect(ctx.destination)

    const convolver = ctx.createConvolver()
    convolver.buffer = this._makeImpulse(2.8)
    this.wet = ctx.createGain()
    this.wet.gain.value = 0.45
    convolver.connect(this.wet)
    this.wet.connect(this.master)
    this.reverb = convolver

    this.filter = ctx.createBiquadFilter()
    this.filter.type = 'lowpass'
    this.filter.frequency.value = 900
    this.filter.Q.value = 0.7

    const lfo = ctx.createOscillator()
    lfo.frequency.value = 0.06
    const lfoGain = ctx.createGain()
    lfoGain.gain.value = 380
    lfo.connect(lfoGain)
    lfoGain.connect(this.filter.frequency)
    lfo.start()

    this.filter.connect(this.master)
    this.filterSend = ctx.createGain()
    this.filterSend.gain.value = 0.35
    this.filter.connect(this.filterSend)
    this.filterSend.connect(convolver)

    this._startAir()
    this._startPadVoices()
  }

  _makeImpulse(seconds) {
    const ctx = this.ctx
    const rate = ctx.sampleRate
    const length = Math.floor(rate * seconds)
    const impulse = ctx.createBuffer(2, length, rate)
    for (let ch = 0; ch < 2; ch++) {
      const data = impulse.getChannelData(ch)
      for (let i = 0; i < length; i++) {
        data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / length, 2.6)
      }
    }
    return impulse
  }

  _noiseBuffer(seconds) {
    const ctx = this.ctx
    const length = Math.floor(ctx.sampleRate * seconds)
    const buffer = ctx.createBuffer(1, length, ctx.sampleRate)
    const data = buffer.getChannelData(0)
    let last = 0
    for (let i = 0; i < length; i++) {
      const white = Math.random() * 2 - 1
      last = (last + 0.02 * white) / 1.02
      data[i] = last * 3.5
    }
    return buffer
  }

  _startAir() {
    const ctx = this.ctx
    const src = ctx.createBufferSource()
    src.buffer = this._noiseBuffer(4)
    src.loop = true
    const bp = ctx.createBiquadFilter()
    bp.type = 'bandpass'
    bp.frequency.value = 340
    bp.Q.value = 0.4
    const gain = ctx.createGain()
    gain.gain.value = 0.016
    src.connect(bp)
    bp.connect(gain)
    gain.connect(this.master)
    src.start()
  }

  _makeVoice() {
    const ctx = this.ctx
    const gain = ctx.createGain()
    gain.gain.value = 0
    const oscs = [-5, 5].map((detune) => {
      const osc = ctx.createOscillator()
      osc.type = 'sawtooth'
      osc.detune.value = detune
      osc.connect(gain)
      osc.start()
      return osc
    })
    gain.connect(this.filter)
    return { gain, oscs }
  }

  _startPadVoices() {
    this.voices = []
    this._applyChord(CHORDS[0], 4)

    this.chordTimer = setInterval(() => {
      this.chordIndex = (this.chordIndex + 1) % CHORDS.length
      this._applyChord(CHORDS[this.chordIndex], 5)
    }, 11000)
  }

  _applyChord(chord, fade) {
    if (!this.ctx) return
    const now = this.ctx.currentTime

    chord.forEach((freq, i) => {
      if (!this.voices[i]) this.voices[i] = this._makeVoice()
      const voice = this.voices[i]

      voice.oscs.forEach((osc) => {
        osc.frequency.cancelScheduledValues(now)
        osc.frequency.setValueAtTime(Math.max(osc.frequency.value, 20), now)
        osc.frequency.exponentialRampToValueAtTime(freq, now + fade * 0.5)
      })

      const target = freq < 150 ? 0.05 : 0.032
      voice.gain.gain.cancelScheduledValues(now)
      voice.gain.gain.setValueAtTime(voice.gain.gain.value, now)
      voice.gain.gain.linearRampToValueAtTime(target, now + fade * 0.6)
    })

    for (let i = chord.length; i < this.voices.length; i++) {
      const voice = this.voices[i]
      if (voice) {
        voice.gain.gain.cancelScheduledValues(now)
        voice.gain.gain.setValueAtTime(voice.gain.gain.value, now)
        voice.gain.gain.linearRampToValueAtTime(0, now + fade * 0.6)
      }
    }
  }

  start() {
    this._ensure()
    if (!this.ctx) return
    this.ctx.resume()
    const now = this.ctx.currentTime
    this.master.gain.cancelScheduledValues(now)
    this.master.gain.setValueAtTime(this.master.gain.value, now)
    this.master.gain.linearRampToValueAtTime(0.55, now + 2.2)
    this.running = true
    this._scheduleBell()
  }

  stop() {
    if (!this.ctx) return
    const now = this.ctx.currentTime
    this.master.gain.cancelScheduledValues(now)
    this.master.gain.setValueAtTime(this.master.gain.value, now)
    this.master.gain.linearRampToValueAtTime(0, now + 0.7)
    this.running = false
    if (this.bellTimer) {
      clearTimeout(this.bellTimer)
      this.bellTimer = null
    }
  }

  _scheduleBell() {
    if (this.bellTimer) clearTimeout(this.bellTimer)
    this.bellTimer = setTimeout(() => {
      if (this.running) {
        this._bell(BELLS[Math.floor(Math.random() * BELLS.length)], 0.04)
        if (Math.random() > 0.6) {
          setTimeout(() => this.running && this._bell(BELLS[Math.floor(Math.random() * BELLS.length)], 0.025), 420)
        }
        this._scheduleBell()
      }
    }, 7000 + Math.random() * 8000)
  }

  _bell(freq, peak) {
    if (!this.ctx) return
    const ctx = this.ctx
    const now = ctx.currentTime
    const gain = ctx.createGain()
    gain.gain.setValueAtTime(0, now)
    gain.gain.linearRampToValueAtTime(peak, now + 0.015)
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 4)
    const send = ctx.createGain()
    send.gain.value = 0.9
    gain.connect(this.master)
    gain.connect(send)
    send.connect(this.reverb)
    for (const mult of [1, 2.01]) {
      const osc = ctx.createOscillator()
      osc.type = 'sine'
      osc.frequency.value = freq * mult
      const og = ctx.createGain()
      og.gain.value = mult === 1 ? 1 : 0.25
      osc.connect(og)
      og.connect(gain)
      osc.start(now)
      osc.stop(now + 4.2)
    }
  }

  whoosh(duration = 0.95) {
    if (!this.ctx || !this.running) return
    const ctx = this.ctx
    const now = ctx.currentTime
    const src = ctx.createBufferSource()
    src.buffer = this._noiseBuffer(duration + 0.2)
    const bp = ctx.createBiquadFilter()
    bp.type = 'bandpass'
    bp.Q.value = 1.1
    bp.frequency.setValueAtTime(240, now)
    bp.frequency.exponentialRampToValueAtTime(1900, now + duration * 0.45)
    bp.frequency.exponentialRampToValueAtTime(200, now + duration)
    const gain = ctx.createGain()
    gain.gain.setValueAtTime(0, now)
    gain.gain.linearRampToValueAtTime(0.14, now + duration * 0.4)
    gain.gain.linearRampToValueAtTime(0, now + duration)
    const send = ctx.createGain()
    send.gain.value = 0.5
    src.connect(bp)
    bp.connect(gain)
    gain.connect(this.master)
    gain.connect(send)
    send.connect(this.reverb)
    src.start(now)
    src.stop(now + duration + 0.1)
  }

  chime() {
    if (!this.ctx || !this.running) return
    this._bell(659.25, 0.05)
    setTimeout(() => this.running && this._bell(987.77, 0.035), 140)
  }

  click() {
    if (!this.ctx || !this.running) return
    const ctx = this.ctx
    const now = ctx.currentTime
    const osc = ctx.createOscillator()
    osc.type = 'triangle'
    osc.frequency.setValueAtTime(1750, now)
    osc.frequency.exponentialRampToValueAtTime(900, now + 0.06)
    const gain = ctx.createGain()
    gain.gain.setValueAtTime(0.055, now)
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.09)
    osc.connect(gain)
    gain.connect(this.master)
    osc.start(now)
    osc.stop(now + 0.1)
  }
}

const engine = new GalleryAudioEngine()

export function AudioProvider({ children }) {
  const [isPlaying, setIsPlaying] = useState(false)
  const playingRef = useRef(false)

  useEffect(() => {
    playingRef.current = isPlaying
  }, [isPlaying])

  useEffect(() => {
    return () => engine.stop()
  }, [])

  const start = useCallback(() => {
    engine.start()
    if (engine.ctx) setIsPlaying(true)
  }, [])

  const stop = useCallback(() => {
    engine.stop()
    setIsPlaying(false)
  }, [])

  const toggle = useCallback(() => {
    if (playingRef.current) stop()
    else start()
  }, [stop, start])

  const sfx = useCallback((name) => {
    if (!playingRef.current) return
    if (name === 'whoosh') engine.whoosh()
    else if (name === 'chime') engine.chime()
    else if (name === 'click') engine.click()
  }, [])

  return (
    <AudioContext.Provider value={{ isPlaying, toggle, playWhoosh: () => sfx('whoosh'), playChime: () => sfx('chime'), playClick: () => sfx('click') }}>
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
