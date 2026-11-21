"""Страница i-love-me.ru/brand (вариант Б1 «Атомный номер 85») из данных справочника.
Запуск: python3 tools/build_brand.py <путь к репозиторию справочника>"""
import json, re, sys, base64, pathlib, html
E = html.escape
SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '../mesoestetic-guide_ru')
ROOT = pathlib.Path(__file__).resolve().parent.parent
s = (SRC / 'index.html').read_text(encoding='utf-8')
grab = lambda name: json.loads(re.search(rf'^const {name} = (\{{.*?\}});\s*$', s, re.M).group(1))
A, PH = grab('DATA')['about'], grab('PH')
(ROOT / 'img/brand').mkdir(parents=True, exist_ok=True)
for k, v in PH.items():
    (ROOT / 'img/brand' / f'{k}.webp').write_bytes(base64.b64decode(v.split(',', 1)[1]))
nb = lambda t: re.sub(r'(^|[\s(«])([а-яёА-ЯЁa-zA-Z]{1,2}) ', '\\1\\2 ', E(t))
F, H, PR = A['facts'], A['history'], A['principles']
ME = '<svg class="me" viewBox="0 0 100 100" aria-hidden="true"><rect x="3.5" y="3.5" width="93" height="93" fill="none" stroke="#fff" stroke-width="7"/><text x="11" y="74" font-size="46" font-weight="700" fill="#fff">Me</text><text x="88" y="21" font-size="11" font-weight="700" fill="#fff" text-anchor="end">85</text></svg>'
facts = ''.join(f'<div class="glass rv" style="--d:{i * 70}ms"><b>{E(b)}</b><span>{nb(t)}</span></div>' for i, (b, t) in enumerate(F))
tl = ''.join(f'<div class="glass"><b>{y}</b><span>{nb(t)}</span></div>' for y, t in H)
pr = ''.join(f'<div class="glass rv" style="--d:{i * 80}ms"><i>0{i + 1}</i><h3>{E(b)}</h3><p>{nb(t)}</p></div>' for i, (b, t) in enumerate(PR))
gal = [('building', 'Штаб-квартира mesoestetic Pharma Group, Виладеканс'), ('prod015', 'Производственный цех'), ('prod007', 'Чистая зона'), ('prod017', 'Линия фасовки'),
       ('prod024', 'Наполнение флаконов'), ('prod025', 'Производство ампул'), ('sunset', 'Кампус компании на закате')]
galh = ''.join(f'<figure class="g{i}"><img src="../img/brand/{k}.webp" alt="{E(c)}" loading="lazy"><figcaption>{E(c)}</figcaption></figure>' for i, (k, c) in enumerate(gal))
ct = A['contact']

out = f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>О бренде mesoestetic — фармацевтическая лаборатория с 1985 года</title>
<meta name="description" content="{E(A['lead'])}">
<meta property="og:title" content="mesoestetic — атомный номер 85"><meta property="og:description" content="{E(A['lead'])}">
<meta property="og:image" content="https://i-love-me.ru/img/og-brand.jpg"><meta name="theme-color" content="#030303">
<link rel="icon" href="../img/icon-192.png"><link rel="apple-touch-icon" href="../img/apple-touch-icon.png">
<style>
*{{box-sizing:border-box;margin:0}}html{{background:#030303}}html,body{{overflow-x:hidden}}
body{{font-family:Inter,"Helvetica Neue",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased;background:#030303;color:#f3f3f3;-webkit-text-size-adjust:100%}}
a{{color:inherit;text-decoration:none}}.w{{max-width:1100px;margin:0 auto;padding:0 40px}}.me text{{font-family:Inter,Arial,sans-serif}}
.top{{position:sticky;top:0;z-index:20;background:rgba(3,3,3,.6);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-bottom:1px solid rgba(255,255,255,.08)}}
.top .w{{display:flex;align-items:center;height:64px;gap:10px}}.top .me{{width:30px}}.top b{{font-size:17px}}.top nav{{margin-left:auto;display:flex;gap:6px}}.top nav a{{padding:8px 13px;font-size:14px;color:#bdbdbd;border-radius:999px}}.top nav a.on{{color:#fff}}.top nav a.cta{{border:1px solid rgba(255,255,255,.3);color:#fff;font-weight:600}}
.mono{{font-family:"SF Mono",ui-monospace,Menlo,Consolas,"DejaVu Sans Mono",monospace;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#8d8d8d}}
.glass{{background:linear-gradient(150deg,rgba(255,255,255,.1),rgba(255,255,255,.03));border:1px solid rgba(255,255,255,.14);border-radius:24px;backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}}
.rv{{opacity:0;transform:translateY(36px);transition:opacity .9s var(--d,0ms),transform .9s cubic-bezier(.2,.8,.2,1) var(--d,0ms)}}.rv.in{{opacity:1;transform:none}}
.hero{{position:relative;height:calc(100svh - 64px);min-height:600px;max-height:900px;display:flex;align-items:center;justify-content:center;overflow:hidden}}
.glow{{position:absolute;width:640px;height:640px;border-radius:50%;background:conic-gradient(#F57CAC,#AE8BCD,#24AEEA,#79BFAB,#F2B705,#F57CAC);filter:blur(110px);opacity:.35;animation:rot 22s linear infinite}}@keyframes rot{{to{{transform:rotate(360deg)}}}}
.orb{{position:absolute;border:1px solid rgba(255,255,255,.14);border-radius:50%}}.orb i{{position:absolute;top:-5px;left:50%;width:10px;height:10px;margin-left:-5px;border-radius:50%;background:#fff;box-shadow:0 0 16px #fff}}
.o1{{width:440px;height:440px;animation:rot 9s linear infinite}}.o2{{width:600px;height:220px;transform:rotate(30deg)}}.o3{{width:560px;height:200px;transform:rotate(-35deg);border-color:rgba(255,255,255,.08)}}
.el{{position:relative;width:300px;height:300px;border:16px solid #fff;display:flex;align-items:flex-end;padding:22px;animation:pop 1.2s cubic-bezier(.2,.8,.2,1) both}}@keyframes pop{{from{{transform:scale(.6);opacity:0}}}}
.el b{{font-size:150px;line-height:.8;letter-spacing:-.05em}}.el i{{position:absolute;top:16px;right:22px;font-style:normal;font-size:40px;font-weight:700}}.el small{{position:absolute;bottom:-46px;left:0;font-size:22px;font-weight:600}}
.ann{{position:absolute;font-size:14px;color:#cfcfcf;display:flex;align-items:center;gap:10px;white-space:nowrap;animation:fade 1s 1s both}}@keyframes fade{{from{{opacity:0}}}}.ann::before{{content:"";width:70px;height:1px;background:rgba(255,255,255,.5)}}
.a1{{left:calc(50% + 160px);top:calc(50% - 140px)}}.a2{{right:calc(50% + 160px);top:calc(50% + 70px);flex-direction:row-reverse;animation-delay:1.3s}}.a3{{left:calc(50% + 110px);top:calc(50% + 175px);animation-delay:1.6s}}
.legend{{display:none}}
h1{{font-size:76px;letter-spacing:-.05em;line-height:.95;margin-top:14px}}
.sec{{padding:110px 0}}.lead{{font-size:26px;line-height:1.4;max-width:820px;letter-spacing:-.01em;margin-top:22px}}.lead.m{{color:#a8a8a8}}
.facts{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:44px}}.facts div{{padding:30px}}.facts b{{font-size:56px;letter-spacing:-.04em;display:block;margin-bottom:6px}}.facts span{{color:#a3a3a3;font-size:15px;line-height:1.45}}
.tlw{{position:relative;margin-top:40px}}.tlw::before{{content:"";position:absolute;left:0;right:0;top:0;height:1px;background:linear-gradient(90deg,#fff,rgba(255,255,255,.1))}}
.tl{{display:flex;gap:16px;overflow-x:auto;padding:30px 40px 24px;margin:0 -40px;scroll-snap-type:x mandatory;scrollbar-width:none;-webkit-overflow-scrolling:touch;cursor:grab}}.tl::-webkit-scrollbar{{display:none}}
.tl div{{flex:none;width:250px;scroll-snap-align:start;padding:24px;position:relative}}.tl div::before{{content:"";position:absolute;left:24px;top:-35px;width:10px;height:10px;border-radius:50%;background:#fff;box-shadow:0 0 14px #fff}}
.tl b{{font-size:38px;letter-spacing:-.03em;display:block;margin-bottom:10px}}.tl span{{color:#b3b3b3;font-size:15px;line-height:1.45}}
.hint{{display:flex;justify-content:space-between;align-items:center;margin-top:6px}}.hint button{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.25);color:#fff;width:44px;height:44px;border-radius:50%;font-size:18px;cursor:pointer;margin-left:8px}}
.pr{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:40px}}.pr div{{padding:32px}}.pr h3{{font-size:24px;margin:16px 0 10px;letter-spacing:-.02em}}.pr p{{color:#a8a8a8;line-height:1.5}}.pr i{{font-style:normal;font-size:13px;color:#8d8d8d}}
.gal{{display:grid;grid-template-columns:repeat(6,1fr);grid-auto-rows:150px;gap:12px;margin-top:40px}}
.gal figure{{position:relative;overflow:hidden;border-radius:20px;margin:0}}.gal img{{width:100%;height:100%;object-fit:cover;transition:transform .8s}}.gal figure:hover img{{transform:scale(1.05)}}
.gal figcaption{{position:absolute;left:0;right:0;bottom:0;padding:30px 16px 12px;font-size:13px;color:#eee;background:linear-gradient(transparent,rgba(0,0,0,.7))}}
.g0{{grid-column:span 4;grid-row:span 3}}.g1,.g2{{grid-column:span 2;grid-row:span 1}}.g1{{grid-row:span 2}}.g3,.g4,.g5{{grid-column:span 2;grid-row:span 2}}.g6{{grid-column:span 6;grid-row:span 3}}
.sun{{margin-top:16px;padding:32px;display:grid;grid-template-columns:auto 1fr;gap:24px;align-items:center}}.sun b{{font-size:54px;letter-spacing:-.04em;background:linear-gradient(90deg,#F2B705,#79BFAB);-webkit-background-clip:text;background-clip:text;color:transparent}}.sun p{{color:#b5b5b5;line-height:1.55}}
.back{{text-align:center;padding:40px 0 110px}}.back a{{display:inline-block;background:#fff;color:#000;border-radius:16px;padding:16px 24px;font-weight:600}}
footer{{border-top:1px solid rgba(255,255,255,.1);padding:34px 0 calc(34px + env(safe-area-inset-bottom));color:#888;font-size:14px;line-height:1.6}}
@media(max-width:700px){{.w{{padding:0 22px}}.top nav a:not(.cta){{display:none}}.hero{{height:600px;min-height:0;padding-bottom:110px}}
.el{{width:200px;height:200px;border-width:11px;padding:16px}}.el b{{font-size:100px}}.el i{{font-size:26px;top:10px;right:14px}}.el small{{font-size:17px;bottom:-36px}}
.o1{{width:300px;height:300px}}.o2{{width:380px;height:150px}}.o3{{width:340px;height:120px}}.glow{{width:420px;height:420px}}.ann{{display:none}}
.legend{{display:grid;gap:8px;position:absolute;bottom:22px;left:22px;right:22px;font-size:13px;color:#cfcfcf;animation:fade 1s 1s both}}.legend span::before{{content:"— ";color:#777}}
h1{{font-size:38px}}.lead{{font-size:19px}}.sec{{padding:70px 0}}.facts{{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}}.facts div{{padding:18px}}.facts b{{font-size:32px}}.facts span{{font-size:13px}}
.tl{{padding:30px 22px 24px;margin:0 -22px}}.tl div{{width:220px}}.pr{{grid-template-columns:1fr}}.pr div{{padding:24px}}
.gal{{grid-template-columns:repeat(2,minmax(0,1fr));grid-auto-rows:120px}}.g0,.g6{{grid-column:span 2;grid-row:span 2}}.g1,.g2,.g3,.g4{{grid-column:span 1;grid-row:span 1}}.g5{{grid-column:span 2;grid-row:span 1}}
.sun{{grid-template-columns:1fr;padding:24px;gap:8px}}.sun b{{font-size:40px}}}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}.rv{{opacity:1;transform:none}}}}
</style></head><body>
<header class="top"><div class="w"><a href="../" style="display:flex;align-items:center;gap:10px" aria-label="На главную">{ME}<b>mesoestetic</b></a><nav><a href="../diagnostika/">Диагностика</a><a class="on" href="./">О бренде</a><a class="cta" href="../#download">Скачать</a></nav></div></header>
<section class="hero"><div class="glow"></div><div class="orb o1"><i></i></div><div class="orb o2"></div><div class="orb o3"></div>
<div class="el" role="img" aria-label="Знак mesoestetic: элемент Me с атомным номером 85"><i>85</i><b>Me</b><small>mesoestetic</small></div>
<span class="ann a1">атомный номер 85 — год основания</span><span class="ann a2">символ Me — инициалы бренда</span><span class="ann a3">название — логотип</span>
<div class="legend"><span>85 — год основания</span><span>Me — инициалы бренда</span><span>название — логотип</span></div></section>
<section class="sec"><div class="w"><span class="mono">01 · Кто мы</span><h1 class="rv">Фармацевтическая<br>лаборатория<br>из&nbsp;Барселоны</h1><p class="lead rv">{nb(A['lead'])}</p><p class="lead m rv">{nb(A['quote'])}</p>
<div class="facts">{facts}</div></div></section>
<section class="sec" style="padding-top:0"><div class="w"><span class="mono">02 · 40 лет за 10 секунд</span><h1 class="rv">История</h1>
<div class="tlw"><div class="tl" id="tl">{tl}</div></div><div class="hint"><span class="mono">листайте →</span><span><button type="button" data-tl="-1" aria-label="Назад">←</button><button type="button" data-tl="1" aria-label="Вперёд">→</button></span></div></div></section>
<section class="sec" style="padding-top:20px"><div class="w"><span class="mono">03 · Принципы</span><h1 class="rv">Наука — до&nbsp;красоты</h1><div class="pr">{pr}</div></div></section>
<section class="sec" style="padding-top:0"><div class="w"><span class="mono">04 · Собственное производство</span><h1 class="rv">От молекулы<br>до&nbsp;флакона</h1><p class="lead m rv">{nb(A['production'])}</p>
<div class="gal rv">{galh}</div><div class="sun glass rv"><b>100%</b><p>{nb(A['sustain'])}</p></div></div></section>
<div class="back"><a href="../">Скачать справочник специалиста</a></div>
<footer><div class="w"><b style="color:#fff">{E(ct[0])}</b><br>{E(ct[1].splitlines()[0])}<br>+7 (495) 960-14-36 · mesoestetic@beauty-a.ru</div></footer>
<script>
(function(){{
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window){{ var io = new IntersectionObserver(function(es){{ es.forEach(function(x){{ if (x.isIntersecting){{ x.target.classList.add('in'); io.unobserve(x.target); }} }}); }}, {{threshold: .12}}); rv.forEach(function(x){{ io.observe(x); }}); }}
  else rv.forEach(function(x){{ x.classList.add('in'); }});
  var tl = document.getElementById('tl');
  document.querySelectorAll('[data-tl]').forEach(function(b){{ b.addEventListener('click', function(){{ tl.scrollBy({{left: +b.dataset.tl * 266, behavior: 'smooth'}}); }}); }});
  // перетаскивание мышью на компьютере
  var down = false, sx = 0, sl = 0;
  tl.addEventListener('mousedown', function(e){{ down = true; sx = e.pageX; sl = tl.scrollLeft; tl.style.scrollSnapType = 'none'; }});
  addEventListener('mouseup', function(){{ if (down){{ down = false; tl.style.scrollSnapType = ''; }} }});
  addEventListener('mousemove', function(e){{ if (down){{ e.preventDefault(); tl.scrollLeft = sl - (e.pageX - sx); }} }});
}})();
</script></body></html>'''
(ROOT / 'brand/index.html').write_text(out, encoding='utf-8')
print('brand/index.html', len(out))
