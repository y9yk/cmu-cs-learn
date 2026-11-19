# CMU CS Learn · 한국어 독학 가이드

카네기멜론에서 공개하는 컴퓨터과학 강의를 관심 분야와 학습 목표에 맞춰 찾는 비공식 인덱스입니다. 2026-11-19에 [CMU 공식 강의 목록](https://www.cs.cmu.edu/learn/)을 확인했습니다. YouTube 공개 과목 8개와 2027년 1월 공개 예정 과목 5개를 구분했습니다. 영상을 무료로 보는 것과 정규 수강·인증은 별개이며, 자가 학습 교재와 AI 튜터는 공식 안내상 이후 공개 예정입니다.

## 추천 학습 경로

| 목표 | 추천 순서 | 남길 결과물 |
| --- | --- | --- |
| AI 에이전트를 만들고 운영하기 | 11-768 AI Agents → 17-645 ML in Production → 15-442 ML Systems | 읽기 전용 에이전트의 평가 케이스, 운영 지표, 서빙 지연 비교 |
| 백엔드 설계·테크 리드 | 17-214 Software Construction → 17-635 Software Architectures → 17-643 Quality Management | 아키텍처 결정 기록 하나와 릴리스 체크리스트 |
| 컴퓨터과학·ML 기초 새로 시작 | 15-110 Computing → 15-259 Probability → 07-280 AI and ML I → 10-605 Large Datasets | 기초 Python 연습 후 작은 데이터로 기준 모델과 검증 결과 재현 |

위 순서와 실습 아이디어는 독학용 제안입니다. 공식 선수 조건은 각 강의계획서를 참고하세요. 아직 공개 전인 과목은 연습만 먼저 하거나 공개 후 이어갈 수 있습니다.

## 과목 색인

### YouTube 공개 · 8개

- **11-768** AI Agents · [강의진 과목 사이트](https://www.cmu-agents.com/)
- **17-645** Machine Learning in Production · [강의진 과목·교재](https://mlip-cmu.github.io/)
- **15-442** Machine Learning Systems · [강의진 과목 사이트](https://mlsyscourse.org/)
- **17-635** Software Architectures · [CMU 공개 강의 목록](https://www.cs.cmu.edu/learn/)
- **17-214** Principles of Software Construction · [강의진 봄 학기 보충 자료](https://cmu-17-214.github.io/s2026/)
- **17-643** Quality Management · [CMU 공개 강의 목록](https://www.cs.cmu.edu/learn/)
- **10-605** Machine Learning with Large Datasets · [강의진 과목 사이트](https://10605.github.io/)
- **15-110** Principles of Computing · [CMU 강의계획서](https://www.cs.cmu.edu/~15110/syllabus.html)

### 2027년 1월 공개 예정 · 5개

- **15-259** Probability and Computing
- **11-777** Multimodal Machine Learning · [가을 학기 보충 자료](https://multicomp.cs.cmu.edu/mmml-course/fall2026/)
- **07-280** AI and Machine Learning I
- **17-619** Product Management Essentials
- **17-627** Requirements for Embedded Systems

## 검색 페이지 사용

`docs/index.html`을 브라우저로 열거나, 저장소 루트에서 `python3 -m http.server 8000 --directory docs` 실행 후 `http://localhost:8000`을 여세요. 한·영 과목명, 과목 코드, 교수와 주제를 검색할 수 있고 주제·공개 상태·완료 상태도 함께 거를 수 있습니다. 완료 표시는 저장을 허용한 같은 브라우저에만 남습니다. 계정, 서버, 분석 도구에 학습 기록을 보내지 않습니다.

GitHub Pages를 켜려면 저장소 **Settings → Pages → Deploy from a branch → main → /docs → Save**를 선택하세요. 설정 방식은 [GitHub 공식 문서](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)를 참고하세요.

## 목록 유지보수

`catalog.json`이 기본 데이터입니다. 공식 목록에서 공개 상태와 링크를 확인한 다음 이 파일을 수정하고 `python3 build.py`를 실행해 `docs/index.html`을 갱신하세요. 링크가 강의진의 정규 학기 자료라면 CS Learn 영상과 구분해 표시합니다. 글과 미니 실습은 별도 작성했으며 영상·슬라이드·자막을 복제하지 않습니다.

```sh
python3 build.py --check
python3 -m unittest discover -s tests
node --test tests/search.test.cjs
```
