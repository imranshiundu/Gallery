const FLAG_KEY = '__galleryBonusDisabled__'

export function bonusDisabled() {
  if (typeof window === 'undefined') return false
  if (window[FLAG_KEY] === true) return true
  try {
    const params = new URLSearchParams(window.location.search)
    if (params.get('bonus') === 'off') {
      window[FLAG_KEY] = true
      return true
    }
  } catch (e) {}
  return false
}