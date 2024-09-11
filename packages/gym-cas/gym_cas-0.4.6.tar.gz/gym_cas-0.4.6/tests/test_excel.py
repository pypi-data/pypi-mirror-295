from gym_cas import excel_read


def test_excel_read_without_module():
    data = None
    try:
        data = excel_read("test.xlsx", "A1:C3")
    except ImportError:
        assert True
    assert data is None
