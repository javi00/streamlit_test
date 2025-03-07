import streamlit as st
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time

# Set Streamlit page config (no wide layout)
st.set_page_config(page_title="Real-Time Audio Visualizer")

# Sidebar for settings (optional for future adjustments)
st.sidebar.title("Audio Settings")
st.sidebar.write("Future options can be added here.")

# Audio capture settings
SAMPLE_RATE = 16000  # Sample rate in Hz
DURATION = 0.5  # Time window in seconds
BUFFER_SIZE = int(SAMPLE_RATE * DURATION)  # Number of samples in the buffer
audio_buffer = np.zeros(BUFFER_SIZE)  # Circular buffer for audio storage

# Create placeholders for plots
col1, col2 = st.columns(2)  # Use two columns for a compact layout
waveform_plot = col1.empty()
energy_plot = col2.empty()

# Function to capture audio
def audio_callback(indata, frames, time, status):
    """Callback function to store real-time audio in a buffer."""
    global audio_buffer
    if status:
        print(status)
    audio_buffer = np.roll(audio_buffer, -frames)  # Shift old samples
    audio_buffer[-frames:] = indata[:, 0]  # Insert new samples

# Start real-time audio stream
stream = sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    callback=audio_callback,
    blocksize=int(SAMPLE_RATE * 0.1)  # Update every 100ms
)
stream.start()

# **Real-Time Loop**
while True:
    # Copy latest buffer data
    data = np.copy(audio_buffer)

    # Compute energy
    energy = np.sum(data ** 2) / len(data)

    # Plot waveform with a compact size
    fig_wave, ax_wave = plt.subplots(figsize=(6, 3))  # Smaller width & height
    ax_wave.plot(data, color='blue')
    ax_wave.set_title("Audio Waveform (Live)")
    ax_wave.set_xlabel("Samples")
    ax_wave.set_ylabel("Amplitude")
    waveform_plot.pyplot(fig_wave)  # Update waveform plot
    plt.close(fig_wave)  # Prevent memory leak

    # Plot energy with a compact size
    fig_energy, ax_energy = plt.subplots(figsize=(6, 3))  # Smaller bar chart
    ax_energy.bar(["Energy"], [energy], color='red')
    ax_energy.set_ylim(0, 0.1)  # Set y-limit for better visualization
    ax_energy.set_title("Signal Energy")
    energy_plot.pyplot(fig_energy)  # Update energy plot
    plt.close(fig_energy)  # Prevent memory leak

    # Control refresh rate
    time.sleep(0.1)  # Update every 100ms
