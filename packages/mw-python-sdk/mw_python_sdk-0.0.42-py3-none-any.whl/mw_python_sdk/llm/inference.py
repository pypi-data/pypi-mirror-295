import uvicorn
import json
import tempfile
import subprocess
from mw_python_sdk import download_dir, download_file, upload_file


def serve(
    model_id: str,
    host: str = "127.0.0.1",
    port: int = 8000,
    dtype: str = "half",
    max_model_len: int = 4096,
):
    if model_id == "_echo_":
        uvicorn.run("mw_python_sdk.llm.echo_server:app", host=host, port=port)
    else:
        model_dir = download_dir(model_id)
        subprocess.call(
            [
                "bash",
                "-c",
                f"python -m vllm.entrypoints.openai.api_server --max-model-len={max_model_len} --dtype={dtype} --model '{model_dir}' --host {host} --port {port}",
            ]
        )


def inference(
    model_id: str,
    source_dataset_id: str,
    source_dataset_path: str,
    destination_dataset_id: str,
    destination_dataset_path: str,
    dtype: str = "half",
    max_model_len: int = 4096,
):
    from vllm import LLM, SamplingParams

    model_dir = download_dir(model_id)
    input_content_path = download_file(source_dataset_id, source_dataset_path)

    with open(input_content_path, "r") as input_file:
        prompts = json.load(input_file)
        # Create a sampling params object.
        sampling_params = SamplingParams(temperature=0.8, top_p=0.95)
        # Create an LLM.
        llm = LLM(model=str(model_dir), dtype=dtype, max_model_len=max_model_len)
        # Generate texts from the prompts. The output is a list of RequestOutput objects
        # that contain the prompt, generated text, and other information.
        outputs = llm.generate(prompts, sampling_params)
        answers = []
        # Print the outputs.
        for output in outputs:
            prompt = output.prompt
            generated_text = output.outputs[0].text
            answers.append({"prompt": prompt, "answer": generated_text})
        # Create a temporary file
        with tempfile.NamedTemporaryFile(
            delete=False, mode="w+", suffix=".json"
        ) as tmp_file:
            # Write the Python object as JSON to the temporary file
            json.dump(answers, tmp_file)
            tmp_file.flush()
            #print(tmp_file.name)
            upload_file(
                tmp_file.name,
                destination_dataset_path,
                destination_dataset_id,
                overwrite=True,
            )
