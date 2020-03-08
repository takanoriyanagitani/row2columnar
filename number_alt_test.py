import number_alt

def test_number_alt_float_none():
  assert 0.0 == number_alt.number_alt_float_none()
  assert 0.0 == number_alt.number_alt_float_none(0.0)
  assert 0.0 == number_alt.number_alt_float_none(0.0, 0.0)
  assert 0.0 == number_alt.number_alt_float_none(None, 0.0)
  assert 1.0 == number_alt.number_alt_float_none(None, 1.0)
  assert 1.0 == number_alt.number_alt_float_none(1.0,  0.0)

def test_number_alt_float_nan():
  assert 0.0 == number_alt.number_alt_float_nan()
  assert 0.0 == number_alt.number_alt_float_nan(float("nan"))
  assert 0.0 == number_alt.number_alt_float_nan(float("nan"), 0.0)
  assert 1.0 == number_alt.number_alt_float_nan(float("nan"), 1.0)
  assert 1.0 == number_alt.number_alt_float_nan(1.0, 0.0)

def test_number_alt_float_nn():
  assert 0.0 == number_alt.number_alt_float_nn()
  assert 0.0 == number_alt.number_alt_float_nn(None)
  assert 0.0 == number_alt.number_alt_float_nn(None, 0.0)
  assert 0.0 == number_alt.number_alt_float_nn(float("nan"), 0.0)
  assert 1.0 == number_alt.number_alt_float_nn(float("nan"), 1.0)
  assert 1.0 == number_alt.number_alt_float_nn(None, 1.0)
  assert 1.0 == number_alt.number_alt_float_nn(1.0, 0.0)
