# 1) Define your library of prompt templates
PROMPT_TEMPLATES = {
    "zero_shot": (
        "For each method in the given Java code, write a general description "
        "of what it does, listing its @param and @return. "
        "{file_name}\n"   # we’ll .format() this
        "{method_stub}"
    ),

    "few_shot": (
        "Example 1:\n"
        "  foo(int x)\n"
        "  @param x; the input value\n"
        "  @return int; the result doubled\n"
        "  Overview: doubles the input value.\n"
        "\n"
        "Example 2:\n"
        "  bar(String s)\n"
        "  @param s; the input string\n"
        "  @return String; uppercase version\n"
        "  Overview: converts string to uppercase.\n"
        "\n"
        "Now document the methods in:\n"
        "{file_name}\n"
        "{method_stub}"
    ),

    "chain_of_thought": (
        "We want to document Java methods. Let's think step by step:\n"
        "1) Identify the method signature and its parameters.\n"
        "2) List @param lines and @return line.\n"
        "3) Write an Overview sentence.\n"
        "\n"
        "{file_name}\n"
    ),

    "hybrid": (
        # few-shot + CoT in one
        "We want to document Java methods. we want them in the format below:\n"
        "Example:\n"
        "  Q: foo(int x) /** doubles x */  →\n"
        "  1) param x; the input integer\n"
        "  2) return int; x*2\n"
        "  Overview: returns double the input\n"
        "\n"
        "Now you:\n"
        "{file_name}\n"
    ),
}