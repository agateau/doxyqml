import logging
import re

TYPE_RX = "(?P<prefix>\s+type:)(?P<type>[\w.<>|]+)"

def post_process_type(rx, text, type):
    match = rx.search(text)
    if match:
        type = match.group("type")
        text = text[:match.start("prefix")] + text[match.end("type"):]
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
    type_rx = re.compile(TYPE_RX)

    DEFAULT_PROPERTY_COMMENT = "/** @remark This is the default property */"

    def __init__(self):
        self.type = ""
        self.is_default = False
        self.name = ""
        self.doc = ""

    def __str__(self):
        self.post_process_doc()
        lst = [self.doc]
        lst.append("Q_PROPERTY(%s %s)" % (self.type, self.name))
        return "\n".join(lst)

    def post_process_doc(self):
        self.doc, self.type = post_process_type(self.type_rx, self.doc, self.type)
        if self.is_default:
            self.doc = self.doc + "\n" + self.DEFAULT_PROPERTY_COMMENT


class QmlFunction(object):
    doc_arg_rx = re.compile(r"[@\\]param" + TYPE_RX + "\s+(?P<name>\w+)")
    return_rx = re.compile(r"[@\\]return" + TYPE_RX)
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
            # For each argument with a specified type, update arg.type and return a typeless @param line
            type = match.group("type")
            name = match.group("name")
            for arg in self.args:
                if arg.name == name:
                    arg.type = type
                    break
            else:
                logging.warning("In function %s(): Unknown argument %s" % (self.name, name))
            return "@param %s" % name

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
