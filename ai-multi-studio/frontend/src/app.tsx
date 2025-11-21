import { PropsWithChildren, useEffect } from 'react'
import Taro from '@tarojs/taro'
import './styles/theme.scss'

function App({ children }: PropsWithChildren) {
  useEffect(() => {
    Taro.setNavigationBarColor({
      frontColor: '#ffffff',
      backgroundColor: '#030712'
    })
  }, [])

  return children
}

export default App
