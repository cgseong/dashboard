# 🛡 해커톤 GitHub 활동 대시보드 (dashboard 레포)

이 레포는 교수/TA가 여러 학생 팀의 GitHub 활동을 한눈에 모니터링하기 위한 **정적 대시보드**를 제공합니다.  
각 팀 레포에서 Repobeats·커밋 정보를 생산하고, 이 레포에서 CSV + HTML로 종합해 보여줍니다.

---

## 구조 개요

- `index.html`  
  - `teams.csv`를 읽어 각 팀 카드(팀명, 표절 점수, 커밋 수, Repobeats 그래프)를 렌더링하는 대시보드 페이지입니다.
  - GitHub Pages에서 호스팅해 교수/TA가 브라우저로 바로 접근합니다.

- `teams.csv`  
  - 팀 메타데이터와 평가 지표를 담는 데이터 소스입니다.
  - 주요 컬럼:
    - `name` : 팀명
    - `id` : GitHub owner (사용자/조직)
    - `repo` : 레포 이름
    - `plagScore` : 표절 점수 (0–100)
    - `similarWith` : 유사 코드가 발견된 팀/레포
    - `commits` : 지정된 기간 동안의 총 커밋 수

- `scripts/update_commits.py`  
  - GitHub REST API를 사용해 각 팀 레포의 커밋 수를 집계하고, `teams.csv`의 `commits` 컬럼을 자동으로 갱신합니다.

- `.github/workflows/update-commits.yml`  
  - 위 스크립트를 주기적으로 실행하는 GitHub Actions 워크플로우입니다.
  - 매일 정해진 시각 또는 수동 실행으로 `teams.csv`를 업데이트합니다.

---

## GitHub Pages 설정

1. 이 레포의 **Settings → Pages**로 이동합니다.
2. Source에서 `Deploy from a branch` 선택.
3. Branch: `main` / `/ (root)` 선택 후 저장.
4. 몇 분 후 다음과 같은 URL에서 대시보드를 확인할 수 있습니다.

```text
https://<username>.github.io/dashboard/
