export const cameraWaypoints = [
  { position: [0, 1.6, 2.5], lookAt: [0, 1.5, -3.8], fov: 45 },
  { position: [-2.8, 1.6, 1.8], lookAt: [-5.8, 1.5, 1.6], fov: 42 },
  { position: [-2.8, 1.4, -2.2], lookAt: [-5.8, 1.5, -2.5], fov: 42 },
  { position: [-2.8, 1.8, 2.6], lookAt: [-5.8, 1.8, 2.5], fov: 42 },
  { position: [-2.5, 1.5, -1.2], lookAt: [-3.2, 1.4, -3.8], fov: 40 },
  { position: [0, 1.5, 1.8], lookAt: [0, 1.5, -3.8], fov: 38 },
  { position: [2.5, 1.5, -1.2], lookAt: [3.2, 1.4, -3.8], fov: 40 },
  { position: [2.8, 1.6, 1.8], lookAt: [5.8, 1.5, 1.65], fov: 42 },
  { position: [2.8, 1.8, 2.6], lookAt: [5.8, 1.8, 2.5], fov: 42 },
  { position: [-2.8, 1.6, 1.2], lookAt: [-3.2, 1.6, 3.8], fov: 40 },
  { position: [0, 1.5, 1.8], lookAt: [0, 1.5, 3.8], fov: 38 },
]

export function easeInOutCubic(t) {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2
}

export function easeOutElastic(t) {
  const c4 = (2 * Math.PI) / 3
  return t === 0 ? 0 : t === 1 ? 1 : Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * c4) + 1
}