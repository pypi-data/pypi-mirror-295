class WorkspaceHeader:
    def render(self, project_name):
        return (
            f"Project {project_name}".ljust(50)
            + " " * 12
            + "[PAIR PROGRAMMER]\n"
            + "=" * 79
        )
