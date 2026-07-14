# 01. Git

# 1\. GitHub Flow
*   GitHub Flow 전략으로 진행

| Branch | 설명 |  |
| ---| ---| --- |
| main | 항상 배포 가능한 최신 코드 |  |
| feature/\* 또는 이슈번호-작업내용 | 기능/이슈 단위 브랜치(main 에서 분기 > main 으로 PR) |  |

# 2\. Git Worktree
*   새로운 기능을 추가할 때는 다음과 같이 새로운 branch 를 추가하여 진행

```bash
git worktree add -b <새브랜치명> <경로> <기준브랜치>

# Example
git worktree add -b feature-<기능명> ../feature/<기능명> develop
```

*   이후 개발이 완료되면 main branch 에 merge 를 수행하해당 worktree 는 제거

```bash
# Example

# main branch 로 이동
git checkout main

# merge 수행
git merge feature-<기능>

# 원격저장소 push
git push origin main
```

# 참고 자료
*   [https://velog.io/@kw2577/Git-branch-%EC%A0%84%EB%9E%B5](https://velog.io/@kw2577/Git-branch-%EC%A0%84%EB%9E%B5)
*   [https://okbear3.tistory.com/73](https://okbear3.tistory.com/73)