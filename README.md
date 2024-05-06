# 🍺 Obrew Ai Engine

This project handles all requests from client chat apps using a single api. The goal is to provide a modular architecture that allows rapid development of chat-based front-end apps. Client apps need only make HTTP requests to perform any function related to ai workloads.

## Introduction

This is a hybrid Node.js + Python app that uses Next.js as the frontend and FastAPI as the API backend. It ships with a GUI to allow you to manually configure the backend ai services which use Python libraries. Configuration can also be done programmatically. Launch this desktop app locally, then navigate your browser to any web app that supports this project's api and start using ai locally with your own private data for free:

## Features Roadmap

- ✅ Inference: Run open-source AI models for free
- ✅ Provide easy to use desktop installers
- ✅ Embeddings: Create vector embeddings from a text or document files
- ✅ Search: Using a vector database and Llama Index to make semantic or similarity queries
- ✅ Build custom bots from a mix of LLM's, software configs and prompt configs
  <!-- - ❌ Cloud platform (subscription, host your infra with us) -->
  <!-- - ❌ Enterprise service (subscription & paid support, bring your own infra) -->
- ❌ Chats: Save/Retrieve chat message history
- ❌ Auto Agents (Assistants)
- ❌ Agent Teams
- ❌ Multi-Chat
- ❌ Long-term memory across conversations
- ❌ UI generation

## How It Works

- Startup and shutdown of the backend services is done via the front-end UI or REST api.

- The Python/FastAPI server (Obrew api) operates under `localhost:8008`.

- 3rd party client apps will call the Obrew api to perform all functions needed.

## Getting Started

### Dependencies

First, install the dependencies for javascript:

```bash
yarn install
```

Install dependencies for python listed in your requirements.txt file:

Be sure to run this command with admin privileges. This command is optional and is also run on each `yarn build`.

```bash
pip install -r requirements.txt
# or
yarn python-deps
```

## Testing locally

### Run Front-End

Run development front-end webserver (unstable):

```bash
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Run Backend API

If you wish to run the backend server seperately, right-click over `src/backends/main.py` and choose "run python file in terminal" to start server:

Or

```bash
# from working dir
python src/backends/main.py
```

Or (recommended)

```bash
yarn server:dev
# or
yarn server:prod
```

The Obrew api server will be running on [https://localhost:8008](https://localhost:8008)

\*Note if the server fails to start be sure to run `yarn makecert` command to create certificate files necessary for https (these go into `/public` folder). If you dont want https then simply comment out the 2 lines `ssl_keyfile` and `ssl_certfile` when initiating the server.

### Run the Electron app (UI and Backend) in development

This is the preferred method of running the app:

```bash
yarn start
```

## Build steps

This project is meant to be deployed locally on the client's machine. It is a next.js app using serverless runtimes all wrapped by Electron to create a native app. We do this to package up dependencies to make installation easier on the user and to provide the app access to the local OS disk space.

### Building llama.cpp

When you do the normal `pip install llama-cpp-python`, it installs with only CPU support by default.

If you want GPU support for various platforms you must build llama.cpp from source and then pip --force-reinstall.

Follow these steps to build llama-cpp-python for your hardware and platform.

#### Build for Nvidia GPU (cuBLAS) support on Windows

1. Install Visual Studio (Community 2019 is fine) with components:

- C++ CMake tools for Windows
- C++ core features
- Windows 10/11 SDK
- Visual Studio Build Tools

2. Install the CUDA Toolkit:

- Download CUDA Toolkit from https://developer.nvidia.com/cuda-toolkit
- Install only components for CUDA
- If the installation fails, you will need to uncheck everything and only install `visual_studio_integration`. Next proceed to install packages one at a time or in batches until everything is installed.
- Add CUDA_PATH (C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.2) to your environment variables

3. llama-cpp-python build steps:

If on Windows, run the following using "Command Prompt" tool. If you are developing in a python virtual or Anaconda env, be sure you have the env activated first and then run from Windows cmd prompt.

```cmd
set FORCE_CMAKE=1 && set CMAKE_ARGS=-DLLAMA_CUBLAS=on && pip install llama-cpp-python --force-reinstall --ignore-installed --upgrade --no-cache-dir --verbose
```

- If CUDA is detected but you get `No CUDA toolset found` error, copy all files from:

`C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.3\extras\visual_studio_integration\MSBuildExtensions`

into

`C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\MSBuild\Microsoft\VC\v160\BuildCustomizations`

(Adjust the path/version as necessary)

4. Once everything is installed, be sure to set `n_gpu_layers` to an integer higher than 0 to offload inference layers to gpu. You will need to play with this number depending on VRAM and context size of model.

#### Build GPU support for other platforms

See here https://github.com/ggerganov/llama.cpp#build

and here https://github.com/abetlen/llama-cpp-python/blob/main/README.md#installation-with-specific-hardware-acceleration-blas-cuda-metal-etc

for steps to compile to other targets.

- Zig is described as being capable of cross-compilation so it may be good option for release tooling.
- You can install it via Chocolatey: `choco install zig`

Run the command below in powershell to set your env variables:

```
[Environment]::SetEnvironmentVariable(
   "Path",
   [Environment]::GetEnvironmentVariable("Path", "Machine") + ";C:\Zig\zig.exe",
   "Machine"
)
```

## Bundling

### Bundling Nvida CUDA toolkit deps:

If you already have the required toolkit files installed and have built for GPU then the necessary GPU drivers/dlls should be detected by PyInstaller and included in the `_deps` dir.

### Python server

#### Packaging the Python exe with PyInstaller:

This is handled automatically by npm scripts so you do not need to execute these manually. The -F flag bundles everything into one .exe file.

To install the pyinstaller tool:

```bash
pip install -U pyinstaller
```

Then use it to bundle a python script:

```bash
pyinstaller -c -F your_program.py
```

#### Packaging python server with auto-py-to-exe (recommended):

This is a GUI tool that greatly simplifies the process. You can also save and load configs. It uses PyInstaller under the hood and requires it to be installed. Please note if using a conda or virtual environment, be sure to install both PyInstaller and auto-py-to-exe in your virtual environment and also run them from there, otherwise one or both will build from incorrect deps.

To run:

```bash
auto-py-to-exe
```

#### Packaging application with Electron for release (deprecated)

This will build the production deps and then bundle them with pre-built Electron binaries into an installer/distributable.
Please note, "yarn" should be used as the package manager as npm/pnpm will not work for packaging node_modules for some reason.
Electron Builder commands: https://www.electron.build/cli.html

This will create an installer (preferred). Copy the file from `/release/[app-name][version].exe` and put into your Github releases.

```bash
yarn release
```

This will create a folder with all the raw files in `/release/win-unpacked` (when built for windows). Useful for dev since you can inspect the loose files in folder.

```bash
yarn unpacked
```

## Production

### Deploy to public over internet

For production deployments you will either want to run the server behind a reverse proxy using something like Traefic-Hub (free and opens your self hosted server to public internet using encrypted https protocol).

### Deploy to local network over https

If you wish to deploy this on your private network for local access from any device on that network, you will need to run the server using https which requires SSL certificates.

This command will create a self-signed key and cert files in your current dir that are good for 100 years. These files should go in the `/public` folder.

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 36500
# OR
yarn makecert
```

This should be enough for any webapp served over https to access the server. If you see "Warning: Potential Security Risk Ahead" in your browser when using the webapp, you can ignore it by clicking `advanced` then `Accept the Risk` button to continue.

### Inno Installer Setup Wizard

1. Download Inno Setup from (here)[https://jrsoftware.org/isinfo.php]

2. Install and run the setup wizard for a new script

3. Follow the instructions and before it asks to compile the script, cancel and inspect the script where it points to your included files/folders

4. Be sure to append `/[your_included_folder_name]` after the `DestDir: "{app}"`. So instead of `{app}` we have `{app}/assets`. This will ensure it point to the correct paths of the added files you told pyinstaller to include.

5. After that compile the script and it should output your setup file where you specified.

### Create a release on Github with link to installer

1. Create a tag with:

Increase the patch version by 1 (x.x.1 to x.x.2)

```bash
yarn version --patch
```

Will increase the minor version by 1 (x.1.x to x.2.x)

```bash
yarn version --minor
```

Will increase the major version by 1 (1.x.x to 2.x.x)

```bash
yarn version --major
```

2. Create a new release in Github and choose the tag just created or enter a new tag name for Github to make.

3. Drag & Drop the binary file you wish to bundle with the release. Then hit done.

4. If the project is public then the latest release's binary should be available on the web to anyone with the link:

https://github.com/[github-user]/[project-name]/releases/latest/download/[installer-file-name]

## API Overview

This project deploys several backend servers exposed using the `/v1` endpoint. The goal is to separate all OS level logic and processing from the client apps. This can make deploying new apps and swapping out engine functionality easier.

A complete list of endpoint documentation can be found [here](https://localhost:8000/docs) after Obrew Server is started.

## Managing Python dependencies

It is highly recommended to use an package/environment manager like Anaconda to manage Python installations and the versions of dependencies they require. This allows you to create virtual environments from which you can install different versions of software and build/deploy from within this sandboxed environment.

### Switching between virtual environments

The following commands should be done in `Anaconda Prompt` terminal. If on Windows, `run as Admin`.

1. Create a new environment:

```bash
conda create --name env1 python=3.10
```

2. To work in this env, activate it:

```bash
conda activate env1
```

3. When you are done using it, deactivate it:

```bash
conda deactivate
```

4. If using VSCode, you must apply your newly created virtual environment by selecting the `python interpreter` button at the bottom when inside your project directory.

To update PIP package installer:

```bash
conda update pip
```

## Learn More

- Server uses [FastAPI](https://fastapi.tiangolo.com/) - learn about FastAPI features and API.
- Engine uses [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) for Ai inference.
