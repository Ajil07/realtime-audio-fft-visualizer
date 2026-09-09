
import os
import queue
import sys
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

CHUNK_SIZE = 2048
audio_queue = queue.Queue()


def run_microphone():
  sample_rate = 44100

  def callback(indata, frames, time_info, status):
    if status:
      print(status, file=sys.stderr)
    audio_queue.put(indata[:, 0].copy())

  stream = sd.InputStream(
      samplerate=sample_rate,
      blocksize=CHUNK_SIZE,
      channels=1,
      callback=callback,
  )
  return stream, sample_rate


def run_wav_file(file_path):
  try:
    import soundfile as sf
  except ImportError:
    print("\nError: Please install soundfile first: py -m pip install soundfile")
    sys.exit(1)

  if not os.path.exists(file_path):
    print(f"\nError: File '{file_path}' not found.")
    sys.exit(1)

  wav_data, sample_rate = sf.read(file_path, dtype="float32")

  # Downmix stereo to mono if necessary
  if wav_data.ndim > 1:
    wav_data = np.mean(wav_data, axis=1)

  current_idx = 0
  total_frames = len(wav_data)

  def callback(outdata, frames, time_info, status):
    nonlocal current_idx
    if status:
      print(status, file=sys.stderr)

    remaining = total_frames - current_idx
    chunk_len = min(frames, remaining)

    if chunk_len > 0:
      chunk = wav_data[current_idx : current_idx + chunk_len]
      if chunk_len < frames:
        chunk = np.pad(chunk, (0, frames - chunk_len))

      outdata[:, 0] = chunk
      audio_queue.put(chunk.copy())
      current_idx += chunk_len
    else:
      outdata.fill(0)
      raise sd.CallbackStop()

  stream = sd.OutputStream(
      samplerate=sample_rate,
      blocksize=CHUNK_SIZE,
      channels=1,
      callback=callback,
  )
  return stream, sample_rate


# --- CLI Selection ---
print("========================================")
print(" Real-Time Audio FFT Spectrum Analyzer  ")
print("========================================")
print("1. Live Microphone Input")
print("2. Play and Analyze WAV File")
choice = input("\nSelect Mode (1 or 2): ").strip()

if choice == "2":
  wav_path = input("Enter path to .wav file: ").strip().strip('"')
  stream, sample_rate = run_wav_file(wav_path)
else:
  stream, sample_rate = run_microphone()

# --- FFT Bins & Windowing ---
freq_bins = np.fft.rfftfreq(CHUNK_SIZE, d=1.0 / sample_rate)
hanning_window = np.hanning(CHUNK_SIZE)

# --- Matplotlib Canvas Setup ---
fig, ax = plt.subplots(figsize=(10, 5))
(line,) = ax.plot(freq_bins, np.zeros(len(freq_bins)), color="#00ffcc", lw=1.2)
peak_text = ax.text(
    0.70,
    0.90,
    "",
    transform=ax.transAxes,
    color="#ff007f",
    fontsize=11,
    weight="bold",
)

ax.set_facecolor("#121212")
fig.patch.set_facecolor("#121212")
ax.grid(True, color="#2a2a2a", linestyle="--", linewidth=0.7)

title_label = "WAV Playback FFT" if choice == "2" else "Microphone Live FFT"
ax.set_title(title_label, color="white", fontsize=12)
ax.set_xlabel("Frequency (Hz)", color="white")
ax.set_ylabel("Magnitude (dB)", color="white")
ax.set_xscale("log")
ax.set_xlim(20, sample_rate / 2)
ax.set_ylim(-60, 40)
ax.tick_params(colors="white")


def update_plot(frame):
  data = None
  while not audio_queue.empty():
    data = audio_queue.get_nowait()

  if data is not None and len(data) == CHUNK_SIZE:
    windowed = data * hanning_window
    fft_complex = np.fft.rfft(windowed)
    magnitude = np.abs(fft_complex) / CHUNK_SIZE
    magnitude_db = 20 * np.log10(magnitude + 1e-6)
    line.set_ydata(magnitude_db)

    # Detect dominant pitch (excluding 0 Hz DC offset)
    peak_idx = np.argmax(magnitude_db[1:]) + 1
    peak_freq = freq_bins[peak_idx]
    peak_text.set_text(f"Peak: {peak_freq:6.1f} Hz")

  return line, peak_text


with stream:
  ani = animation.FuncAnimation(
      fig, update_plot, interval=25, blit=True, cache_frame_data=False
  )
  plt.tight_layout()
  plt.show()