import hashlib
import sys

from gibson.command.BaseCommand import BaseCommand
from gibson.core.Conversation import Conversation


class WarGames(BaseCommand):
    def execute(self):
        if hashlib.sha256(" ".join(sys.argv[1:]).lower().encode()).hexdigest() != (
            "17dca0c0f6b4fe47e18b34551e3e65d1b91b88c94011be4de552bb64e443f6fc"
        ):
            return False

        self.conversation.newline()
        self.conversation.type("FALKEN'S WEB\n")
        self.conversation.type("BLACK JACK\n")
        self.conversation.type("GIN RUMMY\n")
        self.conversation.type("HEARTS\n")
        self.conversation.type("BRIDGE\n")
        self.conversation.type("CHECKERS\n")
        self.conversation.type("CHESS\n")
        self.conversation.type("POKER\n")
        self.conversation.type("FIGHTER COMBAT\n")
        self.conversation.type("GUERRILLA ENGAGEMENT\n")
        self.conversation.type("DESERT WARFARE\n")
        self.conversation.type("AIR-TO-GROUND ACTIONS\n")
        self.conversation.type("THEATERWIDE TACTICAL WARFARE\n")
        self.conversation.type("THEATERWIDE BIOTOXIC AND CHEMICAL WARFARE\n")
        self.conversation.newline()
        self.conversation.type("GLOBAL THERMONUCLEAR WAR\n", delay=0.2)
        self.conversation.newline()

        return True
