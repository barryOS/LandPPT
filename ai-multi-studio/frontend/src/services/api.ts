import Taro from '@tarojs/taro'

const BASE_URL = process.env.TARO_ENV === 'h5' ? '/api' : 'https://api.example.com'

export async function triggerGeneration(payload: {
  prompt: string
  mode: 'video' | 'image'
  meta?: Record<string, string>
}) {
  return Taro.request({
    url: `${BASE_URL}/ai/generate`,
    method: 'POST',
    data: payload
  })
}
