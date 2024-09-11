import uvicorn
import subprocess
from mw_python_sdk import download_dir


def serve(
    model_id: str,
    host: str = "0.0.0.0",
    port: int = 8000,
    dtype: str = "half",
    max_model_len: int = 4096,
):
    if model_id == "_echo_":
        uvicorn.run("mw_python_sdk.llm.echo_server:app", host="0.0.0.0", port=8000)
    else:
        model_dir = download_dir(model_id)
        subprocess.call(
            [
                "bash",
                "-c",
                f"python -m vllm.entrypoints.openai.api_server --max-model-len={max_model_len} --dtype={dtype} --model '{model_dir}' --host {host} --port {port}",
            ]
        )
