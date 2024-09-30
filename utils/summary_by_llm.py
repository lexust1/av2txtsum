"""
This module generates a chat completion using the OpenAI API and saves
the result as a JSON file in a specified directory.

Functions:
- main: Entry point.
- summary_by_llm: Sends a request to the OpenAI API for chat completion,
  saves the result in a JSON file, and returns the chat
  completion object.

Usage:
The module can be used by importing it and calling the `summary_by_llm`
function with the required parameters such as API key, base URL, model,
messages, temperature, and output path.
"""
# Import the standard libraries
from datetime import datetime
import json
import os

# Import the third party libraries
from dotenv import load_dotenv
import openai
from openai import OpenAI
from openai.types.chat import ChatCompletion

# Set the environment:
load_dotenv()


def summary_by_llm(api_key: str,
                   base_url: str,
                   model: str,
                   messages: list,
                   temperature: float,
                   output_path: str) -> ChatCompletion:
    """Generates a chat completion
    Generates a chat completion using the LLM API, saves the result as
    a JSON file, and returns the chat completion object.

    This function sends a request to the OpenAI API for a chat
    completion using the provided model, messages, and temperature.
    The result is saved in a JSON file in the specified output directory
    with a timestamped filename.

    Args:
        api_key (str): The API key.
        base_url (str): The base URL for accessing the API.
        model (str): The model identifier (e.g., 'gpt-4') used for
            generating the chat completion.
        messages (list): A list of message dictionaries to generate
            the completion (conversation context).
        temperature (float): Sampling temperature for the completion,
            controlling randomness.
        output_path (str): The directory path where the JSON output
            file will be saved.

    Returns:
        ChatCompletion: The chat completion object containing the
            generated completion response.
    """
    # Initialize the API client with the provided API key and base URL.
    client = OpenAI(api_key=api_key, base_url=base_url)
    chat_completion = None
    try:
        # Create the chat completion .
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature
        )
    except openai.BadRequestError as e:
        print(f"Bad request: {e}")
    except openai.AuthenticationError as e:
        print(f"Authentication failed: {e}")
    except openai.PermissionDeniedError as e:
        print(f"Permission denied: {e}")
    except openai.NotFoundError as e:
        print(f"Resource not found: {e}")
    except openai.ConflictError as e:
        print(f"Conflict occurred: {e}")
    except openai.UnprocessableEntityError as e:
        print(f"Unprocessable entity: {e}")
    except openai.RateLimitError as e:
        print(f"Rate limit exceeded: {e}")
    except openai.InternalServerError as e:
        print(f"Internal server error: {e}")
    except openai.LengthFinishReasonError as e:
        print(f"Length finish reason error: {e}")
    except openai.ContentFilterFinishReasonError as e:
        print(f"Content filter finish reason error: {e}")
    except openai.APITimeoutError as e:
        print(f"API timeout error: {e}")
    except openai.APIConnectionError as e:
        print(f"API connection error: {e}")
    except openai.OpenAIError as e:
        print(f"OpenAI error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    if chat_completion is not None:
        # Convert the chat completion object to a dictionary for JSON
        # serialization.
        chat_completion_dict = chat_completion.to_dict()
        # Ensure the output directory exists, and create it if necessary.
        os.makedirs(output_path, exist_ok=True)
        # Generate a timestamped filename for the JSON output.
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"chat_completion_{current_date}.json"
        # Write the chat completion data to the JSON file.
        with open(os.path.join(output_path, output_file), "w",
                  encoding="utf-8") as json_file:
            json.dump(chat_completion_dict, json_file)
    return chat_completion

def main() -> None:
    """Entry point."""
    api_key = os.environ.get("GPT_API_KEY")
    base_url = os.environ.get("GPT_BASE_URL")
    model = "openai/gpt-3.5-turbo-0125"
    messages = [
        {
            "role": "user",
            "content": "Explain the importance of fast language models in one sentence."
        }
    ]
    temperature = 0
    output_path = os.path.join("../data/llm_output", model)
    summary_by_llm(
        api_key=api_key,
        base_url=base_url,
        model=model,
        messages=messages,
        temperature=temperature,
        output_path=output_path
    )



if __name__ == "__main__":
    main()
