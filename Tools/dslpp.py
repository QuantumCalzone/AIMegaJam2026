"""Expand shorthand macros in a DSL source file into plain write_graph_dsl code.

Macros: (V X) (set X v) (get A i) (len A) (str i) (cat a b ...) (log x) (print x)
(streq a b) (add A x) (clear A). Sections start with ';;; GRAPH <Name>'.
Usage: python dslpp.py in.txt out.txt
"""
import re
import sys


def tokenize(s):
    toks = []
    i = 0
    while i < len(s):
        c = s[i]
        if c.isspace():
            i += 1
        elif c == ';':
            while i < len(s) and s[i] != '\n':
                i += 1
        elif c in '()':
            toks.append(c)
            i += 1
        elif c == '"':
            j = i + 1
            while s[j] != '"':
                j += 2 if s[j] == '\\' else 1
            toks.append(s[i:j + 1])
            i = j + 1
        else:
            j = i
            while j < len(s) and not s[j].isspace() and s[j] != ')':
                if s[j] == '(':
                    # A paren glued to an atom is part of its name: ToString(Boolean), OnClicked(VoteBtn0).
                    k = s.index(')', j)
                    j = k + 1
                    continue
                j += 1
            toks.append(s[i:j])
            i = j
    return toks


def parse(toks):
    out = []
    stack = [out]
    for t in toks:
        if t == '(':
            n = []
            stack[-1].append(n)
            stack.append(n)
        elif t == ')':
            stack.pop()
        else:
            stack[-1].append(t)
    return out


def ex(x):
    if not isinstance(x, list) or not x:
        return x
    h = x[0]
    a = [ex(y) for y in x[1:]]
    if h == 'V':
        return ['Variables|Default|Get' + x[1]]
    if h == 'set':
        return ['Variables|Default|Set' + x[1], a[1]]
    if h == 'get':
        return ['Utilities|Array|Get(acopy)', a[0], a[1]]
    if h == 'len':
        return ['Utilities|Array|Length', a[0]]
    if h == 'str':
        return ['Utilities|String|ToString(Integer)', a[0]]
    if h == 'cat':
        r = a[0]
        for y in a[1:]:
            r = ['Utilities|String|Append', r, y]
        return r
    if h == 'log':
        return ['Class|WBPStage|AddLogLine', ':self', ['Variables|Default|GetStage'], ':Line', a[0]]
    if h == 'print':
        return ['Development|PrintString', a[0], 'false']
    if h == 'streq':
        return ['Utilities|String|EqualExactly(String)', a[0], a[1]]
    if h == 'add':
        return ['Utilities|Array|Add', a[0], a[1]]
    if h == 'clear':
        return ['Utilities|Array|Clear', a[0]]
    return [h] + a


BLOCK = {'fn', 'if', 'elif', 'else', 'for', 'event'}
HEADS = {'fn': 3, 'if': 2, 'elif': 2, 'else': 1, 'for': 3, 'event': 3}


def fmt(x, ind=0):
    if not isinstance(x, list):
        return x
    if x and x[0] in BLOCK:
        k = HEADS[x[0]]
        if x[0] == 'event' and (len(x) < 3 or not isinstance(x[2], list) or (x[2] and x[2][0] in BLOCK or (x[2] and isinstance(x[2][0], str) and '|' in x[2][0]))):
            k = 2
        head = ' '.join(fmt(y) for y in x[:k])
        body = ''.join('\n' + '  ' * (ind + 1) + fmt(y, ind + 1) for y in x[k:])
        return '(' + head + body + ')'
    return '(' + ' '.join(fmt(y, ind) for y in x) + ')'


def main():
    src = open(sys.argv[1], encoding='utf-8').read()
    parts = re.split(r'^;;; GRAPH (\w+)\s*$', src, flags=re.M)
    out = []
    for name, body in zip(parts[1::2], parts[2::2]):
        forms = parse(tokenize(body))
        out.append(';;; GRAPH ' + name + '\n' + '\n\n'.join(fmt(ex(f)) for f in forms) + '\n')
    open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(out))
    print('graphs:', ' '.join(parts[1::2]))


main()
