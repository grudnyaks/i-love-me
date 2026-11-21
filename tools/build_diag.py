"""Данные для i-love-me.ru/diagnostika из справочника (DIAG, препараты, фото).
Запуск: python3 tools/build_diag.py <путь к репозиторию справочника>"""
import json, re, sys, pathlib, shutil
SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '../mesoestetic-guide_ru')
ROOT = pathlib.Path(__file__).resolve().parent.parent
s = (SRC / 'index.html').read_text(encoding='utf-8')
grab = lambda name: json.loads(re.search(rf'^const {name} = (\{{.*\}});\s*$', s, re.M).group(1))
D, DIAG = grab('DATA'), grab('DIAG')
CODES = ['T-DABS0002', 'T-DABS0003', 'T-DABS0004', 'T-DAFS0003', 'T-DAFS0004', 'T-DAFS0005', 'T-DAWS0003', 'T-DAWS0004', 'T-DAWS0005', 'T-DAWS0006', 'T-DAWS0007', 'T-DMOI0001',
         'T-DHIG0004', 'T-DHIG0005', 'T-DHIG0009', 'T-DHIG0010', 'T-DSUN0030', 'T-DSUN0034', 'T-PHIG0023', 'T-PPEL0001'] + [f'T-PAGE{n:04d}' for n in range(9, 20)]
photos = set(D.get('photos', [])); out = {}
(ROOT / 'img/p/sm').mkdir(parents=True, exist_ok=True)
for p in D['products']:
    if p['code'] not in CODES: continue
    ph = p['code'] in photos
    out[p['code']] = {'ru': p['ru'], 'en': p['en'], 'size': p.get('size', ''), 'ph': ph}
    if ph:
        shutil.copy(SRC / 'photos' / f"{p['code']}.webp", ROOT / 'img/p' / f"{p['code']}.webp")
        shutil.copy(SRC / 'photos/sm' / f"{p['code']}.webp", ROOT / 'img/p/sm' / f"{p['code']}.webp")
miss = [c for c in CODES if c not in out]
data = {'diag': DIAG, 'prod': out}
(ROOT / 'diagnostika/data.js').write_text('window.DGDATA = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
print('препаратов', len(out), 'с фото', sum(v['ph'] for v in out.values()), 'нет в базе', miss)
