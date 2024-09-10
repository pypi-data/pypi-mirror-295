import gibson.core.Colors as Colors
from gibson.command.BaseCommand import BaseCommand
from gibson.core.Memory import Memory


class Help(BaseCommand):
    def execute(self):
        dev_off = ""
        dev_on = ""

        if self.configuration.project is not None:
            dev_off = "*" if self.configuration.project.dev.active is False else ""
            dev_on = "*" if self.configuration.project.dev.active is True else ""

        subcommands = {
            "auth": {
                "description": "login | logout",
                "memory": None,
            },
            "build": {
                "description": "create the entities in the datastore",
                "memory": "stored",
            },
            "code": {"description": "pair program", "memory": None},
            "conf": {"description": "set a configuration variable", "memory": None},
            "count": {
                "description": "show the number of entities stored",
                "memory": "last | stored",
            },
            "dev": {
                "description": f"mode off{dev_off} | on{dev_on}",
                "memory": None,
            },
            "forget": {
                "description": "delete memory",
                "memory": "all | last | stored",
            },
            "help": {"description": "for help", "memory": None},
            "import": {
                "description": "configure from a data source",
                "memory": "stored",
            },
            "list": {
                "description": "show the names of entities in your project",
                "memory": None,
            },
            "merge": {
                "description": "move last changes into project",
                "memory": "last -> stored",
            },
            "model": {
                "description": "write the model code for an entity",
                "memory": "stored",
            },
            "modify": {
                "description": "change an entity using natural language",
                "memory": "last > stored",
            },
            "new": {"description": "create something new", "memory": None},
            "openapi": {"description": "build from an OpenAPI spec", "memory": "last"},
            "remove": {
                "description": "remove an entity from the project",
                "memory": "last > stored",
            },
            "rename": {
                "description": "rename an entity",
                "memory": "last > stored",
            },
            "rewrite": {
                "description": "rewrite code",
                "memory": "stored",
            },
            "schema": {
                "description": "write the schema code for an entity",
                "memory": "stored",
            },
            "show": {"description": "display an entity", "memory": "last > stored"},
            "test": {
                "description": "write the unit tests for an entity",
                "memory": "stored",
            },
            "tree": {"description": "illustrate the project layout", "memory": None},
            "? | q": {"description": "ask a question", "memory": None},
        }

        self.conversation.set_delay(0.001)
        self.configuration.display_project()
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command)} {Colors.subcommand('[command]')}\n\n"
        )
        self.conversation.type(" command  description" + " " * 40 + "memory\n")
        self.conversation.type(" -------  -----------" + " " * 40 + "------\n")

        for subcommand, config in subcommands.items():
            memory = ""
            if config["memory"] is not None:
                memory = f"[{config['memory']}]"

            spaces = 61 - (8 + 2 + len(config["description"]))

            self.conversation.type(
                f"{Colors.subcommand(subcommand.rjust(8))}"
                + f"  {config['description']}"
                + " " * spaces
                + f"{Colors.hint(memory)}\n"
            )

        self.conversation.newline()

        if self.configuration.project is not None:
            self.conversation.type("memory:\n\n")
            stats = Memory(self.configuration).stats()
            self.conversation.type(
                f"{str(stats['entities']['num']).rjust(8)}"
                + f"  {stats['entities']['word']}"
                + " " * (43 if stats["entities"]["word"] == "entities" else 45)
                + "[stored]\n"
            )
            self.conversation.type(
                f"{str(stats['last']['num']).rjust(8)}"
                + f"  {stats['last']['word']}"
                + " " * (43 if stats["last"]["word"] == "entities" else 45)
                + "[last]\n\n"
            )
