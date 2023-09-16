'use client'

import { useEffect, useState } from 'react'
import textModels from '@/models/models'
import AppsBrowser from '@/components/AppsBrowser'
import TextInferenceConfigMenu, {
  CURRENT_DOWNLOAD_PATH,
} from '@/components/text-inference-config/TextInferenceConfigMenu'
import TextModelBrowserMenu, {
  ITEM_CURRENT_MODEL,
} from '@/components/text-model-browser/ModelBrowser'

export default function Home() {
  // App vars
  const INFERENCE_IP = 'http://localhost:8008'
  const [isStarted, setIsStarted] = useState(false)
  const [savePath, setSavePath] = useState<string>('')
  const [currentTextModel, setCurrentTextModel] = useState<string>('')
  // Handlers
  const onTestInference = async () => {
    console.log('@@ Testing inference...')

    const options = {
      prompt: 'Whats your name',
    }

    try {
      const response = await fetch(INFERENCE_IP + '/v1/completions', {
        method: 'POST',
        mode: 'cors', // must be enabled otherwise wont redirect
        redirect: 'follow', // we want to follow the re-direct automatically
        cache: 'no-cache',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(options),
      })
      const result = await response.json()
      console.log('@@ [onLoadModel] Result:', result)
    } catch (error) {
      console.log('@@ [Error] Failed to connect to backend:', error)
    }
  }
  // Company credits (built by)
  const renderCredits = () => {
    return (
      <div className="fixed bottom-0 left-0 z-30 flex h-36 w-full flex-col items-center justify-end bg-gradient-to-t from-white via-white font-mono text-sm dark:from-zinc-900 dark:via-zinc-900 lg:static lg:h-auto lg:w-auto lg:bg-none">
        <button
          // onClick={onTestInference}
          className="pointer-events-none flex place-items-center gap-2 p-4 lg:pointer-events-auto lg:p-0"
        >
          Built with 🍺{' '}
          {/* <Image
              src="/vercel.svg"
              alt="Vercel Logo"
              className="dark:invert"
              width={100}
              height={24}
              priority
            /> */}
          <h2 className="text-md">Spread Shot Studios</h2>
        </button>
        <p className="pb-4">
          Refer to{' '}
          <a
            href="http://localhost:8008/docs"
            target="_blank"
            className="text-yellow-400"
            rel="noreferrer"
          >
            http://localhost:8008/docs
          </a>{' '}
          for api docs
        </p>
      </div>
    )
  }

  // Initialize default model path if non selected/stored
  useEffect(() => {
    const saveDefaultPath = async () => {
      const desktopDir = async (): Promise<string> => {
        // Get cwd
        try {
          const basepath = await window.electron.api('getPath', 'desktop')
          return basepath || ''
        } catch (err) {
          console.log('@@ Error getting cwd:', err)
          return ''
        }
      }
      const path = await desktopDir()
      if (path) {
        setSavePath(path)
        localStorage.setItem(CURRENT_DOWNLOAD_PATH, path)
      }
    }
    // Load path from persistent storage
    const storedPath = localStorage.getItem(CURRENT_DOWNLOAD_PATH)
    storedPath && setSavePath(storedPath)
    const currModel = localStorage.getItem(ITEM_CURRENT_MODEL)
    currModel && setCurrentTextModel(currModel)

    if (!storedPath) saveDefaultPath()
  }, [])

  return (
    <div className="xs:p-0 mb-32 flex min-h-screen flex-col items-center justify-between overflow-x-hidden lg:mb-0 lg:p-24">
      {/* Ai Inference config menu */}
      <div className="text-md z-10 w-full items-center justify-center font-mono lg:flex">
        <TextInferenceConfigMenu
          ip={INFERENCE_IP}
          isStarted={isStarted}
          setIsStarted={setIsStarted}
          savePath={savePath}
          setSavePath={setSavePath}
          currentTextModelId={currentTextModel}
        />
      </div>

      {/* Background flare */}
      <div className={`-z-100 relative ${!isStarted && 'm-16'}`}>
        <div className="before:absolute before:-z-20 before:h-[300px] before:w-[480px] before:-translate-x-1/2 before:rounded-full before:bg-gradient-radial before:from-white before:to-transparent before:blur-2xl before:content-[''] after:absolute after:-z-20 after:h-[180px] after:w-[240px] after:translate-x-1/4 after:bg-gradient-conic after:from-sky-200 after:via-blue-200 after:blur-2xl after:content-[''] before:dark:bg-gradient-to-br before:dark:from-transparent before:dark:to-blue-700 before:dark:opacity-10 after:dark:from-sky-900 after:dark:via-[#0141ff] after:dark:opacity-40 before:lg:h-[360px]"></div>
      </div>
      {/* Title and Credits */}
      <div className="relative flex-col place-items-center">
        {/* <Image
          className="relative dark:drop-shadow-[0_0_0.3rem_#ffffff70] dark:invert"
          src="/next.svg"
          alt="Next.js Logo"
          width={180}
          height={37}
          priority
        /> */}
        <h1 className="text-center text-4xl">🍺HomebrewAi</h1>
        {renderCredits()}
      </div>

      {/* Footer menus */}
      {isStarted ? (
        <AppsBrowser />
      ) : (
        <TextModelBrowserMenu
          data={textModels}
          currentTextModel={currentTextModel}
          savePath={savePath}
          setCurrentTextModel={setCurrentTextModel}
        />
      )}
    </div>
  )
}