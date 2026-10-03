  (function () {
    var S = {
      pr: [
        ['p', '$ '], ['c', 'python evaluation/run_reviews.py'], ['n'],
        ['p', '$ '], ['c', 'python evaluation/judge_results.py'], ['n'],
        ['d', '  15 golden fixtures · model openai/gpt-oss-120b'], ['n'], ['n'],
        ['o', '  category      recall      precision   F2'], ['n'],
        ['o', '  security      '], ['g', '5/5 100%'], ['o', '    1.000       1.000'], ['n'],
        ['o', '  performance   '], ['g', '5/5 100%'], ['o', '    1.000       1.000'], ['n'],
        ['o', '  structural    4/5  80%    1.000       0.833'], ['n'],
        ['o', '  overall       '], ['g', '14/15 93.3%'], ['o', ' 1.000       0.946'], ['n'], ['n'],
        ['g', '  0 false positives']
      ],
      cq: [
        ['p', '$ '], ['c', 'cd Evaluation'], ['n'],
        ['p', '$ '], ['c', 'python evaluate_rag_offline.py'], ['n'],
        ['d', '  68 CUAD questions · generator gemini-2.5-flash · separate judge'], ['n'], ['n'],
        ['o', '  faithfulness        '], ['g', '0.89'], ['d', '   (was 0.68)'], ['n'],
        ['o', '  answer relevancy    0.69'], ['n'],
        ['o', '  context precision   0.66'], ['n'],
        ['o', '  context recall      '], ['g', '0.83'], ['d', '   (was 0.69)'], ['n'], ['n'],
        ['o', '  out-of-scope        '], ['g', '6/6 refused'], ['o', ', zero LLM calls']
      ],
      rf: [
        ['p', '$ '], ['c', 'uv run python scripts/ask_depgraph.py \\'], ['n'],
        ['c', '    "How do I fix CVE-2024-45296 in express@4.17.1?"'], ['n'], ['n'],
        ['o', '  my-api'], ['n'],
        ['o', '  └─ express@4.17.1'], ['n'],
        ['o', '     └─ path-to-regexp@0.1.7  '], ['r', 'CVE-2024-45296'], ['n'], ['n'],
        ['o', '  fix: upgrade express to '], ['g', '4.22.0'], ['n'],
        ['o', '       or add an npm override'], ['n'], ['n'],
        ['d', '  sources: [G1] dependency chain  [A1] osv.dev advisory']
      ]
    };
    var screen = document.getElementById('screen');
    if (!screen) return;
    var tabs = document.querySelectorAll('.tab');
    var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    var run = 0;

    function span(cls, text) {
      var s = document.createElement('span');
      if (cls && cls !== 'o' && cls !== 'c') s.className = cls;
      s.textContent = text; return s;
    }
    function renderAll(parts) {
      screen.textContent = '';
      parts.forEach(function (p) { screen.appendChild(p[0] === 'n' ? document.createTextNode('\n') : span(p[0], p[1])); });
      var c = document.createElement('span'); c.className = 'caret'; screen.appendChild(c);
    }
    function animate(parts) {
      var id = ++run; screen.textContent = '';
      var caret = document.createElement('span'); caret.className = 'caret';
      var i = 0;
      function next() {
        if (id !== run) return;
        if (i >= parts.length) { screen.appendChild(caret); return; }
        var p = parts[i++];
        if (p[0] === 'n') { screen.appendChild(document.createTextNode('\n')); return setTimeout(next, 40); }
        if (p[0] === 'c') {
          var s = span('c', ''), k = 0; screen.appendChild(s); screen.appendChild(caret);
          (function type() {
            if (id !== run) return;
            if (k < p[1].length) { s.textContent += p[1][k++]; return setTimeout(type, 22); }
            caret.remove(); setTimeout(next, 180);
          })();
          return;
        }
        screen.appendChild(span(p[0], p[1])); setTimeout(next, 30);
      }
      next();
    }
    function show(k, anim) {
      tabs.forEach(function (t) { t.setAttribute('aria-selected', t.dataset.k === k ? 'true' : 'false'); });
      if (anim && !reduce) animate(S[k]); else { run++; renderAll(S[k]); }
    }
    tabs.forEach(function (t) {
      t.addEventListener('click', function () { show(t.dataset.k, true); });
      t.addEventListener('keydown', function (e) {
        var list = Array.prototype.slice.call(tabs), i = list.indexOf(t);
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
          var n = list[(i + (e.key === 'ArrowRight' ? 1 : list.length - 1)) % list.length];
          n.focus(); show(n.dataset.k, true);
        }
      });
    });
    show('pr', false);
  })();

  var copyBtn = document.getElementById('copy-email');
  if (copyBtn) copyBtn.addEventListener('click', function () {
    var btn = this, el = document.getElementById('email');
    var done = function () { btn.textContent = 'Copied'; setTimeout(function () { btn.textContent = 'Copy'; }, 1600); };
    var fallback = function () {
      var r = document.createRange(); r.selectNodeContents(el);
      var s = getSelection(); s.removeAllRanges(); s.addRange(r); btn.textContent = 'Selected';
    };
    try { navigator.clipboard.writeText(el.textContent).then(done, fallback); } catch (e) { fallback(); }
  });

  // Demo videos: small inline mini-player with a full-screen option.
  document.querySelectorAll('.mini').forEach(function (card) {
    var v = card.querySelector('video'), play = card.querySelector('.mini-play'), fs = card.querySelector('.mini-fs');
    if (!v) return;
    var start = function () { var p = v.play(); if (p && p.catch) p.catch(function () {}); };
    v.controls = false; play.hidden = false;
    play.addEventListener('click', function () { v.controls = true; play.hidden = true; start(); });
    v.addEventListener('play', function () { v.controls = true; play.hidden = true; });
    v.addEventListener('ended', function () { v.controls = false; play.hidden = false; });
    fs.addEventListener('click', function () {
      v.controls = true; play.hidden = true;
      if (v.requestFullscreen) { v.requestFullscreen().catch(function () {}); }
      else if (v.webkitRequestFullscreen) { v.webkitRequestFullscreen(); }
      else if (v.webkitEnterFullscreen) { v.webkitEnterFullscreen(); }
      start();
    });
  });
