from gibson.display.WorkspaceHeader import WorkspaceHeader


def test_render():
    assert WorkspaceHeader().render("abc def ghi") == (
        """Project abc def ghi                                           [PAIR PROGRAMMER]
==============================================================================="""
    )
