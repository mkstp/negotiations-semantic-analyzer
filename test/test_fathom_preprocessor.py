import fathom_preprocessor as fp

def test_convert_time():
    assert fp.convert_time(['00:00', '00:15', '1:00'], 120) == [15, 45, 60]