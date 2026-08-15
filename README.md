<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>청시대(청소년시대연합) — 소개</title>

  <style>
    :root{
      --navy: #071930;       /* 메인 네이비 */
      --navy-2: #0f2a4a;     /* 진한 네이비 */
      --navy-3: #153a62;     /* 보조 네이비 */
      --accent: #d88a00;     /* 로고의 주황 계열을 보조색으로 사용 */
      --dot-size:12px;
      --active-dot-size:16px;
      --transition-duration:700ms;
    }

    /* 폰트: 시스템에 설치된 Apple SD 산돌고딕 Neo 우선 사용.
       웹폰트 파일이 있으면 아래 예시대로 @font-face 추가 가능(라이선스 확인). */
    html,body{
      height:100%;
      margin:0;
      font-family: "Apple SD 산돌고딕 Neo", "AppleSDSandolNeo", system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans KR", "Helvetica Neue", Arial, "Noto Sans", sans-serif;
      -webkit-font-smoothing:antialiased;
      -moz-osx-font-smoothing:grayscale;
      background: var(--navy);
      color: #fff;
      overflow: hidden; /* 스크롤은 JS로 제어 */
    }

    /* 상단 고정 헤더: 로고 + 브랜드명 */
    .header {
      position: fixed;
      top: 18px;
      left: 24px;
      display:flex;
      align-items:center;
      gap:12px;
      z-index: 120;
      pointer-events: auto;
    }
    .logo {
      width:72px;
      height:72px;
      display:inline-flex;
      align-items:center;
      justify-content:center;
      background: rgba(255,255,255,0.03);
      border-radius:10px;
      padding:6px;
      box-shadow: 0 6px 18px rgba(0,0,0,0.45);
    }
    .logo img {
      width:100%;
      height:100%;
      object-fit:contain;
      display:block;
    }
    .brand {
      font-size:18px;
      font-weight:700;
      letter-spacing:0.2px;
      color: #fff;
      text-shadow: 0 2px 8px rgba(0,0,0,0.45);
    }
    .brand small {
      display:block;
      font-size:12px;
      font-weight:500;
      opacity:0.85;
      margin-top:2px;
      color: rgba(255,255,255,0.9);
    }

    /* 전체 컨테이너: 각 섹션을 수직으로 쌓음 */
    .container {
      height:100vh;
      width:100%;
      position:relative;
    }
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
      font-size:clamp(28px,6vw,64px);
      color:#fff;
      flex-direction:column;
      text-align:center;
      padding: 28px;
    }

    /* 섹션별 네이비 톤 배경 */
    #s1{ background: linear-gradient(180deg, var(--navy) 0%, var(--navy-2) 100%); }
    #s2{ background: linear-gradient(180deg, var(--navy-2) 0%, var(--navy-3) 100%); }
    #s3{ background: linear-gradient(180deg, var(--navy-3) 0%, #1e4b7a 100%); }
    #s4{ background: linear-gradient(180deg, #152d4e 0%, #0b2440 100%); }

    /* 오른쪽 네비(점) */
    .nav-dots {
      position: fixed;
      right: 24px;
      top: 50%;
      transform: translateY(-50%);
      display:flex;
      flex-direction:column;
      gap:12px;
      z-index: 100;
      user-select:none;
    }
    .dot {
      width:var(--dot-size);
      height:var(--dot-size);
      border-radius:50%;
      background: rgba(255,255,255,0.45);
      display:inline-block;
      cursor:pointer;
      transition: all 220ms;
      box-shadow: 0 2px 6px rgba(0,0,0,0.25) inset;
    }
    .dot.active {
      width:var(--active-dot-size);
      height:var(--active-dot-size);
      background: var(--accent);
      box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    }

    .hint {
      position: fixed;
      left: 50%;
      transform: translateX(-50%);
      bottom: 18px;
      color: rgba(255,255,255,0.9);
      font-size:14px;
      z-index: 80;
      pointer-events:none;
      text-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }

    /* 섹션 텍스트 스타일 */
    .section h1{
      margin:0;
      font-weight:800;
      font-size: clamp(24px,6vw,48px);
      letter-spacing: -0.5px;
    }
    .section p{
      margin:12px 0 0 0;
      font-size:16px;
      opacity:0.95;
      max-width:900px;
    }

    @media (max-width:600px){
      .nav-dots { right:12px; gap:10px; }
      .logo { width:56px; height:56px; }
      .brand { font-size:16px; }
    }
  </style>
</head>
<body>
  <!-- 상단 로고: 같은 폴더에 logo.png로 저장해주세요 -->
  <a href="#" class="header" aria-label="청시대 홈으로">
    <div class="logo">
      <img src="./logo.png" alt="청시대 로고 (청소년시대연합)">
    </div>
    <div class="brand">
      청시대
      <small>청소년시대연합</small>
    </div>
  </a>

  <div class="container" id="container">
    <div class="sections" id="sections">
      <section id="s1" class="section" data-index="0">
        <div>
          <h1>1. 청시대 소개</h1>
          <p>청소년시대연합 — 당신의 이야기를 함께합니다.</p>
        </div>
      </section>

      <section id="s2" class="section" data-index="1">
        <div>
          <h1>2. 미션</h1>
          <p>청소년의 목소리를 연결하고 성장하는 커뮤니티.</p>
        </div>
      </section>

      <section id="s3" class="section" data-index="2">
        <div>
          <h1>3. 활동</h1>
          <p>워크숍, 캠페인, 멘토링 등 다양한 활동을 소개합니다.</p>
        </div>
      </section>

      <section id="s4" class="section" data-index="3">
        <div>
          <h1>4. 참여하기</h1>
          <p>함께할 청소년을 기다립니다 — 지금 바로 참여하세요.</p>
        </div>
      </section>
    </div>
  </div>

  <div class="nav-dots" id="navDots" aria-hidden="false"></div>
  <div class="hint">마우스 휠 / 아래로 드래그(터치)로 이동 — 마지막에서 다음은 처음으로 이동합니다</div>

  <script>
    (function(){
      const sectionsEl = document.getElementById('sections');
      const sectionEls = Array.from(document.querySelectorAll('.section'));
      const navDots = document.getElementById('navDots');
      const total = sectionEls.length;
      let current = 0;
      let isAnimating = false;
      const transitionMs = 700;
      let touchStartY = 0;
      let touchEndY = 0;
      const touchThreshold = 50; // px

      // 네비 점 생성
      for(let i=0;i<total;i++){
        const d = document.createElement('div');
        d.className = 'dot' + (i===0? ' active' : '');
        d.dataset.index = i;
        d.addEventListener('click', (e)=>{
          goTo(parseInt(e.currentTarget.dataset.index,10));
        });
        navDots.appendChild(d);
      }

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
        current = ((idx % total) + total) % total; // 루프
        setTransformForIndex(current);
        updateDots();
        setTimeout(()=>{ isAnimating = false; }, transitionMs + 50);
      }

      function next(){
        goTo(current + 1);
      }
      function prev(){
        goTo(current - 1);
      }

      // 사이즈 변경 시 위치 재설정
      function resizeHandler(){
        setTransformForIndex(current);
      }
      window.addEventListener('resize', resizeHandler);

      // 마우스 휠 이벤트 (디바운스)
      let wheelDebounce = false;
      window.addEventListener('wheel', (e) => {
        if(wheelDebounce || isAnimating) return;
        wheelDebounce = true;
        setTimeout(()=> wheelDebounce = false, transitionMs + 50);
        if(e.deltaY > 10) next();
        else if(e.deltaY < -10) prev();
      }, {passive: true});

      // 터치: 아래로 드래그하면 다음(section1 -> section2)
      window.addEventListener('touchstart', (e) => {
        if(e.touches && e.touches.length > 0){
          touchStartY = e.touches[0].clientY;
        }
      }, {passive: true});
      window.addEventListener('touchend', (e) => {
        if(e.changedTouches && e.changedTouches.length > 0){
          touchEndY = e.changedTouches[0].clientY;
          const diff = touchStartY - touchEndY;
          if(Math.abs(diff) > touchThreshold){
            if(diff > 0) next(); // 위로 스와이프 -> 다음
            else prev();
          }
        }
      }, {passive: true});

      // 키보드(위/아래)
      window.addEventListener('keydown', (e) => {
        if(e.key === 'ArrowDown' || e.key === 'PageDown') next();
        else if(e.key === 'ArrowUp' || e.key === 'PageUp') prev();
      });

      // 초기 위치 세팅
      setTransformForIndex(0);
    })();
  </script>
</body>
</html>
