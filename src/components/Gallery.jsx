import React, { useRef, useState, useEffect } from 'react'
import { useThree, useFrame } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'
import { cameraWaypoints, easeInOutCubic, easeOutElastic } from '../data/cameraWaypoints'

function CameraController({ currentIndex }) {
  const { camera } = useThree()
  const targetPos = useRef([0, 1.6, 2.5])
  const targetLookAt = useRef([0, 1.5, -3.8])
  const targetFov = useRef(45)
  const currentPos = useRef([0, 1.6, 2.5])
  const currentLookAt = useRef([0, 1.5, -3.8])
  const currentFov = useRef(45)
  const transitionProgress = useRef(1)
  const isTransitioning = useRef(false)
  const pauseTimer = useRef(0)
  const idleTime = useRef(0)
  const lastIndex = useRef(currentIndex)

  useEffect(() => {
    if (currentIndex !== lastIndex.current) {
      const waypoint = cameraWaypoints[currentIndex]
      if (waypoint) {
        targetPos.current = waypoint.position
        targetLookAt.current = waypoint.lookAt
        targetFov.current = waypoint.fov || 45
        transitionProgress.current = 0
        isTransitioning.current = true
        pauseTimer.current = 0
        lastIndex.current = currentIndex
      }
    }
  }, [currentIndex])

  useFrame((_, delta) => {
    if (isTransitioning.current) {
      transitionProgress.current = Math.min(transitionProgress.current + delta * 1.2, 1)
      const eased = easeInOutCubic(transitionProgress.current)
      
      for (let i = 0; i < 3; i++) {
        currentPos.current[i] = currentPos.current[i] + (targetPos.current[i] - currentPos.current[i]) * eased * 0.15
        currentLookAt.current[i] = currentLookAt.current[i] + (targetLookAt.current[i] - currentLookAt.current[i]) * eased * 0.15
      }
      currentFov.current += (targetFov.current - currentFov.current) * eased * 0.15
      
      camera.position.set(currentPos.current[0], currentPos.current[1], currentPos.current[2])
      camera.lookAt(currentLookAt.current[0], currentLookAt.current[1], currentLookAt.current[2])
      camera.fov = currentFov.current
      camera.updateProjectionMatrix()
      
      if (transitionProgress.current >= 1) {
        isTransitioning.current = false
        pauseTimer.current = 1.5
      }
    } else if (pauseTimer.current > 0) {
      pauseTimer.current -= delta
      const swayAmount = 0.008
      const swaySpeed = 0.4
      currentPos.current[0] += Math.sin(idleTime.current * swaySpeed) * swayAmount * delta * 60
      currentPos.current[2] += Math.cos(idleTime.current * swaySpeed * 0.7) * swayAmount * delta * 60
      currentLookAt.current[0] += Math.sin(idleTime.current * swaySpeed * 1.3) * swayAmount * 0.5 * delta * 60
      currentLookAt.current[1] += Math.cos(idleTime.current * swaySpeed * 0.9) * swayAmount * 0.3 * delta * 60
      
      camera.position.set(currentPos.current[0], currentPos.current[1], currentPos.current[2])
      camera.lookAt(currentLookAt.current[0], currentLookAt.current[1], currentLookAt.current[2])
      idleTime.current += delta
    } else {
      idleTime.current += delta
      const driftAmount = 0.003
      const driftSpeed = 0.15
      currentPos.current[0] += Math.sin(idleTime.current * driftSpeed) * driftAmount * delta * 60
      currentPos.current[2] += Math.cos(idleTime.current * driftSpeed * 0.7) * driftAmount * delta * 60
      currentLookAt.current[0] += Math.sin(idleTime.current * driftSpeed * 1.3) * driftAmount * 0.5 * delta * 60
      currentLookAt.current[1] += Math.cos(idleTime.current * driftSpeed * 0.9) * driftAmount * 0.3 * delta * 60
      
      camera.position.set(currentPos.current[0], currentPos.current[1], currentPos.current[2])
      camera.lookAt(currentLookAt.current[0], currentLookAt.current[1], currentLookAt.current[2])
    }
  })

  return null
}

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
      <ambientLight intensity={0.35} />
      <directionalLight position={[5, 8, 5]} intensity={0.7} color="#fff8f0" castShadow />
      <directionalLight position={[-5, 8, 5]} intensity={0.5} color="#fff5e8" />
      <pointLight position={[0, 3.2, 0]} intensity={0.4} color="#ffffff" distance={12} decay={2} />
      
      <spotLight 
        position={[-5.94, 3.2, 2.5]} 
        target={[-5.94, 1.5, 1.6]} 
        angle={0.35} 
        penumbra={0.5} 
        intensity={0.8} 
        color="#fff9f0"
        distance={6}
        decay={2}
      />
      <spotLight 
        position={[-5.94, 3.2, -1]} 
        target={[-5.94, 1.5, -2.5]} 
        angle={0.35} 
        penumbra={0.5} 
        intensity={0.8} 
        color="#fff9f0"
        distance={6}
        decay={2}
      />
      <spotLight 
        position={[-5.94, 3.2, -4]} 
        target={[-5.94, 1.5, -4]} 
        angle={0.35} 
        penumbra={0.5} 
        intensity={0.8} 
        color="#fff9f0"
        distance={6}
        decay={2}
      />
      <spotLight 
        position={[0, 3.2, -4]} 
        target={[0, 1.5, -3.8]} 
        angle={0.3} 
        penumbra={0.5} 
        intensity={0.7} 
        color="#fff9f0"
        distance={6}
        decay={2}
      />
      <spotLight 
        position={[5.94, 3.2, -4]} 
        target={[5.94, 1.5, -4]} 
        angle={0.35} 
        penumbra={0.5} 
        intensity={0.8} 
        color="#fff9f0"
        distance={6}
        decay={2}
      />
      <spotLight 
        position={[5.94, 3.2, 2.5]} 
        target={[5.94, 1.5, 1.65]} 
        angle={0.35} 
        penumbra={0.5} 
        intensity={0.8} 
        color="#fff9f0"
        distance={6}
        decay={2}
      />
      <spotLight 
        position={[5.94, 3.2, -1]} 
        target={[5.94, 1.5, -2.5]} 
        angle={0.35} 
        penumbra={0.5} 
        intensity={0.8} 
        color="#fff9f0"
        distance={6}
        decay={2}
      />
      <spotLight 
        position={[0, 3.2, 4]} 
        target={[0, 1.5, 3.8]} 
        angle={0.3} 
        penumbra={0.5} 
        intensity={0.7} 
        color="#fff9f0"
        distance={6}
        decay={2}
      />
      <spotLight 
        position={[-3.2, 3.2, 4]} 
        target={[-3.2, 1.6, 3.8]} 
        angle={0.3} 
        penumbra={0.5} 
        intensity={0.7} 
        color="#fff9f0"
        distance={6}
        decay={2}
      />
      <spotLight 
        position={[3.2, 3.2, 4]} 
        target={[3.2, 1.6, 3.8]} 
        angle={0.3} 
        penumbra={0.5} 
        intensity={0.7} 
        color="#fff9f0"
        distance={6}
        decay={2}
      />
      
      <GalleryScene />
    </group>
  )
}
