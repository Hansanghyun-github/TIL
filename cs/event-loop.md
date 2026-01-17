# 이벤트 루프 (Event Loop)

## 정의

### 일반적 정의 (컴퓨터 과학)

> An event loop is **a programming construct or design pattern** commonly used in event-driven software. It allows a program to handle asynchronous events and operations by repeatedly checking for and dispatching events or messages in a loop.

이벤트 루프는 이벤트 기반 소프트웨어에서 일반적으로 사용되는 **프로그래밍 구조 또는 디자인 패턴**이다. 루프에서 이벤트나 메시지를 반복적으로 확인하고 디스패치하여 비동기 이벤트와 작업을 처리한다.

**출처**: https://en.wikipedia.org/wiki/Event_loop

### Python 공식 문서 정의

> **The event loop is the core of every asyncio application.** Event loops run asynchronous tasks and callbacks, perform network IO operations, and run subprocesses.

**이벤트 루프는 모든 asyncio 애플리케이션의 핵심이다.** 이벤트 루프는 비동기 태스크와 콜백을 실행하고, 네트워크 I/O 작업을 수행하며, 서브프로세스를 실행한다.

**출처**: https://docs.python.org/3/library/asyncio-eventloop.html

### Python 개념적 설명

> **Everything in asyncio happens relative to the event loop.** It's the star of the show. It's like an orchestra conductor. It's behind the scenes managing resources.

**asyncio의 모든 것은 이벤트 루프를 중심으로 일어난다.** 이벤트 루프는 쇼의 주인공이다. **오케스트라 지휘자**와 같다. 무대 뒤에서 자원을 관리한다.

**출처**: https://docs.python.org/3/howto/a-conceptual-overview-of-asyncio.html

### Node.js 공식 문서 정의

> It presents an event loop **as a runtime construct instead of as a library**. This behavior is like browser JavaScript — the event loop is hidden from the user.

이벤트 루프를 라이브러리가 아닌 **런타임 구조물**로 제공한다. 이 동작은 브라우저 JavaScript와 같다 — 이벤트 루프는 사용자에게 숨겨져 있다.

**출처**: https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick

---

## 핵심 특징

### 1. 스케줄러 역할

이벤트 루프는 **Worker가 아니라 스케줄러**다.

| 개념 | 역할 | 비유 |
|------|------|------|
| 이벤트 루프 | 스케줄러 (관리자) | 공장 관리자, 오케스트라 지휘자 |
| 코루틴 | Worker (일꾼) | 공장 노동자, 연주자 |

```
이벤트 루프:
  "A야, 네 차례야. 일해."
  "A가 I/O 기다린다고? 알겠어, 대기."
  "B야, 네 차례야. 일해."
  "A한테 응답 왔네. A야, 다시 일해."
```

### 2. 동작 방식

```
┌─────────────────────────────────────┐
│           이벤트 루프                │
│                                     │
│  1. 이벤트 대기 (I/O, 타이머 등)     │
│            ↓                        │
│  2. 이벤트 발생 → 핸들러 실행        │
│            ↓                        │
│  3. 1번으로 돌아감 (무한 반복)       │
│                                     │
└─────────────────────────────────────┘
```

**의사 코드**:
```python
while True:                      # 무한 루프
    event = wait_for_event()     # 이벤트 대기
    handler = get_handler(event) # 해당 핸들러 찾기
    handler()                    # 핸들러 실행
```

### 3. 범용적인 디자인 패턴

이벤트 루프는 **특정 언어의 개념이 아니라 컴퓨터 과학의 범용 디자인 패턴**이다.

| 분야 | 예시 |
|------|------|
| GUI 프레임워크 | Windows Message Loop, macOS Run Loop, Java Swing |
| 웹 브라우저 | JavaScript Event Loop |
| 서버 | Node.js, Nginx, Python asyncio |
| 모바일 | iOS, Android UI 스레드 |

### 4. 명시적 vs 암시적

| 언어/환경 | 이벤트 루프 | 설명 |
|----------|------------|------|
| JavaScript (브라우저) | 암시적 | 개발자가 직접 다루지 않음 |
| Node.js | 암시적 | 내장, 자동 실행 |
| Python asyncio | **명시적** | `asyncio.run()` 호출 필요 |
| Java Swing | 암시적 | EDT가 자동 관리 |

---

## 역사

| 연도 | 사건 |
|------|------|
| 1965 | Multics 프로젝트 - 인터럽트 기반 I/O로 비동기 이벤트 처리 기초 |
| 1973 | Xerox Alto - 최초의 GUI 기반 이벤트 루프 구현 |
| 1980s | 윈도우 시스템에서 GUI 상호작용을 위해 보편화 |

**출처**: https://en.wikipedia.org/wiki/Event_loop

---

## 스레드와의 관계

### 기본 관계: 1 : 0~1

**Python 공식 문서**:
> The policy object gets and sets a separate event loop per _context_. **This is per-thread by default.**

정책 객체는 컨텍스트별로 별도의 이벤트 루프를 설정한다. **기본적으로 이것은 스레드 단위이다.**

**출처**: https://docs.python.org/3/library/asyncio-policy.html

```
스레드 1개  :  이벤트 루프 0~1개

┌─────────────────────────────────────┐
│              스레드                  │
│                                     │
│   이벤트 루프가 있을 수도 있고       │
│   없을 수도 있음                     │
│                                     │
└─────────────────────────────────────┘
```

### 이벤트 루프가 없는 스레드

| 스레드 종류 | 이벤트 루프 | 용도 |
|------------|------------|------|
| asyncio 사용 스레드 | 있음 | 코루틴 스케줄링 |
| ThreadPoolExecutor 워커 | 없음 | 블로킹 I/O 실행 |
| 일반 threading.Thread | 없음 | 동기 코드 실행 |

```python
# 이벤트 루프 없음 - 일반 Python 프로그램
def main():
    print("Hello")
    time.sleep(1)

main()

# 이벤트 루프 있음 - asyncio 사용할 때만
async def main():
    await asyncio.sleep(1)

asyncio.run(main())  # ← 여기서 이벤트 루프 생성
```

---

## 코루틴과의 관계

### 기본 관계: 1 : N

```
이벤트 루프 1개  :  코루틴 N개

┌─────────────────────────────────────┐
│            이벤트 루프               │
│                                     │
│   코루틴1  코루틴2  코루틴3  ...     │
│                                     │
└─────────────────────────────────────┘
```

**Python 공식 문서**:
> The event loop contains **a collection of jobs to be run**. The event loop takes a job from its backlog of work and invokes it. Once it pauses or completes, **it returns control to the event loop**, which then selects another job.

이벤트 루프는 **실행할 작업들의 모음**을 가지고 있다. 작업이 일시 중지되거나 완료되면, **이벤트 루프에 제어권을 반환**하고, 이벤트 루프는 다른 작업을 선택한다.

**출처**: https://docs.python.org/3/howto/a-conceptual-overview-of-asyncio.html

---

## 전체 계층 구조

```
프로세스 (1개)
    │
    ├── 스레드 (N개)              ← OS가 관리
    │       │
    │       └── 이벤트 루프 (0~1개)   ← 앱이 관리 (asyncio 사용 시)
    │               │
    │               └── 코루틴 (N개)  ← 이벤트 루프가 관리
```

---

## Go는 왜 이벤트 루프를 사용하지 않나?

### Python: GIL 때문에 이벤트 루프 필요

**Python 공식 문서**:
> **Due to the GIL**, asyncio.to_thread() can typically only be used to make IO-bound functions non-blocking.

**GIL 때문에**, 멀티스레딩이 제한적 → 단일 스레드에서 동시성 달성을 위해 이벤트 루프 사용

**출처**: https://docs.python.org/3/library/asyncio-dev.html

### Go: GIL 없음, 런타임 스케줄러 사용

**Go 공식 문서**:
> Goroutines are **multiplexed dynamically onto threads** as needed. The approach yields: **No locks. No condition variables. No callbacks.**

고루틴은 필요에 따라 **스레드에 동적으로 다중화**된다. 결과: **락 없음. 조건 변수 없음. 콜백 없음.**

**출처**: https://go.dev/talks/2012/concurrency.slide

| 언어 | GIL | 동시성 모델 |
|------|-----|------------|
| Python | 있음 | 이벤트 루프 + async/await |
| Go | 없음 | 런타임 스케줄러 + goroutine |

---

## 참고 자료

- Wikipedia - Event loop: https://en.wikipedia.org/wiki/Event_loop
- Python asyncio Event Loop: https://docs.python.org/3/library/asyncio-eventloop.html
- Python Conceptual Overview: https://docs.python.org/3/howto/a-conceptual-overview-of-asyncio.html
- Node.js Event Loop: https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick
- Go Concurrency Patterns: https://go.dev/talks/2012/concurrency.slide
