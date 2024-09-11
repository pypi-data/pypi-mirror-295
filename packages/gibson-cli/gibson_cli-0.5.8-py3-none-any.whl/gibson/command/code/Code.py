import sys

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand
from gibson.command.code.Entity import CodeEntity


class Code(BaseCommand):
    def execute(self):
        if len(sys.argv) == 4 and sys.argv[2] == "entity":
            CodeEntity(self.configuration).execute()
        else:
            self.usage()

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command)} {Colors.subcommand('code')} {Colors.argument('entity')} {Colors.input('[entity name]')} {Colors.hint('create a new entity')}\n"
        )
        self.conversation.newline()
        self.conversation.type(
            '  To create a new entity named "user":\n'
            f"      {Colors.command(self.configuration.command)} {Colors.subcommand('code')} {Colors.argument('entity')} {Colors.input('user')}\n"
        )
        self.conversation.newline()
        exit(1)
