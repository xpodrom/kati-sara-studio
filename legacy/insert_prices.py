import json

rows = json.load(open('legacy/prices.json', encoding='utf-8'))
blocks = []
for g in rows:
    cat = g['category']
    items_html = []
    for it in g['items']:
        if 'to' in it:
            price = f'<span class="pm">מ</span> {it["from"]} <span class="pto">עד</span> {it["to"]}'
        else:
            price = f'<span class="pm">מ</span> {it["from"]}'
        items_html.append(
            f'<div class="prow"><span class="pname">{it["name"]}</span>'
            f'<span class="pval">{price} <i>₪</i></span></div>'
        )
    blocks.append(
        f'<div class="pcat"><h3>{cat}</h3>{"".join(items_html)}</div>'
    )

section = '''<section class="panel hl" id="prc" style="min-height:auto;padding:10svh 6vw">
<div>
<div class="kick rl">המחירון</div>
<h2 class="rl" style="margin-top:10px">המחירון הרשמי</h2>
<p class="sub rl" style="transition-delay:.2s">הרשימה המלאה כפי שמופיעה בסטודיו — <b>מחירי התחלה ("מ-")</b>, והרבה טיפולים בטווח לפי מורכבות ואורך שיער. המחיר הסופי נקבע תמיד בשיחה לפני הטיפול, ובלי הפתעות במכשיר.</p>
<div class="pgrid">%s</div>
</div>
</section>
''' % ("".join(blocks))

t = open('index.html', encoding='utf-8').read()
anchor = '<section class="panel final" id="s5">'
assert anchor in t and '#prc' not in t
t = t.replace(anchor, section + anchor)
open('index.html', 'w', encoding='utf-8').write(t)
print('section inserted, size:', len(t))
print('pcat count:', t.count('class="pcat"'))
print('prow count:', t.count('class="prow"'))
