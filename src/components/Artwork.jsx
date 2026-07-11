import React, { useMemo } from 'react'
import * as THREE from 'three'

function PaintingFrame({ size, position, rotation }) {
  const [width, height] = size
  const frameThickness = 0.04
  const frameDepth = 0.03
  const borderWidth = 0.06

  const frameColor = '#2a2a2a'
  const matColor = '#f8f8f8'

  return (
    <group position={position} rotation={rotation}>
      <mesh position={[0, 0, -frameDepth / 2]}>
        <planeGeometry args={[width + borderWidth * 2, height + borderWidth * 2]} />
        <meshStandardMaterial color={frameColor} roughness={0.6} metalness={0.2} />
      </mesh>

      <mesh position={[0, 0, -frameDepth / 2 - 0.001]}>
        <planeGeometry args={[width + borderWidth, height + borderWidth]} />
        <meshStandardMaterial color={matColor} roughness={0.8} />
      </mesh>

      <mesh position={[0, 0, 0.001]}>
        <planeGeometry args={[width, height]} />
        <meshStandardMaterial 
          color="#e8e0d8"
          roughness={0.9}
          metalness={0.0}
        />
      </mesh>

      {[
        [-width / 2 - borderWidth / 2, 0, 0],
        [width / 2 + borderWidth / 2, 0, 0],
        [0, -height / 2 - borderWidth / 2, 0],
        [0, height / 2 + borderWidth / 2, 0]
      ].map((pos, i) => (
        <mesh key={i} position={pos}>
          <boxGeometry args={[
            i < 2 ? borderWidth : width + borderWidth * 2,
            i < 2 ? height + borderWidth * 2 : borderWidth,
            frameDepth
          ]} />
          <meshStandardMaterial color={frameColor} roughness={0.5} metalness={0.3} />
        </mesh>
      ))}
    </group>
  )
}

function PaintingCanvas({ size, position, rotation, artworkId }) {
  const colorScheme = useMemo(() => {
    const schemes = [
      { primary: '#4a6fa5', secondary: '#8fb3d9', accent: '#c9a87c', bg: '#f5f0e8' },
      { primary: '#2d4a3e', secondary: '#7fb397', accent: '#d4a574', bg: '#f0ebe3' },
      { primary: '#8b4a4a', secondary: '#d49a9a', accent: '#f5d6a8', bg: '#faf5f0' },
      { primary: '#3d3d5c', secondary: '#7a7aaa', accent: '#d4c4a8', bg: '#f2f0ec' },
      { primary: '#5c4a3d', secondary: '#aa8a6a', accent: '#d4b896', bg: '#f8f4ee' },
      { primary: '#2a4a5c', secondary: '#6a8a9a', accent: '#d4c8a8', bg: '#f0f2f5' },
      { primary: '#4a3d5c', secondary: '#8a6a9a', accent: '#d4a8c8', bg: '#f5f0f8' },
      { primary: '#5c5c3d', secondary: '#9a9a6a', accent: '#d4d4a8', bg: '#f8f8f0' },
      { primary: '#3d5c4a', secondary: '#6a9a7a', accent: '#a8d4b8', bg: '#f0f8f2' },
      { primary: '#5c3d3d', secondary: '#9a6a6a', accent: '#d4a8a8', bg: '#f8f0f0' },
      { primary: '#4a4a5c', secondary: '#8a8a9a', accent: '#c8c8d4', bg: '#f2f2f8' },
      { primary: '#5c4a4a', secondary: '#9a7a7a', accent: '#d4b8b8', bg: '#f8f2f2' }
    ]
    return schemes[(artworkId - 1) % schemes.length]
  }, [artworkId])

  const canvasTexture = useMemo(() => {
    const canvas = document.createElement('canvas')
    canvas.width = 512
    canvas.height = 384
    const ctx = canvas.getContext('2d')

    ctx.fillStyle = colorScheme.bg
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    const patternSeed = artworkId * 17
    const random = (seed) => {
      const x = Math.sin(seed) * 10000
      return x - Math.floor(x)
    }

    for (let i = 0; i < 5; i++) {
      ctx.save()
      ctx.globalAlpha = 0.3 + random(patternSeed + i) * 0.4
      ctx.fillStyle = i % 2 === 0 ? colorScheme.primary : colorScheme.secondary
      
      const shapeType = Math.floor(random(patternSeed + i + 100) * 3)
      const x = random(patternSeed + i + 200) * canvas.width
      const y = random(patternSeed + i + 300) * canvas.height
      const size = 50 + random(patternSeed + i + 400) * 150

      if (shapeType === 0) {
        ctx.beginPath()
        ctx.ellipse(x, y, size, size * 0.6, random(patternSeed + i + 500) * Math.PI, 0, Math.PI * 2)
        ctx.fill()
      } else if (shapeType === 1) {
        ctx.fillRect(x - size / 2, y - size / 2, size, size * 0.7)
      } else {
        ctx.beginPath()
        ctx.moveTo(x, y - size / 2)
        ctx.lineTo(x + size / 2, y + size / 2)
        ctx.lineTo(x - size / 2, y + size / 2)
        ctx.closePath()
        ctx.fill()
      }
      ctx.restore()
    }

    for (let i = 0; i < 8; i++) {
      ctx.save()
      ctx.globalAlpha = 0.15 + random(patternSeed + i + 600) * 0.2
      ctx.strokeStyle = colorScheme.accent
      ctx.lineWidth = 2 + random(patternSeed + i + 700) * 4
      ctx.beginPath()
      
      let x = random(patternSeed + i + 800) * canvas.width
      let y = random(patternSeed + i + 900) * canvas.height
      ctx.moveTo(x, y)
      
      for (let j = 0; j < 4; j++) {
        x += (random(patternSeed + i + j + 1000) - 0.5) * 200
        y += (random(patternSeed + i + j + 1100) - 0.5) * 150
        ctx.lineTo(x, y)
      }
      ctx.stroke()
      ctx.restore()
    }

    const texture = new THREE.CanvasTexture(canvas)
    texture.needsUpdate = true
    return texture
  }, [colorScheme, artworkId])

  return (
    <mesh position={position} rotation={rotation}>
      <planeGeometry args={size} />
      <meshStandardMaterial 
        map={canvasTexture}
        roughness={0.85}
        metalness={0.0}
      />
    </mesh>
  )
}

function SculpturePlaceholder({ position, rotation, type = 'abstract' }) {
  if (type === 'abstract') {
    return (
      <group position={position} rotation={rotation}>
        <mesh position={[0, 0.3, 0]} rotation={[0.1, 0.3, 0]}>
          <torusKnotGeometry args={[0.25, 0.08, 100, 16, 2, 3]} />
          <meshStandardMaterial 
            color="#c9a87c"
            roughness={0.3}
            metalness={0.4}
          />
        </mesh>
      </group>
    )
  }

  return (
    <group position={position} rotation={rotation}>
      <mesh position={[0, 0.35, 0]}>
        <icosahedronGeometry args={[0.3, 1]} />
        <meshStandardMaterial 
          color="#8a8a8a"
          roughness={0.4}
          metalness={0.3}
          wireframe
        />
      </mesh>
      <mesh position={[0, 0.35, 0]}>
        <icosahedronGeometry args={[0.28, 0]} />
        <meshStandardMaterial 
          color="#d4d4d4"
          roughness={0.5}
          metalness={0.2}
        />
      </mesh>
    </group>
  )
}

export default function Artwork({ artwork }) {
  const { type, position, rotation, size } = artwork

  if (type === 'painting') {
    return (
      <group>
        <PaintingFrame 
          size={size} 
          position={position} 
          rotation={rotation} 
        />
        <PaintingCanvas 
          size={size} 
          position={[position[0], position[1], position[2] + 0.02]} 
          rotation={rotation}
          artworkId={artwork.id}
        />
      </group>
    )
  }

  if (type === 'sculpture') {
    const sculptureType = artwork.id === 7 ? 'abstract' : 'geometric'
    return (
      <SculpturePlaceholder 
        position={position}
        rotation={rotation}
        type={sculptureType}
      />
    )
  }

  return null
}
