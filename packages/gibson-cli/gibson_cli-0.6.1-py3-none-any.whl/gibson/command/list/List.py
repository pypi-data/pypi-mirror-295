import sys

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand
from gibson.command.list.Entities import Entities
from gibson.command.list.Projects import Projects


class List(BaseCommand):
    def execute(self):
        if len(sys.argv) == 3 and sys.argv[2] == "entities":
            Entities(self.configuration).execute()
        elif len(sys.argv) == 3 and sys.argv[2] == "projects":
            Projects(self.configuration).execute()
        else:
            self.usage()

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command)} {Colors.subcommand('list')} {Colors.arguments(['entities', 'projects'])}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command)} {Colors.subcommand('list')} {Colors.argument('entities')} {Colors.hint('list all entities')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command)} {Colors.subcommand('list')} {Colors.argument('projects')} {Colors.hint('list all projects')}\n"
        )
        self.conversation.newline()
        exit(1)
