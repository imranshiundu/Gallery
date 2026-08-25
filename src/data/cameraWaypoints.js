export const cameraWaypoints = [
  { position: [3.6, 2.4, 2.9], lookAt: [-1, 1.3, -1.2], fov: 55 },
  { position: [-2.6, 1.62, 0.35], lookAt: [-5.9, 1.6, 0], fov: 40 },
  { position: [-2.6, 1.66, 2.5], lookAt: [-5.9, 1.62, 2.5], fov: 42 },
  { position: [-2.6, 1.62, -2.5], lookAt: [-5.9, 1.58, -2.5], fov: 42 },
  { position: [-3, 1.66, 1.1], lookAt: [-3, 1.6, 3.9], fov: 40 },
  { position: [0, 1.62, 1.0], lookAt: [0, 1.56, 3.9], fov: 40 },
  { position: [3, 1.66, 1.1], lookAt: [3, 1.6, 3.9], fov: 40 },
  { position: [2.6, 1.66, -0.35], lookAt: [5.9, 1.6, 0], fov: 42 },
  { position: [2.6, 1.62, -2.5], lookAt: [5.9, 1.56, -2.5], fov: 40 },
  { position: [-3, 1.62, -1.1], lookAt: [-3, 1.56, -3.9], fov: 40 },
  { position: [0, 1.66, -1.05], lookAt: [0, 1.6, -3.9], fov: 40 },
  { position: [3, 1.62, -1.1], lookAt: [3, 1.56, -3.9], fov: 40 },
]

export function easeInOutCubic(t) {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2
}
