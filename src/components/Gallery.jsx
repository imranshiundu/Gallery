import React, { useRef, useState, useEffect } from 'react'
import { useThree, useFrame } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'

const cameraWaypoints = [
  { position: [0, 1.6, 5], lookAt: [-5.5, 1.6, 0] },
  { position: [-2, 1.6, 4], lookAt: [-3, 1.6, -3.9] },
  { position: [0, 1.6, 5], lookAt: [0, 1.6, -3.9] },
  { position: [2, 1.6, 4], lookAt: [3, 1.6, -3.9] },
  { position: [4, 1.6, 3], lookAt: [5.5, 1.6, 0] },
  { position: [4, 1.6, 1], lookAt: [5.5, 1.6, 2.5] },
  { position: [0, 1.6, 2], lookAt: [-2, 0.5, 0] },
  { position: [3, 1.6, 3], lookAt: [2, 0.5, 1.5] },
  { position: [-4, 1.6, -1], lookAt: [-5.5, 1.6, 2.5] },
  { position: [-2, 1.6, -4], lookAt: [-3, 1.6, 3.9] },
  { position: [0, 1.6, -4], lookAt: [0, 1.6, 3.9] },
  { position: [2, 1.6, -4], lookAt: [3, 1.6, 3.9] }
]

function CameraController({ currentIndex }) {
  const { camera } = useThree()
  const targetPos = useRef([0, 1.6, 5])
  const targetLookAt = useRef([0, 1.6, 0])
  const currentPos = useRef([0, 1.6, 5])
  const currentLookAt = useRef([0, 1.6, 0])

  useEffect(() => {
    const waypoint = cameraWaypoints[currentIndex]
    if (waypoint) {
      targetPos.current = waypoint.position
      targetLookAt.current = waypoint.lookAt
    }
  }, [currentIndex])

  useFrame((_, delta) => {
    const lerpFactor = 1 - Math.pow(0.01, delta)

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
        position={[0, 3.4, 0]}
        angle={Math.PI / 4}
        penumbra={0.5}
        intensity={1.5}
        color="#fff5e6"
        castShadow={false}
      />
      
      <spotLight
        position={[-4, 3.4, 0]}
        angle={Math.PI / 6}
        penumbra={0.6}
        intensity={1.2}
        color="#fff8f0"
        distance={8}
      />
      
      <spotLight
        position={[4, 3.4, 0]}
        angle={Math.PI / 6}
        penumbra={0.6}
        intensity={1.2}
        color="#fff8f0"
        distance={8}
      />
      
      <spotLight
        position={[0, 3.4, -3]}
        angle={Math.PI / 6}
        penumbra={0.6}
        intensity={1.0}
        color="#fffaf5"
        distance={8}
      />
      
      <spotLight
        position={[0, 3.4, 3]}
        angle={Math.PI / 6}
        penumbra={0.6}
        intensity={1.0}
        color="#fffaf5"
        distance={8}
      />

      <GalleryScene />
    </group>
  )
}
