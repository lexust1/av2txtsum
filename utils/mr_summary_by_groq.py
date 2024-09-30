"""
This module processes and summarizes text by interacting with the Groq
API. It splits a transcript into chunks, sends the chunks for
summarization, and outputs the summarized sections.

Functions:
- split_transcript: Splits a transcript into a specified number of
    chunks.
- _send_request: Sends a request to the Groq API to summarize a chunk
    of text.
- execute_tasks: Creates and executes tasks to summarize multiple
    chunks of text.
- main: Entry point.

Usage:
The module can be used by importing it and calling the split_transcript
and execute_tasks functions.
"""

# Import the built-in libraries.
import os
import asyncio

# Import the third-party libraries.
from dotenv import load_dotenv
from groq import AsyncGroq


# Initialize the Groq client with the API key from environment variables
load_dotenv()
client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))


def split_transcript(transcript: str, num_chunks: int) -> list:
    """Splits a transcript into a specified number of chunks.

    Splits a transcript into a specified number of chunks, ensuring
    chunks are divided at the nearest sentence boundary (dot).

    Args:
        transcript (str): The complete transcript.
        num_chunks (int): The number of chunks.

    Returns:
        chunks[lst]: A list of transcript chunks.
    """
    # Calculate the approximate size of each chunk.
    transcript_len = len(transcript)
    chunk_size = round(transcript_len / (num_chunks - 1))
    # Initialize an empty list to store the chunks and set the starting
    # index.
    chunks = []
    start = 0
    # Iterate over chunks
    for _ in range(num_chunks):
        end = start + chunk_size
        # Adjust the end index to find the nearest dot before the chunk
        # boundary.
        if end < transcript_len:
            dot_index = transcript.rfind('.', start, end)
            if dot_index != -1:
                # Include the dot in the chunk
                end = dot_index + 1
        # Append the current chunk to the list and update the starting
        # index.
        chunks.append(transcript[start:end].strip())
        start = end
    # Handle any remaining text that has not been included in the chunks
    if start < transcript_len:
        chunks.append(transcript[start:].strip())
    return chunks


async def _send_request(instruction: str, chunk: str):
    """Sends a request to the Groq API to summarize a chunk of text.

        Sends a request to the Groq API to summarize a chunk of text
        based on the provided instruction.

        Args:
            instruction (str): The instruction for the Groq API.
            chunk (str): The chunk of text to be summarized.

        Returns:
            str: The response in the JSON.
        """
    # Send a request to the Groq API with the provided instruction and
    # text chunk.
    response = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{instruction}\n\nThe text:\n\n{chunk}",
            }
        ],
        model="llama3-groq-70b-8192-tool-use-preview",
        temperature=0,
        max_tokens=8192
    )
    # Return the response JSON.
    return response


async def execute_tasks(instruction: str, chunks: list) -> tuple:
    """Creates and executes tasks to summarize multiple chunks of text.

    Creates a list of tasks for summarizing each chunk of text using
    the provided instruction, sends these tasks concurrently to the
    Groq API, and waits for all responses.

    Args:
        instruction (str): The instruction for summarizing the text,
            which will be used for each chunk.
        chunks (list): A list of text chunks to be summarized.

    Returns:
        tuple: A tuple containing the responses from the Groq API. Each
               element in the tuple corresponds to the summarized text
               for a chunk, preserving the order of chunks.
    """
    # Create a list of tasks, each of which sends a request to the Groq
    # to summarize a chunk of text based on the provided instruction.
    tasks = [_send_request(instruction, chunk) for chunk in chunks]
    # Run the tasks concurrently and wait for all of them to complete.
    responses = await asyncio.gather(*tasks)
    # Return the tuple of responses
    return responses


async def main() -> None:
    """Entry point."""
    # Instruction for Groq.
    instruction = (
        "I give a chunk of a full text. Please summarize this. "
        "You should divide the chunk into several logical parts. "
        "The division should reflect a logical separation based on "
        "topics, themes, or any natural breakpoints in the text. "
        "Label each part with a brief heading that describes the focus or "
        "content of that section. Summarize every part.\n\n"
        "Please provide the output in the following format:\n\n"
        "Part 1: [Descriptive Heading]\n"
        "[The text from the first section]\n\n"
        "Part 2: [Descriptive Heading]\n"
        "[The text from the second section]\n"
    )
    # Path to the transcript file.
    transcript_path = "../data/cleaned_whisper_transcript_max_context_64.txt"
    with open(transcript_path, "r") as file:
        transcript = file.read()
    # Divide the transcript into 4 chunks using the split_transcript
    # function.
    chunks = split_transcript(transcript, 4)
    # Run the tasks concurrently and collect the responses.
    responses = await execute_tasks(instruction, chunks)
    # Print each response message and a number of tokens of all
    # response messages.
    token_num = 0
    for num, response in enumerate(responses, start=1):
        print(f"Section #{num}\n\n{response.choices[0].message.content}\n\n")
        token_num += response.usage.completion_tokens
    print(token_num)


if __name__ == "__main__":
    asyncio.run(main())
