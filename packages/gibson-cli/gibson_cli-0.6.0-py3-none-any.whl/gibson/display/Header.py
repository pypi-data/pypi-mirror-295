class Header:
    def render(self, text):
        header = "+--------------------------------------------------------------+\n"
        header += "| " + text + " " * (61 - len(text)) + "|\n"
        header += "+--------------------------------------------------------------+"
        return header
