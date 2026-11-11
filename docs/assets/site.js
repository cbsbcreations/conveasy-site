// Voice demo: the Vapi PUBLIC key "conveasy.be website". In Vapi it only works on conveasy.be, www.conveasy.be and the test address
// (cbsbcreations.github.io) and only with the assistant TEST Conveasy. A new address has to be added to the key in Vapi (API Keys).
var VAPI_PUBLIC_KEY = '9fbb5145-6656-435c-910f-0977d6ca78c5';
var VAPI_SDK_URL = 'https://cdn.jsdelivr.net/npm/@vapi-ai/web@3.0.1/+esm';
// WhatsApp chat demo: the n8n workflow "Conveasy — Website chat demo (WhatsApp)". It gets POST {message, history, lang}
// and answers {reply, buttons}, {limit: true} or {error}. No key is needed here; the workflow only answers conveasy.be.
var CHAT_DEMO_ENDPOINT = 'https://balloz.app.n8n.cloud/webhook/conveasy-site-wa-demo';

(function () {
  var root = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // The preview build (orange bar on top) runs inside Claude's preview, where a page cannot use the microphone or reach Vapi and n8n
  var isPreview = !!document.querySelector('.preview-bar');

  // Close open menus when clicking elsewhere
  document.addEventListener('click', function (e) {
    document.querySelectorAll('details.dd[open], details.mobile-menu[open]').forEach(function (d) { if (!d.contains(e.target)) d.removeAttribute('open'); });
  });

  // Copy WhatsApp number
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-copy');
      var done = function () { var old = btn.textContent; btn.textContent = btn.getAttribute('data-done') || 'OK'; setTimeout(function () { btn.textContent = old; }, 1800); };
      try { navigator.clipboard.writeText(text).then(done, function () { selectNum(); }); } catch (err) { selectNum(); }
    });
  });
  function selectNum() {
    var el = document.querySelector('.wa-number'); if (!el) return;
    var r = document.createRange(); r.selectNodeContents(el); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
  }

  // Demo form: opens the email app with the request to conveasyai@gmail.com
  var form = document.querySelector('form.lead-form');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    var lines = [];
    form.querySelectorAll('.field').forEach(function (f) {
      var lab = f.querySelector('label'), inp = f.querySelector('input, textarea');
      if (lab && inp && inp.value.trim()) lines.push(lab.textContent.trim() + ': ' + inp.value.trim());
    });
    var picked = [];
    form.querySelectorAll('input[name=interest]:checked').forEach(function (c) { picked.push(c.parentNode.textContent.trim()); });
    var leg = form.querySelector('legend');
    if (picked.length && leg) lines.push(leg.textContent.trim() + ' ' + picked.join(', '));
    var rest = form.querySelector('[name=restaurant]');
    var subject = (form.getAttribute('data-subject') || 'Demo') + (rest && rest.value.trim() ? ' - ' + rest.value.trim() : '');
    var url = 'mailto:' + form.getAttribute('data-to') + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
    var msg = form.querySelector('.form-msg'); if (msg) msg.hidden = false;
    window.location.href = url;
  });

  // Header state
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 24); };
    onScroll(); window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Button labels roll up on hover
  document.querySelectorAll('a.btn').forEach(function (btn) {
    for (var i = 0; i < btn.childNodes.length; i++) {
      var n = btn.childNodes[i];
      if (n.nodeType === 3 && n.textContent.trim()) {
        var t = n.textContent.trim();
        var wrap = document.createElement('span'); wrap.className = 'roll';
        var inner = document.createElement('span'); inner.className = 'roll-in'; inner.setAttribute('data-t', t); inner.textContent = t;
        wrap.appendChild(inner); btn.replaceChild(wrap, n);
        break;
      }
    }
  });

  // Star field behind the page
  (function stars() {
    var c = document.createElement('canvas');
    c.className = 'stars'; c.setAttribute('aria-hidden', 'true');
    document.body.insertBefore(c, document.body.firstChild);
    var ctx = c.getContext && c.getContext('2d'); if (!ctx) return;
    var W = 0, H = 0, list = [], running = false, t0 = performance.now();
    function make() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = window.innerWidth; H = window.innerHeight;
      c.width = W * dpr; c.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(W * H / 5200); list = [];
      for (var i = 0; i < n; i++) {
        var depth = Math.random();
        list.push({ x: Math.random() * W, y: Math.random() * H * 1.6, r: 0.35 + depth * 0.95, a: 0.25 + Math.random() * 0.6, s: 0.6 + Math.random() * 1.8, p: Math.random() * 6.28, d: 0.05 + depth * 0.3, v: 0.004 + depth * 0.012 });
      }
    }
    function draw(now) {
      var time = (now - t0) / 1000, sy = window.scrollY || 0, span = H * 1.6;
      ctx.clearRect(0, 0, W, H);
      for (var i = 0; i < list.length; i++) {
        var s = list[i];
        var y = (s.y - sy * s.d - (reduce ? 0 : time * s.v * 60)) % span; if (y < 0) y += span;
        if (y > H) continue;
        var tw = reduce ? 1 : 0.55 + 0.45 * Math.sin(time * s.s + s.p);
        ctx.globalAlpha = s.a * tw;
        ctx.fillStyle = s.r > 1.05 ? '#FFE3C4' : '#FFFFFF';
        ctx.beginPath(); ctx.arc(s.x, y, s.r, 0, 6.2832); ctx.fill();
      }
      ctx.globalAlpha = 1;
    }
    function loop(now) { if (!running) return; draw(now); requestAnimationFrame(loop); }
    function start() { if (reduce || running) return; running = true; requestAnimationFrame(loop); }
    make(); draw(performance.now()); start();
    window.addEventListener('resize', function () { make(); draw(performance.now()); });
    if (reduce) window.addEventListener('scroll', function () { draw(performance.now()); }, { passive: true });
    document.addEventListener('visibilitychange', function () { if (document.hidden) running = false; else start(); });
  })();

  // Headlines: words blur in one by one
  function splitWords(el) {
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null), nodes = [], n, idx = 0;
    while ((n = walker.nextNode())) nodes.push(n);
    nodes.forEach(function (node) {
      var parts = node.textContent.split(/(\s+)/), frag = document.createDocumentFragment();
      parts.forEach(function (p) {
        if (!p) return;
        if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
        var s = document.createElement('span'); s.className = 'w'; s.style.setProperty('--i', idx++); s.textContent = p; frag.appendChild(s);
      });
      node.parentNode.replaceChild(frag, node);
    });
    el.classList.add('split-ready');
  }
  if (!reduce && 'IntersectionObserver' in window) {
    var heads = document.querySelectorAll('.hero h1, .section-head h2, .cta h2');
    var ho = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); ho.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -6% 0px' });
    heads.forEach(function (h) { splitWords(h); ho.observe(h); });
  }

  // Reveal on scroll
  var sel = '.section-head > p, .section-head > .eyebrow, .card, .feature, .shot, .price, .faq details, .steps li, .cta p, .cta .btn-row, .stats';
  var items = Array.prototype.slice.call(document.querySelectorAll(sel));
  items.forEach(function (el) { el.classList.add('rv'); });
  var native = window.CSS && CSS.supports && CSS.supports('animation-timeline: view()');
  if (!reduce && !native && 'IntersectionObserver' in window) {
    root.classList.add('rv-js');
    var vh = window.innerHeight || 800;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.remove('below'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) {
      if (el.getBoundingClientRect().top > vh * 0.92) {
        var sibs = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
        el.style.setProperty('--d', Math.min(sibs, 5) * 0.07 + 's');
        el.classList.add('below');
        io.observe(el);
      }
    });
  }

  // Order flow: the sticky screen follows the step in view
  var stage = document.querySelector('.flow-stage');
  if (stage && 'IntersectionObserver' in window) {
    var steps = document.querySelectorAll('.flow-steps li');
    var fo = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        stage.setAttribute('data-step', en.target.getAttribute('data-s'));
        steps.forEach(function (li) { li.classList.toggle('on', li === en.target); });
      });
    }, { rootMargin: '-45% 0px -45% 0px' });
    steps.forEach(function (li) { fo.observe(li); });
  }

  // Voice demo ("Probeer onze AI"), Vapi Web SDK loaded on first click
  (function voiceDemo() {
    var btns = document.querySelectorAll('[data-vapi]'); if (!btns.length) return;
    var vapi = null, sdk = null, active = null, timer = null, state = 'idle';
    var MAX_SECONDS = 180;
    var failKey = isPreview ? 'preview' : 'error';
    function box(b) { return b.closest('.demo'); }
    function say(b, key) { var el = box(b) && box(b).querySelector('.demo-state'); if (el) el.textContent = key ? (b.getAttribute('data-m-' + key) || '') : ''; }
    function setState(b, s) {
      state = s; b.setAttribute('data-state', s);
      var lab = b.querySelector('.demo-label');
      if (lab) lab.textContent = b.getAttribute(s === 'idle' ? 'data-l-start' : s === 'live' ? 'data-l-stop' : 'data-l-wait');
      var d = box(b); if (d) { d.classList.toggle('is-live', s === 'live'); d.classList.toggle('is-connecting', s === 'connecting'); }
      b.setAttribute('aria-pressed', s === 'idle' ? 'false' : 'true');
    }
    function orb(v) { if (!active) return; var o = box(active) && box(active).querySelector('.demo-orb'); if (o) o.style.setProperty('--v', reduce ? 0 : Math.min(1, v || 0)); }
    function end(msg) {
      clearTimeout(timer); timer = null;
      if (active) { setState(active, 'idle'); say(active, msg); orb(0); }
      active = null;
    }
    function load() {
      if (!sdk) sdk = import(VAPI_SDK_URL).then(function (m) {
        var V = m && m.default ? m.default : m; if (V && V.default) V = V.default;
        vapi = new V(VAPI_PUBLIC_KEY);
        vapi.on('call-start', function () { if (!active) return; setState(active, 'live'); say(active, 'live'); timer = setTimeout(function () { try { vapi.stop(); } catch (e) {} }, MAX_SECONDS * 1000); });
        vapi.on('call-end', function () { end('ended'); });
        vapi.on('error', function () { try { vapi.stop(); } catch (e) {} end(failKey); });
        vapi.on('volume-level', orb);
        return vapi;
      });
      return sdk;
    }
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        if (state !== 'idle') { if (active === b) { try { vapi && vapi.stop(); } catch (e) {} end('ended'); } return; }
        if (!VAPI_PUBLIC_KEY || VAPI_PUBLIC_KEY === 'VAPI_PUBLIC_KEY') { say(b, 'notset'); return; }
        active = b; setState(b, 'connecting'); say(b, '');
        load().then(function (v) { return v.start(b.getAttribute('data-vapi'), { maxDurationSeconds: MAX_SECONDS }); })
          .then(function (call) { if (!call && state === 'connecting') end(failKey); })
          .catch(function () { sdk = null; end(failKey); });
      });
    });
  })();

  // WhatsApp-style ordering chat demo. The page keeps the conversation and sends it along with every message; nothing is stored on a server.
  (function waDemo() {
    var boxes = document.querySelectorAll('[data-wa-demo]'); if (!boxes.length) return;
    var ready = CHAT_DEMO_ENDPOINT && CHAT_DEMO_ENDPOINT !== 'CHAT_DEMO_ENDPOINT';
    var MAX_TURNS = 20, TIMEOUT_MS = 30000;
    function now() { var d = new Date(); return ('0' + d.getHours()).slice(-2) + ':' + ('0' + d.getMinutes()).slice(-2); }
    boxes.forEach(function (box) {
      var log = box.querySelector('.wa-log'), form = box.querySelector('.wa-input'), input = form.querySelector('input'), chips = box.querySelector('.wa-chips');
      var history = [], busy = false, turns = 0;
      box.querySelectorAll('.wa-msg time').forEach(function (t) { t.textContent = now(); });
      function add(text, cls) {
        var m = document.createElement('div'); m.className = 'wa-msg ' + cls;
        var p = document.createElement('p'); p.textContent = text; m.appendChild(p);
        var t = document.createElement('time'); t.textContent = now(); m.appendChild(t);
        log.appendChild(m); log.scrollTop = log.scrollHeight; return m;
      }
      function typing() {
        var m = document.createElement('div'); m.className = 'wa-msg in wa-typing';
        m.setAttribute('aria-label', box.getAttribute('data-m-typing') || '');
        m.innerHTML = '<span></span><span></span><span></span>';
        log.appendChild(m); log.scrollTop = log.scrollHeight; return m;
      }
      // Reply buttons under the conversation, like WhatsApp's: the suggestions at the start, later the ones the assistant offers
      function quick(list) {
        if (!chips) return;
        chips.textContent = '';
        (Array.isArray(list) ? list : []).slice(0, 3).forEach(function (label) {
          var c = document.createElement('button'); c.type = 'button'; c.className = 'wa-chip'; c.textContent = String(label); chips.appendChild(c);
        });
        chips.hidden = !chips.children.length;
        log.scrollTop = log.scrollHeight;
      }
      function done() { busy = false; form.classList.remove('is-busy'); }
      function send(text) {
        text = (text || '').trim(); if (!text || busy) return;
        add(text, 'out'); input.value = ''; quick([]);
        busy = true; form.classList.add('is-busy');
        var ty = typing();
        if (!ready) { setTimeout(function () { ty.remove(); add(box.getAttribute('data-m-notset'), 'in sys'); done(); }, 700); return; }
        if (turns >= MAX_TURNS) { setTimeout(function () { ty.remove(); add(box.getAttribute('data-m-limit'), 'in sys'); done(); }, 500); return; }
        turns++;
        var ctl = window.AbortController ? new AbortController() : null;
        var timer = setTimeout(function () { if (ctl) ctl.abort(); }, TIMEOUT_MS);
        fetch(CHAT_DEMO_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, signal: ctl ? ctl.signal : undefined,
          body: JSON.stringify({ message: text, history: history, lang: box.getAttribute('data-lang') }) })
          .then(function (r) { if (!r.ok) throw new Error('http'); return r.json(); })
          .then(function (d) {
            if (d && d.limit) { ty.remove(); turns = MAX_TURNS; add(box.getAttribute('data-m-limit'), 'in sys'); return; }
            var reply = d && typeof d.reply === 'string' ? d.reply.trim() : '';
            if (!reply) throw new Error('empty');
            history.push({ role: 'user', content: text }, { role: 'assistant', content: reply });
            ty.remove(); add(reply, 'in'); quick(d.buttons);
          })
          .catch(function () { ty.remove(); add(box.getAttribute(isPreview ? 'data-m-preview' : 'data-m-error') || box.getAttribute('data-m-error'), 'in sys'); })
          .then(function () { clearTimeout(timer); done(); });
      }
      form.addEventListener('submit', function (e) { e.preventDefault(); send(input.value); });
      if (chips) chips.addEventListener('click', function (e) { var c = e.target.closest ? e.target.closest('.wa-chip') : null; if (c) send(c.textContent); });
    });
  })();

  // Soft light that follows the pointer on cards
  if (!reduce && window.matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('.card, .price').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        el.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }
})();
