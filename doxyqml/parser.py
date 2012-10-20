import lexer

from qmlclass import QmlArgument, QmlProperty, QmlFunction, QmlSignal


class ParserError(Exception):
    def __init__(self, msg, token):
        Exception.__init__(self, msg)
        self.token = token


class SkipBlockParser(object):
    def parse(self, main):
        count = 1
        while True:
            token = main.consume_wo_comments()
            if token.type == lexer.BLOCK_START:
                count += 1
            elif token.type == lexer.BLOCK_END:
                count -= 1
                if count == 0:
                    main.pop()
                    return


class ClassParser(object):
    def parse(self, main):
        token = main.consume_wo_comments()
        if token.type != lexer.BLOCK_START:
            raise ParserError("Expected '{' after base class name", token)
        comments = []
        while not main.at_end():
            token = main.consume()
            if token.type == lexer.COMMENT:
                comments.append(token.value)
            else:
                done = self.parse_token(main, token, comments)
                if done:
                    break
                comments = []

    def parse_token(self, main, token, comments):
        if token.type == lexer.KEYWORD:
            if token.value == "property":
                obj = self.parse_property(main)
                obj.doc = comments
                main.dst.properties.append(obj)
            elif token.value == "function":
                obj = self.parse_function(main)
                obj.doc = comments
                main.dst.functions.append(obj)
            elif token.value == "signal":
                obj = self.parse_signal(main)
                obj.doc = comments
                main.dst.signals.append(obj)
            else:
                raise ParserError("Unknown keyword '%s'" % token.value, token)

        elif token.type == lexer.BLOCK_START:
            main.push(SkipBlockParser())

        elif token.type == lexer.BLOCK_END:
            return True

        return False


    def parse_property(self, main):
        prop = QmlProperty()
        token = main.consume_expecting(lexer.ELEMENT)
        if token.value == "default":
            prop.default = True
            token = main.consume_expecting(lexer.ELEMENT)

        prop.type = token.value

        token = main.consume_expecting(lexer.ELEMENT)
        prop.name = token.value
        return prop


    def parse_function(self, main):
        obj = QmlFunction()
        token = main.consume_expecting(lexer.ELEMENT)
        obj.name = token.value

        main.consume_expecting(lexer.CHAR, "(")
        obj.args = self.parse_arguments(main)
        return obj


    def parse_arguments(self, main, typed=False):
        token = main.consume_wo_comments()
        if token.type == lexer.CHAR and token.value == ")":
            return []
        elif token.type != lexer.ELEMENT:
            raise ParserError("Unxpected token %s" % token, token)

        args = []
        while True:
            if typed:
                arg_type = token.value
                token = main.consume_expecting(lexer.ELEMENT)
                arg = QmlArgument(token.value)
                arg.type = arg_type
            else:
                arg = QmlArgument(token.value)
            args.append(arg)

            token = main.consume_expecting(lexer.CHAR)
            if token.value == ")":
                return args
            elif token.value != ",":
                raise ParserError("Unxpected token %s" % token, token)

            token = main.consume_expecting(lexer.ELEMENT)


    def parse_signal(self, main):
        obj = QmlSignal()
        token = main.consume_expecting(lexer.ELEMENT)
        obj.name = token.value

        idx = main.idx
        token = main.consume_wo_comments()
        if token.type == lexer.CHAR and token.value == "(":
            obj.args = self.parse_arguments(main, typed=True)
        else:
            main.idx = idx
        return obj


class HeaderParser(object):
    def parse(self, main):
        while not main.at_end():
            token = main.consume()
            if token.type == lexer.COMMENT:
                main.dst.comments.append(token.value)
            elif token.type == lexer.IMPORT:
                pass
            elif token.type == lexer.ELEMENT:
                main.dst.base_name = token.value
                main.push(ClassParser())
                return
            else:
                raise ParserError("Unexpected token: %s" % token, token)


class Parser(object):
    def __init__(self, dst, tokens):
        self.dst = dst
        self.tokens = tokens
        self.idx = 0
        self.parsers = []

    def consume(self):
        token = self.tokens[self.idx]
        self.idx += 1
        return token

    def consume_wo_comments(self):
        while True:
            token = self.consume()
            if token.type != lexer.COMMENT:
                return token

    def consume_expecting(self, type, value=None):
        token = self.consume_wo_comments()
        if token.type != type:
            raise ParserError("Expected token of type '%s', got '%s' instead" % (type, token.type), token)
        if value is not None and token.value != value:
            raise ParserError("Expected token with value '%s', got '%s' instead" % (value, token.value), token)
        return token

    def at_end(self):
        return self.idx == len(self.tokens)

    def parse(self):
        self.push(HeaderParser())
        while not self.at_end():
            self.parsers[-1].parse(self)

    def push(self, parser):
        self.parsers.append(parser)

    def pop(self):
        self.parsers.pop()
