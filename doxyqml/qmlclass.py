import re

TYPE_PREFIX_RX = "type\s*:\s*"
TYPE_RX = "[\w.<>|]+"

def post_process_type(rx, text, type):
    match = rx.search(text)
    if match:
        type = match.group(2)
        text = text[:match.start(1)] + text[match.end(1):]
    return text, type

class QmlClass(object):
    def __init__(self, name):
        self.name = name
        self.base_name = ""
        self.comments = []
        self.properties = []
        self.functions = []
        self.signals = []

    def __str__(self):
        lst = []
        lst.extend([str(x) for x in self.comments])
        lst.append("class %s : public %s {" % (self.name, self.base_name))
        lst.append("public:")
        lst.extend([str(x) for x in self.properties])
        lst.extend([str(x) for x in self.functions])
        if self.signals:
            lst.append("Q_SIGNALS:")
            lst.extend([str(x) for x in self.signals])
        lst.append("};")
        return "\n".join(lst)


class QmlArgument(object):
    def __init__(self, name):
        self.type = ""
        self.name = name

    def __str__(self):
        if self.type == "":
            return self.name
        else:
            return self.type + " " + self.name


class QmlProperty(object):
    def __init__(self):
        self.type = ""
        self.is_default = False
        self.name = ""
        self.doc = ""

    def __str__(self):
        lst = [self.doc]
        lst.append("Q_PROPERTY(%s %s)" % (self.type, self.name))
        return "\n".join(lst)


class QmlFunction(object):
    doc_arg_rx = re.compile("@param\s+" + TYPE_PREFIX_RX + "(" + TYPE_RX + ")\s+(\w+)")
    return_rx = re.compile("@return\s+(" + TYPE_PREFIX_RX + "(" + TYPE_RX + ")\s*)")
    def __init__(self):
        self.type = "void"
        self.name = ""
        self.doc = ""
        self.args = []

    def __str__(self):
        self.post_process_doc()
        arg_string = ", ".join([str(x) for x in self.args])
        lst = [self.doc]
        lst.append("%s %s(%s);" % (self.type, self.name, arg_string))
        return "\n".join(lst)

    def post_process_doc(self):
        def repl(match):
            type = match.group(1)
            name = match.group(2)
            for arg in self.args:
                if arg.name == name:
                    arg.type = type
                    return "@param %s" % name
            return match.group(0)

        self.doc = self.doc_arg_rx.sub(repl, self.doc)
        self.doc, self.type = post_process_type(self.return_rx, self.doc, self.type)


class QmlSignal(object):
    def __init__(self):
        self.name = ""
        self.doc = ""
        self.args = []

    def __str__(self):
        arg_string = ", ".join([str(x) for x in self.args])
        lst = [self.doc]
        lst.append("void %s(%s);" % (self.name, arg_string))
        return "\n".join(lst)
