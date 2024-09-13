import sys

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand
from gibson.command.code.Entity import CodeEntity
from gibson.command.new.Module import NewModule
from gibson.command.new.Project import NewProject


class New(BaseCommand):
    def execute(self):
        if len(sys.argv) == 3 and sys.argv[2] == "project":
            NewProject(self.configuration).execute()
        elif len(sys.argv) == 3 and sys.argv[2] == "module":
            NewModule(self.configuration).execute()
        elif len(sys.argv) == 4 and sys.argv[2] == "entity":
            CodeEntity(self.configuration).execute()
        else:
            self.usage()

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command)} {Colors.subcommand('new')} {Colors.arguments(['project', 'module', 'entity'])} {Colors.hint('create something new')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command)} {Colors.subcommand('new')} {Colors.argument('project')} {Colors.hint('create a new project')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command)} {Colors.subcommand('new')} {Colors.argument('module')} {Colors.hint('create a new module')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command)} {Colors.subcommand('new')} {Colors.argument('entity')} {Colors.input('[entity name]')} {Colors.hint('create a new entity')}\n"
        )
        self.conversation.newline()
        exit(1)
