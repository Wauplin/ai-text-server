export enum ModelType {
  Llama = 'llama',
  Mpt = 'mpt',
  GptJ = 'gptj',
  NeoX = 'gptneox',
  Bloom = 'bloom',
  Gpt2 = 'gpt2',
}

export enum LicenseType {
  Commercial = 'Commercial',
  NonCommercial = 'Non-commercial',
  Academic = 'Academic',
  OpenSource = 'Open-source',
  BigScience = 'BigScience RAIL License v1.0',
  MIT = 'MIT',
  Apache2 = 'Apache-2.0',
  GPL = 'GPL',
  Other = 'Other',
}

export enum Providers {
  TheBloke = 'The Bloke',
  Together = 'Together',
}

export type ModelIntegrity = {
  sha256: string
}

export interface IModelCard {
  id: string
  name: string
  provider: string
  licenses: Array<string>
  description: string
  fileSize: number
  sha256?: string
  ramSize?: number
  fileName: string
  downloadUrl: string
  modelUrl?: string
  modelType?: string
  promptTemplate?: string
  tokenizers?: string[]
  tags?: string[]
}

export const toGB = (size: number) => {
  return size / 1024 / 1024 / 1024
}

const models: Array<IModelCard> = [
  {
    id: 'llama-13b-ggml',
    name: 'Llama 13B',
    provider: Providers.TheBloke,
    licenses: [LicenseType.Other],
    modelType: ModelType.Llama,
    description:
      "These files are GGML format model files for Meta's LLaMA 13b. GGML files are for CPU + GPU inference using llama.cpp and libraries and UIs which support this format.",
    fileSize: 5.59,
    fileName: 'llama-13b.ggmlv3.q3_K_S.bin',
    modelUrl: 'https://huggingface.co/TheBloke/LLaMa-13B-GGML',
    downloadUrl:
      'https://huggingface.co/TheBloke/LLaMa-13B-GGML/resolve/main/llama-13b.ggmlv3.q3_K_S.bin',
    sha256: '9834f27b41ba9dfc8cb3018359fa779330a2f168ac1085d6704fe6b04ce84e1b',
  },
  {
    id: 'llama-2-13b-chat-ggml',
    name: 'Llama 2 13B',
    provider: Providers.TheBloke,
    licenses: [LicenseType.Other],
    description:
      'Llama 2 is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Our fine-tuned LLMs, called Llama-2-Chat, are optimized for dialogue use cases. Llama-2-Chat models outperform open-source chat models on most benchmarks we tested, and in our human evaluations for helpfulness and safety, are on par with some popular closed-source models like ChatGPT and PaLM',
    fileSize: 5.51, // 5508521088 bytes
    fileName: 'llama-2-13b-chat.ggmlv3.q2_K.bin',
    modelType: ModelType.Llama,
    modelUrl: 'https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML',
    downloadUrl:
      'https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q2_K.bin',
    sha256: 'de25498144f05fd3ee41cd2250c16f23a8415a4a4c9f4c1df1a3efd9b3c0991d',
  },
  {
    id: 'wizard-vicuna-15b-coder',
    name: 'Wizard Vicuna 15B Coder',
    provider: Providers.TheBloke,
    licenses: [LicenseType.Other],
    description:
      'Wizardlm: Empowering large language models to follow complex instructions. A StarCoder fine-tuned model using Evol-Instruct method specifically for coding tasks. Use this for code generation, also good at logical reasoning skills.',
    fileSize: 14.3,
    ramSize: 8,
    tokenizers: ['WizardLM/WizardCoder-15B-V1.0'],
    fileName: 'WizardCoder-15B-1.0.ggmlv3.q5_1.bin',
    modelType: ModelType.Gpt2,
    modelUrl: 'https://huggingface.co/TheBloke/WizardCoder-15B-1.0-GGML',
    downloadUrl:
      'https://huggingface.co/TheBloke/WizardCoder-15B-1.0-GGML/resolve/dbbd1178c703672d16e7785f9685200f5a497c8b/WizardCoder-15B-1.0.ggmlv3.q5_1.bin',
    sha256: '1219d9fc6d51901d9a1e58e3cb7f03818d02a1d0ab2d070b4cbabdefeb7d0363',
  },
  {
    id: 'redpajama-chat-3b-ggml',
    name: 'RedPajama Chat 3B',
    provider: Providers.Together,
    licenses: [LicenseType.Apache2],
    description:
      'RedPajama is fine-tuned for Chat conversation. It was developed by Together and leaders from the open-source AI community. The training was done as part of the INCITE 2023 project on Scalable Foundation Models.',
    fileSize: 2.09, // 2086120608 bytes
    ramSize: 16,
    fileName: 'RedPajama-INCITE-Chat-3B-v1-q5_1-ggjt.bin',
    modelType: ModelType.NeoX,
    tokenizers: ['togethercomputer/RedPajama-INCITE-Chat-3B-v1'],
    modelUrl: 'https://huggingface.co/rustformers/redpajama-3b-ggml',
    downloadUrl:
      'https://huggingface.co/rustformers/redpajama-3b-ggml/resolve/ef3021e148238890ceba93c9fe4e17d49d8b279b/RedPajama-INCITE-Chat-3B-v1-q5_1-ggjt.bin',
    sha256: '5943bc928dcaafb6e0155e5517ce00a4ae75e117b9e4e03e1575a24e883d040a',
  },
  // @TODO 404 not found
  {
    id: 'orca-mini-7b-ggml',
    name: 'Orca Mini 7B',
    provider: Providers.TheBloke,
    licenses: [LicenseType.MIT],
    description:
      'An Uncensored LLaMA-7b model trained on explain tuned datasets, created using Instructions and Input from WizardLM, Alpaca & Dolly-V2 datasets and applying Orca Research Paper dataset construction approaches.',
    fileSize: 4.21,
    ramSize: 16,
    fileName: 'orca-mini-v2_7b.ggmlv3.q5_K_M.bin',
    modelType: ModelType.Llama,
    modelUrl: 'https://huggingface.co/TheBloke/orca_mini_7B-GGML',
    downloadUrl:
      'https://huggingface.co/TheBloke/orca_mini_7B-GGML/resolve/main/orca-mini-v2_7b.ggmlv3.q5_K_M.bin',
    sha256: '978484e4053762b55925f4f82e5d6fad92e85d0602e2e8069871ecb103bc3caf',
  },
  {
    id: 'example-cat-anim',
    name: 'Example Cute Cat Animation',
    provider: 'giphy',
    licenses: [LicenseType.Academic, LicenseType.Commercial, LicenseType.Other],
    description: 'This is a test file (gif) for testing download behavior.',
    fileSize: 0.03, // 3060203 bytes
    fileName: 'cute-cat-anim.gif',
    downloadUrl: 'https://media.giphy.com/media/04uUJdw2DliDjsNOZV/giphy.gif',
  },
]

export default models
