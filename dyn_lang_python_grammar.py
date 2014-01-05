from dragonfly import *  # @UnusedWildImport

from lib.custom_objects import SCText


class SeriesMappingRule(CompoundRule):

    def __init__(self, mapping, extras=None, defaults=None):
        mapping_rule = MappingRule(mapping=mapping, extras=extras,
            defaults=defaults, exported=False)
        single = RuleRef(rule=mapping_rule)
        series = Repetition(single, min=1, max=16, name="series")

        compound_spec = "<series>"
        compound_extras = [series]
        CompoundRule.__init__(self, spec=compound_spec,
            extras=compound_extras, exported=True)

    def _process_recognition(self, node, extras):  # @UnusedVariable
        series = extras["series"]
        for action in series:
            action.execute()


special_commands_one = SeriesMappingRule(
    mapping={
        # Keywords:
        "and": Text(" and "),
        "as": Text("as "),
        "assign": Text(" = "),
        "break": Text("break"),
        "divided by": Text(" / "),
        "(dict|dictionary) key value": Text("\"\": \"\",") + Key("left:6"),
        "enumerate": Text("enumerate()") + Key("left"),
        "comment": Text("# "),
        "class": Text("class "),
        "continue": Text("continue"),
        "(def|define|definition)": Text("def "),
        "(def|define|definition) init": Text("def __init__("),
        "doc string": Text('"""Doc string."""') + Key("left:14, s-right:11"),
        "else": Text("else:\n"),
        "except": Text("except "),
        "(el if|else if)": Text("elif "),
        "(el if|else if) <text>": SCText("elif %(text)s"),
        "equals": Text(" == "),
        "false": Text("False"),
        "finally": Text("finally:\n"),
        "for": Text("for "),
        "for <text>": SCText("for %(text)s"),
        "from": Text("from "),
        "from <text>": SCText("from %(text)s"),
        "greater than": Text(" > "),
        "greater [than] equals": Text(" >= "),
        "if": Text("if "),
        "if <text>": SCText("if %(text)s"),
        "in": Text("in "),
        "in <text>": SCText("in %(text)s"),
        "(int|I N T)": Text("int"),
        "(int|I N T)": Text("int()") + Key("left"),
        "init": Text("init"),
        "import": Text("import "),
        "import <text>": SCText("import %(text)s"),
        "(len|L E N)": Text("len("),
        "less than": Text(" < "),
        "less [than] equals": Text(" <= "),
        "(minus|subtract|subtraction)": Text(" - "),
        "(minus|subtract|subtraction) equals": Text(" -= "),
        "modulo": Key("space") + Key("percent") + Key("space"),
        "not equals": Text(" != "),
        "none": Text("None"),
        "or": Text(" or "),
        "pass": Text("pass"),
        "(plus|add|addition)": Text(" + "),
        "(plus|add|addition) equals": Text(" += "),
        "print": Text("print()") + Key("left"),
        "raise": Text("raise"),
        "raise exception": Text("raise Exception()") + Key("left"),
        "return": Text("return"),
        "return <text>": SCText("return %(text)s"),
        "self": Text("self"),
        "(str|S T R)": Text("str"),
        "(str|S T R) paren": Text("str()") + Key("left"),
        "true": Text("True"),
        "try": Text("try:\n"),
        "times": Text(" * "),
        "with": Text("with "),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
    ],
    defaults={
        "n": 1
    }
)

global_context = None  # Context is None, so grammar will be globally active.
grammar = Grammar("Python grammar", context=global_context)
grammar.add_rule(special_commands_one)
grammar.load()
grammar.disable()


def dynamic_enable():
    global grammar
    if grammar.enabled:
        return False
    else:
        grammar.enable()
        return True


def dynamic_disable():
    global grammar
    if grammar.enabled:
        grammar.disable()
        return True
    else:
        return False


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
