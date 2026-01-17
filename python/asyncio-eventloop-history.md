# asyncio와 이벤트 루프: 왜 개발자가 관리할 수 있게 됐나?

## 핵심 요약

Python의 asyncio는 이벤트 루프를 **교체 가능(pluggable)**하게 설계했다. 이유는 **기존 비동기 프레임워크(Twisted, Tornado)와의 호환성** 때문이다.

---

## asyncio 등장 전: 각자의 이벤트 루프

### 2012년 이전 상황

| 프레임워크 | 등장 연도 | 이벤트 루프 |
|-----------|----------|------------|
| Twisted | 2002 | Reactor |
| Tornado | 2009 | IOLoop |
| gevent | 2009 | libev 기반 Hub |
| Qt/PyQt | - | QEventLoop |

각 프레임워크가 **자체 이벤트 루프**를 가지고 있었다.

### Twisted - Reactor

**Twisted 공식 문서**:
> "**The reactor is the core of the event loop within Twisted** – the loop which drives applications using Twisted."

```python
# Twisted 방식
from twisted.internet import reactor

reactor.callLater(1, callback)
reactor.run()  # ← Twisted 자체 이벤트 루프
```

**출처**: https://docs.twisted.org/en/stable/core/howto/reactor-basics.html

### Tornado - IOLoop

**Tornado 공식 문서**:
> "An **I/O event loop** for non-blocking sockets."

```python
# Tornado 방식
from tornado.ioloop import IOLoop

IOLoop.current().call_later(1, callback)
IOLoop.current().start()  # ← Tornado 자체 이벤트 루프
```

**출처**: https://www.tornadoweb.org/en/stable/ioloop.html

### 문제: 호환 불가

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Twisted 앱                    Tornado 앱                  │
│   ───────────                   ───────────                 │
│   reactor.run()                 IOLoop.start()              │
│        ↓                             ↓                      │
│   ┌──────────────┐             ┌──────────────┐             │
│   │   Reactor    │             │   IOLoop     │             │
│   │ (이벤트 루프) │             │ (이벤트 루프) │             │
│   └──────────────┘             └──────────────┘             │
│                                                             │
│   완전히 별개! 서로 호환 안 됨!                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

Twisted 앱에서 Tornado 라이브러리를 쓰려면? **안 됨**. 서로 다른 이벤트 루프를 사용하기 때문.

---

## 왜 두 이벤트 루프가 공존할 수 없나?

### 이벤트 루프는 무한 루프

```python
# 이벤트 루프의 본질
while True:                      # 무한 루프
    event = wait_for_event()     # 이벤트 대기
    handler = get_handler(event)
    handler()                    # 핸들러 실행
```

하나의 이벤트 루프가 실행 중이면, **제어권을 내놓지 않아서** 다른 루프를 시작할 수 없다.

### 실제 에러

```python
import asyncio

async def nested_attempt():
    # 이미 이벤트 루프가 실행 중인 상태에서
    asyncio.run(another_coroutine())  # 새 루프 시작 시도

asyncio.run(nested_attempt())
```

```
❌ RuntimeError: asyncio.run() cannot be called from a running event loop
```

**한 스레드에서 이벤트 루프는 동시에 하나만 실행 가능하다.** (여러 개 생성은 가능, 동시 실행만 불가)

---

## asyncio 등장 (2012년, PEP 3156)

### 핵심 설계 원칙

**PEP 3156**:
> "**The event loop is the place where most interoperability occurs.** It should be easy for frameworks like Twisted, Tornado, or even gevent to either adapt the default event loop implementation to their needs... or to replace the default event loop implementation with an adaptation of their own."

**이벤트 루프는 대부분의 상호운용성이 발생하는 곳이다.** Twisted, Tornado, gevent 같은 프레임워크들이 기본 이벤트 루프를 수정하거나, 자신들의 이벤트 루프로 대체할 수 있어야 한다.

**출처**: https://peps.python.org/pep-3156/

### 양방향 적응 지원

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   방향 1: 기존 프레임워크 → asyncio                          │
│   ─────────────────────────────────────                     │
│   Twisted/Tornado가 asyncio 이벤트 루프를 사용              │
│                                                             │
│   방향 2: asyncio → 기존 프레임워크                          │
│   ─────────────────────────────────────                     │
│   asyncio가 Twisted/Tornado의 이벤트 루프를 사용            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 제어권은 메인 프로그램에게

**PEP 3156**:
> "**Which event loop implementation is used should be under control of the main program.**"

**어떤 이벤트 루프 구현을 사용할지는 메인 프로그램이 제어해야 한다.** 라이브러리가 아닌 애플리케이션이 결정.

---

## 계층화된 API 설계

**Python 공식 문서**:
> "**Application developers should typically use the high-level asyncio functions, such as asyncio.run()**, and should rarely need to reference the loop object or call its methods. **This section is intended mostly for authors of lower-level code, libraries, and frameworks, who need finer control over the event loop behavior.**"

**출처**: https://docs.python.org/3/library/asyncio-eventloop.html

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   일반 개발자                                                │
│   ───────────                                               │
│   asyncio.run(main())  ← 이것만 사용                         │
│                                                             │
│   라이브러리/프레임워크 작성자                                │
│   ─────────────────────────────                             │
│   loop = asyncio.get_event_loop()                           │
│   asyncio.set_event_loop_policy(MyPolicy())                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## asyncio 등장 후: 통합

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   표준 이벤트 루프 (asyncio)                                 │
│   ─────────────────────────                                 │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              asyncio Event Loop                     │   │
│   │                                                     │   │
│   │   Twisted    Tornado    새 라이브러리               │   │
│   │   (어댑터)    (어댑터)                               │   │
│   │                                                     │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   → 하나의 표준 이벤트 루프를 공유!                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Tornado의 변화

**Tornado 6.0+ 공식 문서**:
> "IOLoop is a **wrapper around the asyncio event loop**."

Tornado의 IOLoop이 asyncio 이벤트 루프를 감싸는 래퍼가 되었다.

### Twisted의 변화

```python
# Twisted에서 asyncio 이벤트 루프 사용
from twisted.internet import asyncioreactor
asyncioreactor.install()  # asyncio 루프를 Twisted reactor로 사용

from twisted.internet import reactor
reactor.run()  # 내부적으로 asyncio 이벤트 루프 사용
```

---

## Policy 시스템과 미래

### Policy 시스템 (Python 3.4~3.15)

**Python 공식 문서**:
> "**An event loop policy is a global object used to get and set the current event loop**, as well as create new event loops. The default policy can be replaced with built-in alternatives to use different event loop implementations."

**출처**: https://docs.python.org/3/library/asyncio-policy.html

```python
# 커스텀 이벤트 루프 정책 설정
import asyncio

class MyPolicy(asyncio.DefaultEventLoopPolicy):
    def get_event_loop(self):
        loop = super().get_event_loop()
        # 커스텀 로직
        return loop

asyncio.set_event_loop_policy(MyPolicy())
```

### Python 3.16에서 Policy 시스템 제거 예정

**Python 공식 문서** ([Pending removal in Python 3.16](https://docs.python.org/3/deprecations/pending-removal-in-3.16.html)):

제거되는 것들:
- `asyncio.get_event_loop_policy()`
- `asyncio.set_event_loop_policy()`
- `asyncio.AbstractEventLoopPolicy`
- `asyncio.DefaultEventLoopPolicy`

**이유** ([GitHub Issue #127949](https://github.com/python/cpython/issues/127949)):
> "asyncio's policy system has been **a source of confusion and problems** in asyncio for a very long time. The policies **no longer serve a real purpose**."

### 새로운 방식: loop_factory

```python
# Python 3.16+ 권장 방식
import asyncio

# loop_factory로 직접 지정
asyncio.run(main(), loop_factory=asyncio.SelectorEventLoop)

# 또는 Runner 사용
with asyncio.Runner(loop_factory=asyncio.SelectorEventLoop) as runner:
    runner.run(main())
```

**출처**: https://docs.python.org/3/library/asyncio-runner.html

---

## 타임라인 요약

| 연도 | 사건 |
|------|------|
| 2002 | Twisted 등장 (자체 Reactor) |
| 2009 | Tornado 등장 (자체 IOLoop) |
| 2012 | PEP 3156 제안 (asyncio 설계) |
| 2014 | Python 3.4에 asyncio 포함 |
| 2015 | Python 3.5에 async/await 문법 추가 |
| 2020 | Tornado 6.0 - asyncio 이벤트 루프 래핑 |
| 2024 | Python 3.14 - Policy 시스템 deprecated |
| 예정 | Python 3.16 - Policy 시스템 제거, loop_factory 사용 |

---

## 결론

| 질문 | 답 |
|------|-----|
| 왜 이벤트 루프를 개발자가 관리할 수 있나? | 기존 프레임워크(Twisted, Tornado)와 호환성을 위해 |
| 왜 호환성이 필요했나? | 10년 이상 사용된 프레임워크들이 각자의 이벤트 루프를 가지고 있었음 |
| 왜 두 이벤트 루프가 공존 불가? | 한 스레드에서 이벤트 루프는 동시에 하나만 실행 가능 |
| 해결책은? | 이벤트 루프를 교체 가능(pluggable)하게 설계 |
| 앞으로는? | Policy 시스템 제거, loop_factory로 단순화 |

**핵심**: asyncio는 새로운 표준을 만들면서도 기존 생태계를 버리지 않기 위해 이벤트 루프를 교체 가능하게 설계했다. 이제 대부분의 프레임워크가 asyncio를 수용했기 때문에, 복잡한 Policy 시스템은 더 이상 필요하지 않다.

---

## 왜 이벤트 루프가 자동 생성되지 않나?

### Python은 동기 언어로 시작했다

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   1991년: Python 탄생                                       │
│           동기 언어로 설계                                   │
│           이벤트 루프 개념 없음                              │
│                                                             │
│           ↓ (23년 후)                                       │
│                                                             │
│   2014년: asyncio 추가 (Python 3.4)                         │
│           비동기 기능이 "선택적으로" 추가됨                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

이미 **23년간 동기 코드**가 작성되어 있었다. 이걸 다 깨뜨릴 수 없었다.

### 이벤트 루프가 필요 없는 코드

```python
# 대부분의 Python 코드 - 이벤트 루프 불필요
def main():
    data = read_file("data.txt")      # 동기 I/O
    result = process(data)            # CPU 연산
    print(result)                     # 출력

main()
```

이런 코드에 이벤트 루프를 **강제로 할당하면**:

| 문제 | 설명 |
|------|------|
| 리소스 낭비 | 이벤트 루프는 무한 루프 - CPU/메모리 소비 |
| 복잡성 증가 | 단순한 스크립트에 불필요한 인프라 |
| 기존 코드 호환성 | 23년간의 동기 코드가 깨질 수 있음 |

### Go와의 차이

| | Python | Go |
|--|--------|-----|
| 탄생 | 1991년 (동기 언어) | 2009년 (동시성 내장) |
| 비동기 추가 | 2014년 (23년 후) | 처음부터 |
| 이벤트 루프 | opt-in (필요할 때만) | 항상 내장 |

Go는 처음부터 동시성을 핵심 기능으로 설계했기 때문에, 모든 프로그램에 런타임 스케줄러가 내장되어 있다.

### Python의 설계 철학

**"Explicit is better than implicit"** (명시적인 것이 암시적인 것보다 낫다)

```python
# Python - 명시적으로 이벤트 루프 실행
async def main():
    await do_something()

asyncio.run(main())  # ← "나 비동기 쓸거야" 명시
```

**"You don't pay for what you don't use"**

동기 코드만 쓰는 프로그램이 비동기 인프라 비용을 지불할 필요 없다.

---

## 참고 자료

- PEP 3156: https://peps.python.org/pep-3156/
- Python asyncio Event Loop: https://docs.python.org/3/library/asyncio-eventloop.html
- Python asyncio Policy: https://docs.python.org/3/library/asyncio-policy.html
- Python asyncio Runner: https://docs.python.org/3/library/asyncio-runner.html
- Twisted Reactor Basics: https://docs.twisted.org/en/stable/core/howto/reactor-basics.html
- Tornado IOLoop: https://www.tornadoweb.org/en/stable/ioloop.html
- GitHub: Deprecate asyncio policy system: https://github.com/python/cpython/issues/127949
