#!/usr/bin/env python3
"""Rewrite relative internal links/assets to root-relative clean URLs and make
og/twitter/JSON-LD image URLs absolute. Idempotent. Run from repo root."""
import re, os, sys, posixpath
ROOT = os.getcwd()
ORIGIN = "https://unpeeldesign.com"
SKIP = re.compile(r'^(https?:|mailto:|tel:|#|data:|javascript:|//)')
ATTR = re.compile(r'''(?P<pre>\b(?:href|src|poster|content)=)(?P<q>["'])(?P<val>[^"']*)(?P=q)''')

def clean_page(path):            # 'nl/index.html' -> '/nl/', 'works.html' -> '/works'
    if path.endswith('index.html'):
        d = path[:-len('index.html')]
        return '/' + d
    return '/' + re.sub(r'\.html$', '', path)

def rewrite(html_path):
    page_dir = posixpath.dirname(html_path.replace(os.sep, '/'))
    src = open(html_path, encoding='utf-8').read()
    def repl(m):
        val = m.group('val')
        if SKIP.match(val) or val == '' or val.startswith('/'):
            # content="..." for og:image already root-relative -> make absolute below
            if m.group('pre').startswith('content=') and val.startswith('/uploads/'):
                return f"{m.group('pre')}{m.group('q')}{ORIGIN}{val}{m.group('q')}"
            return m.group(0)
        # only touch content= when it's a path to an upload (og:image/twitter:image)
        if m.group('pre').startswith('content=') and not re.match(r'^(\.\./)*uploads/', val):
            return m.group(0)
        frag = ''
        if '#' in val:
            val, frag = val.split('#', 1); frag = '#' + frag
        target = posixpath.normpath(posixpath.join(page_dir, val)) if page_dir else posixpath.normpath(val)
        if target.startswith('..'):
            return m.group(0)
        if target.endswith('.html'):
            new = clean_page(target)
        else:
            new = '/' + target
        if m.group('pre').startswith('content='):
            new = ORIGIN + new
        return f"{m.group('pre')}{m.group('q')}{new}{frag}{m.group('q')}"
    out = ATTR.sub(repl, src)
    # JSON-LD / inline: "image": "uploads/..." or "../uploads/..."
    out = re.sub(r'("(?:image|logo|thumbnailUrl|contentUrl)"\s*:\s*")(?:\.\./)*(uploads/[^"]+)"', lambda m: f'{m.group(1)}{ORIGIN}/{m.group(2)}"', out)
    if out != src:
        open(html_path, 'w', encoding='utf-8').write(out)
        return True
    return False

changed = 0
for dp, dn, fn in os.walk(ROOT):
    if '.git' in dp or 'node_modules' in dp: continue
    for f in fn:
        if f.endswith('.html') and f != 'index-v1.html':
            p = os.path.relpath(os.path.join(dp, f), ROOT)
            if rewrite(p): changed += 1; print('rewrote', p)
print('changed files:', changed)
