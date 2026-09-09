# Real-Time Audio FFT Spectrum Analyzer

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PortAudio](https://img.shields.io/badge/Driver-PortAudio-green.svg)](http://www.portaudio.com/)

A low-latency, real-time frequency visualizer written in Python. It captures live input from a microphone or streams an existing `.wav` file, computes the Real Fast Fourier Transform (RFFT) on windowed sample blocks, and renders the dynamic frequency response curve alongside real-time dominant pitch tracking.

---

## Features

* **Dual Input Modes:** Seamlessly toggle between live microphone streaming (`sounddevice`) and synchronized `.wav` playback/analysis (`soundfile`).
* **Non-Blocking Architecture:** Decoupled audio acquisition and UI rendering via thread-safe double buffering (`queue.Queue`) to prevent frame drops.
* **Leakage Reduction:** Standard Hanning windowing applied per temporal frame prior to RFFT computation.
* **Perceptual Log Scaling:** Frequency axis ranges from **20 Hz to 22.05 kHz** on a logarithmic scale to mirror human pitch perception.
* **Peak Frequency Tracking:** Automated real-time extraction and overlay of the dominant fundamental frequency.

---

## Signal Processing Pipeline

The signal pipeline converts continuous acoustic energy into calibrated frequency bins through standard discrete-time processing:

### 1. Discrete Fourier Transform (DFT / RFFT)
Converts time-domain audio samples $x[n]$ into frequency-domain components $X[k]$:

$$X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j 2\pi k n / N}$$

### 2. Nyquist-Shannon Bandwidth
At a sample rate of $f_s = 44.1\text{ kHz}$, the observable bandwidth is bounded by the Nyquist limit:

$$f_{\max} \le \frac{f_s}{2} = 22.05\text{ kHz}$$

### 3. Spectral Bin Resolution
Frequency resolution is defined by block size ($N = 2048$):

$$\Delta f = \frac{f_s}{N} = \frac{44100\text{ Hz}}{2048} \approx 21.53\text{ Hz}$$

---

## Technical Specifications

| Parameter | Value | Description |
| :--- | :--- | :--- |
| **Sample Rate ($f_s$)** | `44,100 Hz` | Standard CD-quality sampling rate |
| **Block Size ($N$)** | `2048 samples` | Temporal frame size (~46.4 ms window) |
| **Window Function** | Hann / Hanning | Suppresses boundary-induced spectral leakage |
| **Frequency Range** | `20 Hz – 22,050 Hz` | Standard audible acoustic spectrum |
| **Buffering** | Lock-free queue | Decouples audio callback thread from GUI |

---

## Getting Started

### Prerequisites

* Python 3.8+
* PortAudio (bundled with wheels on Windows/macOS; Linux may require `sudo apt-get install libportaudio2`)

### Installation

```bash
git clone [https://github.com/Ajil07/realtime-audio-fft-visualizer.git](https://github.com/username/realtime-audio-fft-visualizer.git)
cd realtime-audio-fft-visualizer
pip install -r requirements.txt
