import re, json

t = open('legacy/old-site-index.html', encoding='utf-8', errors='replace').read()

# split document by category h3 headers
parts = re.split(r'<h3 class="CanTranslated">(.*?)</h3>', t)
groups = []
for i in range(1, len(parts), 2):
    cat = parts[i].strip()
    blocks = re.findall(r'<div class="menu_item[^"]*">.*?(?=</div>)', parts[i + 1], flags=re.S)
    rows = []
    for b in blocks:
        m = re.search(r'<h4[^>]*>(.*?)</h4>.*?<span class="price">(.*?)<hr', b, flags=re.S)
        if not m:
            continue
        name = re.sub(r'<[^>]+>', ' ', m.group(1))
        name = re.sub(r'\s+', ' ', name).strip().replace('\\', ' / ')
        ps = m.group(2)
        ps = re.sub(r'<span[^>]*>\s*מ\s*</span>', ' FROM ', ps)
        ps = re.sub(r'<span[^>]*>\s*עד\s*</span>', ' TO ', ps)
        ps_txt = re.sub(r'<[^>]+>', ' ', ps)
        if 'FROM' in ps_txt and 'TO' in ps_txt:
            front = re.search(r'FROM\s*(\d{2,4})', ps_txt)
            back = re.search(r'TO\s*(\d{2,4})', ps_txt)
            if front and back:
                rows.append({'name': name, 'from': int(front.group(1)), 'to': int(back.group(1))})
        else:
            nums = re.findall(r'\d{2,4}', ps_txt)
            if nums:
                rows.append({'name': name, 'from': int(nums[0])})
    groups.append({'category': cat, 'items': rows})
    print(cat, '->', len(rows), 'items')

total = sum(len(g['items']) for g in groups)
print('TOTAL:', total)
json.dump(groups, open('legacy/prices.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
