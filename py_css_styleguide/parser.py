"""
Parser
======

This parser has been done quickly standing only on cases involved by CSS
manifest syntax so it is very naive and may breaks on everything else.

We assume CSS source only contains supported syntax for manifest, everything
else could break process.

This flaw is tempered by the behavior of parser that ignores rules that
don't start with the manifest prefix, so CSS manifest could contains some
other syntax for non styleguide rules.
"""
from collections import OrderedDict

from tinycss2 import parse_stylesheet

from py_css_styleguide.nomenclature import RULE_BASE_PREFIX


class TinycssSourceParser(object):
    """
    CSS parser using tinycss2

    Since tinycss2 only return tokens, this parser is in charge to turn them
    to usable datas: a dict of properties for each selector.
    """
    def digest_prelude(self, rule):
        """
        Walk on rule prelude (aka CSS selector) tokens to return a string of
        the value name (from css selector).

        Actually only simple selector and selector with descendant combinator
        are supported. Using any other selector kind may leads to unexpected
        issues.

        Arguments:
            rule (tinycss2.ast.QualifiedRule): Qualified rule object as
                returned by  tinycss2.

        Returns:
            string: Selector name. If it's a descendant combinator, items are
                joined with ``__``.
        """
        name = []

        for token in rule.prelude:
            if token.type == 'ident':
                name.append(token.value)

        return "__".join(name)

    def digest_content(self, rule):
        """
        Walk on rule content tokens to return a dict of properties.

        This is pretty naive and will choke/fail on everything that is more
        evolved than simple ``ident(string):value(string)``

        Arguments:
            rule (tinycss2.ast.QualifiedRule): Qualified rule object as
                returned by  tinycss2.

        Returns:
            dict: Dictionnary of retrieved variables and properties.
        """
        data = OrderedDict()

        current_key = None

        for token in rule.content:
            # Assume first identity token is the property name
            if token.type == 'ident':
                # Ignore starting '-' from css variables
                name = token.value
                if name.startswith('-'):
                    name = name[1:]

                current_key = name
                data[current_key] = None

            # Assume first following string token is the property value.
            if token.type == 'string':
                data[current_key] = token.value

        return data

    def consume(self, source):
        """
        Parse source and consume tokens from tinycss2.

        Arguments:
            source (string): Source content to parse.

        Returns:
            dict: Retrieved rules.
        """
        manifest = OrderedDict()

        rules = parse_stylesheet(
            source,
            skip_comments=True,
            skip_whitespace=True,
        )

        for rule in rules:
            # Gather rule selector+properties
            name = self.digest_prelude(rule)

            # Ignore everything out of styleguide namespace
            if not name.startswith(RULE_BASE_PREFIX):
                continue

            properties = self.digest_content(rule)
            manifest[name] = properties

        return manifest

    def parse(self, source):
        """
        Read and parse CSS source and return dict of rules.

        Arguments:
            source (string): Source content to parse.

        Returns:
            dict: Selectors with their properties.
        """
        return self.consume(source)
