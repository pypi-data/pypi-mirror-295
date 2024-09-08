from tree_sitter_java import language as java_language  # noqa: F401

java_mapping: dict[str, str] = {
    "block_comment": "Comment",
    "line_comment": "Comment",
    "abstract": "Keyword",
    "assert": "Keyword",
    "boolean": "Keyword",
    "boolean_type": "Keyword",
    "break": "Keyword",
    "byte": "Keyword",
    "case": "Keyword",
    "catch": "Keyword",
    "char": "Keyword",
    "class": "Keyword",
    "do": "Keyword",
    "default": "Keyword",
    "double": "Keyword",
    "else": "Keyword",
    "extends": "Keyword",
    "false": "Keyword",
    "final": "Keyword",
    "finally": "Keyword",
    "float": "Keyword",
    "for": "Keyword",
    "if": "Keyword",
    "implements": "Keyword",
    "import": "Keyword",
    "int": "Keyword",
    "interface": "Keyword",
    "long": "Keyword",
    "new": "Keyword",
    "null_literal": "Keyword",
    "package": "Keyword",
    "private": "Keyword",
    "protected": "Keyword",
    "public": "Keyword",
    "return": "Keyword",
    "short": "Keyword",
    "static": "Keyword",
    "switch": "Keyword",
    "super": "Keyword",
    "this": "Keyword",
    "throw": "Keyword",
    "throws": "Keyword",
    "true": "Keyword",
    "try": "Keyword",
    "void_type": "Keyword",
    "while": "Keyword",
    "identifier": "Identifier",
    "type_identifier": "Identifier",
    "decimal_floating_point_literal": "Number",
    "decimal_integer_literal": "Number",
    "!": "Operator",
    "!=": "Operator",
    "%": "Operator",
    "&&": "Operator",
    "*": "Operator",
    "*=": "Operator",
    "+": "Operator",
    "++": "Operator",
    "+=": "Operator",
    "-": "Operator",
    "--": "Operator",
    "-=": "Operator",
    "/": "Operator",
    "/=": "Operator",
    "<": "Operator",
    "<=": "Operator",
    "=": "Operator",
    "==": "Operator",
    ">": "Operator",
    ">=": "Operator",
    "?": "Operator",
    "||": "Operator",
    "@": "Operator",
    "(": "Punctuation",
    ")": "Punctuation",
    ",": "Punctuation",
    ".": "Punctuation",
    ":": "Punctuation",
    ";": "Punctuation",
    "[": "Punctuation",
    "]": "Punctuation",
    "{": "Punctuation",
    "}": "Punctuation",
    '"': "String",
    "character_literal": "String",
    "escape_sequence": "String",
    "string_fragment": "String",
    "ERROR": "Error",
}


# print(
#     {
#         k: v
#         for k, v in sorted(
#             java_mapping.items(), key=lambda item: (item[1], item)
#         )
#     }
# )
