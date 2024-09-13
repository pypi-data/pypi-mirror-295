from gibson.display.WorkspaceFooter import WorkspaceFooter


def test_render():
    assert WorkspaceFooter().render() == (
        """===============================================================================
[. + enter = exit] [:q + enter = abort] [:w + enter = merge + write code]
Using natural language, tell me how I can modify this entity."""
    )
