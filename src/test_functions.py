"""
Marc St. Pierre
Testing helper functions using pytest
"""

import fathom_preprocessor as fpp

def test_convert_time():
    assert fpp.convert_time(['00:00', '00:15', '1:00'], 120) == [15, 45, 60]
    assert fpp.convert_time(['00:01', '00:15', '1:00'], 120) == [14, 45, 60]
    assert fpp.convert_time(['00:00', '00:00', '1:00'], 60) == [1, 60, 1]

def test_process_speaker_names():
    assert fpp.process_speaker_names([" a\n\r"], False) == ["a"]
    assert fpp.process_speaker_names(["a", "b", "a", "b"], True) == ["Speaker0", "Speaker1", "Speaker0", "Speaker1"]