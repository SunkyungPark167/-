<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>청시대(청소년시대연합) — 단체 소개</title>
  <meta name="description" content="청시대(청소년시대연합) 공식 소개 페이지 — 헌장, 활동, 연혁, 팀, 문의" />

  <style>
    :root{
      --navy: #071930;
      --navy-2: #0f2a4a;
      --navy-3: #153a62;
      --muted: rgba(255,255,255,0.88);
      --accent: #d88a00;
      --surface: rgba(255,255,255,0.03);
      --card-bg: rgba(255,255,255,0.04);
      --dot-size:12px;
      --active-dot-size:16px;
      --transition-duration:700ms;
      --max-width:1100px;
    }

    /* 기본 리셋 */
    html,body{
      height:100%;
      margin:0;
      font-family: "Apple SD 산돌고딕 Neo", "AppleSDSandolNeo", system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans KR", "Helvetica Neue", Arial, "Noto Sans", sans-serif;
      -webkit-font-smoothing:antialiased;
      -moz-osx-font-smoothing:grayscale;
      color:var(--muted);
      overflow: hidden; /* JS로 스크롤 제어 */
      background: var(--navy);
    }

    /* 배경: 이미지2와 비슷한 느낌을 CSS로 재현
       - 메인 그라디언트 (왼쪽 연한 톤 -> 오른쪽 진한 네이비)
       - 중첩된 radial/linear gradients로 얼룩/빛 효과 추가
       - ::before에 작은 점 무늬(그레인)로 텍스처링 */
    body::before{
      content: "";
      position: fixed;
      inset: 0;
      z-index: -3;
      background:
        radial-gradient(1200px 800px at 10% 20%, rgba(120,140,200,0.10), transparent 20%),
        radial-gradient(900px 700px at 85% 80%, rgba(15,40,90,0.25), transparent 28%),
        linear-gradient(180deg, rgba(20,40,90,0.9) 0%, rgba(6,18,39,1) 100%);
      mix-blend-mode: normal;
    }

    /* 부가적인 빛/그레인 레이어 */
    body::after{
      content: "";
      position: fixed;
      inset: 0;
      z-index: -2;
      pointer-events: none;
      background:
        /* subtle blue vignette */
        radial-gradient(60% 60% at 50% 40%, rgba(120,130,210,0.06), transparent 40%),
        radial-gradient(70% 70% at 75% 70%, rgba(0,0,0,0.25), transparent 45%);
      mix-blend-mode: overlay;
      filter: blur(6px) saturate(1.05);
    }

    /* 그레인(노이즈) — 작은 점 패턴을 반복시켜 텍스처 재현 */
    .grain {
      position: fixed;
      inset: 0;
      z-index: -1;
      opacity: 0.14;
      pointer-events: none;
      background-image:
        radial-gradient(rgba(255,255,255,0.02) 1px, transparent 1px);
      background-size: 3px 3px;
      mix-blend-mode: overlay;
      transform: scale(1.15);
      filter: contrast(.95) brightness(.98);
    }

    /* 상단 헤더 */
    .header {
      position: fixed;
      top: 18px;
      left: 24px;
      right:24px;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      z-index: 140;
      pointer-events: auto;
    }
    .branding { display:flex; align-items:center; gap:12px; }
    .logo {
      width:64px; height:64px;
      display:inline-flex; align-items:center; justify-content:center;
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border-radius:14px;
      padding:6px;
      box-shadow: 0 12px 30px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.03);
      border: 1px solid rgba(255,255,255,0.04);
    }
    .logo img { width:100%; height:100%; object-fit:contain; display:block; }
    .brand-text { font-weight:800; color:#fff; line-height:1; text-shadow: 0 2px 10px rgba(0,0,0,0.6); }
    .brand-text .title { font-size:18px; }
    .brand-text .sub { font-size:12px; opacity:0.9; margin-top:2px; }

    .nav { display:flex; gap:10px; align-items:center; }
    .nav button {
      background: transparent;
      color: var(--muted);
      border: 1px solid rgba(255,255,255,0.06);
      padding:8px 12px;
      border-radius:10px;
      cursor:pointer;
      font-weight:600;
      transition: all 160ms ease;
      backdrop-filter: blur(6px) saturate(0.95);
    }
    .nav button:hover { background: rgba(255,255,255,0.03); transform: translateY(-2px); }
    .nav .primary { background: var(--accent); color: #072033; border: none; padding:10px 14px; }

    /* 전체 섹션 컨테이너 */
    .container { height:100vh; width:100%; position:relative; }
    .sections {
      height:100%;
      width:100%;
      transition: transform var(--transition-duration) cubic-bezier(.22,.8,.26,1);
      will-change: transform;
    }
    .section {
      height:100vh;
      width:100%;
      display:flex;
      align-items:center;
      justify-content:center;
      flex-direction:column;
      text-align:center;
      padding: 28px;
      box-sizing:border-box;
    }
    .inner {
      width:100%;
      max-width: var(--max-width);
      margin: 0 auto;
      text-align:left;
    }

    /* 카드 (이미지2 스타일: 큰 라운드 사각) */
    .hero-card {
      width: 70%;
      max-width: 980px;
      min-height: 420px;
      border-radius: 32px;
      padding: 48px;
      box-sizing: border-box;
      background: linear-gradient(180deg, rgba(120,130,220,0.14), rgba(10,20,60,0.5));
      border: 1px solid rgba(255,255,255,0.06);
      box-shadow:
        0 30px 80px rgba(3,10,30,0.65),
        inset 0 1px 0 rgba(255,255,255,0.02);
      color: #fff;
      display:flex;
      flex-direction:column;
      justify-content:flex-start;
      gap:18px;
      position: relative;
      overflow: hidden;
      backdrop-filter: blur(6px) saturate(1.05);
    }

    /* 오른쪽 위 화살표 장식 */
    .hero-card .corner-arrow {
      position:absolute;
      right:22px;
      top:22px;
      width:40px; height:40px;
      border-radius:8px;
      display:flex; align-items:center; justify-content:center;
      color: rgba(255,255,255,0.9);
      font-size:20px;
      opacity:0.9;
    }

    .hero-title { font-size: clamp(28px,6vw,56px); font-weight:900; margin:0; line-height:1.02; letter-spacing:-0.6px; }
    .hero-sub { color: rgba(255,255,255,0.9); font-weight:600; margin-top:6px; }

    /* subtle dark strip at bottom of hero-card to mimic image */
    .hero-card::after {
      content: "";
      position:absolute;
      left:0; right:0; bottom:0;
      height:88px;
      background: linear-gradient(180deg, rgba(0,0,0,0.0), rgba(0,0,0,0.45));
      pointer-events:none;
    }

    /* 기타 섹션 스타일 (헌장, 활동, 연혁, 팀, 연락) - 기본은 이전과 동일 */
    .card { background: var(--card-bg); border-radius:12px; padding:18px; box-shadow: 0 8px 30px rgba(0,0,0,0.45); border: 1px solid rgba(255,255,255,0.04); color:var(--muted); }
    .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:16px; }
    .program { padding:14px; border-radius:10px; background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); min-height:120px; }
    .team-grid { display:grid; grid-template-columns: repeat(4, 1fr); gap:16px; }
    .member { background: var(--card-bg); padding:12px; border-radius:10px; text-align:center; }
    .avatar { width:88px; height:88px; border-radius:10px; margin:0 auto 12px auto; background: rgba(255,255,255,0.02); display:flex; align-items:center; justify-content:center; font-weight:700; color: #fff; overflow:hidden; }

    .nav-dots { position: fixed; right: 24px; top: 50%; transform: translateY(-50%); display:flex; flex-direction:column; gap:12px; z-index: 130; user-select:none; }
    .dot { width:var(--dot-size); height:var(--dot-size); border-radius:50%; background: rgba(255,255,255,0.45); display:inline-block; cursor:pointer; transition: all 220ms; box-shadow: 0 2px 6px rgba(0,0,0,0.25) inset; }
    .dot.active { width:var(--active-dot-size); height:var(--active-dot-size); background: var(--accent); box-shadow: 0 6px 18px rgba(0,0,0,0.35); }

    .hint { position: fixed; left: 50%; transform: translateX(-50%); bottom: 18px; color: rgba(255,255,255,0.85); font-size:13px; z-index: 120; pointer-events:none; text-shadow: 0 2px 6px rgba(0,0,0,0.3); }

    @media (max-width:1100px){
      .grid { grid-template-columns: repeat(2,1fr); }
      .team-grid { grid-template-columns: repeat(2,1fr); }
      .hero-card { width: 90%; padding:32px; border-radius:22px; min-height:360px; }
    }
    @media (max-width:600px){
      .logo { width:52px; height:52px; }
      .nav { display:none; } /* 모바일에서는 점 네비를 사용 */
      .grid { grid-template-columns:1fr; }
      .team-grid { grid-template-columns:1fr; }
      .section { padding:18px; }
      .hero-title { font-size: clamp(20px,8vw,36px); }
      .hero-card { padding:20px; min-height:300px; border-radius:18px; }
    }
  </style>
</head>
<body>
  <!-- Grain layer -->
  <div class="grain" aria-hidden="true"></div>

  <header class="header" role="banner" aria-label="사이트 헤더">
    <div class="branding">
      <div class="logo" aria-hidden="false">
        <!-- 같은 폴더에 logo.png 파일을 넣어주세요 -->
        <img src="./logo.png" alt="청시대 로고">
      </div>
      <div class="brand-text" aria-hidden="false">
        <div class="title">청시대</div>
        <div class="sub">청소년시대연합</div>
      </div>
    </div>

    <nav class="nav" role="navigation" aria-label="페이지 섹션 바로가기">
      <button type="button" data-target="0">소개</button>
      <button type="button" data-target="1">헌장·미션</button>
      <button type="button" data-target="2">활동·프로그램</button>
      <button type="button" data-target="3">연혁</button>
      <button type="button" data-target="4">팀</button>
      <button type="button" data-target="5" class="primary">문의</button>
    </nav>
  </header>

  <main id="main" class="container" role="main">
    <div class="sections" id="sections">

      <!-- 1: 소개 (hero 카드 스타일로 이미지2 느낌 재현) -->
      <section id="s1" class="section" data-index="0" aria-labelledby="intro-title">
        <div class="hero-card" role="region" aria-label="청시대 소개">
          <div class="corner-arrow">↗</div>
          <div style="display:flex; gap:18px; align-items:center;">
            <div style="width:92px; height:92px; border-radius:12px; overflow:hidden; background:transparent;">
              <img src="./logo.png" alt="" style="width:100%;height:100%;object-fit:contain;display:block;">
            </div>
            <div>
              <h1 class="hero-title">청시대 — 청소년시대연합</h1>
              <div class="hero-sub">청소년의 목소리를 모아 함께 성장하는 공식 단체입니다.</div>
            </div>
          </div>

          <div style="flex:1;"></div>

          <div style="display:flex; gap:18px; align-items:center; justify-content:flex-start; flex-wrap:wrap;">
            <div style="font-weight:700; color:rgba(255,255,255,0.95);">주요 활동</div>
            <div style="background:rgba(255,255,255,0.03); padding:8px 12px; border-radius:10px; border:1px solid rgba(255,255,255,0.03);">교육 워크숍</div>
            <div style="background:rgba(255,255,255,0.03); padding:8px 12px; border-radius:10px; border:1px solid rgba(255,255,255,0.03);">멘토링</div>
            <div style="background:rgba(255,255,255,0.03); padding:8px 12px; border-radius:10px; border:1px solid rgba(255,255,255,0.03);">캠페인</div>
          </div>
        </div>
      </section>

      <!-- 이하 기존 섹션들 (헌장·미션, 활동, 연혁, 팀, 문의) 동일 구성 -->
      <section id="s2" class="section" data-index="1" aria-labelledby="mission-title">
        <div class="inner">
          <h1 id="mission-title">헌장 · 미션</h1>
          <p>청시대는 청소년의 권리와 성장을 지지하며 다음 원칙을 준수합니다.</p>
          <div style="height:14px;"></div>
          <div class="card charter" role="list" aria-label="청시대 헌장">
            <ol style="margin:0 0 0 18px; padding:0;">
              <li><strong>참여:</strong> 모든 청소년이 존중받는 참여 기회를 제공합니다.</li>
              <li><strong>교육:</strong> 역량 강화를 위한 실천적 교육을 제공합니다.</li>
              <li><strong>연대:</strong> 지역·기관과 협력하여 지속 가능한 활동을 전개합니다.</li>
              <li><strong>책임:</strong> 투명성과 책임성을 바탕으로 운영합니다.</li>
            </ol>
          </div>
        </div>
      </section>

      <section id="s3" class="section" data-index="2" aria-labelledby="program-title">
        <div class="inner">
          <h1 id="program-title">활동 · 프로그램</h1>
          <p>대표 프로그램 예시입니다.</p>
          <div style="height:16px;"></div>
          <div class="grid">
            <div class="program card">
              <h3>교육 워크숍</h3>
              <p>리더십, 미디어 리터러시, 진로탐색 등 실무 중심 교육을 제공합니다.</p>
            </div>
            <div class="program card">
              <h3>멘토링</h3>
              <p>전문가 멘토와의 1:1 멘토링으로 실질적 성장을 돕습니다.</p>
            </div>
            <div class="program card">
              <h3>캠페인</h3>
              <p>청소년 이슈에 대한 공론화 및 정책 제안을 진행합니다.</p>
            </div>
          </div>
        </div>
      </section>

      <section id="s4" class="section" data-index="3" aria-labelledby="history-title">
        <div class="inner">
          <h1 id="history-title">연혁</h1>
          <p>주요 연혁(예시)</p>
          <div style="height:12px;"></div>
          <div class="card timeline">
            <div class="tl-item"><div class="tl-year">2024</div><div>단체 창립 및 첫 워크숍 개최</div></div>
            <div class="tl-item"><div class="tl-year">2025</div><div>지역 파트너십 확장 · 멘토링 프로그램 시작</div></div>
            <div class="tl-item"><div class="tl-year">2026</div><div>정책 제안 보고서 발간</div></div>
          </div>
        </div>
      </section>

      <section id="s5" class="section" data-index="4" aria-labelledby="team-title">
        <div class="inner">
          <h1 id="team-title">팀 · 구성원</h1>
          <p>운영진 및 활동가를 소개합니다.</p>
          <div style="height:12px;"></div>
          <div class="team-grid">
            <div class="member card">
              <div class="avatar"><img src="./team1.png" alt="" style="width:100%;height:100%;object-fit:cover;display:block"></div>
              <h4>홍길동</h4><small>대표</small>
            </div>
            <div class="member card">
              <div class="avatar"><img src="./team2.png" alt="" style="width:100%;height:100%;object-fit:cover;display:block"></div>
              <h4>김영희</h4><small>프로그램 매니저</small>
            </div>
            <div class="member card">
              <div class="avatar"><img src="./team3.png" alt="" style="width:100%;height:100%;object-fit:cover;display:block"></div>
              <h4>이철수</h4><small>커뮤니티 코디네이터</small>
            </div>
            <div class="member card">
              <div class="avatar">A</div>
              <h4>박수진</h4><small>운영팀</small>
            </div>
          </div>
        </div>
      </section>

      <section id="s6" class="section" data-index="5" aria-labelledby="contact-title">
        <div class="inner">
          <h1 id="contact-title">문의 · 외부 링크</h1>
          <p>문의사항은 아래 연락을 통해 접수해 주세요.</p>
          <div style="height:12px;"></div>
          <div class="card contact-grid">
            <div>
              <p style="margin:0 0 8px 0;"><strong>이메일</strong><br> <a href="mailto:info@example.org" style="color:var(--muted)">info@example.org</a></p>
              <p style="margin:0 0 8px 0;"><strong>전화</strong><br> 02-1234-5678</p>
              <p style="margin:0 0 8px 0;"><strong>주소</strong><br> 서울특별시 예시구 예시로 123</p>

              <div style="height:10px;"></div>
              <p style="margin:0 0 8px 0;"><strong>외부 링크</strong></p>
              <p style="margin:0; display:flex; gap:8px; flex-wrap:wrap;">
                <a class="card" style="padding:8px 10px; border-radius:8px;" href="#" target="_blank" rel="noopener">페이스북</a>
                <a class="card" style="padding:8px 10px; border-radius:8px;" href="#" target="_blank" rel="noopener">인스타그램</a>
                <a class="card" style="padding:8px 10px; border-radius:8px;" href="#" target="_blank" rel="noopener">보고서</a>
              </p>
            </div>

            <div>
              <form class="contact-form" action="mailto:info@example.org" method="post" enctype="text/plain" onsubmit="alert('이 데모 양식은 실제 서버 전송을 구현하지 않습니다. 실서비스용 서버 또는 메일 처리 설정이 필요합니다.'); return false;">
                <label style="display:block; font-weight:700; margin-bottom:6px;">이름</label>
                <input type="text" name="name" placeholder="이름">
                <label style="display:block; font-weight:700; margin:8px 0 6px 0;">이메일</label>
                <input type="email" name="email" placeholder="your@email.com">
                <label style="display:block; font-weight:700; margin:8px 0 6px 0;">문의</label>
                <textarea name="message" rows="5" placeholder="문의 내용을 입력하세요"></textarea>
                <button type="submit">보내기</button>
              </form>
            </div>
          </div>

        </div>
      </section>

    </div>
  </main>

  <div class="nav-dots" id="navDots" aria-hidden="false" role="navigation" aria-label="섹션 점 내비게이션"></div>
  <div class="hint">마우스 휠 / 아래로 드래그(터치)로 이동 — 마지막에서 다음은 처음으로 이동합니다</div>

  <script>
    (function(){
      const sectionsEl = document.getElementById('sections');
      const sectionEls = Array.from(document.querySelectorAll('.section'));
      const navDots = document.getElementById('navDots');
      const navButtons = Array.from(document.querySelectorAll('.nav button'));
      const total = sectionEls.length;
      let current = 0;
      let isAnimating = false;
      const transitionMs = 700;
      let touchStartY = 0;
      let touchEndY = 0;
      const touchThreshold = 50; // px

      // create dots
      for(let i=0;i<total;i++){
        const d = document.createElement('div');
        d.className = 'dot' + (i===0? ' active' : '');
        d.dataset.index = i;
        d.setAttribute('role','button');
        d.setAttribute('aria-label','섹션 '+(i+1)+'로 이동');
        d.tabIndex = 0;
        d.addEventListener('click', (e)=>{
          goTo(parseInt(e.currentTarget.dataset.index,10));
        });
        d.addEventListener('keydown', (e)=>{
          if(e.key === 'Enter' || e.key === ' ') { e.preventDefault(); goTo(parseInt(e.currentTarget.dataset.index,10)); }
        });
        navDots.appendChild(d);
      }

      // nav buttons (header)
      navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
          const idx = parseInt(btn.dataset.target, 10);
          goTo(idx);
        });
      });

      function updateDots(){
        document.querySelectorAll('.dot').forEach((dot, idx) => {
          if(idx === current) dot.classList.add('active');
          else dot.classList.remove('active');
        });
      }

      function setTransformForIndex(idx){
        const y = -idx * window.innerHeight;
        sectionsEl.style.transform = `translateY(${y}px)`;
      }

      function goTo(idx){
        if(isAnimating) return;
        isAnimating = true;
        current = ((idx % total) + total) % total; // loop safe
        setTransformForIndex(current);
        updateDots();
        sectionEls[current].focus && sectionEls[current].setAttribute('tabindex','-1');
        setTimeout(()=>{ isAnimating = false; }, transitionMs + 50);
      }

      function next(){ goTo(current + 1); }
      function prev(){ goTo(current - 1); }

      // resize handler
      window.addEventListener('resize', ()=> setTransformForIndex(current));

      // wheel (debounced)
      let wheelDebounce = false;
      window.addEventListener('wheel', (e) => {
        if(wheelDebounce || isAnimating) return;
        wheelDebounce = true;
        setTimeout(()=> wheelDebounce = false, transitionMs + 50);
        if(e.deltaY > 10) next();
        else if(e.deltaY < -10) prev();
      }, {passive: true});

      // touch
      window.addEventListener('touchstart', (e) => {
        if(e.touches && e.touches.length > 0) touchStartY = e.touches[0].clientY;
      }, {passive: true});
      window.addEventListener('touchend', (e) => {
        if(e.changedTouches && e.changedTouches.length > 0){
          touchEndY = e.changedTouches[0].clientY;
          const diff = touchStartY - touchEndY;
          if(Math.abs(diff) > touchThreshold){
            if(diff > 0) next();
            else prev();
          }
        }
      }, {passive: true});

      // keyboard
      window.addEventListener('keydown', (e) => {
        if(e.key === 'ArrowDown' || e.key === 'PageDown') next();
        else if(e.key === 'ArrowUp' || e.key === 'PageUp') prev();
        else if(e.key === 'Home') goTo(0);
        else if(e.key === 'End') goTo(total-1);
      });

      // initial transform
      setTransformForIndex(0);

    })();
  </script>
</body>
</html>
