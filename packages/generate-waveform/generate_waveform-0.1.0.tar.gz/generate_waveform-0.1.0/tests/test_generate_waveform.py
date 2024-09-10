import numpy as np
import pytest

from generate_waveform.generate_waveform.server import generate_waveform


def test_generate_waveform_sine():
    wave_type = 'sine'
    frequency = 440.0
    duration = 1.0
    sample_rate = 44100

    waveform = generate_waveform(wave_type, frequency, duration, sample_rate)
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    expected_waveform = np.sin(2 * np.pi * frequency * t).tolist()

    assert len(waveform) == len(expected_waveform)
    # relative tolerance for floating-point comparison
    assert np.allclose(waveform, expected_waveform, rtol=1e-5)


def test_generate_waveform_square():
    wave_type = 'square'
    frequency = 440.0
    duration = 1.0
    sample_rate = 44100

    waveform = generate_waveform(wave_type, frequency, duration, sample_rate)
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    expected_waveform = np.sign(np.sin(2 * np.pi * frequency * t)).tolist()

    assert len(waveform) == len(expected_waveform)
    assert np.allclose(waveform, expected_waveform, rtol=1e-5)


def test_generate_waveform_triangle():
    wave_type = 'triangle'
    frequency = 440.0
    duration = 1.0
    sample_rate = 44100

    waveform = generate_waveform(wave_type, frequency, duration, sample_rate)
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    expected_waveform = 2 * \
        np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
    expected_waveform = expected_waveform.tolist()

    assert len(waveform) == len(expected_waveform)
    assert np.allclose(waveform, expected_waveform, rtol=1e-5)


def test_generate_waveform_invalid_type():
    with pytest.raises(ValueError, match="Invalid wave_type. Supported types: sine, square, triangle"):
        generate_waveform('invalid', 440.0, 1.0, 44100)
