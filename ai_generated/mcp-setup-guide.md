# MCP 설정 가이드

Claude Code에서 MCP 서버를 연결하는 방법을 정리합니다.

---

## Atlassian (Confluence, Jira)

```bash
claude mcp add atlassian --transport sse --url "https://mcp.atlassian.com/v1/sse" -s user
```

### 동작 원리

1. `mcp.atlassian.com`은 Atlassian이 운영하는 **중앙 프록시 서버**
2. OAuth 로그인 시 발급된 토큰에 **워크스페이스 정보와 권한**이 포함됨
3. Claude Code가 요청하면, 중앙 서버가 토큰을 보고 **해당 워크스페이스로 라우팅**
4. 별도 서버 설치 없이 OAuth 인증만으로 접근 가능

---

## DataHub

(TODO)

---

## Slack

(TODO)
