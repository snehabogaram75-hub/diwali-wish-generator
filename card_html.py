import html

TEMPLATE = """
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@400;500&family=Noto+Sans+Telugu:wght@400;600&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
  body { margin:0; display:flex; flex-direction:column; align-items:center; font-family:'Poppins',sans-serif; }
  #card { width:540px; height:675px; box-sizing:border-box; position:relative; overflow:hidden; border-radius:24px;
    background: radial-gradient(circle at 50% 38%, #7a1f3d 0%, #3d0f2e 45%, #1a0620 100%); color:#fff4d6; text-align:center; }
  #card::before { content:''; position:absolute; inset:14px; border:2px solid #f5b83d; border-radius:16px; opacity:.85; }
  .stars { position:absolute; inset:0; background-image:
     radial-gradient(2px 2px at 20% 15%, #ffd97a, transparent), radial-gradient(2px 2px at 80% 20%, #ffd97a, transparent),
     radial-gradient(1.5px 1.5px at 35% 30%, #fff, transparent), radial-gradient(2px 2px at 65% 10%, #fff, transparent),
     radial-gradient(1.5px 1.5px at 10% 40%, #ffd97a, transparent), radial-gradient(2px 2px at 90% 45%, #ffd97a, transparent),
     radial-gradient(1.5px 1.5px at 50% 22%, #fff, transparent); }
  .inner { position:relative; padding:44px 44px 0; }
  .greet { font-family:'Playfair Display',serif; font-size:44px; color:#f5b83d; margin:0; letter-spacing:1px; }
  .name { font-size:22px; margin:6px 0 0; letter-spacing:3px; text-transform:uppercase; opacity:.95; }
  svg { width:230px; margin:14px 0 6px; }
  .wish { font-family:'Poppins','Noto Sans Telugu',sans-serif; font-size:19px; line-height:1.55; margin:0 6px; }
  .foot { position:absolute; bottom:34px; width:100%; font-family:'Playfair Display',serif; color:#f5b83d; font-size:18px; letter-spacing:3px; }
  #dl { margin:18px 0 8px; padding:12px 26px; font-size:16px; border:none; border-radius:30px; background:#e8590c; color:#fff; cursor:pointer; font-family:'Poppins',sans-serif; }
  #dl:hover { background:#c94a08; }
</style>

<div id="card">
  <div class="stars"></div>
  <div class="inner">
    <h1 class="greet">Happy Diwali</h1>
    <p class="name">__NAME__</p>
    <svg viewBox="0 0 200 170" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#ffb347" stop-opacity=".75"/><stop offset="100%" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
        <linearGradient id="flame" x1="0" y1="1" x2="0" y2="0"><stop offset="0%" stop-color="#ff7a00"/><stop offset="60%" stop-color="#ffc233"/><stop offset="100%" stop-color="#fff3a0"/></linearGradient>
        <linearGradient id="body" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#f08a24"/><stop offset="100%" stop-color="#a8400f"/></linearGradient>
      </defs>
      <circle cx="100" cy="62" r="62" fill="url(#glow)"/>
      <path d="M100 8 C122 38 130 58 100 88 C70 58 78 38 100 8Z" fill="url(#flame)"/>
      <path d="M100 40 C111 56 113 66 100 80 C87 66 89 56 100 40Z" fill="#fffbe0" opacity=".9"/>
      <rect x="98" y="84" width="4" height="12" rx="2" fill="#4a2410"/>
      <path d="M14 98 Q100 88 186 98 Q176 158 100 158 Q24 158 14 98Z" fill="url(#body)"/>
      <ellipse cx="100" cy="98" rx="86" ry="11" fill="#c75a14"/>
      <ellipse cx="100" cy="98" rx="70" ry="7" fill="#7a2c08"/>
      <path d="M40 124 Q100 140 160 124" stroke="#ffd27a" stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/>
      <circle cx="70" cy="136" r="3" fill="#ffd27a"/><circle cx="100" cy="142" r="3" fill="#ffd27a"/><circle cx="130" cy="136" r="3" fill="#ffd27a"/>
    </svg>
    <p class="wish">__WISH__</p>
  </div>
  <div class="foot">SHUBH DEEPAVALI</div>
</div>
<button id="dl">Download Card 📥</button>
<script>
  document.getElementById('dl').onclick = function () {
    document.fonts.ready.then(function () {
      html2canvas(document.getElementById('card'), {scale: 2, backgroundColor: null, useCORS: true}).then(function (c) {
        var a = document.createElement('a');
        a.download = 'diwali_wish.png';
        a.href = c.toDataURL('image/png');
        a.click();
      });
    });
  };
</script>
"""

def card_html(name, wish):
    return TEMPLATE.replace("__NAME__", html.escape(name)).replace("__WISH__", html.escape(wish))
