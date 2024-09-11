import re

import gibson.core.Colors as Colors
from gibson.api.ProjectApi import ProjectApi
from gibson.command.BaseCommand import BaseCommand


class Projects(BaseCommand):
    def execute(self):
        self.configuration.require_login()
        projects = ProjectApi(self.configuration).all_projects()

        if len(projects) == 0:
            self.conversation.type(
                f"No projects found. Create one with {Colors.command('gibson')} {Colors.subcommand('new')} {Colors.argument('project')}\n"
            )
            exit(1)

        self.conversation.type("Name".ljust(40))
        self.conversation.type("ID")
        self.conversation.newline()
        self.conversation.type("----".ljust(40))
        self.conversation.type("-" * 36)
        self.conversation.newline()

        for project in projects:
            name = project["name"] if project["name"] is not None else "Untitled"
            name = re.sub(r"^(.{36}).*$", "\g<1>...", name).ljust(40)
            self.conversation.type(f"{Colors.command(name)}")
            self.conversation.type(f"{project['uuid']}")
            self.conversation.newline()
