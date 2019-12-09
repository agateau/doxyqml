import doxyqml.lexer as lexer

from doxyqml.qmlclass import QmlComponent, QmlArgument, QmlProperty, QmlFunction, QmlSignal, QmlAttribute


class QmlParserError(Exception):
    def __init__(self, msg, token):
        Exception.__init__(self, msg)
        self.token = token


class QmlParserUnexpectedTokenError(QmlParserError):
    def __init__(self, token):
        QmlParserError.__init__(self, "Unexpected token: %s" % str(token), token)


def parse_class_definition(reader, cls):
    token = reader.consume_wo_comments()
    if token.type != lexer.BLOCK_START:
        raise QmlParserError("Expected '{' after base class name", token)
    last_comment_token = None
    while not reader.at_end():
        token = reader.consume()
        if is_comment_token(token):
            if last_comment_token:
                cls.add_element(last_comment_token.value)
            last_comment_token = token
        elif token.type == lexer.KEYWORD:
            parse_class_content(reader, cls, token, last_comment_token)
            last_comment_token = None
        elif token.type == lexer.COMPONENT:
            parse_class_component(reader, cls, token, last_comment_token)
            last_comment_token = None
        elif token.type == lexer.ATTRIBUTE:
            parse_class_attribute(reader, cls, token, last_comment_token)
            last_comment_token = None
        elif token.type == lexer.BLOCK_START:
            skip_block(reader)
        elif token.type == lexer.BLOCK_END:
            break
    if last_comment_token:
        cls.add_element(last_comment_token.value)


def parse_class_content(reader, cls, token, doc_token):
    keyword = token.value
    if keyword.endswith("property"):
        obj = parse_property(reader, keyword)
    elif keyword == "function":
        obj = parse_function(reader)
    elif keyword == "signal":
        obj = parse_signal(reader)
    else:
        raise QmlParserError("Unknown keyword '%s'" % keyword, token)
    if doc_token is not None:
        obj.doc = doc_token.value
        obj.doc_is_inline = (doc_token.type == lexer.ICOMMENT)
    cls.add_element(obj)


def parse_class_component(reader, cls, token, doc_token):
    obj = QmlComponent(token.value)
    parse_class_definition(reader, obj)

    if doc_token is not None:
        obj.comment = doc_token.value

    cls.add_element(obj)


def parse_class_attribute(reader, cls, token, doc_token):
    obj = QmlAttribute()
    obj.name = token.value

    # Should be colon
    token = reader.consume_expecting(lexer.CHAR)
    token = reader.consume()
    if token.type == lexer.BLOCK_START:
        skip_block(reader)
    else:
        obj.value = token.value

    if doc_token is not None:
        obj.doc = doc_token.value

    cls.add_element(obj)


def parse_property(reader, property_token_value):
    prop = QmlProperty()
    prop.is_default = property_token_value.startswith("default")
    prop.is_readonly = property_token_value.startswith("readonly")

    token = reader.consume_expecting(lexer.ELEMENT)
    prop.type = token.value

    token = reader.consume_expecting(lexer.ELEMENT)
    prop.name = token.value
    return prop


def parse_function(reader):
    obj = QmlFunction()
    token = reader.consume_expecting(lexer.ELEMENT)
    obj.name = token.value

    reader.consume_expecting(lexer.CHAR, "(")
    obj.args = parse_arguments(reader)
    return obj


def parse_signal(reader):
    obj = QmlSignal()
    token = reader.consume_expecting(lexer.ELEMENT)
    obj.name = token.value

    idx = reader.idx
    token = reader.consume_wo_comments()
    if token.type == lexer.CHAR and token.value == "(":
        obj.args = parse_arguments(reader, typed=True)
    else:
        reader.idx = idx
    return obj


def parse_arguments(reader, typed=False):
    token = reader.consume_wo_comments()
    if token.type == lexer.CHAR and token.value == ")":
        return []
    elif token.type != lexer.ELEMENT:
        raise QmlParserUnexpectedTokenError(token)

    args = []
    while True:
        if typed:
            arg_type = token.value
            token = reader.consume_expecting(lexer.ELEMENT)
            arg = QmlArgument(token.value)
            arg.type = arg_type
        else:
            arg = QmlArgument(token.value)

        token = reader.consume_expecting(lexer.CHAR)

        if token.value == "=":
            token = reader.consume_expecting([lexer.ELEMENT, lexer.STRING])
            arg.default_value = token.value
            token = reader.consume_expecting(lexer.CHAR)

        args.append(arg)

        if token.value == ")":
            return args
        elif token.value != ",":
            raise QmlParserUnexpectedTokenError(token)

        token = reader.consume_expecting(lexer.ELEMENT)


def skip_block(reader):
    count = 1
    while True:
        token = reader.consume_wo_comments()
        if token.type == lexer.BLOCK_START:
            count += 1
        elif token.type == lexer.BLOCK_END:
            count -= 1
            if count == 0:
                return


def parse_header(reader, cls):
    while not reader.at_end():
        token = reader.consume()
        if is_comment_token(token):
            cls.add_header_comment(token.value)
        elif token.type == lexer.IMPORT:
            cls.add_import(token.value)
        elif token.type == lexer.PRAGMA:
            cls.add_pragma(token.value)
        elif token.type == lexer.COMPONENT:
            cls.base_name = token.value
            return
        else:
            raise QmlParserUnexpectedTokenError(token)


def parse_footer(reader, cls):
    while not reader.at_end():
        token = reader.consume()
        if is_comment_token(token):
            cls.add_footer_comment(token.value)
        else:
            raise QmlParserUnexpectedTokenError(token)


def is_comment_token(token):
    return token.type in (lexer.COMMENT, lexer.ICOMMENT)


class TokenReader(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0

    def consume(self):
        token = self.tokens[self.idx]
        self.idx += 1
        return token

    def consume_wo_comments(self):
        while True:
            token = self.consume()
            if not is_comment_token(token):
                return token

    def consume_expecting(self, expected_types, value=None):
        token = self.consume_wo_comments()
        if type(expected_types) is list:
            if token.type not in expected_types:
                raise QmlParserError(
                    "Expected token of type '%s', got '%s' instead" % (expected_types, token.type), token)
        elif token.type != expected_types:
            raise QmlParserError(
                "Expected token of type '%s', got '%s' instead" % (expected_types, token.type), token)
        if value is not None and token.value != value:
            raise QmlParserError("Expected token with value '%s', got '%s' instead" % (
                value, token.value), token)
        return token

    def at_end(self):
        return self.idx == len(self.tokens)


def parse(tokens, cls):
    reader = TokenReader(tokens)
    parse_header(reader, cls)
    parse_class_definition(reader, cls)
    parse_footer(reader, cls)
