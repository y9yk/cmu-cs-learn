"""Build the dependency-free CMU CS Learn study guide from catalog.json."""
from html import escape
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent


def e(value):
    return escape(str(value), quote=True)


def link(label, url, klass=''):
    return f'<a class="{e(klass)}" href="{e(url)}">{e(label)} <span aria-hidden="true">↗</span></a>'


def route_html(route, by_id):
    parts = ''.join(
        f'<li><a href="#course-{e(i)}" data-route-course>'
        f'<span>{e(i)}</span> {e(by_id[i]["ko"])}'
        f'{" <small>예정</small>" if by_id[i]["status"] == "planned" else ""}</a></li>'
        for i in route['steps']
    )
    return (f'<article class="route"><p class="eyebrow">{e(route["label"])}</p>'
            f'<h3>{e(route["title"])}</h3><p>{e(route["description"])}</p>'
            f'<ol>{parts}</ol><p class="route-goal"><strong>남길 결과물</strong> {e(route["goal"])}</p></article>')


def course_html(c, track, official):
    key = ' '.join([c['id'], c['id'].replace('-', ''), c['title'], c['ko'], c['faculty'], c['level'],
                    track, c['summary'], c['prepare'], ' '.join(c['tags'])])
    status = 'YouTube 공개' if c['status'] == 'available' else '2027년 1월 예정'
    tags = ''.join(f'<li>{e(t)}</li>' for t in c['tags'])
    resources = [link('CS Learn에서 강의 찾기' if c['status'] == 'available' else 'CMU 공개 일정 확인', official)]
    resources.extend(link(r['label'], r['url']) for r in c['resources'])
    links = ''.join(f'<li>{a}</li>' for a in resources)
    cid = f'course-{e(c["id"])}'
    return f"""
    <article id="{cid}" class="course" tabindex="-1" aria-labelledby="{cid}-title"
      data-course data-id="{e(c['id'])}" data-track="{e(c['track'])}" data-status="{e(c['status'])}" data-keywords="{e(key)}">
      <div class="course-meta"><span class="course-id">{e(c['id'])}</span><span class="badge {e(c['status'])}">{status}</span></div>
      <h3 id="{cid}-title">{e(c['ko'])}</h3>
      <p class="en" lang="en">{e(c['title'])}</p>
      <p class="byline">{e(c['faculty'])}</p>
      <p class="summary">{e(c['summary'])}</p>
      <ul class="tags" aria-label="주제"><li class="level">{e(c['level'])}</li>{tags}</ul>
      <details><summary>독학 준비와 실습</summary><dl><dt>준비</dt><dd>{e(c['prepare'])}</dd>
      <dt>미니 실습</dt><dd>{e(c['practice'])}</dd></dl></details>
      <ul class="links" aria-label="강의 자료">{links}</ul>
      <button class="mark requires-js" type="button" data-mark aria-pressed="false">완료로 표시</button>
    </article>"""


def document(data):
    courses = data['courses']
    tracks = data['tracks']
    by_id = {c['id']: c for c in courses}
    routes = ''.join(route_html(r, by_id) for r in data['routes'])
    cards = ''.join(course_html(c, tracks[c['track']], data['source']) for c in courses)
    track_opts = ''.join(f'<option value="{e(k)}">{e(v)}</option>' for k, v in tracks.items())
    available = sum(c['status']=='available' for c in courses)
    planned = sum(c['status']=='planned' for c in courses)
    updated = e(data['checked'])
    official = link('CMU 공식 강의 목록', data['source'], 'official')
    announcement = link('CMU 출시 공지', data['announcement'])
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="카네기멜론 CS Learn 공개 강의를 찾아보고 AI 에이전트, ML 시스템, 소프트웨어 설계, 컴퓨팅 기초를 공부하는 한국어 길잡이.">
  <meta name="theme-color" content="#132b28">
  <title>CMU CS Learn · 한국어 독학 가이드</title>
  <link rel="stylesheet" href="./style.css">
  <script defer src="./study.js"></script>
</head>
<body>
  <a class="skip" href="#library">과목 목록으로 건너뛰기</a>
  <header class="mast">
    <div class="shell topbar">
      <a href="./" class="brand" aria-label="CS Learn 독학 가이드 홈"><span class="brand-icon" aria-hidden="true">⌘</span> CS Learn <span class="brand-note">독학 가이드</span></a>
      <nav aria-label="페이지"><a href="#paths">학습 경로</a><a href="#library">과목 검색</a></nav>
    </div>
    <div class="shell hero">
      <div class="hero-copy">
        <p class="eyebrow"><span class="signal"></span> Carnegie Mellon University · 비공식 학습 인덱스</p>
        <h1>CMU 컴퓨터과학,<br><span>관심 있는 과목부터.</span></h1>
        <p>강의는 CMU 원본에서, 학습 순서와 실습 아이디어는 여기서. 공개 강의와 공개 예정 과목을 한국어로 찾아보세요.</p>
        <div class="hero-actions"><a class="cta" href="#library">과목 찾아보기 <span aria-hidden="true">↓</span></a>{official}</div>
      </div>
      <aside class="snapshot" aria-label="과목 공개 현황">
        <span class="eyebrow">공개 현황</span>
        <dl><div><dt>YouTube 공개</dt><dd>{available:02}</dd></div>
        <div><dt>2027년 1월 예정</dt><dd>{planned:02}</dd></div>
        <div><dt>추천 학습 경로</dt><dd>{len(data['routes']):02}</dd></div></dl>
        <p>공식 목록 확인 · <time datetime="{updated}">{updated}</time></p>
      </aside>
    </div>
  </header>
  <main class="shell">
    <section id="paths" aria-labelledby="paths-title">
      <div class="section-title"><p class="eyebrow">01 / ROADMAP</p><h2 id="paths-title">어디부터 볼까요?</h2><p>목표에 맞는 첫 과목을 고르세요. 순서는 학습용 추천이며 CMU의 공식 선수과목이 아닙니다.</p></div>
      <div class="routes">{routes}</div>
    </section>
    <section id="library" aria-labelledby="library-title">
      <div class="section-title"><p class="eyebrow">02 / CATALOG</p><h2 id="library-title">과목 라이브러리</h2><p>한·영 과목명, 코드, 교수진, 주제 키워드로 검색하세요.</p></div>
      <form id="filters" class="requires-js" role="search" aria-label="과목 검색 및 필터">
        <label class="search">과목 검색<input type="search" name="q" placeholder="예: 11-768, 서빙, software" autocomplete="off"></label>
        <label>주제<select name="track"><option value="all">전체</option>{track_opts}</select></label>
        <label>공개 상태<select name="status"><option value="all">전체</option><option value="available">YouTube 공개</option><option value="planned">공개 예정</option></select></label>
        <label>학습 상태<select name="progress"><option value="all">전체</option><option value="open">미완료</option><option value="done">완료</option></select></label>
        <button class="clear" type="button" data-reset>초기화</button>
      </form>
      <p id="result-count" aria-live="polite">{len(courses)}개 과목</p>
      <p id="storage-note" hidden>이 브라우저가 저장 공간에 접근할 수 없어 체크 표시를 새로고침 후에는 유지할 수 없습니다.</p>
      <p class="storage requires-js">완료 체크는 이 브라우저에만 저장되며 외부로 전송되지 않아요.</p>
      <noscript><p>이 환경에서는 검색과 완료 체크를 쓸 수 없지만, 아래 전체 목록과 강의 링크는 그대로 이용할 수 있어요.</p></noscript>
      <div class="empty" id="empty" hidden><h3>검색 결과가 없어요</h3><p>키워드를 줄이거나 필터를 초기화해 보세요.</p><button class="clear" type="button" data-reset>검색·필터 초기화</button></div>
      <div class="courses">{cards}</div>
    </section>
  </main>
  <footer><div class="shell footer-inner">
    <div><strong>CMU CS Learn · 한국어 독학 가이드</strong><p>CMU와 별개인 비공식 정리입니다. 소개·준비·실습은 독학용 제안이며 강의 영상·슬라이드·자막은 재배포하지 않습니다. CMU의 자가 학습 교재와 AI 튜터는 공식 안내상 별도 공개 예정입니다.</p></div>
    <div class="foot-links">{official}{announcement}<a href="#library">과목 목록 ↑</a></div>
  </div></footer>
</body>
</html>
"""


def main():
    data = json.loads((BASE / 'catalog.json').read_text(encoding='utf-8'))
    html = document(data)
    out = BASE / 'docs' / 'index.html'
    if sys.argv[1:] == ['--check']:
        if not out.exists() or out.read_text(encoding='utf-8') != html:
            raise SystemExit('docs/index.html을 다시 생성하세요: python3 build.py')
    elif not sys.argv[1:]:
        out.write_text(html, encoding='utf-8')
    else:
        raise SystemExit('usage: python3 build.py [--check]')


if __name__ == '__main__':
    main()
