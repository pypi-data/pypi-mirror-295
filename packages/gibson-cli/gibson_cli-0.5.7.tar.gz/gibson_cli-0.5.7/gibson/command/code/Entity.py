import os
import sys
from string import Template

from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.command.Merge import Merge
from gibson.command.rewrite.Rewrite import Rewrite
from gibson.core.Configuration import Configuration
from gibson.display.Header import Header
from gibson.display.WorkspaceFooter import WorkspaceFooter
from gibson.display.WorkspaceHeader import WorkspaceHeader
from gibson.services.code.context.schema.Manager import (
    Manager as CodeContextSchemaManager,
)
from gibson.structure.Entity import Entity


class CodeEntity(BaseCommand):
    CODE_WRITER_ENTITY_MODIFIER_NOOP = ""

    def __init__(self, configuration: Configuration):
        super().__init__(configuration)
        self.__context = None

    def __add_foreign_key(self, entity, entity_name):
        entity_keys = self.__context.get_entity_keys(entity_name)
        if entity_keys is None:
            self.conversation.type(
                f'\nThe entity you referenced, "{entity_name}", does not exist.\n'
            )
            self.conversation.wait()
            return False

        best_sql_foreign_key = entity_keys.best_sql_foreign_key()
        if best_sql_foreign_key is None:
            self.conversation.type(
                f'\nYou cannot make a foreign key to "{entity_name}".\n'
                + "It does not have primary or unique keys.\n"
            )
            self.conversation.wait()
            return False

        foreign_key, index, data_types = best_sql_foreign_key

        for i in range(len(foreign_key.attributes)):
            entity.add_attribute(
                foreign_key.attributes[i],
                data_types[i],
                after="uuid",
                before="date_created",
            )

        entity.add_foreign_key(foreign_key)
        entity.add_index(index)

        return True

    def configure_definition(self):
        existing_entity = self.memory.recall_entity(sys.argv[3])
        if existing_entity is not None:
            return existing_entity["definition"]

        parts = sys.argv[3].split("_")
        if len(parts) > 1 and parts[1] == "ref":
            # This is a reference table implementation. We will handle this here.
            with open(self.get_default_ref_table_template_path()) as f:
                definition = Template(f.read()).substitute({"entity_name": sys.argv[3]})

                self.memory.append_last({"definition": definition, "name": sys.argv[3]})

                self.conversation.type(
                    "Reference table created and stored in last memory. What's next?\n"
                )
                self.conversation.newline()

                exit(1)

        with open(self.get_default_table_template_path()) as f:
            return Template(f.read()).substitute({"entity_name": sys.argv[3]})

    def execute(self):
        cli = Cli(self.configuration)

        self.configuration.require_project()
        definition = self.configure_definition()

        self.__context = CodeContextSchemaManager().from_code_writer_schema_context(
            cli.code_writer_schema_context()
        )

        data = cli.code_writer_entity_modifier(
            self.__context.json,
            sys.argv[3],
            definition,
            self.CODE_WRITER_ENTITY_MODIFIER_NOOP,
        )
        entity = Entity().import_from_struct(data)

        while True:
            self.__render_workspace(entity, data["code"][0]["definition"])

            input_ = input("> ")
            if input_ in [".", ":q", ":w"]:
                self.conversation.newline()

                if input_ == ":q":
                    exit(1)

                self.memory.remember_last({"entities": [data["entity"]]})

                if input_ == ".":
                    self.conversation.type(
                        "Damn we write good code. I stored this in last memory. "
                        + "Your move.\n"
                    )
                else:
                    self.conversation.mute()
                    Merge(self.configuration).execute()
                    self.conversation.unmute()

                    Rewrite(self.configuration, wipe=False).write()

                self.conversation.newline()

                exit(1)
            elif input_ == "":
                continue

            talk_to_gibsonai = True

            parts = input_.split(" ")
            if parts[0] == "fk":
                input_ = self.CODE_WRITER_ENTITY_MODIFIER_NOOP
                if not self.__add_foreign_key(entity, parts[1]):
                    # If the entity was not modified, likely because the table
                    # referenced does not exist or does not contain indexes which
                    # can be used for a foreign key, do not waste the network call
                    # to GibsonAI since there is nothing to do.
                    talk_to_gibsonai = False

            if talk_to_gibsonai is True:
                data = cli.code_writer_entity_modifier(
                    self.__context.json,
                    data["entity"]["name"],
                    entity.create_statement(),
                    input_,
                )
                entity = Entity().import_from_struct(data)

    def get_default_ref_table_template_path(self):
        return os.path.dirname(__file__) + "/../../data/default-ref-table.tmpl"

    def get_default_table_template_path(self):
        return os.path.dirname(__file__) + "/../../data/default-table.tmpl"

    def __render_workspace(self, entity: Entity, model):
        self.configuration.platform.cmd_clear()

        print("")
        print(WorkspaceHeader().render(self.configuration.project.name))

        print("")
        print(Header().render("SQL"))
        print("")
        print(entity.create_statement())

        print("")
        print(Header().render("Model"))
        print("")
        print(model)

        print("")
        print(WorkspaceFooter().render())
