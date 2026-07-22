import React, { useRef, useState, useEffect } from 'react'
import { useThree, useFrame } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'

const cameraWaypoints = [
  { position: [0, 0, 1.6], lookAt: [0, -3.9, 1.6] },
  { position: [-3, 0, 1.6], lookAt: [-5.94, 0, 1.6] },
  { position: [-3, -2.5, 1.65], lookAt: [-5.94, -2.5, 1.65] },
  { position: [-3, 2.5, 1.6], lookAt: [-5.94, 2.5, 1.6] },
  { position: [-3, -1, 1.65], lookAt: [-3, -3.94, 1.65] },
  { position: [0, -1, 1.6], lookAt: [0, -3.94, 1.6] },
  { position: [3, -1, 1.65], lookAt: [3, -3.94, 1.65] },
  { position: [3, 0, 1.65], lookAt: [5.94, 0, 1.65] },
  { position: [3, 2.5, 1.6], lookAt: [5.94, 2.5, 1.6] },
  { position: [-3, 1, 1.6], lookAt: [-3, 3.94, 1.6] },
  { position: [0, 1, 1.65], lookAt: [0, 3.94, 1.65] },
  { position: [3, 1, 1.6], lookAt: [3, 3.94, 1.6] },
  { position: [-0.5, 0, 1.8], lookAt: [-2, 0, 1.0] },
  { position: [3.5, 1, 1.8], lookAt: [2, 1.5, 1.0] },
]

function CameraController({ currentIndex }) {
  const { camera } = useThree()
  const targetPos = useRef([0, 0, 1.6])
  const targetLookAt = useRef([0, -3.9, 1.6])
  const currentPos = useRef([0, 0, 1.6])
  const currentLookAt = useRef([0, -3.9, 1.6])

  useEffect(() => {
    const waypoint = cameraWaypoints[currentIndex]
    if (waypoint) {
      targetPos.current = waypoint.position
      targetLookAt.current = waypoint.lookAt
    }
  }, [currentIndex])

  useFrame((_, delta) => {
    const lerpFactor = 1 - Math.pow(0.005, delta)
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

function ExternalModel({ position, scale }) {
  const { scene } = useGLTF('/models/plant.glb')
  return <primitive object={scene} position={position} scale={scale} />
}

function GalleryScene() {
  const { scene } = useGLTF('/models/gallery.glb')

  useEffect(() => {
    if (scene) {
      scene.traverse((child) => {
        if (child.isLight) {
          child.visible = false
        }
      })
    }
  }, [scene])

  return (
    <group>
      <primitive object={scene} />
      <ExternalModel position={[4.5, 0, 0]} scale={[0.5, 0.5, 0.5]} />
      <ExternalModel position={[-4.5, -2, 0]} scale={[0.4, 0.4, 0.4]} />
    </group>
  )
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
    const handleTouchStart = (e) => { touchStartX = e.touches[0].clientX }
    const handleTouchEnd = (e) => {
      const deltaX = e.changedTouches[0].clientX - touchStartX
      if (Math.abs(deltaX) > 50) {
        setCurrentIndex(prev => deltaX < 0
          ? Math.min(prev + 1, cameraWaypoints.length - 1)
          : Math.max(prev - 1, 0))
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
    const handleNav = (e) => setCurrentIndex(e.detail.index)
    window.addEventListener('gallery-set-index', handleNav)
    return () => window.removeEventListener('gallery-set-index', handleNav)
  }, [])

  return (
    <group ref={groupRef}>
      <CameraController currentIndex={currentIndex} />
      <GalleryScene />
    </group>
  )
}
