import { useState } from 'react'
import { View, Text, Textarea, Picker, Button } from '@tarojs/components'
import { triggerGeneration } from '@/services/api'
import './index.scss'

const industries = ['文旅', '教育', '汽车', '地产']
const modes = ['video', 'image']

function Home() {
  const [prompt, setPrompt] = useState('')
  const [industryIndex, setIndustryIndex] = useState(0)
  const [modeIndex, setModeIndex] = useState(0)
  const [status, setStatus] = useState('等待注入灵感...')

  const currentIndustry = industries[industryIndex]
  const currentMode = modes[modeIndex]

  const handleSubmit = async () => {
    setStatus('AI 导演正在调度镜头...')
    try {
      await triggerGeneration({
        prompt,
        mode: currentMode as 'video' | 'image',
        meta: { industry: currentIndustry }
      })
      setStatus('任务已排队，请在项目空间查看进度')
    } catch (error) {
      setStatus('触发失败，请稍后重试')
    }
  }

  return (
    <View className='home-page'>
      <View className='hero-card glass-card'>
        <Text className='eyebrow'>多端 AI 影像工作台</Text>
        <Text className='title'>启动你的未来感作品</Text>
        <Text className='subtitle'>连接 Sora2 + Gemini，一站式生成视频与图像</Text>
      </View>

      <View className='control-card glass-card'>
        <Text className='section-title'>行业情境</Text>
        <Picker mode='selector' range={industries} onChange={(e) => setIndustryIndex(Number(e.detail.value))}>
          <View className='selector'>{currentIndustry}</View>
        </Picker>

        <Text className='section-title'>提示词</Text>
        <Textarea
          className='prompt'
          value={prompt}
          placeholder='描述场景、镜头、情绪...'
          onInput={(e) => setPrompt(e.detail.value)}
        />

        <Text className='section-title'>输出形态</Text>
        <Picker mode='selector' range={['未来短片', '沉浸海报']} onChange={(e) => setModeIndex(Number(e.detail.value))}>
          <View className='selector'>{currentMode === 'video' ? '未来短片' : '沉浸海报'}</View>
        </Picker>

        <Button className='submit' onClick={handleSubmit}>启动生成</Button>
        <Text className='status'>{status}</Text>
      </View>
    </View>
  )
}

export default Home
