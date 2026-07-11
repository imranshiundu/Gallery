import React, { useState, Suspense } from 'react'
import { Canvas } from '@react-three/fiber'
import Gallery from './components/Gallery'
import LoadingScreen from './components/LoadingScreen'
import Navigation from './components/Navigation'
import InfoPanel from './components/InfoPanel'
import AudioToggle from './components/AudioToggle'
import { AudioProvider } from './hooks/useAudio'

export default function App() {
  const [loaded, setLoaded] = useState(false)

  return (
    <AudioProvider>
      <div style={{ width: '100%', height: '100%', position: 'relative' }}>
        <LoadingScreen onComplete={() => setLoaded(true)} />
        
        <Canvas
          className="gallery-canvas"
          camera={{ position: [0, 1.6, 0], fov: 60, near: 0.1, far: 100 }}
          dpr={[1, 1.5]}
          gl={{ 
            antialias: true,
            alpha: false,
            powerPreference: 'high-performance'
          }}
          shadows={false}
        >
          <color attach="background" args={['#1a1a1a']} />
          <fog attach="fog" args={['#1a1a1a', 10, 30]} />
          
          <Suspense fallback={null}>
            <Gallery loaded={loaded} />
          </Suspense>
        </Canvas>

        {loaded && (
          <div className="overlay">
            <div className="gallery-title">Gallery</div>
            <AudioToggle />
            <Navigation />
            <InfoPanel />
          </div>
        )}
      </div>
    </AudioProvider>
  )
}
