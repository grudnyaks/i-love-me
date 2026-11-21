"""Собирает главную i-love-me.ru (вариант «Орбита») из данных справочника.
Запуск: python3 tools/build_landing.py <путь к index.html справочника>"""
import json, re, sys, html, pathlib
E = html.escape
src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '../mesoestetic-guide_ru/index.html').read_text(encoding='utf-8')
D = json.loads(re.search(r'^const DATA = (\{.*\});\s*$', src, re.M).group(1))
L = D['lines']; NP = len(D['products']); NPR = len(D.get('protocols', [])) or 25
cnt = {l['id']: sum(p['line'] == l['id'] for p in D['products']) for l in L}
ROOT = pathlib.Path(__file__).resolve().parent.parent
APK = 'https://github.com/grudnyaks/mesoestetic-guide_ru/releases/latest/download/mesoestetic-guide.apk'
WEB = 'https://app.i-love-me.ru/'

ME = lambda c='currentColor', cls='': f'<svg class="me {cls}" viewBox="0 0 100 100" aria-hidden="true"><rect x="3.5" y="3.5" width="93" height="93" fill="none" stroke="{c}" stroke-width="7"/><text x="11" y="74" font-size="46" font-weight="700" fill="{c}">Me</text><text x="88" y="21" font-size="11" font-weight="700" fill="{c}" text-anchor="end">85</text><text x="12" y="88" font-size="8" font-weight="600" fill="{c}">mesoestetic</text></svg>'
AND = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M17.6 9.5l1.7-3a.4.4 0 0 0-.7-.4l-1.8 3A10.6 10.6 0 0 0 12 8a10.6 10.6 0 0 0-4.8 1.1l-1.8-3a.4.4 0 0 0-.7.4l1.7 3A9.6 9.6 0 0 0 2 17h20a9.6 9.6 0 0 0-4.4-7.5zM7 14.3a1 1 0 1 1 0-2 1 1 0 0 1 0 2zm10 0a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>'
APL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16.4 12.6c0-2.6 2.1-3.8 2.2-3.9a4.8 4.8 0 0 0-3.8-2c-1.6-.2-3.1.9-3.9.9s-2-.9-3.4-.9a5 5 0 0 0-4.2 2.6c-1.8 3.1-.5 7.7 1.3 10.2.9 1.2 1.9 2.6 3.2 2.6s1.8-.8 3.3-.8 2 .8 3.3.8 2.2-1.3 3-2.5a10.8 10.8 0 0 0 1.4-2.8 4.3 4.3 0 0 1-2.4-4.2zM13.9 5a4.4 4.4 0 0 0 1-3.2 4.5 4.5 0 0 0-2.9 1.5 4.2 4.2 0 0 0-1 3.1 3.7 3.7 0 0 0 2.9-1.4z"/></svg>'
DL = f'<div class="dl"><a class="b1" href="{APK}" data-os="android">{AND}<span><small>Скачать для</small>Android</span></a><a class="b2" href="#ios" data-os="ios">{APL}<span><small>Установить на</small>iPhone</span></a></div>'
step = 360 / len(L)
TILES = ''.join(f'<div class="tl" style="--c:{l["color"]};--a:{i * step:.3f}deg"><b>{E(l["sym"])}</b></div>' for i, l in enumerate(L))
SCR = ''.join(f'<img src="img/app_{n}.webp" alt="" style="--k:{k}"{" loading=lazy" if k else ""}>' for k, n in enumerate(['home_d', 'line_d', 'proto', 'prod']))

html_out = f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>mesoestetic — справочник специалиста</title>
<meta name="description" content="Приложение-справочник mesoestetic® для косметологов и врачей: {NP} препаратов, {len(L)} линий, протоколы и диагностика age element®.">
<meta property="og:title" content="mesoestetic — главный элемент для экспертов в уходе за кожей">
<meta property="og:description" content="Справочник специалиста: препараты, составы, протоколы и диагностика — в телефоне.">
<meta property="og:image" content="https://i-love-me.ru/img/og.jpg"><meta name="theme-color" content="#030303">
<link rel="icon" href="img/icon-192.png"><link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<style>
*{{box-sizing:border-box;margin:0}}html{{background:#030303;scroll-behavior:smooth}}html,body{{overflow-x:hidden}}
body{{font-family:Inter,"Helvetica Neue",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased;background:#030303;color:#f3f3f3;-webkit-text-size-adjust:100%}}
a{{color:inherit;text-decoration:none}}.w{{max-width:1200px;margin:0 auto;padding:0 40px}}.me text{{font-family:Inter,Arial,sans-serif}}
.top{{position:sticky;top:0;z-index:20;background:rgba(3,3,3,.6);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-bottom:1px solid rgba(255,255,255,.08)}}
.top .w{{display:flex;align-items:center;height:68px;gap:12px}}.top .me{{width:32px}}.top b{{font-size:18px;letter-spacing:-.01em}}
.top nav{{margin-left:auto;display:flex;gap:6px;align-items:center}}.top nav a{{padding:8px 14px;font-size:14px;color:#bdbdbd;border-radius:999px}}.top nav a:hover{{color:#fff}}
.top nav a.cta{{border:1px solid rgba(255,255,255,.3);color:#fff;font-weight:600}}
.hero{{position:relative;height:900px;display:flex;align-items:flex-start;justify-content:center;padding-top:50px;overflow:hidden}}
.glow,.orbit{{position:absolute;left:50%;top:calc(50px + 314px);border-radius:50%;transform:translate(-50%,-50%)}}
.glow{{width:760px;height:760px;background:conic-gradient(from 0deg,#F57CAC,#AE8BCD,#24AEEA,#79BFAB,#F2B705,#E2001A,#F57CAC);filter:blur(110px);opacity:.42;animation:rot 20s linear infinite}}
.orbit{{width:780px;height:780px;border:1px dashed rgba(255,255,255,.12);animation:rot 60s linear infinite}}
@keyframes rot{{to{{transform:translate(-50%,-50%) rotate(360deg)}}}}@keyframes unrot{{to{{transform:rotate(-360deg)}}}}
.orbit .tl{{position:absolute;left:50%;top:50%;width:70px;height:70px;margin:-35px;transform:rotate(var(--a)) translateY(-390px) rotate(calc(-1 * var(--a)))}}
.orbit .tl b{{display:flex;width:100%;height:100%;border-radius:14px;padding:8px;font-size:24px;animation:unrot 60s linear infinite;
 background:linear-gradient(150deg,color-mix(in srgb,var(--c) 70%,transparent),rgba(255,255,255,.05));border:1px solid color-mix(in srgb,var(--c) 80%,#fff 20%);box-shadow:0 0 24px -4px var(--c),inset 0 1px 0 rgba(255,255,255,.4)}}
.phone{{position:relative;z-index:2;width:290px;aspect-ratio:390/844;border-radius:46px;padding:11px;background:linear-gradient(145deg,#3a3a3a,#0b0b0b 40%,#2b2b2b);
 box-shadow:0 50px 90px -30px rgba(0,0,0,.8),inset 0 0 0 1.5px rgba(255,255,255,.25);animation:tilt 9s ease-in-out infinite}}
@keyframes tilt{{0%,100%{{transform:perspective(1200px) rotateY(-14deg) rotateX(6deg)}}50%{{transform:perspective(1200px) rotateY(14deg) rotateX(-4deg) translateY(-10px)}}}}
.scr{{position:relative;width:100%;height:100%;border-radius:36px;overflow:hidden;background:#000}}
.scr img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;animation:scr 12s infinite;animation-delay:calc(var(--k) * 3s)}}
@keyframes scr{{0%{{opacity:0;transform:translateY(14px)}}5%,25%{{opacity:1;transform:none}}30%,100%{{opacity:0}}}}
.ttl{{position:absolute;z-index:3;left:0;right:0;bottom:36px;text-align:center}}
h1{{font-size:110px;line-height:.9;letter-spacing:-.055em;mix-blend-mode:difference;animation:blin 1.4s .2s cubic-bezier(.2,.8,.2,1) both}}
@keyframes blin{{from{{filter:blur(20px);opacity:0;transform:translateY(30px)}}to{{filter:none;opacity:1;transform:none}}}}
.sub{{text-align:center;padding:10px 0 80px}}.sub p{{font-size:20px;color:#b9b9b9;max-width:640px;margin:0 auto 32px;line-height:1.5}}
.dl{{display:flex;gap:12px;flex-wrap:wrap;justify-content:center}}.dl a{{display:flex;align-items:center;gap:12px;padding:13px 22px 13px 18px;border-radius:16px;font-weight:600;font-size:19px;line-height:1.05;transition:transform .2s}}
.dl a:active{{transform:scale(.97)}}.dl svg{{width:28px;height:28px}}.dl small{{display:block;font-size:11.5px;font-weight:500;opacity:.7}}
.dl .b1{{background:#fff;color:#000}}.dl .b2{{border:1px solid rgba(255,255,255,.35);background:rgba(255,255,255,.06)}}
.dl.ios .b2{{order:-1;background:#fff;color:#000}}.dl.ios .b1{{background:rgba(255,255,255,.06);color:#fff;border:1px solid rgba(255,255,255,.35)}}
.rows{{border-top:1px solid rgba(255,255,255,.12)}}.row{{display:grid;grid-template-columns:120px 1fr 1.2fr;gap:30px;align-items:center;padding:40px 0;border-bottom:1px solid rgba(255,255,255,.12)}}
.row b{{font-size:60px;letter-spacing:-.04em}}.row h3{{font-size:34px;letter-spacing:-.03em;transition:color .3s}}.row p{{color:#9d9d9d;font-size:17px;line-height:1.5}}
.row:hover h3{{background:linear-gradient(90deg,#F57CAC,#24AEEA);-webkit-background-clip:text;background-clip:text;color:transparent}}
.row a.more{{display:inline-block;margin-top:10px;color:#fff;border-bottom:1px solid rgba(255,255,255,.4)}}
.rv{{opacity:0;transform:translateY(30px);transition:opacity .8s,transform .8s cubic-bezier(.2,.8,.2,1)}}.rv.in{{opacity:1;transform:none}}
.end{{text-align:center;padding:110px 0 90px}}.end .me{{width:110px;margin-bottom:30px;filter:drop-shadow(0 0 30px rgba(174,139,205,.8))}}
.end h2{{font-size:60px;letter-spacing:-.045em;line-height:.98;margin-bottom:34px}}.note{{color:#8a8a8a;margin-top:24px;font-size:15px;line-height:1.6}}.note a{{color:#ddd}}
footer{{border-top:1px solid rgba(255,255,255,.1);padding:34px 0 calc(34px + env(safe-area-inset-bottom));color:#777;font-size:14px;line-height:1.6}}footer .w{{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}}
.modal{{position:fixed;inset:0;z-index:50;display:flex;align-items:flex-end;justify-content:center;background:rgba(0,0,0,.6);backdrop-filter:blur(6px);opacity:0;pointer-events:none;transition:opacity .3s}}
.modal.on{{opacity:1;pointer-events:auto}}.sheet{{width:100%;max-width:520px;background:#141414;border:1px solid rgba(255,255,255,.12);border-radius:28px 28px 0 0;padding:28px 26px calc(28px + env(safe-area-inset-bottom));transform:translateY(40px);transition:transform .35s cubic-bezier(.2,.8,.2,1)}}
.modal.on .sheet{{transform:none}}.sheet h3{{font-size:24px;margin-bottom:6px}}.sheet .s{{color:#9d9d9d;margin-bottom:18px;line-height:1.45}}
.sheet ol{{list-style:none;padding:0;counter-reset:i}}.sheet li{{counter-increment:i;display:grid;grid-template-columns:36px 1fr;gap:12px;align-items:center;padding:12px 0;border-top:1px solid rgba(255,255,255,.08);font-size:16px;line-height:1.4}}
.sheet li::before{{content:counter(i);width:30px;height:30px;border-radius:50%;background:#fff;color:#000;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px}}
.sheet li svg{{width:18px;height:18px;vertical-align:-3px}}.sheet .go{{display:block;text-align:center;margin-top:18px;background:#fff;color:#000;border-radius:14px;padding:15px;font-weight:600}}.sheet .x{{float:right;background:none;border:0;color:#999;font-size:26px;cursor:pointer;margin:-8px -6px 0 0}}
@media(min-width:701px){{.modal{{align-items:center}}.sheet{{border-radius:28px}}}}
@media(max-width:700px){{.w{{padding:0 22px}}.top nav a:not(.cta){{display:none}}.hero{{height:680px;padding-top:40px}}.glow,.orbit{{top:calc(40px + 238px)}}
.glow{{width:440px;height:440px}}.orbit{{width:470px;height:470px}}.orbit .tl{{width:48px;height:48px;margin:-24px;transform:rotate(var(--a)) translateY(-235px) rotate(calc(-1 * var(--a)))}}.orbit .tl b{{font-size:17px;border-radius:10px;padding:6px}}
.phone{{width:220px;border-radius:36px;padding:8px}}.scr{{border-radius:29px}}h1{{font-size:54px}}.ttl{{bottom:24px}}.sub p{{font-size:17px}}
.row{{grid-template-columns:70px 1fr;padding:26px 0;gap:14px 18px}}.row p{{grid-column:1/-1}}.row b{{font-size:40px}}.row h3{{font-size:26px}}.end h2{{font-size:38px}}.end{{padding:80px 0 60px}}}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}.scr img:first-child{{opacity:1}}.rv{{opacity:1;transform:none}}}}
</style></head><body>
<header class="top"><div class="w">{ME('#fff')}<b>mesoestetic</b><nav><a href="/diagnostika/">Диагностика</a><a href="/brand/">О бренде</a><a class="cta" href="#download">Скачать</a></nav></div></header>
<section class="hero"><div class="glow"></div><div class="orbit">{TILES}</div><div class="phone"><div class="scr">{SCR}</div></div><div class="ttl"><h1>главный элемент</h1></div></section>
<section class="sub" id="download"><div class="w"><p>Приложение-справочник mesoestetic® для косметологов и&nbsp;врачей: {NP}&nbsp;препаратов, {len(L)}&nbsp;линий, протоколы и&nbsp;диагностика — всегда под рукой, даже без интернета.</p>{DL}</div></section>
<div class="w rows">
<div class="row rv"><b>01</b><h3>Препараты и составы</h3><p>Эффекты, активы, идеальный клиент, INCI со&nbsp;ссылками на&nbsp;глоссарий. Умный поиск по&nbsp;задаче кожи.</p></div>
<div class="row rv"><b>02</b><h3>Протоколы</h3><p>{NPR} комбинированных протоколов: кабинет по&nbsp;фазам со&nbsp;временем шагов и&nbsp;домашний уход.</p></div>
<div class="row rv"><b>03</b><h3>Диагностика age element®</h3><p>Персональная формула бустеров и&nbsp;схема домашнего ухода — красивой карточкой для&nbsp;клиента.<br><a class="more" href="/diagnostika/">Пройти диагностику →</a></p></div>
<div class="row rv"><b>04</b><h3>Академия</h3><p>Тесты-ситуации из&nbsp;практики, медали и&nbsp;сертификат специалиста.</p></div></div>
<section class="end"><div class="w rv">{ME('#fff')}<h2>для экспертов<br>в&nbsp;уходе за&nbsp;кожей</h2>{DL}
<p class="note">Доступ по&nbsp;коду — запросите у&nbsp;куратора:<br><a href="mailto:s.gru-pro@yandex.ru">s.gru-pro@yandex.ru</a> · Telegram <a href="https://t.me/gru_s">@gru_s</a></p></div></section>
<footer><div class="w"><span>ООО «Бьюти Альянс» — эксклюзивный дистрибьютор mesoestetic® в&nbsp;России<br>Москва, Огородный проезд, 16/1, стр.&nbsp;4, офис 1212 · +7 (495) 960-14-36</span><span><a href="/brand/">О бренде</a> · <a href="/diagnostika/">Диагностика</a></span></div></footer>
<div class="modal" id="ios" role="dialog" aria-modal="true" aria-label="Установка на iPhone"><div class="sheet"><button class="x" aria-label="Закрыть">×</button>
<h3>Установка на iPhone</h3><p class="s">Справочник ставится на экран «Домой» как приложение — без App Store.</p>
<ol><li><span>Откройте <b>app.i-love-me.ru</b> в&nbsp;Safari</span></li><li><span>Нажмите «Поделиться» <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 15V3m0 0L8 7m4-4l4 4M5 11v9h14v-9"/></svg> внизу экрана</span></li><li><span>Выберите «На экран „Домой“» и&nbsp;нажмите «Добавить»</span></li></ol>
<a class="go" href="{WEB}">Открыть справочник в&nbsp;Safari</a></div></div>
<script>
(function(){{
  var ua = navigator.userAgent, ios = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  if (ios) document.querySelectorAll('.dl').forEach(function(d){{ d.classList.add('ios'); }});
  var m = document.getElementById('ios');
  function open(e){{ e.preventDefault(); m.classList.add('on'); }}
  function close(){{ m.classList.remove('on'); if (location.hash === '#ios') history.replaceState(null, '', location.pathname); }}
  document.querySelectorAll('a[href="#ios"]').forEach(function(a){{ a.addEventListener('click', open); }});
  m.addEventListener('click', function(e){{ if (e.target === m || e.target.closest('.x')) close(); }});
  if (location.hash === '#ios') m.classList.add('on');
  if ('IntersectionObserver' in window){{ var io = new IntersectionObserver(function(es){{ es.forEach(function(x){{ if (x.isIntersecting){{ x.target.classList.add('in'); io.unobserve(x.target); }} }}); }}, {{threshold: .15}});
    document.querySelectorAll('.rv').forEach(function(x){{ io.observe(x); }}); }} else document.querySelectorAll('.rv').forEach(function(x){{ x.classList.add('in'); }});
}})();
</script></body></html>'''
(ROOT / 'index.html').write_text(html_out, encoding='utf-8')
print('index.html', len(html_out), 'байт ·', NP, 'препаратов ·', len(L), 'линий')
