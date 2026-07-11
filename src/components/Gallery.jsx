import React, { useRef, useState, useEffect } from 'react'
import { useThree, useFrame } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'

const cameraWaypoints = [
  // Overview - center of room
  { position: [0, 1.6, 0], lookAt: [0, 1.6, -3.9] },
  
  // West wall paintings (looking left from center)
  { position: [-2, 1.6, 1], lookAt: [-5.9, 1.6, 0] },
  { position: [-2, -1, 1], lookAt: [-5.9, -2.5, 1.65] },
  { position: [-2, 2.5, 1], lookAt: [-5.9, 2.5, 1.6] },
  
  // North wall paintings (looking back from center)
  { position: [-1, -1.5, 1.6], lookAt: [-3, -3.9, 1.65] },
  { position: [1, -1.5, 1.6], lookAt: [0, -3.9, 1.6] },
  { position: [2.5, -1.5, 1.6], lookAt: [3, -3.9, 1.65] },
  
  // East wall paintings (looking right from center)
  { position: [2, 1.6, 1], lookAt: [5.9, 1.6, 1.65] },
  { position: [2, 2.5, 1], lookAt: [5.9, 2.5, 1.6] },
  
  // South wall paintings (looking front from center)
  { position: [-1, 1.5, 1.6], lookAt: [-3, 3.9, 1.6] },
  { position: [1, 1.5, 1.6], lookAt: [0, 3.9, 1.65] },
  { position: [2.5, 1.5, 1.6], lookAt: [3, 3.9, 1.6] },
  
  // Sculptures
  { position: [-0.5, 0.5, 1.8], lookAt: [-2, 0, 1.35] },
  { position: [3, 2.5, 1.8], lookAt: [2, 1.5, 1.4] },
]

function CameraController({ currentIndex }) {
  const { camera } = useThree()
  const targetPos = useRef([0, 1.6, 0])
  const targetLookAt = useRef([0, 1.6, -3.9])
  const currentPos = useRef([0, 1.6, 0])
  const currentLookAt = useRef([0, 1.6, -3.9])

  useEffect(() => {
    const waypoint = cameraWaypoints[currentIndex]
    if (waypoint) {
      targetPos.current = waypoint.position
      targetLookAt.current = waypoint.lookAt
    }
  }, [currentIndex])

  useFrame((_, delta) => {
    const lerpFactor = 1 - Math.pow(0.008, delta)

    for (let i = 0; i < 3; i++) {
      currentPos.current[i] += (targetPos.current[i] - currentPos.current[i]) * lerpFactor
      currentLookAt.current[i] += (targetLookAt.current[i] - currentLookAt.current[i]) * lerpFactor
    }

    camera.position.set(currentPos.current[0], currentPos.current[1], currentPos.current[2])
    camera.lookAt(currentLookAt.current[0], currentLookAt.current[1], currentLookAt.current[2])
  })

  return null
}

export { cameraWaypoints }

function GalleryScene() {
  const { scene } = useGLTF('/models/gallery.glb')
  const sceneRef = useRef()

  useEffect(() => {
    if (scene) {
      scene.traverse((child) => {
        if (child.isLight) {
          child.visible = false
        }
      })
    }
  }, [scene])

  return <primitive ref={sceneRef} object={scene} />
}

export default function Gallery({ loaded }) {
  const groupRef = useRef()
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        setCurrentIndex(prev => Math.min(prev + 1, cameraWaypoints.length - 1))
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        setCurrentIndex(prev => Math.max(prev - 1, 0))
      }
    }

    let touchStartX = 0
    const handleTouchStart = (e) => {
      touchStartX = e.touches[0].clientX
    }

    const handleTouchEnd = (e) => {
      const deltaX = e.changedTouches[0].clientX - touchStartX
      if (Math.abs(deltaX) > 50) {
        if (deltaX < 0) {
          setCurrentIndex(prev => Math.min(prev + 1, cameraWaypoints.length - 1))
        } else {
          setCurrentIndex(prev => Math.max(prev - 1, 0))
        }
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    window.addEventListener('touchstart', handleTouchStart, { passive: true })
    window.addEventListener('touchend', handleTouchEnd, { passive: true })

    return () => {
      window.removeEventListener('keydown', handleKeyDown)
      window.removeEventListener('touchstart', handleTouchStart)
      window.removeEventListener('touchend', handleTouchEnd)
    }
  }, [])

  useEffect(() => {
    window.dispatchEvent(new CustomEvent('gallery-nav-change', { detail: { index: currentIndex } }))
  }, [currentIndex])

  useEffect(() => {
    const handleNav = (e) => {
      setCurrentIndex(e.detail.index)
    }
    window.addEventListener('gallery-set-index', handleNav)
    return () => window.removeEventListener('gallery-set-index', handleNav)
  }, [])

  return (
    <group ref={groupRef}>
      <CameraController currentIndex={currentIndex} />
      
      <ambientLight intensity={0.3} />
      
      <spotLight
        position={[0, 3.3, 0]}
        angle={Math.PI / 3}
        penumbra={0.6}
        intensity={1.2}
        color="#fff8f0"
        castShadow={false}
      />
      
      <spotLight
        position={[-4, 0, 3.3]}
        angle={Math.PI / 5}
        penumbra={0.5}
        intensity={0.9}
        color="#fff5e8"
        distance={10}
      />
      
      <spotLight
        position={[4, 0, 3.3]}
        angle={Math.PI / 5}
        penumbra={0.5}
        intensity={0.9}
        color="#fff5e8"
        distance={10}
      />
      
      <spotLight
        position={[0, -2, 3.3]}
        angle={Math.PI / 5}
        penumbra={0.5}
        intensity={0.8}
        color="#fff8f0"
        distance={10}
      />
      
      <spotLight
        position={[0, 2, 3.3]}
        angle={Math.PI / 5}
        penumbra={0.5}
        intensity={0.8}
        color="#fff8f0"
        distance={10}
      />

      <GalleryScene />
    </group>
  )
}
