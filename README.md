\# Real-Time Audio FFT Spectrum Analyzer



A low-latency, real-time audio frequency visualizer built with Python. This project captures live input from a microphone or streams an existing `.wav` file, computes the Real Fast Fourier Transform (RFFT) on windowed sample blocks, and renders the dynamic frequency response curve with automated peak pitch detection.



\---



\## Key Features



\- \*\*Dual Audio Input Modes:\*\* Supports live microphone streaming via PortAudio (`sounddevice`) or synchronized `.wav` playback and analysis via `soundfile`.

\- \*\*Real-Time FFT Pipeline:\*\* Computes Fast Fourier Transforms asynchronously using thread-safe double buffering (`queue.Queue`) to prevent UI frame drops.

\- \*\*Spectral Leakage Suppression:\*\* Applies a Hanning window across temporal frames prior to transform execution.

\- \*\*Logarithmic Frequency Scale:\*\* Displays $20\\text{ Hz} - 22.05\\text{ kHz}$ on a log axis to model human auditory perception.

\- \*\*Dominant Pitch Tracker:\*\* Automatically detects and displays the fundamental/peak frequency (in Hz) in real time.



\---



\## Core Engineering \& ECE Principles



1\. \*\*Discrete Fourier Transform (DFT / FFT):\*\*

&#x20;  Converts discrete time-domain audio samples $x\[n]$ into frequency-domain spectral components $X\[k]$:

&#x20;  $$X\[k] = \\sum\_{n=0}^{N-1} x\[n] \\cdot e^{-j 2\\pi k n / N}$$



2\. \*\*Nyquist-Shannon Sampling Theorem:\*\*

&#x20;  With a standard sampling frequency of $f\_s = 44.1\\text{ kHz}$, the observable bandwidth is strictly bounded by the Nyquist limit:

&#x20;  $$f\_{\\text{max}} \\le \\frac{f\_s}{2} = 22.05\\text{ kHz}$$



3\. \*\*Spectral Resolution:\*\*

&#x20;  The frequency bin resolution is determined by the frame block size ($N = 2048$):

&#x20;  $$\\Delta f = \\frac{f\_s}{N} = \\frac{44100}{2048} \\approx 21.53\\text{ Hz}$$



\---



\## Getting Started



\### Prerequisites



\- Python 3.8+

\- PortAudio drivers (pre-packaged with wheels on Windows/macOS)



\### Installation



Clone the repository and install dependencies:



\\`\\`\\`bash

git clone https://github.com/<your-username>/realtime-audio-fft-visualizer.git

cd realtime-audio-fft-visualizer

pip install -r requirements.txt

\\`\\`\\`



\### Running the Visualizer



Launch the script using Python:



\\`\\`\\`bash

python realtime\_fft.py

\\`\\`\\`

\*(On Windows, you can also use `py realtime\_fft.py`)\*.



1\. Press `1` for live microphone capture.

2\. Press `2` to supply the path to a `.wav` file for concurrent playback and spectral inspection.



\---



\## Project Structure



\\`\\`\\`text

├── realtime\_fft.py     # Main application script (audio engine \& GUI)

├── requirements.txt    # Python library dependencies

├── .gitignore          # Build, bytecode, and cache exclusions

└── README.md           # Engineering documentation \& manual

\\`\\`\\`

