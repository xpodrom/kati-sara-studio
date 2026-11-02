p = 'index.html'
t = open(p, encoding='utf-8').read()

css_anchor = '.pgrid{display:grid;'
shine_css = '''.giant .r{background:linear-gradient(94deg, #d2ab55 0%, #f6e8c2 22%, #ffe9b8 30%, #d2ab55 46%, #b8903f 78%);background-size:260% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;animation:shine 7s ease-in-out infinite;text-shadow:0 0 26px rgba(210,171,85,.12)}
@keyframes shine{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
#island .island-logo{filter:drop-shadow(0 0 6px rgba(210,171,85,.35));animation:logoPulse 3.2s ease-in-out infinite}
@keyframes logoPulse{0%,100%{filter:drop-shadow(0 0 4px rgba(210,171,85,.28))}50%{filter:drop-shadow(0 0 12px rgba(232,207,148,.6))}}
.srow:hover .sname,.prow:hover .pval{text-shadow:0 0 18px rgba(232,207,148,.5)}
'''
assert css_anchor in t
t = t.replace(css_anchor, shine_css + css_anchor)
open(p, 'w', encoding='utf-8').write(t)
print('css ok, size:', len(t))
