# av2txtsum

This repository is related to automatic speech recognition (ASR).

## Repository Structure

The repository includes the following `.ipynb` files:

### [01_main.ipynb](01_main.ipynb)
This notebook outlines the primary goals and objectives of the analysis. It includes instructions on how to download a video, extract audio, convert a text transcript to an SRT transcript, and describes the main tools and libraries used for transcription.

### [02_whisper.ipynb](02_whisper.ipynb)
Open source project: whisper.cpp (based on OpenAI Whisper)

This notebook describes the results of using whisper.cpp, which is based on OpenAI Whisper.

### [03_seamlessm4t.ipynb](03_seamlessm4t.ipynb)
Open source project: SeamlessM4T

This notebook describes the results of using the SeamlessM4T.

### [04_faster_whisper.ipynb](04_faster_whisper.ipynb)
Open source project: faster-whisper (based on OpenAI Whisper)

This notebook describes the results of using faster-whisper, which is based on OpenAI Whisper.

Additionally, there are a few folders:
- The `data` folder contains the transcripts. MP3, WAV, and MP4 files are excluded due to their significant size, but they can be extracted as described in the `.ipynb` files. 
- The `utils` folder contains several Python files that are excluded from the `.ipynb` files to avoid overloading them with code. Links to these files are included in the `.ipynb` files.
