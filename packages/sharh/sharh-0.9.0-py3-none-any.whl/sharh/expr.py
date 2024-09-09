from __future__ import annotations

from functools import reduce
from typing import Dict, List

VAR_MAPPING = {
    "http.method": "request_method",
    "http.version": "server_protocol",
    "ip.geoip.country": "geoip2_data_country_iso_code",
    "ip.geoip.continent": "geoip2_data_continent_code",
    "ip.geoip.asn": "geoip2_data_asn",
    "ip.addr": "remote_addr",
    "http.headers": "headers",
    "http.headers.user_agent": "http_user_agent",
    "http.headers.x_forwarded_for": "http_x_forwarded_for",
    "http.headers.referer": "http_referer",
    "http.secure": "scheme",
}


def add_literal_literal(l1: Literal, l2: Literal):
    return Disjunction([Conjunction([l1]), Conjunction([l2])])


def add_literal_conjunction(
    literal: Literal, conjunction: Conjunction, literal_first=True
):
    if literal_first:
        return Disjunction([Conjunction([literal]), conjunction])
    return Disjunction([conjunction, Conjunction([literal])])


def add_literal_disjunction(
    literal: Literal, disjunction: Disjunction, literal_first=True
):
    if literal_first:
        return Disjunction([Conjunction([literal]), *disjunction.conjunctions])
    return Disjunction([*disjunction.conjunctions, Conjunction([literal])])


def add_conjunction_conjunction(c1: Conjunction, c2: Conjunction):
    return Disjunction([c1, c2])


def add_conjunction_disjunction(
    conjunction: Conjunction, disjunction: Disjunction, conjunction_first=True
):
    if conjunction_first:
        return Disjunction([conjunction, *disjunction.conjunctions])
    return Disjunction([*disjunction.conjunctions, conjunction])


def add_disjunction_disjunction(d1: Disjunction, d2: Disjunction):
    return Disjunction([*d1.conjunctions, *d2.conjunctions])


def mul_literal_literal(l1: Literal, l2: Literal):
    return Conjunction([l1, l2])


def mul_literal_conjunction(
    literal: Literal, conjunction: Conjunction, literal_first=True
):
    if literal_first:
        return Conjunction([literal, *conjunction.literals])
    return Conjunction([*conjunction.literals, literal])


def mul_literal_disjunction(
    literal: Literal, disjunction: Disjunction, literal_first=True
):
    return Disjunction(
        list(
            map(
                lambda c: mul_literal_conjunction(
                    literal=literal, conjunction=c, literal_first=literal_first
                ),
                disjunction.conjunctions,
            )
        )
    )


def mul_conjunction_conjunction(c1: Conjunction, c2: Conjunction):
    return Conjunction([*c1.literals, *c2.literals])


def mul_conjunction_disjunction(
    conjunction: Conjunction, disjunction: Disjunction, conjunction_first=True
):
    if conjunction_first:
        return Disjunction(
            list(
                map(
                    lambda d: mul_conjunction_conjunction(conjunction, d),
                    disjunction.conjunctions,
                )
            )
        )

    return Disjunction(
        list(
            map(
                lambda d: mul_conjunction_conjunction(d, conjunction),
                disjunction.conjunctions,
            )
        )
    )


def mul_disjunction_disjunction(d1: Disjunction, d2: Disjunction):
    return reduce(
        lambda i, j: Disjunction([*i.conjunctions, *j.conjunctions]),
        map(
            lambda c: mul_conjunction_disjunction(c, d1, conjunction_first=False),
            d2.conjunctions,
        ),
        Disjunction([]),
    )


class DSLOperators:
    EQ = "=="
    NEQ = "!="
    GE = ">="
    LE = "<="
    HAS = "has"
    NOT_HAS = "!has"
    CONTAINS = "contains"
    NOT_CONTAINS = "!contains"
    IN = "in"
    NOT_IN = "!in"


class EXPROperators:
    NOT = "!"
    EQ = "=="
    NEQ = "~="
    GE = ">="
    LE = "<="
    HAS = "has"
    CONTAINS = "~~"
    IN = "in"
    IP_IN = "ipmatch"


class Literal:
    EXPR_OP = {
        DSLOperators.EQ: [EXPROperators.EQ],
        DSLOperators.NEQ: [EXPROperators.NEQ],
        DSLOperators.GE: [EXPROperators.GE],
        DSLOperators.LE: [EXPROperators.LE],
        DSLOperators.HAS: [EXPROperators.HAS],
        DSLOperators.NOT_HAS: [EXPROperators.NOT, EXPROperators.HAS],
        DSLOperators.CONTAINS: [EXPROperators.CONTAINS],
        DSLOperators.NOT_CONTAINS: [EXPROperators.NOT, EXPROperators.CONTAINS],
        DSLOperators.IN: [EXPROperators.IN],
        DSLOperators.NOT_IN: [EXPROperators.NOT, EXPROperators.IN],
    }

    def __init__(self, left, op, right):
        self.op = op
        self.left = left
        self.right = right

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return str([self.left, self.op, self.right])

    def __repr__(self):
        return f"Literal <{str(self)}>"

    def __eq__(self, other):
        return str(self) == str(other)

    def __mul__(self, other):
        if isinstance(other, Literal):
            return mul_literal_literal(self, other)
        if isinstance(other, Conjunction):
            return mul_literal_conjunction(self, other)
        if isinstance(other, Disjunction):
            return mul_literal_disjunction(self, other)

    def __add__(self, other):
        if isinstance(other, Literal):
            return add_literal_literal(self, other)
        if isinstance(other, Conjunction):
            return add_literal_conjunction(self, other)
        if isinstance(other, Disjunction):
            return add_literal_disjunction(self, other)

    def get_op(self):
        if self.left == "ip.addr":
            if self.op == DSLOperators.IN:
                return [EXPROperators.IP_IN]
            elif self.op == DSLOperators.NOT_IN:
                return [EXPROperators.NOT, EXPROperators.IP_IN]

        return self.EXPR_OP[self.op]

    def get_lvalue(self):
        v = VAR_MAPPING.get(self.left)
        if v:
            return v

        elif self.left.startswith("http.headers["):
            header_key = (
                self.left[len("http.headers") :].strip("[]'.").replace("-", "_")
            )
            return "http_" + header_key

        return self.left

    def get_rvalue(self):
        if self.op in (DSLOperators.IN, DSLOperators.NOT_IN):
            return list(map(lambda i: i.strip("' "), self.right.strip("[]").split(",")))

        elif self.left == "http.secure":
            return "https" if self.right == True else "http"

        return self.right

    def to_expr_notation(self):
        return [self.get_lvalue(), *self.get_op(), self.get_rvalue()]


class Conjunction:
    def __init__(self, literals: List[Literal]):
        self.literals = literals

    def __str__(self):
        return f"( {' and '.join(map(lambda i: str(i), self.literals))} )"

    def __repr__(self):
        return f"Conjunction <{str(self)}>"

    def __mul__(self, other):
        if isinstance(other, Literal):
            return mul_literal_conjunction(other, self, literal_first=False)
        if isinstance(other, Conjunction):
            return mul_conjunction_conjunction(self, other)
        if isinstance(other, Disjunction):
            return mul_conjunction_disjunction(self, other)

    def __add__(self, other):
        if isinstance(other, Literal):
            return add_literal_conjunction(other, self, literal_first=False)
        if isinstance(other, Conjunction):
            return add_conjunction_conjunction(self, other)
        if isinstance(other, Disjunction):
            return add_conjunction_disjunction(self, other)

    def to_expr_notation(self):
        if len(self.literals) == 0:
            return []
        elif len(self.literals) == 1:
            return self.literals[0].to_expr_notation()

        return ["AND", *map(lambda literal: literal.to_expr_notation(), self.literals)]


class Disjunction:
    def __init__(self, conjunctions: List[Conjunction]):
        self.conjunctions = conjunctions
        self.original_expr_was_dnf = True

    def __repr__(self):
        return f"Disjunction <{str(self)}>"

    def __str__(self):
        return f"( {' OR '.join(map(lambda i: str(i), self.conjunctions))} )"

    def __mul__(self, other):
        if isinstance(other, Literal):
            return mul_literal_disjunction(other, self, literal_first=False)
        if isinstance(other, Conjunction):
            return mul_conjunction_disjunction(other, self, conjunction_first=False)
        if isinstance(other, Disjunction):
            return mul_disjunction_disjunction(self, other)

    def __add__(self, other):
        if isinstance(other, Literal):
            return add_literal_disjunction(other, self, literal_first=False)
        if isinstance(other, Conjunction):
            return add_conjunction_disjunction(other, self, conjunction_first=False)
        if isinstance(other, Disjunction):
            return add_disjunction_disjunction(self, other)

    def to_expr_notation(self):
        if len(self.conjunctions) == 0:
            return []
        elif len(self.conjunctions) == 1:
            return self.conjunctions[0].to_expr_notation()

        return [
            "OR",
            *map(lambda conjunction: conjunction.to_expr_notation(), self.conjunctions),
        ]
