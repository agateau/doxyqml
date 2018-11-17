import logging
import re

TYPE_RX = r"(?P<prefix>\s+type:)(?P<type>[\w.<>|]+)"


def post_process_type(rx, text, type):
    match = rx.search(text)
    if match:
        type = match.group("type")
        text = text[:match.start("prefix")] + text[match.end("type"):]
    return text, type


class QmlBaseComponent(object):
    def __init__(self, name):
        self.name = name
        self.base_name = ""
        self.elements = []

        lst = name.split(".")
        self.class_name = lst[-1]
        self.namespaces = lst[:-1]

    def get_attributes(self):
        return [x for x in self.elements if isinstance(x, QmlAttribute)]

    def get_properties(self):
        return [x for x in self.elements if isinstance(x, QmlProperty)]

    def get_functions(self):
        return [x for x in self.elements if isinstance(x, QmlFunction)]

    def get_signals(self):
        return [x for x in self.elements if isinstance(x, QmlSignal)]

    def add_element(self, element):
        self.elements.append(element)

    def __str__(self):
        lst = []
        self._export_content(lst)
        return "\n".join(lst)

    def _export_elements(self, input_list, lst, filter=None):
        for element in input_list:
            if filter and not filter(element):
                continue
            doc = str(element)
            if doc:
                lst.append(doc)

    def _start_class(self, lst):
        class_decl = "class " + self.class_name
        if self.base_name:
            class_decl += " : public " + self.base_name

        class_decl += " {"
        lst.append(class_decl)
        lst.append("public:")

    def _end_class(self, lst):
        lst.append("};")


class QmlClass(QmlBaseComponent):
    SINGLETON_COMMENT = "/** @remark This component is a singleton */"
    VERSION_COMMENT = "/** @since %s */"

    def __init__(self, name, version=None):
        QmlBaseComponent.__init__(self, name)
        self.header_comments = []
        self.footer_comments = []
        self.imports = []
        if version:
            self.header_comments.append(QmlClass.VERSION_COMMENT % version)

    def add_pragma(self, decl):
        args = decl.split(' ', 2)[1].strip()

        if args.lower() == "singleton":
            self.header_comments.append(QmlClass.SINGLETON_COMMENT)

    def add_import(self, decl):
        module = decl.split()[1]
        if module[0] == '"':
            # Ignore directory or javascript imports for now
            return
        self.imports.append(module)

    def add_header_comment(self, obj):
        self.header_comments.append(obj)

    def add_footer_comment(self, obj):
        self.footer_comments.append(obj)

    def _export_header(self, lst):
        for module in self.imports:
            lst.append("using namespace %s;" % module.replace('.', '::'))
        if self.namespaces:
            lst.append("namespace %s {" % '::'.join(self.namespaces))

        lst.extend([str(x) for x in self.header_comments])

    def _export_footer(self, lst):
        lst.extend([str(x) for x in self.footer_comments])

        if self.namespaces:
            lst.append("}")

    def _export_content(self, lst):
        self._export_header(lst)

        # Public members.
        self._start_class(lst)

        public_members = []
        private_members = []

        # Sort elements before exporting to reduce the number of times element list must
        # be iterated through.
        for element in self.elements:
            if str(element) == "" or isinstance(element, str) or element.is_public_element():
                # Register empty strings as public to prevent exporting unneeded "private" keyword.
                public_members.append(element)
            else:
                private_members.append(element)

        self._export_elements(public_members, lst)

        if len(private_members) > 0:
            lst.append("private:")
            self._export_elements(private_members, lst)

        self._end_class(lst)
        self._export_footer(lst)

    def is_public_element(self):
        return True


class QmlComponent(QmlBaseComponent):
    """A component inside a QmlClass"""
    def __init__(self, name):
        QmlBaseComponent.__init__(self, name)
        self.comment = None

    def _export_content(self, lst):
        component_id = self.get_component_id()
        if component_id:
            if self.comment:
                lst.append(self.comment)

            lst.append("%s %s;" % (self.class_name, component_id))

        # Export child components with the top-level component. This avoids
        # very deep nesting in the generated documentation.
        self._export_elements(self.elements, lst, filter=lambda x:
                              isinstance(x, QmlComponent))

    def get_component_id(self):
        # Returns the id of the component, if it has one
        for attr in self.get_attributes():
            if attr.name == "id":
                return attr.value
        return None

    def is_public_element(self):
        return False


class QmlArgument(object):
    def __init__(self, name):
        self.type = ""
        self.name = name

    def __str__(self):
        if self.type == "":
            return self.name
        else:
            return self.type + " " + self.name

    def is_public_element(self):
        return True


class QmlAttribute(object):
    def __init__(self):
        self.name = ""
        self.value = ""
        self.type = "var"
        self.doc = ""

    def __str__(self):
        if self.name != "id":
            lst = []
            if len(self.doc) > 0:
                lst.append(self.doc)
            lst.append(self.type + " " + self.name + ";")
            return "\n".join(lst)
        else:
            return ""

    def is_public_element(self):
        return False


class QmlProperty(object):
    type_rx = re.compile(TYPE_RX)

    DEFAULT_PROPERTY_COMMENT = "/** @remark This is the default property */"
    READONLY_PROPERTY_COMMENT = "/** @remark This property is read-only */"

    def __init__(self):
        self.type = ""
        self.is_default = False
        self.is_readonly = False
        self.name = ""
        self.doc = ""
        self.doc_is_inline = False

    def __str__(self):
        self.post_process_doc()
        lst = []
        if not self.doc_is_inline:
            lst.append(self.doc + "\n")
        if self.is_default:
            lst.append(self.DEFAULT_PROPERTY_COMMENT + "\n")
        elif self.is_readonly:
            lst.append(self.READONLY_PROPERTY_COMMENT + "\n")
        lst.append("Q_PROPERTY(%s %s)" % (self.type, self.name))
        if self.doc_is_inline:
            lst.append(" " + self.doc)
        return "".join(lst)

    def post_process_doc(self):
        self.doc, self.type = post_process_type(self.type_rx, self.doc, self.type)

    def is_public_element(self):
        # Doxygen always adds Q_PROPERTY items as public members.
        return True


class QmlFunction(object):
    doc_arg_rx = re.compile(r"[@\\]param" + TYPE_RX + r"\s+(?P<name>\w+)")
    return_rx = re.compile(r"[@\\]returns?" + TYPE_RX)

    def __init__(self):
        self.type = "void"
        self.name = ""
        self.doc = ""
        self.doc_is_inline = False
        self.args = []

    def __str__(self):
        self.post_process_doc()
        arg_string = ", ".join([str(x) for x in self.args])
        lst = []
        if not self.doc_is_inline:
            lst.append(self.doc + "\n")
        lst.append("%s %s(%s);" % (self.type, self.name, arg_string))
        if self.doc_is_inline:
            lst.append(" " + self.doc)
        return "".join(lst)

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

    def is_public_element(self):
        return True


class QmlSignal(object):
    def __init__(self):
        self.name = ""
        self.doc = ""
        self.doc_is_inline = False
        self.args = []

    def __str__(self):
        arg_string = ", ".join([str(x) for x in self.args])
        lst = []
        if not self.doc_is_inline:
            lst.append(self.doc + "\n")
        lst.append("Q_SIGNALS: void %s(%s); " % (self.name, arg_string))
        if self.doc_is_inline:
            lst.append(self.doc + "\n")
        # Appending "public:" here makes it possible to declare a signal without
        # turning all functions defined after into signals.
        # It could be replaced with the use of Q_SIGNAL, but my version of
        # Doxygen (1.8.4) does not support it
        lst.append("public:")
        return "".join(lst)

    def is_public_element(self):
        # Doxygen always adds Q_SIGNALS items as public members.
        return True
