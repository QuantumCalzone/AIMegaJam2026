"""Check the Blueprint graph sources in Graphs/ for the DSL trap that broke T77's StageLine (T107).

In BlueprintTools.write_graph_dsl, when an `if` body ends in a branching node (`Utilities|IsValid`, or any
node written with `(:"...")` exec branches) and code follows that `if`, the code after it becomes the `if`'s
else path: it runs only when the condition is false. T77's BP_Show.StageLine was written that way, so from
T77 to T87 no line's action played; the RiseAll in T87's build sheet (375c20a, Docs/tasks/T87-build.md) had
the same trap, and its WIN REVEAL line never printed.

This check fails a source with an `if` whose body ends in a branching node (directly, or through a nested
`if` that ends the body) when any code follows the `if`: later in the same body, or after an `if` or a
branch that holds it, up to the end of the function, event or loop body. The end of a `for` body goes back to
the loop, so code after a `for` doesn't count (T87's RiseAll ends a loop that way and works). An `if` whose
body ends in `return` is the DSL's known else form (T01) and is not flagged. To fix a flagged graph, move the branching node into a function of
its own and call it (as BP_Show.EmoteSeat does), or move the code that follows so it comes before the `if`.

Usage:
    python Tools/check_graphs.py               # every Graphs/**/*.txt; exit 1 if any fails
    python Tools/check_graphs.py FILE ...      # only these files ('-' reads stdin)
Tools/check_prompts.py --offline runs the same check over Graphs/.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPHS = ROOT / "Graphs"
BLOCKS = {"fn", "event", "if", "elif", "else", "for"}


class Node(list):
    line = 0


def tokenize(src):
    """Tokens with their line numbers. Comments go; strings and `:"Label"` stay whole."""
    toks = []
    i, line, n = 0, 1, len(src)
    while i < n:
        c = src[i]
        if c == "\n":
            line += 1
            i += 1
        elif c.isspace():
            i += 1
        elif c == ";":
            while i < n and src[i] != "\n":
                i += 1
        elif c in "()":
            toks.append((c, line))
            i += 1
        elif c == '"' or (c == ":" and i + 1 < n and src[i + 1] == '"'):
            j = i + 2 if c == ":" else i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
            toks.append((src[i:j + 1], line))
            i = j + 1
        else:
            j = i
            while j < n and not src[j].isspace() and src[j] != ")":
                if src[j] == "(":
                    # A paren glued to an atom is part of its name: ToString(Boolean), OnClicked(VoteBtn0).
                    k = src.find(")", j)
                    j = (k if k >= 0 else n - 1) + 1
                    continue
                j += 1
            toks.append((src[i:j], line))
            i = j
    return toks


def parse(src):
    top = Node()
    stack = [top]
    for t, line in tokenize(src):
        if t == "(":
            node = Node()
            node.line = line
            stack[-1].append(node)
            stack.append(node)
        elif t == ")":
            if len(stack) == 1:
                raise ValueError(f"line {line}: unmatched ')'")
            stack.pop()
        else:
            stack[-1].append(t)
    if len(stack) != 1:
        raise ValueError(f"line {stack[-1].line}: unclosed '('")
    return top


def head(x):
    return x[0] if isinstance(x, list) and x and isinstance(x[0], str) else None


def is_label(x):
    h = head(x)
    return h is not None and h.startswith(':"')


def is_branch_node(x):
    """A node with exec branches: Utilities|IsValid, or any form holding a (:"...") child."""
    h = head(x)
    if h is None or h in BLOCKS:
        return False
    return h == "Utilities|IsValid" or any(is_label(y) for y in x[1:])


def head_len(x):
    """How many items open a block form before its body starts."""
    h = head(x)
    if h in ("fn", "for"):
        return 3
    if h == "event":
        # (event Name (Params) body...) or (event Name body...) when the third item is already a statement.
        if len(x) > 2 and isinstance(x[2], list) and not (head(x[2]) in BLOCKS or (head(x[2]) or "").find("|") >= 0):
            return 3
        return 2
    if h in ("if", "elif"):
        return 2
    if h == "else":
        return 1
    return 1


def then_body(x):
    """An if's own statements, without its elif and else parts."""
    return [y for y in x[head_len(x):] if head(y) not in ("elif", "else")]


def ends_in_branch(stmt):
    if is_branch_node(stmt):
        return True
    h = head(stmt)
    if h == "if":
        body = then_body(stmt)
        return bool(body) and ends_in_branch(body[-1])
    return False


def walk_body(stmts, follows_after, out):
    """Check a list of statements. follows_after: code runs after this body ends (in an enclosing block)."""
    for i, s in enumerate(stmts):
        if not isinstance(s, list):
            continue
        follows = i < len(stmts) - 1 or follows_after
        h = head(s)
        if h == "if":
            body = then_body(s)
            if body and follows and ends_in_branch(body[-1]):
                out.append((s.line, "an if whose body ends in a branching node has code after it; that code becomes the if's else path"))
            walk_body(body, follows, out)
            for y in s[head_len(s):]:
                if head(y) in ("elif", "else"):
                    walk_body(y[head_len(y):], follows, out)
        elif h == "for":
            # The end of a loop body goes back to the loop, not to the code after the loop.
            walk_body(s[head_len(s):], False, out)
        elif is_branch_node(s):
            for y in s[1:]:
                if is_label(y):
                    walk_body(y[1:], follows, out)


def check_text(src):
    """Return [(line, message)] for one graph source."""
    out = []
    try:
        top = parse(src)
    except ValueError as e:
        return [(0, f"can't parse: {e}")]
    for form in top:
        if head(form) in ("fn", "event"):
            walk_body(form[head_len(form):], False, out)
    return out


def check_files(paths):
    """Return [(path, line, message)] for these files."""
    bad = []
    for p in paths:
        src = sys.stdin.read() if str(p) == "-" else Path(p).read_text(encoding="utf-8")
        for line, msg in check_text(src):
            bad.append((str(p), line, msg))
    return bad


def all_sources():
    return sorted(GRAPHS.rglob("*.txt"))


def main(argv):
    paths = argv or all_sources()
    bad = check_files(paths)
    for p, line, msg in bad:
        print(f"FAIL {p}:{line}: {msg}")
    if not argv:
        print(f"graphs: {len(paths)} sources checked, {len(bad)} failed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
