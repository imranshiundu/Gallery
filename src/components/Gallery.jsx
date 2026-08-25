import React, { useRef, useState, useEffect, useMemo } from 'react'
import { useThree, useFrame } from '@react-three/fiber'
import { useGLTF, useTexture, Environment, Lightformer, MeshReflectorMaterial } from '@react-three/drei'
import { cameraWaypoints, easeInOutCubic } from '../data/cameraWaypoints'
import * as THREE from 'three'

function CameraController({ currentIndex }) {
  const { camera } = useThree()
  const startPos = useRef(new THREE.Vector3())
  const startLook = useRef(new THREE.Vector3())
  const targetPos = useRef(new THREE.Vector3())
  const targetLook = useRef(new THREE.Vector3())
  const targetFov = useRef(55)
  const progress = useRef(1)
  const pauseTime = useRef(0)
  const idleTime = useRef(0)
  const prevIndex = useRef(-1)
  const initialized = useRef(false)

  useFrame((_, delta) => {
    const dt = Math.min(delta, 0.05)
    const wp = cameraWaypoints[currentIndex]
    if (!wp) return

    if (!initialized.current) {
      startPos.current.set(...wp.position)
      startLook.current.set(...wp.lookAt)
      targetPos.current.set(...wp.position)
      targetLook.current.set(...wp.lookAt)
      targetFov.current = wp.fov
      camera.position.copy(targetPos.current)
      camera.lookAt(targetLook.current)
      camera.fov = wp.fov
      camera.updateProjectionMatrix()
      prevIndex.current = currentIndex
      initialized.current = true
      return
    }

    if (currentIndex !== prevIndex.current) {
      startPos.current.copy(camera.position)
      startLook.current.copy(targetLook.current)
      targetPos.current.set(...wp.position)
      targetLook.current.set(...wp.lookAt)
      targetFov.current = wp.fov
      progress.current = 0
      pauseTime.current = 0
      prevIndex.current = currentIndex
    }

    if (progress.current < 1) {
      progress.current = Math.min(progress.current + dt * 0.9, 1)
      if (progress.current >= 1) pauseTime.current = 1.5

      const t = easeInOutCubic(progress.current)
      camera.position.lerpVectors(startPos.current, targetPos.current, t)

      const look = new THREE.Vector3().lerpVectors(startLook.current, targetLook.current, t)
      camera.lookAt(look)

      camera.fov = camera.fov + (targetFov.current - camera.fov) * t
      camera.updateProjectionMatrix()
      idleTime.current = 0
    } else if (pauseTime.current > 0) {
      pauseTime.current -= dt
      idleTime.current += dt
      const swayX = Math.sin(idleTime.current * 0.4) * 0.015
      const swayY = Math.cos(idleTime.current * 0.3) * 0.008
      camera.position.set(
        targetPos.current.x + swayX,
        targetPos.current.y + swayY,
        targetPos.current.z
      )
      camera.lookAt(
        targetLook.current.x + swayX,
        targetLook.current.y + swayY,
        targetLook.current.z
      )
    } else {
      idleTime.current += dt
      const driftX = Math.sin(idleTime.current * 0.15) * 0.02
      const driftY = Math.cos(idleTime.current * 0.1) * 0.012
      camera.position.set(
        targetPos.current.x + driftX,
        targetPos.current.y + driftY,
        targetPos.current.z
      )
      camera.lookAt(
        targetLook.current.x + driftX,
        targetLook.current.y + driftY,
        targetLook.current.z
      )
    }
  })

  return null
}

const PAINTINGS = [
  { img: 'painting_01.jpg', pos: [-5.95, 1.6, 0], rotY: Math.PI / 2, size: [1.6, 1.1], frame: 'gilt' },
  { img: 'painting_02.jpg', pos: [-5.95, 1.62, 2.5], rotY: Math.PI / 2, size: [1.2, 0.9], frame: 'modern' },
  { img: 'painting_03.jpg', pos: [-5.95, 1.58, -2.5], rotY: Math.PI / 2, size: [1.8, 1.2], frame: 'wood' },
  { img: 'painting_04.jpg', pos: [-3, 1.6, 3.95], rotY: Math.PI, size: [1.4, 1.0], frame: 'modern' },
  { img: 'painting_05.jpg', pos: [0, 1.56, 3.95], rotY: Math.PI, size: [1.0, 1.4], frame: 'gilt' },
  { img: 'painting_06.jpg', pos: [3, 1.6, 3.95], rotY: Math.PI, size: [1.6, 1.1], frame: 'wood' },
  { img: 'painting_07.jpg', pos: [5.95, 1.6, 0], rotY: -Math.PI / 2, size: [1.4, 1.0], frame: 'wood' },
  { img: 'painting_08.jpg', pos: [5.95, 1.56, -2.5], rotY: -Math.PI / 2, size: [1.2, 1.6], frame: 'gilt' },
  { img: 'painting_09.jpg', pos: [-3, 1.56, -3.95], rotY: 0, size: [1.6, 1.1], frame: 'modern' },
  { img: 'painting_10.jpg', pos: [0, 1.6, -3.95], rotY: 0, size: [1.0, 1.4], frame: 'wood' },
  { img: 'painting_11.jpg', pos: [3, 1.56, -3.95], rotY: 0, size: [1.8, 1.2], frame: 'gilt' },
]

const FRAME_STYLES = {
  gilt: { color: '#b08d3f', roughness: 0.32, metalness: 0.85 },
  wood: { color: '#4a2e1c', roughness: 0.55, metalness: 0.15 },
  modern: { color: '#202024', roughness: 0.38, metalness: 0.45 },
}

function Artwork({ def, texture }) {
  const [w, h] = def.size
  const style = FRAME_STYLES[def.frame] || FRAME_STYLES.modern
  const fw = 0.06
  const fd = 0.055

  return (
    <group position={def.pos} rotation={[0, def.rotY, 0]}>
      <mesh castShadow position={[-(w / 2 + fw / 2), 0, fd / 2]}>
        <boxGeometry args={[fw, h + fw * 2, fd]} />
        <meshStandardMaterial {...style} />
      </mesh>
      <mesh castShadow position={[w / 2 + fw / 2, 0, fd / 2]}>
        <boxGeometry args={[fw, h + fw * 2, fd]} />
        <meshStandardMaterial {...style} />
      </mesh>
      <mesh castShadow position={[0, h / 2 + fw / 2, fd / 2]}>
        <boxGeometry args={[w + fw * 2, fw, fd]} />
        <meshStandardMaterial {...style} />
      </mesh>
      <mesh castShadow position={[0, -(h / 2 + fw / 2), fd / 2]}>
        <boxGeometry args={[w + fw * 2, fw, fd]} />
        <meshStandardMaterial {...style} />
      </mesh>

      <mesh position={[0, 0, fd - 0.012]}>
        <planeGeometry args={[w + 0.07, h + 0.07]} />
        <meshStandardMaterial color="#efe9dc" roughness={0.92} />
      </mesh>

      <mesh position={[0, 0, fd - 0.005]}>
        <planeGeometry args={[w, h]} />
        <meshStandardMaterial map={texture} roughness={0.65} />
      </mesh>

      <mesh position={[0, -(h / 2 + fw + 0.16), 0.006]}>
        <boxGeometry args={[0.24, 0.055, 0.008]} />
        <meshStandardMaterial color="#cfcabf" metalness={0.9} roughness={0.35} />
      </mesh>
    </group>
  )
}

function GalleryWindow({ position, rotY }) {
  const W = 2.2
  const H = 1.8
  const ft = 0.07
  const fd = 0.12

  return (
    <group position={position} rotation={[0, rotY, 0]}>
      <mesh position={[-(W / 2 + ft / 2), 0, fd / 2]}>
        <boxGeometry args={[ft, H + ft * 2, fd]} />
        <meshStandardMaterial color="#141416" metalness={0.7} roughness={0.35} />
      </mesh>
      <mesh position={[W / 2 + ft / 2, 0, fd / 2]}>
        <boxGeometry args={[ft, H + ft * 2, fd]} />
        <meshStandardMaterial color="#141416" metalness={0.7} roughness={0.35} />
      </mesh>
      <mesh position={[0, H / 2 + ft / 2, fd / 2]}>
        <boxGeometry args={[W + ft * 2, ft, fd]} />
        <meshStandardMaterial color="#141416" metalness={0.7} roughness={0.35} />
      </mesh>
      <mesh position={[0, -(H / 2 + ft / 2), fd / 2]}>
        <boxGeometry args={[W + ft * 2, ft, fd]} />
        <meshStandardMaterial color="#141416" metalness={0.7} roughness={0.35} />
      </mesh>
      <mesh position={[0, 0, fd / 2]}>
        <boxGeometry args={[0.05, H, fd * 0.6]} />
        <meshStandardMaterial color="#141416" metalness={0.7} roughness={0.35} />
      </mesh>
      <mesh position={[0, 0, fd / 2]}>
        <boxGeometry args={[W, 0.05, fd * 0.6]} />
        <meshStandardMaterial color="#141416" metalness={0.7} roughness={0.35} />
      </mesh>

      <mesh position={[0, 0, fd - 0.02]}>
        <planeGeometry args={[W, H]} />
        <meshStandardMaterial color="#bcd6e4" transparent opacity={0.18} roughness={0.05} metalness={0.1} />
      </mesh>

      <mesh position={[0, 0, -0.08]} rotation={[0, Math.PI, 0]}>
        <planeGeometry args={[W + 0.6, H + 0.6]} />
        <meshBasicMaterial color="#e6eef6" toneMapped={false} />
      </mesh>
    </group>
  )
}

function DownlightCans() {
  return (
    <group>
      {[...ART_SPOTS.map((s) => s.position), [-2, 3.2, 0.6], [2, 3.2, -0.9]].map((p, i) => (
        <mesh key={i} position={[p[0], 3.43, p[2]]}>
          <cylinderGeometry args={[0.05, 0.065, 0.14, 20]} />
          <meshStandardMaterial color="#141416" metalness={0.6} roughness={0.4} side={THREE.DoubleSide} />
        </mesh>
      ))}
    </group>
  )
}

function AimedSpot({ position, targetPosition, intensity = 55, angle = 0.34 }) {
  const light = useRef()
  const targetObj = useRef()

  useEffect(() => {
    if (light.current && targetObj.current) {
      light.current.target = targetObj.current
    }
  }, [])

  return (
    <>
      <object3D ref={targetObj} position={targetPosition} />
      <spotLight
        ref={light}
        position={position}
        angle={angle}
        penumbra={0.5}
        intensity={intensity}
        color="#fff6e8"
        distance={11}
        decay={2}
      />
    </>
  )
}

const ART_SPOTS = [
  { position: [-2.4, 3.3, 0], target: [-5.94, 1.6, 0] },
  { position: [-2.4, 3.3, 2.5], target: [-5.94, 1.62, 2.5] },
  { position: [-2.4, 3.3, -2.5], target: [-5.94, 1.58, -2.5] },
  { position: [-3, 3.3, 1.0], target: [-3, 1.6, 3.94] },
  { position: [0, 3.25, 1.0], target: [0, 1.56, 3.94] },
  { position: [3, 3.3, 1.0], target: [3, 1.6, 3.94] },
  { position: [2.4, 3.3, 0], target: [5.94, 1.6, 0] },
  { position: [2.4, 3.3, -2.5], target: [5.94, 1.56, -2.5] },
  { position: [-3, 3.25, -1.0], target: [-3, 1.56, -3.94] },
  { position: [0, 3.25, -1.0], target: [0, 1.6, -3.94] },
  { position: [3, 3.25, -1.0], target: [3, 1.56, -3.94] },
]

function ExternalModel({ position, scale }) {
  const { scene } = useGLTF('/models/plant.glb')
  const cloned = useMemo(() => scene.clone(true), [scene])
  useEffect(() => {
    cloned.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true
        child.receiveShadow = true
      }
    })
  }, [cloned])
  return <primitive object={cloned} position={position} scale={scale} />
}

function GalleryScene() {
  const { scene } = useGLTF('/models/gallery.glb')
  const textures = useTexture(PAINTINGS.map((p) => `/textures/paintings/${p.img}`))

  useMemo(() => {
    const doomed = []
    scene.traverse((child) => {
      if (child.name.startsWith('Art_') || child.name.startsWith('WS') || child.name.startsWith('WW')) {
        doomed.push(child)
      } else if (child.isLight) {
        child.visible = false
      } else if (child.isMesh) {
        child.castShadow = true
        child.receiveShadow = true
      }
    })
    doomed.forEach((child) => child.parent && child.parent.remove(child))
  }, [scene])

  useMemo(() => {
    textures.forEach((tex) => {
      tex.colorSpace = THREE.SRGBColorSpace
      tex.anisotropy = 8
    })
  }, [textures])

  return (
    <group>
      <primitive object={scene} />

      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.002, 0]} receiveShadow>
        <planeGeometry args={[12, 8]} />
        <MeshReflectorMaterial
          color="#191a1e"
          metalness={0.25}
          roughness={0.82}
          resolution={512}
          mirror={0.35}
          mixBlur={5}
          mixStrength={2.2}
          blur={[250, 60]}
        />
      </mesh>

      {PAINTINGS.map((def, i) => (
        <Artwork key={def.img} def={def} texture={textures[i]} />
      ))}

      <GalleryWindow position={[-2, 2.25, -3.93]} rotY={0} />
      <GalleryWindow position={[2, 2.25, -3.93]} rotY={0} />
      <GalleryWindow position={[-5.93, 2.25, 0]} rotY={Math.PI / 2} />

      <DownlightCans />

      <ExternalModel position={[-5.1, 0, 3.2]} scale={[0.45, 0.45, 0.45]} />
      <ExternalModel position={[5.1, 0, -3.2]} scale={[0.4, 0.4, 0.4]} />
    </group>
  )
}

export default function Gallery() {
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        setCurrentIndex((prev) => Math.min(prev + 1, cameraWaypoints.length - 1))
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        setCurrentIndex((prev) => Math.max(prev - 1, 0))
      }
    }

    let touchStartX = 0
    const handleTouchStart = (e) => {
      touchStartX = e.touches[0].clientX
    }
    const handleTouchEnd = (e) => {
      const deltaX = e.changedTouches[0].clientX - touchStartX
      if (Math.abs(deltaX) > 50) {
        setCurrentIndex((prev) =>
          deltaX < 0
            ? Math.min(prev + 1, cameraWaypoints.length - 1)
            : Math.max(prev - 1, 0)
        )
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
    window.dispatchEvent(
      new CustomEvent('gallery-nav-change', { detail: { index: currentIndex } })
    )
  }, [currentIndex])

  useEffect(() => {
    const handleNav = (e) => setCurrentIndex(e.detail.index)
    window.addEventListener('gallery-set-index', handleNav)
    return () => window.removeEventListener('gallery-set-index', handleNav)
  }, [])

  return (
    <group>
      <CameraController currentIndex={currentIndex} />

      <ambientLight intensity={0.3} color="#fff4e6" />
      <directionalLight
        position={[4, 7, 3]}
        intensity={0.85}
        color="#fff2e0"
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-left={-9}
        shadow-camera-right={9}
        shadow-camera-top={7}
        shadow-camera-bottom={-7}
        shadow-camera-near={1}
        shadow-camera-far={22}
        shadow-bias={-0.0004}
      />
      <directionalLight position={[-5, 6, 2]} intensity={0.4} color="#ffeedd" />
      <pointLight position={[0, 3.3, 0]} intensity={18} color="#ffffff" distance={16} decay={2} />

      {ART_SPOTS.map((spot, i) => (
        <AimedSpot key={i} position={spot.position} targetPosition={spot.target} />
      ))}

      <AimedSpot position={[-2, 3.2, 0.6]} targetPosition={[-2, 1.35, 0]} intensity={40} />
      <AimedSpot position={[2, 3.2, -0.9]} targetPosition={[2, 1.4, -1.5]} intensity={40} />

      <Environment resolution={64} frames={1}>
        <Lightformer form="rect" intensity={0.9} position={[0, 5, 0]} rotation-x={Math.PI / 2} scale={[10, 6, 1]} color="#fff4e0" />
        <Lightformer form="rect" intensity={0.35} position={[-6, 2, 0]} rotation-y={Math.PI / 2} scale={[6, 3, 1]} color="#e8eeff" />
        <Lightformer form="rect" intensity={0.35} position={[6, 2, 0]} rotation-y={-Math.PI / 2} scale={[6, 3, 1]} color="#ffe9d0" />
      </Environment>

      <GalleryScene />
    </group>
  )
}
