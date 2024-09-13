import sys

import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand
from gibson.command.code.Entity import CodeEntity
from gibson.command.code.Model import CodeModel
from gibson.command.code.Schema import CodeSchema
from gibson.command.code.Tests import CodeTests


class Code(BaseCommand):
    def execute(self):
        if len(sys.argv) == 4 and sys.argv[2] == "entity":
            CodeEntity(self.configuration).execute()
        elif len(sys.argv) == 4 and sys.argv[2] == "model":
            CodeModel(self.configuration).execute()
        elif len(sys.argv) == 4 and sys.argv[2] == "schema":
            CodeSchema(self.configuration).execute()
        elif len(sys.argv) == 4 and sys.argv[2] == "tests":
            CodeTests(self.configuration).execute()
        else:
            self.usage()

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command)} {Colors.subcommand('code')} {Colors.arguments(['entity', 'model', 'schema', 'tests'])} {Colors.input('[entity name]')} {Colors.hint('write code')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command)} {Colors.subcommand('code')} {Colors.argument('entity')} {Colors.input('[entity name]')} {Colors.hint('create or update an entity using the AI pair programmer')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command)} {Colors.subcommand('code')} {Colors.argument('model')} {Colors.input('[entity name]')} {Colors.hint('generate the model code for an entity')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command)} {Colors.subcommand('code')} {Colors.argument('schema')} {Colors.input('[entity name]')} {Colors.hint('generate the schema code for an entity')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command)} {Colors.subcommand('code')} {Colors.argument('tests')} {Colors.input('[entity name]')} {Colors.hint('generate the unit tests for an entity')}\n"
        )
        self.conversation.newline()
        exit(1)
