import typer


llm = typer.Typer(short_help="The LLM management.")


@llm.command(short_help="Start a server for the LLM.")
def serve(
    model: str = typer.Argument("", help="The ID of the LLM model to use."),
    host: str = typer.Argument("0.0.0.0", help="The host of the server."),
    port: int = typer.Argument(8000, help="The port of the server."),
):
    from mw_python_sdk.llm.inference import serve

    serve(model, host=host, port=port)


datasets = typer.Typer(short_help="The datasets management.")


@datasets.command(short_help="Upload a file to the dataset.")
def upload_file(
    source: str = typer.Argument(..., help="The path to the file to upload."),
    destination: str = typer.Argument(
        ..., help="The destination of the file in the dataset."
    ),
    dataset: str = typer.Argument(..., help="The ID of the dataset to upload in."),
    overwrite: bool = typer.Argument(
        False, help="Whether to overwrite the file if it already exists."
    ),
):
    from mw_python_sdk import upload_file

    upload_file(source, destination, dataset, overwrite)


app = typer.Typer()
app.add_typer(llm, name="llm")
app.add_typer(datasets, name="ds")

if __name__ == "__main__":
    app()
