import React, { useState, Suspense } from 'react'
import { Canvas } from '@react-three/fiber'
import Gallery from './components/Gallery'
import LoadingScreen from './components/LoadingScreen'
import EntryScreen from './components/EntryScreen'
import Navigation from './components/Navigation'
import InfoPanel from './components/InfoPanel'
import AudioToggle from './components/AudioToggle'
import { AudioProvider } from './hooks/useAudio'

export default function App() {
  const [loaded, setLoaded] = useState(false)
  const [entered, setEntered] = useState(false)

  return (
    <AudioProvider>
      <div style={{ width: '100%', height: '100%', position: 'relative' }}>
        <Canvas
          className="gallery-canvas"
          camera={{ position: [3.6, 2.4, 2.9], fov: 55, near: 0.1, far: 100 }}
          dpr={[1, 1.5]}
          gl={{
            antialias: true,
            alpha: false,
            powerPreference: 'high-performance'
          }}
          shadows="soft"
        >
          <color attach="background" args={['#16181d']} />
          <fog attach="fog" args={['#16181d', 10, 30]} />
          
          <Suspense fallback={null}>
            <Gallery loaded={entered} />
          </Suspense>
        </Canvas>

        {!loaded && <LoadingScreen onComplete={() => setLoaded(true)} />}

        {loaded && !entered && <EntryScreen onEnter={() => setEntered(true)} />}

        {entered && (
          <div className="overlay">
            <div className="gallery-title">gallery</div>
            <AudioToggle />
            <Navigation />
            <InfoPanel />
          </div>
        )}
      </div>
    </AudioProvider>
  )
}
