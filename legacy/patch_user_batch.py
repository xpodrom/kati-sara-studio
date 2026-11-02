import re, sys
from urllib.parse import quote

p = 'index.html'
t = open(p, encoding='utf-8').read()
ok = []

def rep(tag, old, new, count=1):
    global t
    if old in t:
        t = t.replace(old, new, count)
        ok.append(tag)
    else:
        print('MISS:', tag)

WA = 'https://wa.me/972538247102?text=' + quote('שלום, אני מעוניין בפרטים על טיפול...', safe='')

# 1) remove scene captions
rep('cut element', '<div id="cut">סצנה <b>01</b> מתוך 05</div>\n', '')
rep('cut css', '#cut{position:fixed;top:66px;inset-inline-start:50%;translate:50% 0;z-index:6;font-size:10.5px;letter-spacing:.5em;color:var(--soft);opacity:.7}\n#cut b{color:var(--gold)}\n', '')
rep('cutEl ref', "const cutEl = document.getElementById('cut');\n", '')
rep('cutEl innerHTML', "cutEl.innerHTML = 'סצנה <b>0' + n + '</b> מתוך 05';\n", '')
rep('noscript cut', '#gl,#grain,#cut{display:none}', '#gl,#grain{display:none}')
rep('kick s2', 'סצנה 02 · העבודה', 'העבודה שלך')
rep('kick s3', 'סצנה 03 · הפריימים', 'הפריימים שלנו')
rep('kick s4', 'סצנה 04 · במספרים', 'הדרך שלנו')
rep('kick s5', 'הסצנה האחרונה', 'מחכים לך')

# 2) rings/halo closer to logo + halo-tight
rep('halo closer', '.halo{position:absolute;inset:-16%;', '.halo{position:absolute;inset:-9%;')
rep('ring1 closer', '.ring{position:absolute;inset:-7%;', '.ring{position:absolute;inset:-3%;')
rep('ring2 closer', '.ring.r2{inset:-13%;', '.ring.r2{inset:-6%;')
rep('ring mobile', '.ring{inset:-4%}\n.ring.r2{inset:-9%}', '.ring{inset:-2%}\n.ring.r2{inset:-5%}')

# 3) remove leaking sheen on the bottom CTA
rep('sheen css', '.gbtn::after{content:""; position:absolute; top:0; bottom:0; width:34%;background:linear-gradient(105deg, transparent, rgba(255,255,255,.22), transparent);inset-inline-start:-40%; transform:skewX(-18deg); animation:sheen 5.5s ease-in-out infinite}\n', '')
rep('sheen keyframes', '@keyframes sheen{0%,55%{inset-inline-start:-45%}75%,100%{inset-inline-start:130%}}\n', '')

# 4) more particles + bottom-left bias
rep('arc count', 'const N_ARCS = IS_MOB ? 6 : 9, PER = IS_MOB ? 90 : 150;', 'const N_ARCS = IS_MOB ? 8 : 12, PER = IS_MOB ? 105 : 165;')
rep('arc shift', 'const bx = (a - (N_ARCS-1)/2) * 3.1;\nconst y0 = -7 + Math.sin(a*2.1)*2.4;', 'const bx = (a - (N_ARCS-1)/2) * 3.0 - 2.6;\nconst y0 = -8.2 + Math.sin(a*2.1)*2.2;')

# 5) services: no microblading, old-site service names
rep('svc row1', '<a class="srow" href="tel:0538247102"><span class="snum">01</span><span class="sname">מיקרובלדינג — גבות</span><span class="sdesc">שער-אחר-שער, בקו אמן. גבות שנראות כאילו נולדו ככה</span></a>',
 '<a class="srow" href="tel:0538247102"><span class="snum">01</span><span class="sname">גבות בשיטת הפודרה</span><span class="sdesc">גוון מדויק, מהמם ושפיר</span></a>')
rep('svc sub', '<b>איפור קבוע · מיקרובלדינג גבות · למינציה לריסים · קעקוע קוסמטי.</b>', '<b>איפור קבוע · גבות ושפתיים בשיטת הפודרה · למינציה לריסים · הסרת איפור קבוע.</b>')
rep('og desc', 'מיקרובלדינג, איפור קבוע, למינציה לריסים וקעקוע קוסמטי.', 'איפור קבוע, גבות ושפתיים בשיטת הפודרה, למינציה לריסים והסרת איפור קבוע.')

# 6) numbers section: remove big 21% + facts, keep process steps
rep('deep block', '<div class="deep rl">21%</div>', '')
old_facts = re.search(r'<div class="facts">.*?</div>\n', t, flags=re.S)
if old_facts:
    t = t.replace(old_facts.group(0), '')
    ok.append('facts removed')

# 7) waze deep navigation with coordinates
rep('waze ll', 'href="https://waze.com/ul?q=%D7%91%D7%9C%D7%A4%D7%95%D7%A8%2031%20%D7%90%D7%A9%D7%A7%D7%9C%D7%95%D7%9F&navigate=yes&zoom=17"',
    'href="https://waze.com/ul?ll=31.6903642%2C34.5783461&navigate=yes&zoom=17"')

# 8) whatsapp prefill text everywhere
n = len(re.findall(r'https://wa\.me/972538247102\?text=[^"]*', t))
t = re.sub(r'https://wa\.me/972538247102\?text=[^"]*', WA, t)
ok.append(f'wa links: {n}')

# 9) price disclaimers from old site + dynamic loading hook
DISC = '''<div class="pnotes"><ul>
<li>המחירים לטיפולי איפור קבוע הם לטיפול אחד בלבד, ובמידת הצורך ניתן לקבל טיפול שני להדגשה עד חודשיים מהטיפול הראשון.</li>
<li>כל המחירים ניתנים לשינוי על ידי בעלת העסק על פי שיקול דעתה בכל עת.</li>
<li>בשירותי איפור מקצועי ועיצוב שיער המחיר אינו כולל הגעה לבית הלקוח.</li>
<li>ברכישת חבילת הסרה בלייזר או ברמובר בעלת העסק תוכל לשלב את שתי שיטות הטיפול עפ שיקול דעתה המקצועי.</li>
</ul></div>'''
rep('disclaimers', '</div>\n</div>\n</section>\n<section class="panel final" id="s5">', DISC + '\n</div>\n</div>\n</section>\n<section class="panel final" id="s5">')
rep('pnotes css', 'li>' in t and '.pnotes{margin-top:26px;display:flex;flex-direction:column;gap:8px;color:var(--soft);font-size:13.5px;font-weight:300}\n.pnotes li{list-style:none;border-top:1px dashed rgba(243,237,226,.14);padding-top:8px}\n', '.pnotes{margin-top:26px;display:flex;flex-direction:column;gap:8px;color:var(--soft);font-size:13.5px;font-weight:300}\n.pnotes li{list-style:none;border-top:1px dashed rgba(243,237,226,.14);padding-top:8px}\n')

# 10) two instagram profiles
rep('ig extra', 'aria-label="Instagram"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg></a>\n<a class="sicon" href="https://www.facebook.com/share/1FMhsmJD55/"',
    'aria-label="Instagram"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg></a>\n<a class="sicon" href="https://www.instagram.com/kati_sara_makeup_artist/" target="_blank" rel="noopener" aria-label="Instagram 2"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg></a>\n<a class="sicon" href="https://www.facebook.com/share/1FMhsmJD55/"')

open(p, 'w', encoding='utf-8').write(t)
print('APPLIED:', ok, '| size:', len(t))
