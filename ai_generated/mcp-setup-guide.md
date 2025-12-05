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

> MCP 처음 사용 시 OAuth 인증 필요, 토큰 만료 시 재인증 (브라우저 인증 창 자동 열림)

---

## DataHub

```bash
claude mcp add datahub \
  -e DATAHUB_GMS_URL="https://your-datahub.com/api/gms" \
  -e DATAHUB_GMS_TOKEN="your-token" \
  -s user \
  -- mcp-server-datahub
```

### 사전 준비

1. `pip install mcp-server-datahub`
2. DataHub 설정 > Access Tokens에서 Personal Access Token 발급

### 동작 원리

1. Claude Code 시작 시 `mcp-server-datahub` 프로세스 **자동 실행**
2. 환경변수의 GMS URL과 토큰으로 DataHub 서버에 직접 연결
3. Claude Code 세션 종료 시 프로세스도 함께 종료

---

## Slack

(TODO)
