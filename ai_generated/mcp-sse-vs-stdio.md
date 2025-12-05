# MCP 통신 방식: SSE vs stdio 비교

Claude Code에서 MCP(Model Context Protocol) 서버와 통신하는 두 가지 방식을 비교합니다.

---

## stdio (Standard Input/Output)

```
Claude Code ←→ [stdin/stdout] ←→ 로컬 프로세스
```

### 특징
- **로컬에서 프로세스를 직접 실행**
- Claude Code가 `npx slack-mcp-server` 같은 명령어를 실행
- 표준 입출력(stdin/stdout)으로 JSON 메시지 주고받음
- 프로세스가 Claude Code와 함께 시작/종료됨

### 설정 예시

```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "slack-mcp-server@latest"],
  "env": { "SLACK_MCP_XOXP_TOKEN": "xoxp-..." }
}
```

### CLI 추가 명령어

```bash
claude mcp add slack \
  -e SLACK_MCP_XOXP_TOKEN="xoxp-..." \
  -s user \
  -- npx -y slack-mcp-server@latest
```

---

## SSE (Server-Sent Events)

```
Claude Code ←→ [HTTP/SSE] ←→ 원격 서버
```

### 특징
- **원격 서버에 HTTP로 연결**
- 서버가 이미 실행 중이어야 함
- SSE로 실시간 스트리밍 응답 수신
- OAuth 인증 지원 (Atlassian처럼)

### 설정 예시

```json
{
  "type": "sse",
  "url": "https://mcp.atlassian.com/v1/sse"
}
```

### CLI 추가 명령어

```bash
claude mcp add atlassian \
  --transport sse \
  --url "https://mcp.atlassian.com/v1/sse" \
  -s user
```

---

## 비교표

| 구분 | stdio | SSE |
|------|-------|-----|
| 실행 위치 | 로컬 | 원격 서버 |
| 프로세스 관리 | Claude Code가 관리 | 서버가 관리 |
| 인증 | 환경변수로 토큰 전달 | OAuth 등 지원 |
| 설치 | npm 패키지 필요 | 불필요 |
| 네트워크 | 불필요 (로컬) | 필요 |
| 예시 | Slack, DataHub | Atlassian |

---

## 언제 어떤 방식을 사용하나?

- **stdio**: 오픈소스 MCP 서버를 직접 실행할 때 (대부분의 경우)
- **SSE**: 벤더가 호스팅하는 MCP 서버에 연결할 때 (Atlassian, 회사 내부 서버 등)

---

## 참고: CLI 옵션

| 옵션 | 설명 |
|------|------|
| `-s user` | 전역(user) 범위로 저장 (`~/.claude.json`) |
| `-s project` | 프로젝트 범위로 저장 (`.mcp.json`) |
| `-e KEY=VALUE` | 환경변수 설정 |
| `--transport sse` | SSE 방식 지정 (기본값은 stdio) |
| `--` | 이후는 실행할 명령어와 인자 |
