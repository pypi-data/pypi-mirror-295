from gibson.structure.constraints.ReferenceConstraint import ReferenceConstraint


class ForeignKey:
    def __init__(self):
        self.attributes = None
        self.name = None
        self.reference = None
        self.relationship = None
        self.symbol = None

    def json(self):
        return {
            "attributes": self.attributes,
            "name": self.name,
            "reference": self.reference.json(),
            "relationship": {"type": None},
            "sql": self.sql(),
            "symbol": self.symbol,
        }

    def sql(self):
        if self.attributes is None or self.attributes == []:
            raise RuntimeError("foreign key is missing attributes")

        if self.reference is None or not isinstance(
            self.reference, ReferenceConstraint
        ):
            raise RuntimeError("reference must be instance of ReferenceConstraint")

        parts = []
        if self.symbol is not None:
            parts.append(f"constraint {self.symbol}")

        parts.append("foreign key")
        if self.name is not None:
            parts.append(self.name)

        parts.append("(" + ", ".join(self.attributes) + ")")

        return " ".join(parts) + " " + self.reference.sql()
