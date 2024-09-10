import uvicorn


def serve(model_id: str, host: str = "0.0.0.0", port: int = 8000):
    if model_id == "_echo_":
        uvicorn.run("mw_python_sdk.llm.echo_server:app", host="0.0.0.0", port=8000)
