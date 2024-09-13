import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import gibson.core.Colors as Colors
from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.command.importer.OpenApi import OpenApi
from gibson.command.rewrite.Rewrite import Rewrite
from gibson.db.TableExceptions import TableExceptions


class Import(BaseCommand):
    def execute(self):
        self.configuration.require_project()
        write_code = False

        if len(sys.argv) == 3 and sys.argv[2] == "api":
            entities = self.__import_from_api()
            write_code = self.configuration.project.dev.active
        elif len(sys.argv) == 3 and sys.argv[2] == "datastore":
            entities = self.__import_from_datastore()
            write_code = self.configuration.project.dev.active
        elif len(sys.argv) == 4 and sys.argv[2] == "openapi":
            return OpenApi(self.configuration).execute()
        else:
            self.usage()

        self.memory.remember_entities(entities)

        word_entities = "entity" if len(entities) == 1 else "entities"

        self.conversation.type("\nSummary\n")
        self.conversation.type(f"    {len(entities)} {word_entities} imported\n")
        self.conversation.newline()

        if write_code:
            Rewrite(self.configuration).write()
            self.conversation.newline()

        return True

    def __import_from_api(self):
        self.configuration.display_project()

        self.conversation.type("Connected to API...\n")
        response = Cli(self.configuration).import_()
        self.conversation.type("Building schema...\n")

        for entity in response["project"]["entities"]:
            self.conversation.type(f"    {entity['name']}\n", delay=0.002)

        return response["project"]["entities"]

    def __import_from_datastore(self):
        self.configuration.display_project()

        db = create_engine(self.configuration.project.datastore.uri)
        session = sessionmaker(autocommit=False, autoflush=False, bind=db)()

        table_exceptions = TableExceptions().universal()
        if self.configuration.project.datastore.type == "mysql":
            table_exceptions = TableExceptions().mysql()

        self.conversation.type("Connected to datastore...\n")
        self.conversation.type("Building schema...\n")

        tables = session.execute("show tables").all()

        entities = []
        for table in tables:
            if table[0] not in table_exceptions:
                self.conversation.type(f"    {table[0]}\n", delay=0.002)

                create_statement = session.execute(
                    f"show create table {table[0]}"
                ).one()

                entities.append(
                    {"definition": str(create_statement[1]), "name": str(table[0])}
                )

        return entities

    def usage(self):
        self.configuration.display_project()
        datastore_uri = (
            self.configuration.project.datastore.uri
            if self.configuration.project
            else ""
        )
        self.conversation.type(
            f"usage: {Colors.command(self.configuration.command)} {Colors.subcommand('import')} {Colors.arguments(['api', 'datastore', 'openapi'])} {Colors.hint('import entities')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command)} {Colors.subcommand('import')} {Colors.argument('api')} {Colors.hint(f'import all entities from your project created on {Colors.link(self.configuration.app_domain())}')}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command)} {Colors.subcommand('import')} {Colors.argument('datastore')} {Colors.hint('import all entities from your local datastore')} {Colors.link(datastore_uri)}\n"
        )
        self.conversation.type(
            f"       {Colors.command(self.configuration.command)} {Colors.subcommand('import')} {Colors.argument('openapi')} {Colors.input('path/to/openapi.json')} {Colors.hint('import all entities from an OpenAPI spec file')}\n"
        )
        self.conversation.newline()
        exit(1)
