/* Диагностика age element® — i-love-me.ru/diagnostika (вариант Д1 «Стенд»).
   Логика та же, что в справочнике: баллы по ответам → порядок 4 бустеров → таблица из 52 комбинаций. */
(function(){
'use strict';
var DG = window.DGDATA, DIAG = DG.diag, PROD = DG.prod;
var STEPS = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17];
var KEYS = ['firming', 'antiwrinkle', 'redensifying', 'brightening'];
var COL = {brightening: '#d4b483', firming: '#9aa3a6', antiwrinkle: '#c98f8c', redensifying: '#b9a36a'};
var RU = {brightening: 'тон и сияние', firming: 'упругость', antiwrinkle: 'морщины', redensifying: 'плотность и контур'};
var BCODE = {brightening: 'T-PAGE0010', firming: 'T-PAGE0012', antiwrinkle: 'T-PAGE0011', redensifying: 'T-PAGE0013'};
var MASK = {'crystal fiber': 'T-PAGE0014', 'firming mask': 'T-PAGE0015'};
var HOME = {brightening: {cream: 'T-DABS0002', eye: 'T-DABS0003', serum: 'T-DABS0004'}, firming: {cream: 'T-DAFS0003', eye: 'T-DAFS0004', serum: 'T-DAFS0005'},
  antiwrinkle: {cream: 'T-DAWS0003', eye: 'T-DAWS0004', serum: 'T-DAWS0005'}, redensifying: {cream: 'T-DAWS0007', eye: 'T-DAWS0004', serum: 'T-DMOI0001'}};
var app = document.getElementById('app');
var st = load() || {screen: 'intro', i: 0, a: {}, rank: {}, order: [], tab: 0};

function load(){ try { return JSON.parse(sessionStorage.getItem('dg')); } catch (e) { return null; } }
function save(){ try { sessionStorage.setItem('dg', JSON.stringify(st)); } catch (e) {} }
function esc(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){ return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); }
// висячие предлоги и союзы — неразрывный пробел после коротких слов
function nb(s){ return esc(s).replace(/(^|[\s(«])([а-яёА-ЯЁa-zA-Z]{1,2}) /g, '$1$2 '); }
function ml(v){ return String(v).replace('.', ',') + ' мл'; }
function short(k){ return DIAG.boosterShort[k]; }

/* шприц: колпачок, корпус с делениями, жидкость цвета бустера (уровень 0…1), поршень */
var sid = 0;
function syringe(col, lvl, i, w, anim){
  var g = 'sg' + (++sid), ticks = '';
  for (var k = 0; k < 11; k++) ticks += '<line x1="14" x2="' + (k % 2 ? 19 : 22) + '" y1="' + (60 + k * 14) + '" y2="' + (60 + k * 14) + '" stroke="rgba(255,255,255,.55)" stroke-width="1"/>';
  return '<svg class="syr' + (anim ? ' fill' : '') + '" viewBox="0 0 60 260" style="width:' + w + 'px;--lv:' + Math.max(0, Math.min(1, lvl)).toFixed(3) + ';--i:' + i + '" aria-hidden="true"><defs>'
    + '<linearGradient id="' + g + '" x1="0" x2="1"><stop offset="0" stop-color="' + col + '" stop-opacity=".55"/><stop offset=".45" stop-color="' + col + '"/><stop offset="1" stop-color="' + col + '" stop-opacity=".6"/></linearGradient>'
    + '<linearGradient id="' + g + 'b" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".25" stop-color="#fff" stop-opacity=".05"/><stop offset=".8" stop-color="#fff" stop-opacity=".02"/><stop offset="1" stop-color="#fff" stop-opacity=".25"/></linearGradient></defs>'
    + '<rect x="24" y="2" width="12" height="26" rx="3" fill="rgba(255,255,255,.75)"/><rect x="20" y="26" width="20" height="16" rx="3" fill="rgba(255,255,255,.55)"/>'
    + '<g class="liq"><rect x="13" y="44" width="34" height="168" fill="url(#' + g + ')"/></g>'
    + '<rect x="12" y="42" width="36" height="172" rx="6" fill="url(#' + g + 'b)" stroke="rgba(255,255,255,.55)" stroke-width="1.5"/>' + ticks
    + '<rect x="6" y="212" width="48" height="8" rx="2" fill="rgba(255,255,255,.7)"/><rect x="25" y="220" width="10" height="30" fill="rgba(255,255,255,.5)"/><rect x="14" y="248" width="32" height="8" rx="3" fill="rgba(255,255,255,.75)"/></svg>';
}

function totals(){
  var t = {brightening: 0, firming: 0, antiwrinkle: 0, redensifying: 0};
  STEPS.forEach(function(q){ if (q === 4) return; var a = st.a[q]; if (!a) return;
    ((DIAG.points[q] && DIAG.points[q][a]) || []).forEach(function(e){ if (typeof e.points === 'number') t[e.booster] += e.points; }); });
  Object.keys(st.rank).forEach(function(b){ var r = st.rank[b]; t[b] += r === 1 ? 2 : r === 2 ? 1 : 0; });
  return t;
}
function result(){
  var t = totals(), order = Object.keys(t).sort(function(a, b){ return t[b] - t[a] || ((st.rank[a] || 9) - (st.rank[b] || 9)); });
  var vals = order.map(function(b){ return t[b]; }), pattern = [1];
  for (var i = 1; i < 4; i++) pattern.push(vals[i] === vals[i - 1] ? pattern[i - 1] : pattern[i - 1] + 1);
  var J = JSON.stringify, approx = false;
  var combo = DIAG.combos.filter(function(c){ return J(c.pattern) === J(pattern) && J(c.order) === J(order); })[0];
  if (!combo){ combo = DIAG.combos.filter(function(c){ return J(c.pattern) === J([1, 2, 3, 4]) && J(c.order) === J(order); })[0]; approx = true; }
  return {t: t, order: order, combo: combo, approx: approx, hs: homeScheme(order)};
}
/* домашний уход: утро — главный приоритет, вечер — второй (подсерии смешиваются) — как в справочнике */
function homeScheme(order){
  var p1 = order[0], p2 = order[1], has = function(k){ return p1 === k || p2 === k; };
  var day = function(k){ return k === 'redensifying' ? 'T-DAFS0003' : HOME[k].cream; };
  var night = has('antiwrinkle') || has('redensifying') ? 'T-DAWS0007' : HOME[p2].cream;
  var clean = has('brightening') ? 'T-DHIG0005' : 'T-DHIG0004', spf = has('brightening') ? 'T-DSUN0034' : 'T-DSUN0030';
  var eyeAM = HOME[p1].eye, eyePM = HOME[p2].eye;
  var morning = [{c: clean, how: 'Умыться: небольшое количество на влажную кожу, смыть водой.'}, {c: 'T-DHIG0009', how: 'Освежить кожу тоником-мистом.'},
    {c: HOME[p1].serum, how: '2–3 капли на лицо, шею и декольте до впитывания.'}, {c: eyeAM, how: 'На кожу вокруг глаз лёгкими похлопываниями.'},
    {c: day(p1), how: 'Крем на лицо, шею и декольте.'}, {c: spf, how: 'Последним шагом, каждый день — даже в пасмурную погоду.'}];
  var evening = [{c: clean, how: 'Снять макияж и умыться.'}, {c: HOME[p2].serum, how: '2–3 капли до впитывания.'},
    eyePM !== eyeAM ? {c: eyePM, how: 'Второе средство для век — чтобы работать с обеими задачами.'} : {c: eyeAM, how: 'Вокруг глаз, как утром.'},
    {c: night, how: 'Ночной уход на лицо, шею и декольте.'}];
  var extra = [];
  if (has('antiwrinkle')) extra.push({c: 'T-DAWS0006', how: 'Губы и кожа вокруг рта — утром и вечером.'});
  extra.push({c: 'T-DHIG0010', how: '1–2 раза в неделю вечером вместо умывания. Не накануне и не в день процедуры.'});
  var uniq = function(a){ return a.filter(function(x, i){ return PROD[x.c] && a.findIndex(function(y){ return y.c === x.c; }) === i; }); };
  return [{h: 'Утром', steps: uniq(morning)}, {h: 'Вечером', steps: uniq(evening)}, {h: 'Дополнительно', steps: uniq(extra)}];
}

function vIntro(){
  return '<section class="scr"><span class="mono">Лаборатория mesoestetic · анализ кожи</span><h1>Формула,<br>созданная<br>для вашей кожи</h1>'
    + '<div class="rack">' + KEYS.map(function(k, i){ return '<div class="col">' + syringe(COL[k], .85 - i * .12, i, 58, true) + '<span>' + short(k) + '</span></div>'; }).join('') + '</div><div class="shelf"></div>'
    + '<p class="lead">' + nb('17 вопросов — и четыре бустера age element® смешиваются в персональную формулу на курс из 5 процедур. Плюс схема домашнего ухода.') + '</p>'
    + '<div class="meta glass"><div><b>17</b><span>вопросов</span></div><div><b>4</b><span>бустера</span></div><div><b>~3</b><span>минуты</span></div></div>'
    + '<button class="btn" data-go="start">Начать анализ</button><p class="note">' + nb('Часть вопросов оценивает специалист, часть — клиент. Лучше проходить вместе на консультации.') + '</p></section>';
}
function vQuestion(){
  var qid = STEPS[st.i], t = totals(), mx = Math.max(14, Math.max.apply(null, KEYS.map(function(k){ return t[k]; })) + 4), hint, text, body, ok;
  if (qid === 4){
    hint = 'Клиент вместе со специалистом'; text = DIAG.q4.text;
    body = '<p class="small" style="margin-top:6px">' + nb('Нажимайте по порядку: от самой важной (1) до наименее важной (4).') + '</p><div class="opts">'
      + DIAG.q4.items.map(function(it){ return '<button class="opt' + (st.rank[it[0]] ? ' on' : '') + '" data-rank="' + it[0] + '"><span class="l">' + (st.rank[it[0]] || '') + '</span><span>' + nb(it[1]) + '</span></button>'; }).join('')
      + '</div>' + (st.order.length ? '<button class="reset" data-go="reset">Сбросить порядок</button>' : '');
    ok = st.order.length === 4;
  } else {
    var q = DIAG.questions.filter(function(x){ return x.id === qid; })[0];
    hint = q.hint; text = q.text;
    body = '<div class="opts">' + q.options.map(function(o){ return '<button class="opt' + (st.a[qid] === o[0] ? ' on' : '') + '" data-ans="' + qid + ':' + o[0] + '"><span class="l">' + o[0] + '</span><span>' + nb(o[1]) + '</span></button>'; }).join('') + '</div>';
    ok = !!st.a[qid];
  }
  var pro = /специалист|косметолог/i.test(hint) && !/клиент/i.test(hint);
  return '<section class="scr" data-k="' + st.i + '"><div class="qn"><span class="mono">Вопрос ' + String(st.i + 1).padStart(2, '0') + ' / ' + STEPS.length + '</span><span class="who' + (pro ? ' pro' : '') + '">' + esc(hint) + '</span></div>'
    + '<div class="prog">' + STEPS.map(function(_, k){ return '<i class="' + (k <= st.i ? 'on' : '') + '"></i>'; }).join('') + '</div>'
    + '<h2>' + nb(text) + '</h2>' + body
    + '<div class="mini" aria-hidden="true">' + KEYS.map(function(k, i){ return '<div class="col">' + syringe(COL[k], t[k] / mx, i, 30) + '<span>' + short(k) + '</span></div>'; }).join('') + '</div>'
    + '<p class="mono" style="text-align:center">формула наполняется по ответам</p>'
    + '<div class="nav"><button class="ghost" data-go="back"' + (st.i === 0 ? ' disabled style="opacity:.3"' : '') + '>Назад</button><button class="btn" data-go="next"' + (ok ? '' : ' disabled') + '>' + (st.i === STEPS.length - 1 ? 'Получить формулу' : 'Далее') + '</button></div></section>';
}
function phIcon(c){
  var p = PROD[c]; return p && p.ph ? '<div class="pic"><img src="/img/p/sm/' + c + '.webp" alt="" loading="lazy"></div>' : '<div class="pic no">Me</div>';
}
function vResult(){
  var R = result(), t = R.t, mx = Math.max.apply(null, R.order.map(function(k){ return t[k]; }).concat(1)), c = R.combo;
  var h = '<section class="scr"><span class="mono">Результат' + (c ? ' · протокол № ' + c.protocol : '') + '</span><h1 style="font-size:38px">Ваша формула</h1>'
    + '<p class="lead" style="margin:10px 0 0">Главные задачи кожи: ' + R.order.slice(0, 2).map(function(k){ return RU[k]; }).join(' и ') + '.</p>'
    + '<div class="bars" style="margin-top:16px">' + R.order.map(function(k, i){ return '<div class="r"><b>' + (i + 1) + '</b><span>' + short(k) + '</span><span class="t"><i style="width:' + (t[k] / mx * 100).toFixed(0) + '%;background:' + COL[k] + '"></i></span><em>' + t[k] + '</em></div>'; }).join('') + '</div>';
  if (!c) return h + '<p class="note">Не удалось подобрать протокол. Проверьте ответы.</p>' + actions(false) + '</section>';
  if (R.approx) h += '<p class="note">' + nb('Такое сочетание баллов не описано в таблице напрямую — показан ближайший протокол по порядку приоритетов. Специалист может его скорректировать.') + '</p>';
  var S = [c.s135, c.s24], s = S[st.tab] || S[0];
  h += '<h3>Бустеры в процедуре</h3><div class="tabs glass"><button data-tab="0" class="' + (st.tab ? '' : 'on') + '">Процедуры 1 · 3 · 5</button><button data-tab="1" class="' + (st.tab ? 'on' : '') + '">Процедуры 2 · 4</button></div>'
    + '<div class="dose">' + c.order.map(function(k, i){ var v = s.b[i]; return '<div class="' + (v == null ? 'off' : '') + '">' + syringe(COL[k], v == null ? 0 : v / 2, i, 44, true) + '<b>' + (v == null ? '—' : ml(v)) + '</b><small>' + short(k) + '</small></div>'; }).join('') + '</div>'
    + '<div class="mask glass"><span>в основу</span><b>' + esc(PROD['T-PAGE0009'] ? 'hydrabalance cream' : 'основа') + '</b></div>'
    + '<div class="mask glass" style="margin-top:6px"><span>финиш</span><b>age element ' + esc(s.mask.toLowerCase()) + '</b></div>'
    + '<h3>Ход процедуры · 55 минут</h3><ol class="steps">'
    + '<li><span>Очищение<small>age element cleansing balm</small></span><i></i></li>'
    + '<li><span>Обновление кожи<small>age element resurfacing solution</small></span><i>5 мин</i></li>'
    + '<li><span>Массаж с персональной формулой<small>основа + бустеры по схеме</small></span><i>30 мин</i></li>'
    + '<li><span>Маска<small>age element ' + esc(s.mask.toLowerCase()) + '</small></span><i>' + (/firming/i.test(s.mask) ? '15' : '20') + ' мин</i></li>'
    + '<li><span>Защита<small>SPF 50+</small></span><i></i></li></ol>'
    + '<h3>Домашний уход между процедурами</h3><p class="small">' + nb('Утром — ' + short(R.order[0]) + ', вечером — ' + short(R.order[1]) + ': кожа получает оба направления каждый день.') + '</p>'
    + R.hs.map(function(pt){ return '<div class="hp"><h4>' + pt.h + '</h4>' + pt.steps.map(function(x){ var p = PROD[x.c];
        return '<div class="home glass">' + phIcon(x.c) + '<div><b>' + nb(p.ru) + '</b><span>' + nb(x.how) + '</span></div></div>'; }).join('') + '</div>'; }).join('');
  return h + actions(true) + '</section>';
}
function actions(card){
  return '<div class="acts">' + (card ? '<button class="btn" data-go="card">Сохранить карточку для клиента</button>' : '')
    + '<button class="ghost" data-go="edit">Изменить ответы</button><button class="ghost" data-go="restart">Новый клиент</button></div>';
}

function render(scroll){
  sid = 0;
  app.innerHTML = st.screen === 'intro' ? vIntro() : st.screen === 'result' ? vResult() : vQuestion();
  if (scroll) window.scrollTo(0, 0);
  save();
}
app.addEventListener('click', function(e){
  var x = e.target.closest('[data-go],[data-ans],[data-rank],[data-tab]'); if (!x || x.disabled) return;
  if (x.dataset.ans){ var p = x.dataset.ans.split(':'); st.a[p[0]] = p[1];
    // ответ выбран — шприцы перетекают на новые уровни без перерисовки экрана
    app.querySelectorAll('.opt').forEach(function(o){ o.classList.toggle('on', o === x); });
    var t = totals(), mx = Math.max(14, Math.max.apply(null, KEYS.map(function(k){ return t[k]; })) + 4);
    app.querySelectorAll('.mini .syr').forEach(function(s, i){ s.style.setProperty('--lv', (t[KEYS[i]] / mx).toFixed(3)); });
    var nx = app.querySelector('[data-go="next"]'); if (nx) nx.disabled = false; save(); return; }
  if (x.dataset.rank){ var k = x.dataset.rank; if (!st.rank[k]){ st.order.push(k); st.rank[k] = st.order.length; } render(false); return; }
  if (x.dataset.tab){ st.tab = +x.dataset.tab; var y = window.scrollY; render(false); window.scrollTo(0, y); return; }
  var a = x.dataset.go;
  if (a === 'start'){ st.screen = 'question'; st.i = 0; }
  else if (a === 'reset'){ st.rank = {}; st.order = []; render(false); return; }
  else if (a === 'back'){ if (st.i > 0) st.i--; }
  else if (a === 'next'){ if (st.i < STEPS.length - 1) st.i++; else { st.screen = 'result'; st.tab = 0; } }
  else if (a === 'edit'){ st.screen = 'question'; st.i = 0; }
  else if (a === 'restart'){ st = {screen: 'intro', i: 0, a: {}, rank: {}, order: [], tab: 0}; }
  else if (a === 'card'){ shareCard(); return; }
  render(true);
});

/* ── карточка для клиента (PNG 1080 px): формула курса + домашний уход */
function toast(m){ var t = document.getElementById('toast'); t.textContent = m; t.classList.add('on'); clearTimeout(toast.h); toast.h = setTimeout(function(){ t.classList.remove('on'); }, 2600); }
var FONT = function(w, s){ return w + ' ' + s + 'px Inter,"Helvetica Neue",Helvetica,Arial,sans-serif'; };
function wrap(ctx, text, maxW){ var words = String(text).split(' '), lines = [], cur = '';
  words.forEach(function(w){ var tst = cur ? cur + ' ' + w : w; if (ctx.measureText(tst).width > maxW && cur){ lines.push(cur); cur = w; } else cur = tst; });
  if (cur) lines.push(cur); return lines; }
function cardSyr(ctx, x, y, h, col, lvl){
  var w = h * .23; ctx.save();
  ctx.fillStyle = 'rgba(255,255,255,.75)'; ctx.fillRect(x + w * .38, y, w * .24, h * .1); ctx.fillStyle = 'rgba(255,255,255,.5)'; ctx.fillRect(x + w * .3, y + h * .1, w * .4, h * .06);
  var by = y + h * .16, bh = h * .66; ctx.fillStyle = 'rgba(255,255,255,.08)'; ctx.fillRect(x, by, w, bh);
  var lh = bh * Math.max(0, Math.min(1, lvl)); ctx.fillStyle = col; ctx.fillRect(x + 2, by + bh - lh, w - 4, lh);
  ctx.strokeStyle = 'rgba(255,255,255,.6)'; ctx.lineWidth = 2; ctx.strokeRect(x, by, w, bh);
  ctx.fillStyle = 'rgba(255,255,255,.7)'; ctx.fillRect(x - w * .15, by + bh, w * 1.3, h * .03); ctx.fillRect(x + w * .4, by + bh + h * .03, w * .2, h * .1); ctx.fillRect(x + w * .1, y + h * .95, w * .8, h * .05);
  ctx.restore();
}
function buildCard(){
  var R = result(); if (!R.combo) return null;
  var W = 1080, P = 72, c = document.createElement('canvas'), ctx; c.width = W; c.height = 2600; ctx = c.getContext('2d'); ctx.textBaseline = 'top';
  var draw = function(H){
    ctx.fillStyle = '#060606'; ctx.fillRect(0, 0, W, H);
    var g = ctx.createRadialGradient(W * .7, 360, 40, W * .7, 360, 620); g.addColorStop(0, 'rgba(201,143,140,.45)'); g.addColorStop(1, 'rgba(201,143,140,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    var g2 = ctx.createRadialGradient(W * .15, H * .55, 40, W * .15, H * .55, 600); g2.addColorStop(0, 'rgba(154,163,166,.28)'); g2.addColorStop(1, 'rgba(154,163,166,0)'); ctx.fillStyle = g2; ctx.fillRect(0, 0, W, H);
    var y = P; ctx.strokeStyle = '#fff'; ctx.lineWidth = 7; ctx.strokeRect(P + 3, y + 3, 88, 88); ctx.fillStyle = '#fff'; ctx.font = FONT(700, 42); ctx.fillText('Ae', P + 14, y + 36);
    ctx.font = FONT(600, 26); ctx.fillStyle = '#9a9a9a'; ctx.fillText('ВАШ КУРС AGE ELEMENT®' + ' · ПРОТОКОЛ № ' + R.combo.protocol, P + 124, y + 8);
    ctx.font = FONT(700, 58); ctx.fillStyle = '#fff'; ctx.fillText('Персональная формула', P + 124, y + 42); y += 150;
    ctx.font = FONT(400, 32); ctx.fillStyle = '#cfcfcf'; wrap(ctx, 'Главные задачи кожи: ' + R.order.slice(0, 2).map(function(k){ return RU[k]; }).join(' и ') + '.', W - 2 * P).forEach(function(l){ ctx.fillText(l, P, y); y += 44; }); y += 26;
    [['Процедуры 1 · 3 · 5', R.combo.s135], ['Процедуры 2 · 4', R.combo.s24]].forEach(function(sc){
      ctx.font = FONT(700, 34); ctx.fillStyle = '#fff'; ctx.fillText(sc[0], P, y); ctx.font = FONT(400, 26); ctx.fillStyle = '#9a9a9a'; ctx.textAlign = 'right'; ctx.fillText('маска: ' + sc[1].mask.toLowerCase(), W - P, y + 6); ctx.textAlign = 'left'; y += 60;
      var cw = (W - 2 * P) / 4;
      R.combo.order.forEach(function(k, i){ var v = sc[1].b[i], x = P + i * cw + cw / 2 - 26;
        cardSyr(ctx, x, y, 230, v == null ? 'rgba(255,255,255,.1)' : COL[k], v == null ? 0 : v / 2);
        ctx.textAlign = 'center'; ctx.font = FONT(700, 34); ctx.fillStyle = v == null ? '#555' : '#fff'; ctx.fillText(v == null ? '—' : ml(v), P + i * cw + cw / 2, y + 248);
        ctx.font = FONT(400, 24); ctx.fillStyle = '#9a9a9a'; ctx.fillText(short(k), P + i * cw + cw / 2, y + 292); ctx.textAlign = 'left'; });
      y += 350; });
    ctx.fillStyle = 'rgba(255,255,255,.2)'; ctx.fillRect(P, y, W - 2 * P, 2); y += 40;
    ctx.font = FONT(700, 40); ctx.fillStyle = '#fff'; ctx.fillText('Ваш уход дома', P, y); y += 66;
    R.hs.forEach(function(pt){ ctx.font = FONT(700, 26); ctx.fillStyle = '#9a9a9a'; ctx.fillText(pt.h.toUpperCase(), P, y); y += 42;
      pt.steps.forEach(function(x, i){ var p = PROD[x.c]; ctx.font = FONT(700, 30); ctx.fillStyle = '#fff'; ctx.fillText((i + 1) + '.', P, y);
        wrap(ctx, p.ru, W - 2 * P - 50).forEach(function(l){ ctx.fillText(l, P + 50, y); y += 38; });
        ctx.font = FONT(400, 25); ctx.fillStyle = '#a9a9a9'; wrap(ctx, x.how, W - 2 * P - 50).forEach(function(l){ ctx.fillText(l, P + 50, y); y += 33; }); y += 14; }); y += 16; });
    y += 20; ctx.font = FONT(400, 24); ctx.fillStyle = '#777'; ctx.fillText('mesoestetic® · формула подобрана специалистом по результатам диагностики', P, y); y += 34; ctx.fillText('i-love-me.ru/diagnostika', P, y);
    return y + P;
  };
  var H = draw(2600); c.height = Math.ceil(H); ctx = c.getContext('2d'); ctx.textBaseline = 'top'; draw(c.height);
  return c;
}
function shareCard(){
  var c = buildCard(); if (!c) return;
  c.toBlob(function(b){
    var f = new File([b], 'формула-age-element.png', {type: 'image/png'});
    if (navigator.canShare && navigator.canShare({files: [f]})){ navigator.share({files: [f], title: 'Формула age element®'}).catch(function(){}); return; }
    var a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = f.name; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function(){ URL.revokeObjectURL(a.href); }, 4000); toast('Карточка сохранена');
  }, 'image/png');
}
window.__dgCard = buildCard;   // для проверки вёрстки карточки
render(false);
})();
