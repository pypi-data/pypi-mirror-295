#!/usr/bin/env python3

from gibson.core.CommandRouter import CommandRouter
from gibson.core.Configuration import Configuration


def main():
    configuration = Configuration()
    if configuration.settings is None:
        configuration.initialize()
    else:
        router = CommandRouter(configuration).run()


if __name__ == "__main__":
    main()
