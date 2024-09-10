import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import gibson.core.Colors as Colors
from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.command.rewrite.Rewrite import Rewrite
from gibson.db.TableExceptions import TableExceptions


class Import(BaseCommand):
    def execute(self):
        if len(sys.argv) != 3 and len(sys.argv) != 5:
            self.usage()

        self.configuration.require_project()
        write_code = False
        if len(sys.argv) == 5:
            if sys.argv[3] != ".." or sys.argv[4] != "dev":
                self.usage()

            if self.configuration.project.dev.active is False:
                self.configuration.display_project()
                self.conversation.type(
                    "Dude, seriously?! You have Dev Mode turned off. "
                    + "Why would you do that?\n"
                )
                self.conversation.newline()
                exit(1)

            write_code = True

        if sys.argv[2] == "api":
            entities = self.__import_from_api()
        elif sys.argv[2] == "datastore":
            entities = self.__import_from_datastore()
        else:
            self.usage()

        self.memory.remember_entities(entities)

        word_entities = "entities"
        if len(entities) == 1:
            word_entities = "entity"

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

        entities = []
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
            f"usage: {Colors.command(self.configuration.command)} {Colors.subcommand('import')} {Colors.argument('api')} {Colors.hint('import all entities from your project created on GibsonAI.com')}\n"
        )
        self.conversation.type(
            f"   or: {Colors.command(self.configuration.command)} {Colors.subcommand('import')} {Colors.argument('datastore')} {Colors.hint('import all entities from your local datastore')} {datastore_uri}\n"
        )
        self.conversation.type(
            f"   or: {Colors.command(self.configuration.command)} {Colors.subcommand('import')} {Colors.arguments(['api', 'datastore'])} {Colors.option('.. dev')} {Colors.hint('have dev mode write all the code')}\n"
        )
        self.conversation.newline()
        exit(1)
