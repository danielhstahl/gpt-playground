from gpt4all import GPT4All
from pathlib import Path

DEFAULT_MODEL_LOCATION = "./model"
DEFAULT_MODEL_NAME = "ggml-model-gpt4all-falcon-q4_0.bin"


def download_gpt_model(
    model_name: str = DEFAULT_MODEL_NAME,
    location_of_model: str = DEFAULT_MODEL_LOCATION,
):
    folder = Path(location_of_model)
    folder.mkdir(parents=True, exist_ok=True)  # create the folder if it doesnt exist
    model = GPT4All(model_name, model_path=location_of_model)


if __name__ == "__main__":
    download_gpt_model()
