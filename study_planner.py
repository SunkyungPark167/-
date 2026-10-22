"""
Study Planner (웹 브라우저용, Streamlit)

설치:  pip install streamlit pandas
실행:  streamlit run study_planner.py

데이터는 같은 폴더의 planner_data.json 에 자동 저장됩니다.
"""
import calendar
import hashlib
import hmac
import json
import re
import secrets
import uuid
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
from html import escape as esc
import streamlit as st

LEGACY_DB = Path("planner_data.json")  # 계정 기능 이전 데이터
USERS_DB = Path("planner_users.json")


def user_db(email):
    return Path("planner_" + hashlib.sha1(email.lower().encode()).hexdigest()[:12] + ".json")

TODAY = date.today()
WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

st.set_page_config(page_title="Study Planner", page_icon="📚", layout="wide")

# ---------------- 데이터 ----------------
def blank_data():
    return {"subjects": ["Korean", "Math", "English"], "tasks": [], "exams": [], "logs": []}


_user = st.session_state.get("user")
DB = user_db(_user) if _user else None
if _user and st.session_state.get("data_for") != _user:
    st.session_state.data = json.loads(DB.read_text(encoding="utf-8")) if DB.exists() else blank_data()
    st.session_state.data_for = _user
data = st.session_state.data if _user else blank_data()
if _user:
    data["email"] = _user
for k, v in (('schedule', {}), ('daily', {}), ('resume', {}), ('email', '')):
    data.setdefault(k, v)
for ko, en in zip("월화수목금토일", WEEKDAYS):  # 예전 한글 요일 데이터를 영어 키로 이전
    if ko in data["schedule"]:
        data["schedule"][en] = [{"Time": r.get("시간", r.get("Time", "")), "Plan": r.get("일정", r.get("Plan", ""))}
                                for r in data["schedule"].pop(ko)]
_ren = {"기간": "Period", "활동/경력": "Role / Activity", "내용": "Details", "취득일": "Date", "이름": "Title", "발급기관": "Issuer"}
for k in ("career", "awards"):
    data["resume"][k] = [{_ren.get(a, a): b for a, b in r.items()} for r in data["resume"].get(k, [])]


def save():
    if DB is not None:
        DB.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def new_id():
    return uuid.uuid4().hex[:8]


def label(t):
    return f"{'✅' if t['done'] else '⬜'} [{t['subject']}] {t['title']}"


def tasks_on(day):
    return [t for t in data["tasks"] if t["due"] == day.isoformat()]


def exams_on(day):
    return [e for e in data["exams"] if e["date"] == day.isoformat()]



# ---------------- 1. 과목별 할 일 ----------------
def page_tasks():
    c1, c2 = st.columns(2)
    with c1.form("add_subject", clear_on_submit=True):
        name = st.text_input("New subject")
        if st.form_submit_button("Add subject") and name and name not in data["subjects"]:
            data["subjects"].append(name)
            save()
            st.rerun()
    with c2.form("add_task", clear_on_submit=True):
        subj = st.selectbox("Subject", data["subjects"])
        title = st.text_input("Task")
        due = st.date_input("Due date", TODAY)
        if st.form_submit_button("Add task") and title:
            data["tasks"].append(
                {"id": new_id(), "subject": subj, "title": title,
                 "due": due.isoformat(), "done": False}
            )
            save()
            st.rerun()

    for s in data["subjects"]:
        items = sorted((t for t in data["tasks"] if t["subject"] == s), key=lambda t: t["due"])
        if not items:
            continue
        done_n = sum(t["done"] for t in items)
        st.subheader(f"{s}  ({done_n}/{len(items)})")
        st.progress(done_n / len(items))
        for t in items:
            a, b = st.columns([9, 1])
            checked = a.checkbox(f"{t['title']}  · due  {t['due']}", value=t["done"], key="c" + t["id"])
            if checked != t["done"]:
                t["done"] = checked
                save()
                st.rerun()
            if b.button("🗑️", key="d" + t["id"]):
                data["tasks"].remove(t)
                save()
                st.rerun()

# ---------------- 2. 시험 D-day ----------------
def page_dday():
    with st.form("add_exam", clear_on_submit=True):
        c1, c2 = st.columns(2)
        ename = c1.text_input("Exam name")
        edate = c2.date_input("Exam date", TODAY + timedelta(days=30))
        if st.form_submit_button("Add D-day") and ename:
            data["exams"].append({"id": new_id(), "name": ename, "date": edate.isoformat()})
            save()
            st.rerun()

    for e in sorted(data["exams"], key=lambda e: e["date"]):
        diff = (date.fromisoformat(e["date"]) - TODAY).days
        tag = "D-Day 🔥" if diff == 0 else f"D-{diff}" if diff > 0 else f"D+{-diff}"
        a, b, c = st.columns([3, 2, 1])
        a.metric(e["name"], tag)
        b.write(e["date"])
        if c.button("🗑️", key="e" + e["id"]):
            data["exams"].remove(e)
            save()
            st.rerun()
    if not data["exams"]:
        st.info("Add an exam date to see your countdown.")

# ---------------- 3. 공부 시간 기록 + 통계 ----------------
def page_log():
    with st.form("add_log", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        ldate = c1.date_input("Date", TODAY)
        lsubj = c2.selectbox("Subject", data["subjects"])
        lmin = c3.number_input("Study time (min)", 5, 720, 60, step=5)
        if st.form_submit_button("Add log"):
            data["logs"].append(
                {"date": ldate.isoformat(), "subject": lsubj, "minutes": int(lmin)}
            )
            save()
            st.rerun()

    if data["logs"]:
        df = pd.DataFrame(data["logs"])
        df["date"] = pd.to_datetime(df["date"])
        week_start = pd.Timestamp(TODAY - timedelta(days=TODAY.weekday()))
        hours = lambda x: f"{x / 60:.1f} h"

        m1, m2, m3 = st.columns(3)
        m1.metric("Today", hours(df[df["date"] == pd.Timestamp(TODAY)]["minutes"].sum()))
        m2.metric("This week", hours(df[df["date"] >= week_start]["minutes"].sum()))
        m3.metric("Total", hours(df["minutes"].sum()))

        st.write("**Total by subject (hours)**")
        st.bar_chart(df.groupby("subject")["minutes"].sum() / 60)

        st.write("**Last 14 days (hours)**")
        days = pd.date_range(TODAY - timedelta(days=13), TODAY)
        st.bar_chart(df.groupby("date")["minutes"].sum().reindex(days, fill_value=0) / 60)

        with st.expander("Delete recent logs"):
            for i in range(len(data["logs"]) - 1, max(len(data["logs"]) - 11, -1), -1):
                lg = data["logs"][i]
                a, b = st.columns([8, 1])
                a.write(f"{lg['date']} · {lg['subject']} · {lg['minutes']} min")
                if b.button("🗑️", key=f"l{i}"):
                    data["logs"].pop(i)
                    save()
                    st.rerun()
    else:
        st.info("Log your study time to see stats.")

# ---------------- 4. 오늘 / 이번 주 계획표 ----------------
def page_week():
    st.subheader(f"Today ({TODAY:%b %d})")
    for e in exams_on(TODAY):
        st.write(f"🎯 {e['name']}")
    today_tasks = tasks_on(TODAY)
    for t in today_tasks:
        st.write(label(t))
    if not today_tasks:
        st.caption("Nothing due today 🎉")

    overdue = [t for t in data["tasks"] if t["due"] < TODAY.isoformat() and not t["done"]]
    if overdue:
        st.warning("You have overdue tasks")
        for t in overdue:
            st.write(f"{label(t)}  (due  {t['due']})")

    st.subheader("This week")
    monday = TODAY - timedelta(days=TODAY.weekday())
    for i, col in enumerate(st.columns(7)):
        day = monday + timedelta(days=i)
        col.markdown(f"**{WEEKDAYS[i]} {day.day}**" + (" 👈" if day == TODAY else ""))
        for e in exams_on(day):
            col.caption(f"🎯 {e['name']}")
        for t in tasks_on(day):
            col.caption(label(t))

# ---------------- 5. Monthly Planner ----------------
def page_month():
    c1, c2 = st.columns(2)
    year = int(c1.number_input("Year", 2020, 2100, TODAY.year))
    month = c2.selectbox("Month", list(range(1, 13)), index=TODAY.month - 1,
                         format_func=lambda m: calendar.month_name[m])

    for i, col in enumerate(st.columns(7)):
        col.markdown(f"**{WEEKDAYS[i]}**")
    for week in calendar.Calendar(0).monthdatescalendar(year, month):
        for col, day in zip(st.columns(7), week):
            if day.month != month:
                continue
            col.markdown(f"**{day.day}**" + (" 🔵" if day == TODAY else ""))
            for e in exams_on(day):
                col.caption(f"🎯 {e['name']}")
            for t in tasks_on(day):
                col.caption(label(t))

# ---------------- 6. 구글 캘린더로 내보내기 (.ics) ----------------
def ics_text(text):
    return (text.replace("\\", "\\\\").replace(";", "\\;")
                .replace(",", "\\,").replace("\n", "\\n"))


def make_ics(include_tasks, include_done, include_exams):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Study Planner//KO",
             "CALSCALE:GREGORIAN", "X-WR-CALNAME:Study Planner"]
    count = 0

    def add_event(uid, summary, day):
        nonlocal count
        nxt = day + timedelta(days=1)
        lines.extend([
            "BEGIN:VEVENT", f"UID:{uid}@study-planner", f"DTSTAMP:{stamp}",
            f"DTSTART;VALUE=DATE:{day:%Y%m%d}", f"DTEND;VALUE=DATE:{nxt:%Y%m%d}",
            f"SUMMARY:{ics_text(summary)}", "END:VEVENT",
        ])
        count += 1

    if include_tasks:
        for t in data["tasks"]:
            if t["done"] and not include_done:
                continue
            mark = "✅" if t["done"] else "📚"
            add_event("task-" + t["id"], f"{mark} [{t['subject']}] {t['title']}",
                      date.fromisoformat(t["due"]))
    if include_exams:
        for e in data["exams"]:
            add_event("exam-" + e["id"], f"🎯 {e['name']}", date.fromisoformat(e["date"]))

    lines.append("END:VCALENDAR")
    return ("\r\n".join(lines) + "\r\n").encode("utf-8"), count


def page_ics():
    st.subheader("Export to Google Calendar")
    inc_tasks = st.checkbox("Include tasks", value=True)
    inc_done = st.checkbox("Include completed tasks (✅)", value=True)
    inc_exams = st.checkbox("Include exam D-days", value=True)

    ics_bytes, n = make_ics(inc_tasks, inc_done, inc_exams)
    st.write(f"Events to export: **{n}**")
    st.download_button("📥 Download calendar file (.ics)", data=ics_bytes,
                       file_name="study_planner.ics", mime="text/calendar", disabled=(n == 0))

    st.markdown(
        """
**How to add it to Google Calendar** (use the website on a computer)
1. Go to calendar.google.com → **Other calendars +** → **Create new calendar** → name it `Study Planner`
2. Click ⚙️ **Settings** → **Import & export** on the left
3. Choose `study_planner.ics` under **Select file from your computer**
4. Under **Add to calendar**, pick `Study Planner`, then click **Import**

If you import again after editing, matching events usually update instead of duplicating.
If things get messy, delete the `Study Planner` calendar, recreate it, and re-import.
"""
    )

# ====================== 새 화면들 ======================
UA = "Mozilla/5.0 (personal study planner)"
QUOTES = [
    "A journey of a thousand miles begins with a single step. — Lao Tzu",
    "Well begun is half done. — Proverb",
    "Never leave that till tomorrow which you can do today. — Benjamin Franklin",
    "Success is the sum of small efforts, repeated day in and day out. — Robert Collier",
    "There is no royal road to geometry. — Euclid",
    "My strength lies solely in my tenacity. — Louis Pasteur",
    "Even the darkest night will end and the sun will rise. — Victor Hugo",
    "Slow and steady wins the race. — Aesop",
    "Rome wasn't built in a day. — Proverb",
    "We are what we repeatedly do. — Will Durant",
    "The expert in anything was once a beginner. — Helen Hayes",
    "It always seems impossible until it's done. — Nelson Mandela",
    "Don't watch the clock; do what it does. Keep going. — Sam Levenson",
    "Education is the passport to the future. — Malcolm X",
]
NEWS_FEEDS = {
    "🏛️ Politics": [("Guardian", "https://www.theguardian.com/politics/rss"),
                ("BBC", "http://feeds.bbci.co.uk/news/politics/rss.xml")],
    "💰 Economy": [("Guardian", "https://www.theguardian.com/business/rss"),
                ("BBC", "http://feeds.bbci.co.uk/news/business/rss.xml")],
    "🌏 World": [("Guardian", "https://www.theguardian.com/world/rss"),
                ("BBC", "http://feeds.bbci.co.uk/news/world/rss.xml")],
    "💻 Tech & Science": [("BBC", "http://feeds.bbci.co.uk/news/technology/rss.xml"),
                  ("NYT", "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml")],
}

st.session_state.setdefault("rev", 0)
st.session_state.setdefault("page", "🏠 Home")
st.session_state.setdefault("news_cat", list(NEWS_FEEDS)[0])
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&family=Instrument+Serif:ital@0;1&family=Hanken+Grotesk:wght@400;500;600;700&display=swap');
.stApp, .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, button, input, textarea {font-family:'Noto Sans KR',sans-serif;}
.stApp {background: radial-gradient(1100px 480px at 8% -8%, rgba(122,23,48,.16), transparent), radial-gradient(900px 420px at 100% 0%, rgba(60,8,20,.12), transparent);}
h1 {background:linear-gradient(90deg,#2a060f,#8c1c34); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; font-weight:800 !important;}
h2, h3 {font-weight:800 !important;}
/* 카드 / 폼 / 지표 */
div[data-testid="stVerticalBlockBorderWrapper"], [data-testid="stForm"], [data-testid="stMetric"]
{border-radius:20px !important; border:1px solid rgba(110,18,40,.28) !important; box-shadow:0 8px 28px rgba(110,18,40,.10);}
[data-testid="stForm"] {background:rgba(110,18,40,.04); padding:1.1rem;}
[data-testid="stMetric"] {background:rgba(110,18,40,.07); padding:.9rem 1.1rem;}
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div {border-radius:12px !important;}
button[role="tab"] {font-weight:700;}
/* 기본 버튼 */
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button
{border-radius:14px; font-weight:700; border:2px solid rgba(110,18,40,.35); transition:all .18s ease;}
.stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover
{transform:translateY(-2px); box-shadow:0 10px 22px rgba(110,18,40,.30); border-color:#7a1730;}
button[data-testid^="stBaseButton-primary"] {background:linear-gradient(135deg,#3a0b15,#7a1730) !important; border:none !important;}
button[data-testid^="stBaseButton-primary"], button[data-testid^="stBaseButton-primary"] * {color:#fff !important;}
/* 큰 버튼 (주간/월간/뉴스 분야) */
:is(.st-key-go_week, .st-key-go_month, [class*="st-key-news_"]) button
{height:115px; font-size:1.3rem; border:none !important; border-radius:22px; box-shadow:0 10px 26px rgba(0,0,0,.18);}
:is(.st-key-go_week, .st-key-go_month, [class*="st-key-news_"]) button, :is(.st-key-go_week, .st-key-go_month, [class*="st-key-news_"]) button *
{color:#fff !important; font-weight:800;}
:is(.st-key-go_week, .st-key-go_month, [class*="st-key-news_"]) button:hover {transform:translateY(-4px) scale(1.02);}
.st-key-go_week button {background:linear-gradient(135deg,#2a060f,#5a1022) !important;}
.st-key-go_month button {background:linear-gradient(135deg,#6d1224,#9b2239) !important;}
.st-key-news_0 button {background:linear-gradient(135deg,#3a0b15,#6d1224) !important;}
.st-key-news_1 button {background:linear-gradient(135deg,#5a1022,#8c1c34) !important;}
.st-key-news_2 button {background:linear-gradient(135deg,#2a060f,#4a0e1c) !important;}
.st-key-news_3 button {background:linear-gradient(135deg,#7a1730,#a3243f) !important;}
/* 사이드바 */
[data-testid="stSidebar"] {background:linear-gradient(180deg,#1c0509,#3a0b15 60%,#5a1022);}
[data-testid="stSidebar"] * {color:#f3efff !important;}
[data-testid="stSidebar"] [role="radiogroup"] label {padding:.55rem .8rem; border-radius:12px; margin-bottom:2px; transition:background .15s;}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {background:rgba(255,255,255,.13);}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {background:rgba(255,255,255,.24); font-weight:800;}
[data-testid="stSidebar"] button {background:rgba(255,255,255,.14) !important; border:1px solid rgba(255,255,255,.45) !important;}
/* 명언 / 태그 */
.quote {border-left:5px solid #7a1730; background:rgba(122,23,48,.10); padding:.85rem 1.2rem; border-radius:0 16px 16px 0; font-size:1.05rem; margin:.2rem 0 1.3rem;}
.tag {display:inline-block; background:rgba(110,18,40,.14); color:#7a1730; font-weight:700; font-size:.8rem; padding:.15rem .7rem; border-radius:999px;}
/* 첫 화면 */
.hero-card {text-align:center; color:#fff; padding:4.2rem 1.5rem 3.4rem; border-radius:32px; margin-bottom:1.6rem; box-shadow:0 24px 60px rgba(60,8,20,.45);
 background:radial-gradient(500px 260px at 15% 10%, rgba(255,255,255,.22), transparent), radial-gradient(420px 240px at 90% 90%, rgba(214,170,110,.30), transparent), linear-gradient(135deg,#1f0409,#4a0d1b 55%,#7a1730);}
.hero-card h1 {background:none; -webkit-text-fill-color:#fff; font-size:3.2rem; line-height:1.25; margin:.8rem 0;}
.hero-card p {font-size:1.2rem; opacity:.92; color:#fff;}
.hero-card .pill {background:#f1d9b5; -webkit-text-fill-color:#2a060f; border-radius:999px; padding:0 .6em;}
.chips span {display:inline-block; background:rgba(255,255,255,.2); border:1px solid rgba(255,255,255,.4); border-radius:999px; padding:.3rem .9rem; margin:.2rem; font-size:.9rem; font-weight:700;}
.feat {text-align:center; padding:1.4rem 1rem; border-radius:22px; border:1px solid rgba(110,18,40,.28); background:rgba(110,18,40,.06); height:100%;}
.feat .ico {font-size:2.2rem;}
/* 개성 있는 제목 글꼴: 아래 --display 한 줄만 바꾸면 전체 제목 글꼴이 바뀝니다 */
:root {--display:'The Seasons','Instrument Serif','Playfair Display',Georgia,serif;}
h1, h2, h3, .hero-card h1, .quote {font-family:var(--display) !important; font-weight:400 !important; letter-spacing:-.01em;}
h1 {font-size:3.2rem !important;}
h2 {font-size:2.2rem !important;}
h3 {font-size:1.7rem !important;}
.hero-card h1 {font-size:4.2rem !important; line-height:1.08;}
.hero-card .pill {font-style:italic;}
.quote {font-style:italic; font-size:1.4rem; line-height:1.4;}
@media (prefers-color-scheme: dark) {
 h1 {background:linear-gradient(90deg,#f3d3d9,#e08a9b); -webkit-background-clip:text; background-clip:text;}
 .tag {color:#f0a9b6;}
}
/* 부제목: Aileron 스타일 (설치돼 있으면 Aileron, 없으면 Hanken Grotesk) */
:root {--sub:'Aileron','Hanken Grotesk','Inter','Noto Sans KR',sans-serif;}
h2, h3, h4, .quote, .hero-card p, .tag {font-family:var(--sub) !important; font-style:normal !important;}
h2, h3 {font-weight:600 !important; letter-spacing:-.01em;}
h2 {font-size:1.9rem !important;}
h3 {font-size:1.45rem !important;}
.quote {font-size:1.1rem !important; font-weight:500 !important; letter-spacing:.01em; line-height:1.5;}
/* 상단 바 + 떠 있는 메뉴 창 + 로그인 창 */
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {display:none;}
.brand {font-family:var(--display); font-size:2rem; line-height:1.6; background:linear-gradient(90deg,#2a060f,#8c1c34); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;}
[data-testid="stPopover"] button {background:linear-gradient(135deg,#3a0b15,#7a1730) !important; border:none !important; border-radius:14px; font-weight:700;}
[data-testid="stPopover"] button, [data-testid="stPopover"] button * {color:#fff !important;}
[data-testid="stPopoverBody"] {border-radius:20px !important; border:1px solid rgba(110,18,40,.4) !important; box-shadow:0 24px 60px rgba(60,8,20,.40) !important; padding:.9rem;}
div[role="dialog"] {border-radius:26px !important;}
.st-key-open_auth button {height:58px; font-size:1.15rem;}
@media (prefers-color-scheme: dark) {.brand {background:linear-gradient(90deg,#f3d3d9,#e08a9b); -webkit-background-clip:text; background-clip:text;}}
</style>""", unsafe_allow_html=True)


def goto(p):
    st.session_state.page = p


def table_editor(store, key, cols, ekey):
    """표를 편집하면 자동 저장 (store[key] = [{열: 값}, ...])"""
    df = pd.DataFrame(store.get(key, []), columns=cols)
    ed = st.data_editor(df, num_rows="dynamic", hide_index=True,
                        key=f"{ekey}_{st.session_state.rev}")
    rows = [r for r in ed.fillna("").to_dict("records")
            if any(str(v).strip() for v in r.values())]
    if rows != store.get(key, []):
        store[key] = rows
        save()
        st.session_state.rev += 1
        st.rerun()


# ---------- 첫 화면 (이메일 로그인) ----------
def landing():
    st.markdown(
        '<div class="hero-card"><div class="chips"><span>📅 Daily Planner</span><span>📝 Resume</span>'
        '<span>📰 Headlines</span><span>🎯 D-day</span></div>'
        '<h1>Plan it. Track it.<br>Make it <span class="pill">stick</span>.</h1>'
        '<p>Tasks · schedules · countdowns · news — your all-in-one study planner</p></div>',
        unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    if mid.button("🚀 Get started", type="primary", key="open_auth", width="stretch"):
        auth_dialog()
    mid.caption("Log in or create an account — your data stays on this computer.")
    if not st.session_state.get("auth_seen"):
        st.session_state.auth_seen = True
        auth_dialog()
    st.write("")
    feats = [("✅", "Today's tasks", "Subjects, tasks and homework at a glance"), ("⏱️", "Study Log", "Stack up hours and see your charts"),
             ("📰", "Headlines", "News by topic, in three lines")]
    for col, (ico, t, d) in zip(st.columns(3), feats):
        col.markdown(f'<div class="feat"><div class="ico">{ico}</div><b>{t}</b><br>{d}</div>',
                     unsafe_allow_html=True)


# ---------- 1. 데일리 플래너 ----------
def page_daily():
    sub = st.session_state.get("sub")
    if sub:
        st.button("← Back to Daily Planner", key="back_daily", on_click=goto_sub, args=(None,))
        st.title(sub)
        SUBPAGES[sub][0]()
        return
    st.title("📚 Study Planner")
    st.markdown(f'<div class="quote">💬 {QUOTES[TODAY.toordinal() % len(QUOTES)]}</div>', unsafe_allow_html=True)
    wd = WEEKDAYS[TODAY.weekday()]
    iso = TODAY.isoformat()
    left, right = st.columns([3, 2])
    with left, st.container(border=True):
        st.subheader(f"Today's tasks · {TODAY:%b %d} ({wd})")
        with st.form("quick_add", clear_on_submit=True):
            c1, c2 = st.columns([1, 3])
            subj = c1.selectbox("Subject", data["subjects"], label_visibility="collapsed")
            title = c2.text_input("Task", label_visibility="collapsed",
                                  placeholder="Add today's task or homework")
            if st.form_submit_button("Add") and title:
                data["tasks"].append({"id": new_id(), "subject": subj, "title": title,
                                      "due": iso, "done": False})
                save()
                st.rerun()
        for t in tasks_on(TODAY):
            a, b = st.columns([9, 1])
            checked = a.checkbox(f"[{t['subject']}] {t['title']}", value=t["done"], key="td" + t["id"])
            if checked != t["done"]:
                t["done"] = checked
                save()
                st.rerun()
            if b.button("🗑️", key="tx" + t["id"]):
                data["tasks"].remove(t)
                save()
                st.rerun()
        notes = st.text_area("📝 Homework & notes", value=data["daily"].get(iso, ""), height=160)
        if notes != data["daily"].get(iso, ""):
            data["daily"][iso] = notes
            save()
    with right, st.container(border=True):
        st.subheader(f"Daily schedule · {wd}")
        table_editor(data["schedule"], wd, ["Time", "Plan"], "sch_" + wd)
        with st.expander("Edit other days' schedules"):
            other = st.selectbox("Day", list(WEEKDAYS), index=TODAY.weekday())
            table_editor(data["schedule"], other, ["Time", "Plan"], "sch2_" + other)
        st.caption("Saved per weekday — today's schedule shows automatically.")
    st.divider()
    render_tiles()


# ---------- 2. 이력서 ----------
def page_resume():
    st.title("📝 Resume")
    r = data.setdefault("resume", {})
    edit, view = st.tabs(["✏️ Edit", "👀 Preview"])
    with edit:
        with st.form("resume_form"):
            c1, c2 = st.columns(2)
            r["name"] = c1.text_input("Name", r.get("name", ""))
            r["school"] = c2.text_input("School / Affiliation", r.get("school", ""))
            r["contact"] = c1.text_input("Contact / Email", r.get("contact", data.get("email", "")))
            r["goal"] = c2.text_input("Goal / Career interest", r.get("goal", ""))
            r["intro"] = st.text_area("About me", r.get("intro", ""), height=140)
            r["skills"] = st.text_input("Skills (comma-separated)", r.get("skills", ""))
            if st.form_submit_button("Save", type="primary"):
                save()
                st.success("Saved!")
        st.write("**Experience & activities**")
        table_editor(r, "career", ["Period", "Role / Activity", "Details"], "res_career")
        st.write("**Awards & certificates**")
        table_editor(r, "awards", ["Date", "Title", "Issuer"], "res_awards")
    with view:
        md = f"# {r.get('name') or '(Your name)'}\n{r.get('school', '')}  \n{r.get('contact', '')}\n\n"
        md += f"**Goal** {r.get('goal', '')}\n\n## About me\n{r.get('intro', '')}\n\n"
        md += f"## Skills\n{r.get('skills', '')}\n\n## Experience & activities\n"
        md += "\n".join(f"- **{x['Period']}** {x['Role / Activity']} — {x['Details']}" for x in r.get("career", []))
        md += "\n\n## Awards & certificates\n"
        md += "\n".join(f"- {x['Date']} {x['Title']} ({x['Issuer']})" for x in r.get("awards", []))
        with st.container(border=True):
            st.markdown(md)
        st.download_button("📥 Save resume (.md)", md.encode("utf-8"), "resume.md", "text/markdown")


# ---------- 3. 뉴스 ----------
def og_image(html):
    for pat in (r'<meta[^>]+property=["\']og:image["\'][^>]*content=["\']([^"\']+)',
                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']'):
        m = re.search(pat, html)
        if m:
            return m.group(1)
    return None


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_news(cat, per_source=3):
    import feedparser
    import requests
    import trafilatura
    out = []
    for src, url in NEWS_FEEDS[cat]:
        for e in feedparser.parse(url, agent=UA).entries[:per_source]:
            img = (e.get("media_content") or e.get("media_thumbnail") or [{}])[0].get("url")
            text = ""
            try:
                html = requests.get(e.link, headers={"User-Agent": UA}, timeout=10).text
                text = trafilatura.extract(html) or ""
                img = img or og_image(html)
            except Exception:
                pass
            text = text or re.sub(r"<[^>]+>", "", e.get("summary", ""))
            sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))]
            lines = [s[:120] for s in sents if len(s) > 15][:3]
            out.append({"src": src, "title": e.get("title", ""), "link": e.link, "lines": lines, "image": img})
    return out


def page_news():
    st.title("📰 Headlines")
    art_css("news_", NEWS_ART, 130)
    cols = st.columns(len(NEWS_FEEDS))
    for i, cat in enumerate(NEWS_FEEDS):
        if cols[i].button(cat, key=f"news_{i}", width="stretch"):
            st.session_state.news_cat = cat
    cat = st.session_state.news_cat
    st.subheader(cat)
    try:
        with st.spinner("Loading news… (the first load takes a moment)"):
            items = fetch_news(cat)
    except ImportError:
        st.error("Please install first in PowerShell:  pip install feedparser requests trafilatura")
        return
    if not items:
        st.warning("Couldn't load articles. Check your internet connection or the feed URLs (NEWS_FEEDS).")
    for it in items:
        with st.container(border=True):
            c1, c2 = st.columns([1, 2])
            if it.get("image"):
                c1.image(it["image"], width="stretch")
            else:
                c1.markdown('<div style="height:150px;border-radius:14px;display:flex;align-items:center;justify-content:center;'
                            'font-size:2.6rem;background:linear-gradient(135deg,#3a0b15,#7a1730)">📰</div>', unsafe_allow_html=True)
            c2.markdown(f"<span class='tag'>{it['src']}</span>", unsafe_allow_html=True)
            c2.markdown(f"#### [{it['title']}]({it['link']})")
            for ln in it["lines"]:
                c2.markdown(f"- {ln}")
    st.caption("Summaries are the first three sentences of each article. Click a title to read the full story.")


# ---------- 화면 전환 ----------
from urllib.parse import quote


def goto_sub(name):
    st.session_state.sub = name


def tile_art(kind):
    """타일/뉴스 버튼용 일러스트(SVG). 색은 크림색 하나로 통일."""
    c = "#f1d9b5"

    def box(x, y, w, h, o, r=9):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}" opacity="{o}"/>'

    def ln(w=12):
        return f'fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'

    if kind == "week":
        s = "".join(box(40 + i * 48, 60 + (i % 3) * 14, 34, 110 - (i % 3) * 14, .95 if i == 3 else .35) for i in range(7))
    elif kind == "month":
        s = "".join(box(50 + (i % 7) * 45, 30 + (i // 7) * 38, 34, 28, .95 if i == 16 else .3, 7) for i in range(28))
    elif kind == "tasks":
        s = "".join(f'<circle cx="80" cy="{60 + i * 50}" r="16" fill="{c}" opacity="{.95 if i < 2 else .3}"/>'
                    + box(115, 52 + i * 50, 210 - i * 40, 16, .4, 8) for i in range(3))
    elif kind == "dday":
        s = (f'<circle cx="200" cy="110" r="62" {ln()} stroke-opacity=".3"/>'
             f'<circle cx="200" cy="110" r="62" {ln()} stroke-dasharray="250 400" transform="rotate(-90 200 110)"/>')
    elif kind == "log":
        s = "".join(box(60 + i * 55, 170 - h, 38, h, .95 if i == 4 else .35) for i, h in enumerate([40, 70, 55, 100, 130]))
    elif kind == "ics":
        s = box(100, 40, 150, 130, .35, 16) + box(100, 40, 150, 34, .95, 16) + f'<path d="M265 115h75m-26-26 26 26-26 26" {ln()}/>'
    elif kind == "resume":
        s = (box(120, 25, 160, 190, .35, 16) + f'<circle cx="200" cy="85" r="22" fill="{c}" opacity=".95"/>'
             + box(150, 125, 100, 12, .7, 6) + box(150, 150, 100, 12, .5, 6) + box(150, 175, 66, 12, .4, 6))
    elif kind == "politics":
        s = (f'<path d="M110 70h180L200 30z" fill="{c}" opacity=".9"/>'
             + "".join(box(125 + i * 45, 85, 24, 70, .5 if i % 2 else .9, 6) for i in range(4)) + box(100, 165, 200, 14, .9, 6))
    elif kind == "economy":
        pts = [(50, 170), (130, 120), (190, 140), (350, 45)]
        s = f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" {ln()}/>' + "".join(
            f'<circle cx="{x}" cy="{y}" r="9" fill="{c}"/>' for x, y in pts)
    elif kind == "world":
        s = (f'<circle cx="200" cy="110" r="68" {ln()}/><ellipse cx="200" cy="110" rx="28" ry="68" {ln(8)} stroke-opacity=".5"/>'
             f'<path d="M135 110h130" {ln(8)} stroke-opacity=".5"/>')
    else:
        s = box(140, 50, 120, 120, .35, 18) + box(170, 80, 60, 60, .95, 10) + "".join(
            f'<path d="M{x} 30v20M{x} 170v20" {ln(8)}/>' for x in (165, 200, 235))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240" preserveAspectRatio="xMidYMid slice">{s}</svg>'


def art_css(prefix, items, h):
    """버튼마다 그림 + 어두운 그라데이션 + 글자(왼쪽 아래) 스타일을 입혀요."""
    css = ""
    for i, (kind, c1, c2) in enumerate(items):
        uri = "data:image/svg+xml;utf8," + quote(tile_art(kind))
        k = f".st-key-{prefix}{i} button"
        css += (f'{k}{{height:{h}px;display:flex;align-items:flex-end;justify-content:flex-start;padding:1rem 1.2rem;'
                f'border:none !important;border-radius:22px;text-align:left;'
                f'background:linear-gradient(180deg,rgba(0,0,0,0) 35%,rgba(20,3,8,.85)),url("{uri}") center/cover no-repeat,'
                f'linear-gradient(135deg,{c1},{c2}) !important;}}'
                f'{k}, {k} *{{color:#fff !important;font-weight:800;font-size:1.2rem;}}')
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


NEWS_ART = [("politics", "#3a0b15", "#6d1224"), ("economy", "#5a1022", "#8c1c34"),
            ("world", "#2a060f", "#4a0e1c"), ("tech", "#7a1730", "#a3243f")]

# 이름: (화면 함수, 이모지, 그림 종류, 색1, 색2)
SUBPAGES = {
    "Weekly Planner": (page_week, "📆", "week", "#2a060f", "#5a1022"),
    "Monthly Planner": (page_month, "🗓️", "month", "#6d1224", "#9b2239"),
    "Tasks by Subject": (page_tasks, "✅", "tasks", "#3a0b15", "#6d1224"),
    "D-day": (page_dday, "🎯", "dday", "#5a1022", "#8c1c34"),
    "Study Log": (page_log, "⏳", "log", "#2a060f", "#4a0e1c"),
    "Google Calendar": (page_ics, "📤", "ics", "#7a1730", "#a3243f"),
}


def render_tiles():
    st.subheader("Planner toolkit")
    art_css("tile_", [(v[2], v[3], v[4]) for v in SUBPAGES.values()], 170)
    names = list(SUBPAGES)
    for row in (0, 3):
        for j, col in enumerate(st.columns(3)):
            n = names[row + j]
            col.button(f"{SUBPAGES[n][1]} {n}", key=f"tile_{row + j}", on_click=goto_sub, args=(n,), width="stretch")


# ---------- 계정 (이메일 + 비밀번호) ----------
def load_users():
    return json.loads(USERS_DB.read_text(encoding="utf-8")) if USERS_DB.exists() else {}


def hash_pw(pw, salt):
    return hashlib.pbkdf2_hmac("sha256", pw.encode(), bytes.fromhex(salt), 200_000).hex()


def sign_up(email, pw):
    users = load_users()
    if email in users:
        return "An account with this email already exists."
    first = not users
    salt = secrets.token_hex(16)
    users[email] = {"salt": salt, "hash": hash_pw(pw, salt)}
    if first and LEGACY_DB.exists() and not user_db(email).exists():  # 예전 데이터는 첫 계정으로 이어받기
        user_db(email).write_text(LEGACY_DB.read_text(encoding="utf-8"), encoding="utf-8")
    USERS_DB.write_text(json.dumps(users, indent=2), encoding="utf-8")
    return None


def log_in(email, pw):
    u = load_users().get(email)
    return bool(u) and hmac.compare_digest(u["hash"], hash_pw(pw, u["salt"]))


def nav(name):
    st.session_state.page = name
    st.session_state.sub = None


def enter(email):
    st.session_state.user = email
    nav("🏠 Home")
    st.rerun()


@st.dialog("Welcome to Study Planner")
def auth_dialog():
    t_in, t_up = st.tabs(["Log in", "Sign up"])
    with t_in, st.form("li_form"):
        e = st.text_input("Email", placeholder="you@example.com")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Log in", type="primary"):
            if log_in(e.strip().lower(), p):
                enter(e.strip().lower())
            else:
                st.error("Email or password is incorrect.")
    with t_up, st.form("su_form"):
        e = st.text_input("Email", placeholder="you@example.com", key="su_e")
        p1 = st.text_input("Create a password (6+ characters)", type="password", key="su_p1")
        p2 = st.text_input("Confirm password", type="password", key="su_p2")
        if st.form_submit_button("Create account", type="primary"):
            e = e.strip().lower()
            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", e):
                st.error("Please check your email format.")
            elif len(p1) < 6:
                st.error("Password must be at least 6 characters.")
            elif p1 != p2:
                st.error("Passwords don't match.")
            else:
                err = sign_up(e, p1)
                if err:
                    st.error(err)
                else:
                    enter(e)


# ---------- 홈 ----------
def page_home():
    name = esc(st.session_state.user.split("@")[0])
    st.markdown(
        f'<div class="hero-card"><div class="chips"><span>{TODAY:%A · %B %d}</span></div>'
        f'<h1>Welcome back, <span class="pill">{name}</span></h1>'
        f'<p>{QUOTES[TODAY.toordinal() % len(QUOTES)]}</p></div>', unsafe_allow_html=True)
    todays = tasks_on(TODAY)
    nxt = sorted((e for e in data["exams"] if e["date"] >= TODAY.isoformat()), key=lambda e: e["date"])
    week0 = (TODAY - timedelta(days=TODAY.weekday())).isoformat()
    mins = sum(l["minutes"] for l in data["logs"] if l["date"] >= week0)
    m1, m2, m3 = st.columns(3)
    m1.metric("Today's tasks", f"{sum(t['done'] for t in todays)}/{len(todays)} done")
    if nxt:
        d = (date.fromisoformat(nxt[0]["date"]) - TODAY).days
        m2.metric(nxt[0]["name"], "D-Day 🔥" if d == 0 else f"D-{d}")
    else:
        m2.metric("Next exam", "—")
    m3.metric("Study time this week", f"{mins / 60:.1f} h")
    st.subheader("Where to?")
    art_css("home_", [("month", "#3a0b15", "#6d1224"), ("resume", "#5a1022", "#8c1c34"),
                      ("world", "#2a060f", "#4a0e1c")], 220)
    for i, (col, n) in enumerate(zip(st.columns(3), [n for n in PAGES if n != "🏠 Home"])):
        col.button(n, key=f"home_{i}", on_click=nav, args=(n,), width="stretch")


PAGES = {"🏠 Home": page_home, "📅 Daily Planner": page_daily, "📝 Resume": page_resume, "📰 News": page_news}

if "user" not in st.session_state:
    landing()
else:
    top = st.columns([5, 1.4])
    top[0].markdown('<div class="brand">📚 Study Planner</div>', unsafe_allow_html=True)
    with top[1].popover("☰ Menu", width="stretch"):
        st.caption(st.session_state.user)
        for i, n in enumerate(PAGES):
            st.button(n, key=f"nav_{i}", on_click=nav, args=(n,), width="stretch")
        if st.button("Log out", key="logout", width="stretch"):
            for k in ("user", "data", "data_for", "sub"):
                st.session_state.pop(k, None)
            st.rerun()
    PAGES[st.session_state.page]()
