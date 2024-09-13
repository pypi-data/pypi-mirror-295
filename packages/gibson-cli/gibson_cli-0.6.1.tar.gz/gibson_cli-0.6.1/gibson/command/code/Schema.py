import sys

import gibson.core.Colors as Colors
from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.core.TimeKeeper import TimeKeeper
from gibson.dev.Dev import Dev


class CodeSchema(BaseCommand):
    def execute(self):
        self.configuration.require_project()
        entity = self.memory.recall_stored_entity(sys.argv[3])
        if entity is None:
            self.conversation.not_sure_no_entity(
                self.configuration.project.name, sys.argv[3]
            )
            exit(1)

        time_keeper = TimeKeeper()

        cli = Cli(self.configuration)
        response = cli.code_schemas([entity["name"]])

        Dev(self.configuration).schema(
            response["code"][0]["entity"]["name"], response["code"][0]["definition"]
        )

        if self.configuration.project.dev.active is True:
            self.conversation.type(
                f"Gibson wrote the following {Colors.argument('schema')} code to your project:\n"
            )

        print(response["code"][0]["definition"])
        time_keeper.display()
