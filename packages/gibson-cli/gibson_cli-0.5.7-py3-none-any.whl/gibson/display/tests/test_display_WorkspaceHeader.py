from gibson.display.WorkspaceHeader import WorkspaceHeader


def test_render():
    assert WorkspaceHeader().render("abc def ghi") == (
        """Workspace abc def ghi                                          [CONTEXT LOADED]
==============================================================================="""
    )
