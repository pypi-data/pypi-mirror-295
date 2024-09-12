from krri_common.utils.krri_math import KRRIMath


def test_divide_precision():
    expected = KRRIMath.divide_precision(0.00012, 0.00004)
    assert expected == 3
