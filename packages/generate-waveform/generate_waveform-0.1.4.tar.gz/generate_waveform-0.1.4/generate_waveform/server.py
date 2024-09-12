from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse

app = FastAPI()


# Endpoint to generate and return waveform PNG
@app.get("/generate_waveform/")
async def get_waveform(
    wave_type: str = Query(...,
                           description="Type of wave: sine, square, or triangle"),
    frequency: float = Query(
        440.0, description="Frequency of the waveform in Hz"),
    duration: float = Query(
        1.0, description="Duration of the waveform in seconds"),
    sample_rate: int = Query(
        44100, description="Sample rate in samples per second"),
    output_format: str = Query(
        "json", description="Output format of the wave: json, png")
):
    waveform = generate_waveform(
        wave_type, frequency, duration, sample_rate)

    if output_format.lower() == 'json':
        return waveform

    time = np.linspace(0, duration, len(waveform),
                       endpoint=False)  # Create time axis

    plt.figure(figsize=(10, 4))
    plt.plot(time, waveform)
    plt.title(f"{wave_type.capitalize()} Wave - Frequency: {frequency} Hz")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)

    # Save plot to BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()  # Close the plot to avoid displaying in an interactive environment
    buf.seek(0)

    # Return PNG image as streaming response
    return StreamingResponse(buf, media_type="image/png")


def generate_waveform(wave_type, frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    if wave_type == 'sine':
        waveform = np.sin(2 * np.pi * frequency * t)
    elif wave_type == 'square':
        waveform = np.sign(np.sin(2 * np.pi * frequency * t))
    elif wave_type == 'triangle':
        waveform = 2 * \
            np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
    else:
        raise ValueError(
            "Invalid wave_type. Supported types: sine, square, triangle")

    return waveform.tolist()
