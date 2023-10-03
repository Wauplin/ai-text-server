import json
import uvicorn
import subprocess
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from inference import redirects

# from llama_cpp.server.app import create_app
# from pydantic_settings import BaseSettings


app = FastAPI(
    title="🍺 HomeBrew API server",
    version="0.0.1",
)

# Configure CORS settings
origins = [
    "http://localhost:3000",  # (optional) for testing client apps
    "https://hoppscotch.io",  # (optional) for testing endpoints
    "http://localhost:8000",  # (required) Homebrew front-end
    "https://brain-dump-dieharders.vercel.app/",  # (required) client app origin
]


# Redirect requests to our custom endpoints
# @app.middleware("http")
# async def redirect_middleware(request: Request, call_next):
#     return await redirects.text(request, call_next, str(app.PORT_TEXT_INFERENCE))


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# Also works with "shutdown"
@app.on_event("startup")
async def startup_event():
    print("[homebrew api] Server started up.")


class ConnectResponse(BaseModel):
    message: str
    success: bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Connected to api server on port 8008.",
                    "success": True,
                }
            ]
        }
    }


# Tell client we are ready to accept requests
@app.get("/v1/connect")
def connect() -> ConnectResponse:
    return {
        "message": f"Connected to api server on port {app.PORT_HOMEBREW_API}. Refer to 'http://localhost:{app.PORT_HOMEBREW_API}/docs' for api docs.",
        "success": True,
    }


# Load in the ai model to be used for inference.
class LoadInferenceRequest(BaseModel):
    modelId: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "modelId": "llama-2-13b-chat-ggml",
                }
            ]
        }
    }


class LoadInferenceResponse(BaseModel):
    message: str
    success: bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "AI model [llama-2-13b-chat-ggml] loaded.",
                    "success": True,
                }
            ]
        }
    }


@app.post("/v1/text/load")
def load_inference(data: LoadInferenceRequest) -> LoadInferenceResponse:
    try:
        model_id: str = data.modelId
        # Logic to load the specified ai model here...
        return {"message": f"AI model [{model_id}] loaded.", "success": True}
    except KeyError:
        raise HTTPException(
            status_code=400, detail="Invalid JSON format: 'modelId' key not found"
        )


class StartInferenceRequest(BaseModel):
    filePath: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "filePath": "C:\\Project Files\\brain-dump-ai\\models\\llama-2-13b-chat.ggmlv3.q2_K.bin",
                }
            ]
        }
    }


class StartInferenceResponse(BaseModel):
    message: str
    port: int
    docs: str
    success: bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "AI text inference started.",
                    "port": 8080,
                    "docs": "http://localhost:8080/docs",
                    "success": True,
                }
            ]
        }
    }


# Starts the text inference server
@app.post("/v1/text/start")
def start_inference(data: StartInferenceRequest) -> StartInferenceResponse:
    try:
        model_file_path: str = data.filePath
        isStarted = start_text_inference_server(model_file_path)
        return {
            "message": "AI inference started.",
            "port": app.PORT_TEXT_INFERENCE,
            "docs": f"http://localhost:{app.PORT_TEXT_INFERENCE}/docs",
            "success": isStarted,
        }
    except KeyError:
        raise HTTPException(
            status_code=400, detail="Invalid JSON format: 'filePath' key not found"
        )


@app.get("/v1/services/shutdown")
async def shutdown_text_inference():
    try:
        print("[homebrew api] Shutting down all services")
        app.text_inference_process.kill()
        return {
            "message": "Services shutdown.",
            "success": True,
        }
    except Exception as e:
        print(f"[homebrew api] Error shutting down services: {e}")
        return {
            "message": f"Error shutting down services: {e}",
            "success": False,
        }


# Pre-process docs into a text format specified by user.
@app.post("/v1/embeddings/pre-process")
def pre_process_documents():
    return {"message": "pre_process_documents"}


# Create vector embeddings from the pre-processed documents, then store in database.
@app.post("/v1/embeddings/create")
def create_embeddings():
    return {"message": "create_embeddings"}


# Use Llama Index to run queries on vector database embeddings.
@app.post("/v1/search/similiar")
def search_similiar():
    return {"message": "search_similiar"}


# Methods...


def start_homebrew_server():
    try:
        print("Starting API server...")
        # Start the ASGI server
        uvicorn.run(app, host="0.0.0.0", port=app.PORT_HOMEBREW_API, log_level="info")
        return True
    except:
        print("Failed to start API server")
        return False


def start_text_inference_server(file_path: str):
    try:
        # curr_dir = os.getcwd()
        # model_filename = "llama-13b.ggmlv3.q3_K_S.bin"
        # path = os.path.join(curr_dir, f"models/{model_filename}").replace(
        #     "\\", "/"
        # )
        path = file_path.replace("\\", "/")

        # class Settings(BaseSettings):
        #     model: str
        #     alias_name: str
        #     n_ctx: int
        #     n_gpu_layers: int
        #     seed: int
        #     cache: bool
        #     cache_type: str
        #     verbose: bool

        # @TODO Send these settings to inference engine
        # settings = Settings(
        #     model="models/llama-13b.ggmlv3.q3_K_S.bin",
        #     alias_name="Llama13b",
        #     n_ctx=512,
        #     n_gpu_layers=2,
        #     seed=-1,
        #     cache=True,
        #     cache_type="disk",
        #     verbose=True,
        # )

        # appInference = create_app(settings)
        # uvicorn.run(
        #     appInference,
        #     # host=os.getenv("HOST", "localhost"),
        #     host="0.0.0.0",
        #     # port=int(os.getenv("PORT", str(app.PORT_TEXT_INFERENCE))),
        #     port=str(app.PORT_TEXT_INFERENCE),
        #     log_level="info",
        # )

        # @TODO Pass all inference params to command
        # Command to execute
        serve_llama_cpp = [
            "python",
            "-m",
            "llama_cpp.server",
            "--host",
            "0.0.0.0",
            "--port",
            str(app.PORT_TEXT_INFERENCE),
            "--model",
            path,
        ]
        # Execute the command
        # Note, in llama_cpp/server/app.py -> `settings.model_name` needed changing to `settings.alias_name` due to namespace clash with Pydantic.
        proc = subprocess.Popen(serve_llama_cpp)
        app.text_inference_process = proc
        print(f"Starting Inference server from: {file_path} with pid: {proc.pid}")
        return True
    except:
        print("Failed to start Inference server")
        return False


if __name__ == "__main__":
    # Open and read the JSON constants file
    with open("./shared/constants.json", "r") as json_file:
        data = json.load(json_file)
        app.PORT_HOMEBREW_API = data["PORT_HOMEBREW_API"]
        app.PORT_TEXT_INFERENCE = data["PORT_TEXT_INFERENCE"]
    # Starts the homebrew API server
    start_homebrew_server()
