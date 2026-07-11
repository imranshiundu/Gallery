import React from 'react'
import * as THREE from 'three'

function Wall({ position, rotation, width, height, color = '#f5f5f5' }) {
  return (
    <mesh position={position} rotation={rotation} receiveShadow>
      <planeGeometry args={[width, height]} />
      <meshStandardMaterial 
        color={color}
        roughness={0.9}
        metalness={0.0}
      />
    </mesh>
  )
}

function Floor() {
  return (
    <mesh position={[0, 0, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
      <planeGeometry args={[12, 8]} />
      <meshStandardMaterial 
        color="#2a2a2a"
        roughness={0.3}
        metalness={0.1}
      />
    </mesh>
  )
}

function Ceiling() {
  return (
    <mesh position={[0, 3.5, 0]} rotation={[Math.PI / 2, 0, 0]}>
      <planeGeometry args={[12, 8]} />
      <meshStandardMaterial 
        color="#fafafa"
        roughness={0.95}
        metalness={0.0}
      />
    </mesh>
  )
}

function Baseboard({ position, rotation }) {
  return (
    <mesh position={position} rotation={rotation}>
      <boxGeometry args={[12, 0.12, 0.03]} />
      <meshStandardMaterial color="#e8e8e8" roughness={0.8} />
    </mesh>
  )
}

function Pillar({ position }) {
  return (
    <group position={position}>
      <mesh position={[0, 1.75, 0]}>
        <cylinderGeometry args={[0.15, 0.15, 3.5, 16]} />
        <meshStandardMaterial color="#f0f0f0" roughness={0.6} metalness={0.05} />
      </mesh>
      <mesh position={[0, 3.5, 0]}>
        <cylinderGeometry args={[0.2, 0.15, 0.1, 16]} />
        <meshStandardMaterial color="#e8e8e8" roughness={0.7} />
      </mesh>
      <mesh position={[0, 0.05, 0]}>
        <cylinderGeometry args={[0.15, 0.2, 0.1, 16]} />
        <meshStandardMaterial color="#e8e8e8" roughness={0.7} />
      </mesh>
    </group>
  )
}

function Bench({ position, rotation = [0, 0, 0] }) {
  return (
    <group position={position} rotation={rotation}>
      <mesh position={[0, 0.45, 0]}>
        <boxGeometry args={[1.8, 0.06, 0.5]} />
        <meshStandardMaterial color="#1a1a1a" roughness={0.4} metalness={0.2} />
      </mesh>
      <mesh position={[-0.75, 0.22, 0]}>
        <boxGeometry args={[0.05, 0.44, 0.4]} />
        <meshStandardMaterial color="#1a1a1a" roughness={0.4} metalness={0.3} />
      </mesh>
      <mesh position={[0.75, 0.22, 0]}>
        <boxGeometry args={[0.05, 0.44, 0.4]} />
        <meshStandardMaterial color="#1a1a1a" roughness={0.4} metalness={0.3} />
      </mesh>
    </group>
  )
}

function Pedestal({ position, height = 0.9 }) {
  return (
    <group position={position}>
      <mesh position={[0, height / 2, 0]}>
        <boxGeometry args={[0.5, height, 0.5]} />
        <meshStandardMaterial color="#f8f8f8" roughness={0.5} metalness={0.05} />
      </mesh>
      <mesh position={[0, height + 0.025, 0]}>
        <boxGeometry args={[0.55, 0.05, 0.55]} />
        <meshStandardMaterial color="#f0f0f0" roughness={0.6} />
      </mesh>
    </group>
  )
}

export default function Room() {
  const wallHeight = 3.5
  const roomWidth = 12
  const roomDepth = 8

  return (
    <group>
      <Floor />
      <Ceiling />

      <Wall 
        position={[0, wallHeight / 2, -roomDepth / 2]} 
        rotation={[0, 0, 0]}
        width={roomWidth}
        height={wallHeight}
        color="#f5f5f5"
      />
      <Wall 
        position={[0, wallHeight / 2, roomDepth / 2]} 
        rotation={[0, Math.PI, 0]}
        width={roomWidth}
        height={wallHeight}
        color="#f8f8f8"
      />
      <Wall 
        position={[-roomWidth / 2, wallHeight / 2, 0]} 
        rotation={[0, Math.PI / 2, 0]}
        width={roomDepth}
        height={wallHeight}
        color="#f2f2f2"
      />
      <Wall 
        position={[roomWidth / 2, wallHeight / 2, 0]} 
        rotation={[0, -Math.PI / 2, 0]}
        width={roomDepth}
        height={wallHeight}
        color="#f2f2f2"
      />

      <Baseboard position={[0, 0.06, -roomDepth / 2 + 0.015]} rotation={[0, 0, 0]} />
      <Baseboard position={[0, 0.06, roomDepth / 2 - 0.015]} rotation={[0, Math.PI, 0]} />
      <Baseboard position={[-roomWidth / 2 + 0.015, 0.06, 0]} rotation={[0, Math.PI / 2, 0]} />
      <Baseboard position={[roomWidth / 2 - 0.015, 0.06, 0]} rotation={[0, -Math.PI / 2, 0]} />

      <Pillar position={[-3, 0, 0]} />
      <Pillar position={[3, 0, 0]} />

      <Bench position={[0, 0, 0]} rotation={[0, 0, 0]} />
      <Bench position={[-4, 0, 2]} rotation={[0, Math.PI / 6, 0]} />
      <Bench position={[4, 0, -2]} rotation={[0, -Math.PI / 4, 0]} />

      <Pedestal position={[-2, 0, 0]} height={0.9} />
      <Pedestal position={[2, 0, 1.5]} height={1.1} />

      <mesh position={[-1, 0.3, 1.5]} rotation={[0, 0.2, 0]}>
        <cylinderGeometry args={[0.25, 0.3, 0.6, 12]} />
        <meshStandardMaterial color="#d4a574" roughness={0.7} metalness={0.1} />
      </mesh>

      <mesh position={[1.5, 0.2, -1]} rotation={[0, -0.1, 0]}>
        <boxGeometry args={[0.6, 0.4, 0.4]} />
        <meshStandardMaterial color="#4a4a4a" roughness={0.5} metalness={0.2} />
      </mesh>
    </group>
  )
}
