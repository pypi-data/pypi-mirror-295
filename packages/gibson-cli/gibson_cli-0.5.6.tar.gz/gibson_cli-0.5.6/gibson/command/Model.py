import sys

import gibson.core.Colors as Colors
from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.core.TimeKeeper import TimeKeeper
from gibson.dev.Dev import Dev


class Model(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3:
            self.usage()

        self.configuration.require_project()
        entity = self.memory.recall_stored_entity(sys.argv[2])
        if entity is None:
            self.conversation.not_sure_no_entity(
                self.configuration.project.name, sys.argv[2]
            )
            exit(1)

        time_keeper = TimeKeeper()

        cli = Cli(self.configuration)
        response = cli.code_models([entity["name"]])

        Dev(self.configuration).model(
            response["code"][0]["entity"]["name"], response["code"][0]["definition"]
        )

        print(response["code"][0]["definition"])
        time_keeper.display()

    def usage(self):
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command)} {Colors.subcommand('model')} {Colors.input('[entity name]')} {Colors.hint('generate the model for an entity')}\n"
        )
        self.conversation.newline()
        exit(1)
