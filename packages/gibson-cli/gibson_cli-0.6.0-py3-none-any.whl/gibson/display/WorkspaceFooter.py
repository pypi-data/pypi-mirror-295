class WorkspaceFooter:
    def render(self):
        return (
            "=" * 79
            + "\n"
            + "[. + enter = exit] "
            + "[:q + enter = abort] "
            + "[:w + enter = merge + write code]\n"
            + "Using natural language, tell me how I can modify this entity."
        )
