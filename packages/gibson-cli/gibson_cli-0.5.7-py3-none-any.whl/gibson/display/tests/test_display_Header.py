from gibson.display.Header import Header


def test_render():
    assert Header().render("abc def ghi") == (
        """+--------------------------------------------------------------+
| abc def ghi                                                  |
+--------------------------------------------------------------+"""
    )
