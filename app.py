import streamlit as st
from streamlit_webrtc import webrtc_streamer
import numpy as np
import matplotlib.pyplot as plt
import av

# Title
st.title("🎙️ Real-Time Audio Capture in Streamlit Cloud")

# WebRTC microphone streamer
webrtc_ctx = webrtc_streamer(key="mic", audio=True, video=False)

# Create placeholders for plots
col1, col2 = st.columns(2)  # Use two columns for layout
waveform_plot = col1.empty()
energy_plot = col2.empty()

# Function to process audio frames
def process_audio_frame(audio_frame: av.AudioFrame):
    """Extracts raw audio data from the WebRTC audio stream."""
    audio_data = np.array(audio_frame.to_ndarray())  # Convert audio to NumPy array
    return audio_data

# Live audio processing loop
if webrtc_ctx.audio_receiver:
    while True:
        # Get the latest audio frame
        audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
        if not audio_frames:
            continue

        # Process the audio frame
        audio_data = process_audio_frame(audio_frames[0])

        # Compute energy
        energy = np.sum(audio_data ** 2) / len(audio_data)

        # Plot waveform
        fig_wave, ax_wave = plt.subplots(figsize=(6, 3))
        ax_wave.plot(audio_data, color='blue')
        ax_wave.set_title("Audio Waveform (Live)")
        ax_wave.set_xlabel("Samples")
        ax_wave.set_ylabel("Amplitude")
        waveform_plot.pyplot(fig_wave)
        plt.close(fig_wave)  # Prevent memory leaks

        # Plot energy
        fig_energy, ax_energy = plt.subplots(figsize=(4, 3))
        ax_energy.bar(["Energy"], [energy], color='red')
        ax_energy.set_ylim(0, max(energy * 1.2, 0.1))  # Auto-scale y-axis
        ax_energy.set_title("Signal Energy")
        energy_plot.pyplot(fig_energy)
        plt.close(fig_energy)  # Prevent memory leaks

