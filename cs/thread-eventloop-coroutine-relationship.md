# 스레드, 이벤트 루프, 코루틴의 관계

## 계층 구조

```
프로세스 (1개)
    │
    ├── 스레드 (N개)              ← OS가 관리
    │       │
    │       └── 이벤트 루프 (0~1개)   ← 앱이 관리
    │               │
    │               └── 코루틴 (N개)  ← 이벤트 루프가 관리
```

---

## 관계 요약

| 관계 | 비율 | 설명 |
|------|------|------|
| 스레드 : 이벤트 루프 | **1 : 0~1** | 스레드에 이벤트 루프가 있거나 없음 |
| 이벤트 루프 : 코루틴 | **1 : N** | 하나의 이벤트 루프가 여러 코루틴 관리 |

---

## 스레드 : 이벤트 루프 = 1 : 0~1

### 공식 문서 근거

**Python 공식 문서**:
> The policy object gets and sets a separate event loop per _context_. **This is per-thread by default.**

정책 객체는 컨텍스트별로 별도의 이벤트 루프를 설정한다. **기본적으로 이것은 스레드 단위이다.**

**출처**: https://docs.python.org/3/library/asyncio-policy.html

### 이벤트 루프가 있는 스레드 vs 없는 스레드

```
┌─────────────────────────────────────────────────────────┐
│                       프로세스                           │
│                                                         │
│   ┌─────────────────────────────────────────────────┐   │
│   │              스레드 1 (이벤트 루프 있음)          │   │
│   │                                                 │   │
│   │   ┌─────────────────────────────────────────┐   │   │
│   │   │            이벤트 루프                   │   │   │
│   │   │   코루틴1  코루틴2  코루틴3              │   │   │
│   │   └─────────────────────────────────────────┘   │   │
│   └─────────────────────────────────────────────────┘   │
│                                                         │
│   ┌─────────────────────────────────────────────────┐   │
│   │              스레드 2 (이벤트 루프 없음)          │   │
│   │                                                 │   │
│   │           일반 동기 코드 실행                    │   │
│   │           (ThreadPoolExecutor 워커 등)          │   │
│   └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 언제 이벤트 루프가 있나?

| 스레드 종류 | 이벤트 루프 | 이유 |
|------------|------------|------|
| asyncio 사용 스레드 | 있음 | 여러 코루틴을 동시에 관리 |
| ThreadPoolExecutor 워커 | 없음 | 단일 블로킹 작업만 실행 |
| 일반 threading.Thread | 없음 | 동시성 관리 불필요 |

```python
# 이벤트 루프 없음
def main():
    print("Hello")
    time.sleep(1)
main()

# 이벤트 루프 있음 (asyncio.run()에서 생성)
async def main():
    await asyncio.sleep(1)
asyncio.run(main())
```

---

## 이벤트 루프 : 코루틴 = 1 : N

### 공식 문서 근거

**Python 공식 문서**:
> The event loop contains **a collection of jobs to be run**. The event loop takes a job from its backlog of work and invokes it.

이벤트 루프는 **실행할 작업들의 모음**을 가지고 있다. 이벤트 루프는 대기 중인 작업을 가져와 실행한다.

**출처**: https://docs.python.org/3/howto/a-conceptual-overview-of-asyncio.html

### 역할 분담

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   이벤트 루프 (스케줄러)                                 │
│   ─────────────────────                                 │
│   - 누가 실행될지 결정                                   │
│   - I/O 이벤트 감시                                     │
│   - 작업 대기열 관리                                     │
│   - 직접 "일"을 하지 않음                                │
│                                                         │
│         │                                               │
│         ▼                                               │
│                                                         │
│   코루틴 (Worker)                                        │
│   ───────────────                                       │
│   - 실제 비즈니스 로직 수행                              │
│   - await에서 제어권 반환                                │
│   - 이벤트 루프에 의해 실행됨                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 실행 흐름

```python
async def worker(name):
    print(f"{name}: 작업 시작")
    await asyncio.sleep(1)  # ← 이벤트 루프에 제어권 반환
    print(f"{name}: 작업 완료")

async def main():
    await asyncio.gather(worker("A"), worker("B"), worker("C"))
```

```
이벤트 루프: worker A 실행
worker A: "작업 시작" 출력, await에서 양보
이벤트 루프: worker B 실행
worker B: "작업 시작" 출력, await에서 양보
이벤트 루프: worker C 실행
worker C: "작업 시작" 출력, await에서 양보
이벤트 루프: (1초 후) sleep 완료 이벤트 감지
이벤트 루프: worker A 재개
worker A: "작업 완료" 출력
...
```

---

## 관리 주체 비교

| 개념 | 관리 주체 | 스케줄링 방식 |
|------|----------|--------------|
| 스레드 | OS (커널) | 선점형 |
| 이벤트 루프 | 앱 (라이브러리) | - |
| 코루틴 | 이벤트 루프 | 협력형 |

### 선점형 vs 협력형

**스레드 (선점형)**:
```python
def task():
    x = 0
    for i in range(1000000):
        x += 1  # ← OS가 여기서 갑자기 전환할 수 있음
    return x
```

**코루틴 (협력형)**:
```python
async def task():
    x = 0
    for i in range(1000000):
        x += 1  # ← 여기서는 절대 전환 안됨
    await something()  # ← 오직 여기서만 전환
    return x
```

---

## 비유로 이해하기

```
회사 (프로세스)
    │
    ├── 부서 (스레드)                    ← 회사가 관리
    │       │
    │       └── 부서장 (이벤트 루프)      ← 부서 내 관리자
    │               │
    │               └── 직원들 (코루틴)   ← 부서장이 업무 배분
```

- **부서 (스레드)**: 독립적인 작업 공간
- **부서장 (이벤트 루프)**: 직원들에게 업무 배분, 일 안 함
- **직원 (코루틴)**: 실제 업무 수행, 막히면 부서장에게 보고

---

## 왜 이런 구조인가?

### 이벤트 루프가 필요한 이유: I/O 동시성

```
1만 개의 네트워크 연결을 처리하려면?

방법 1: 스레드 1만 개 → 메모리 폭발 (스레드당 ~MB)
방법 2: 이벤트 루프 + epoll/kqueue → 단일/소수 스레드로 처리 가능
```

→ **I/O 동시성**을 효율적으로 처리하기 위해 이벤트 루프 필요 (Python, Go 둘 다)

### Python이 이벤트 루프를 명시적으로 노출하는 이유

**PEP 3156**:
> "The event loop is **the place where most interoperability occurs**."

asyncio 등장 전, 이미 여러 비동기 프레임워크가 존재:
- Twisted (2002~) - 자체 이벤트 루프
- Tornado (2009~) - 자체 이벤트 루프
- Qt/PyQt - 자체 이벤트 루프

→ 기존 **비동기 프레임워크들과 호환**되도록 이벤트 루프를 **교체 가능(pluggable)**하게 설계

**출처**: https://peps.python.org/pep-3156/

---

## Go와의 비교

### 핵심: Go도 내부적으로 이벤트 루프(epoll/kqueue)를 사용한다

**Dave Cheney (Go 핵심 기여자)**:
> "Go's scheduler **acts a lot like the main loop in an event-driven server**."

**출처**: https://dave.cheney.net/2015/08/08/performance-without-the-event-loop

### 차이점: 노출 방식

| 구분 | Python | Go |
|------|--------|-----|
| epoll/kqueue 사용 | ✅ 사용 | ✅ 사용 |
| 개발자에게 노출 | **명시적** (`async/await`) | **숨겨져 있음** |
| 코드 스타일 | 비동기 스타일 | 동기 스타일 |
| 이벤트 루프 교체 | 가능 (pluggable) | 불가 (런타임 내장) |

```python
# Python - 개발자가 비동기임을 명시
async def fetch():
    response = await aiohttp.get(url)
    return response
```

```go
// Go - 동기처럼 작성, 런타임이 알아서 처리
func fetch() {
    response := http.Get(url)  // 내부적으로 epoll 사용
    return response
}
```

---

## 참고 자료

- Python asyncio Policy: https://docs.python.org/3/library/asyncio-policy.html
- Python Conceptual Overview: https://docs.python.org/3/howto/a-conceptual-overview-of-asyncio.html
- Python asyncio-dev: https://docs.python.org/3/library/asyncio-dev.html
- Go Concurrency Patterns: https://go.dev/talks/2012/concurrency.slide
