# asyncio.Semaphore vs threading.Semaphore

## 한눈에 비교

| 구분 | asyncio.Semaphore | threading.Semaphore |
|------|-------------------|---------------------|
| **용도** | 코루틴 동기화 | 스레드 동기화 |
| **스레드 안전** | ❌ | ✅ |
| **이벤트 루프** | 단일 루프에 바인딩 | 무관 |
| **사용 컨텍스트** | `async` 함수 내부 | 일반 함수 |
| **동시성 모델** | 협력적 (cooperative) | 선점적 (preemptive) |

---

## 왜 asyncio.Semaphore는 이벤트 루프에 바인딩되나?

`asyncio.Semaphore`는 단순 카운터가 아니라 **대기(waiting) 기능**이 있다.

- `acquire()` 시 값이 0이면 → Future를 생성해서 대기
- Future는 **특정 이벤트 루프에 종속**됨
- 따라서 Semaphore도 해당 루프에 바인딩됨

## 왜 async 함수에서만 사용 가능한가?

`acquire()`가 코루틴(`async def`)이고, 내부에서 `await`를 사용하기 때문.

```
asyncio.Semaphore = 카운터 + Future 기반 대기 → 이벤트 루프 필요
threading.Semaphore = 카운터 + OS 수준 대기 → 이벤트 루프 무관
```

---

## 기본 사용법

### asyncio.Semaphore

```python
import asyncio

async def main():
    sem = asyncio.Semaphore(2)  # 최대 2개 동시 실행

    async def task(name):
        async with sem:
            print(f"{name} 시작")
            await asyncio.sleep(1)
            print(f"{name} 완료")

    await asyncio.gather(
        task("A"), task("B"), task("C"), task("D")
    )

asyncio.run(main())
```

### threading.Semaphore

```python
import threading
import time

sem = threading.Semaphore(2)  # 최대 2개 동시 실행

def task(name):
    with sem:
        print(f"{name} 시작")
        time.sleep(1)
        print(f"{name} 완료")

threads = [threading.Thread(target=task, args=(n,)) for n in ["A", "B", "C", "D"]]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

---

## 멀티스레드 환경에서의 차이

### asyncio.Semaphore (스레드별 독립)

```
설정: Semaphore(2), 스레드 3개, 각 스레드에서 코루틴 3개

스레드 0: [sem0] → 2개씩 실행
스레드 1: [sem1] → 2개씩 실행  ← 각자 독립적인 Semaphore
스레드 2: [sem2] → 2개씩 실행

결과: 최대 6개 동시 실행 (3 × 2)
```

### threading.Semaphore (전역 공유)

```
설정: Semaphore(2), 스레드 3개, 각 스레드에서 작업 3개

스레드 0: ─┐
스레드 1: ─┼─ [전역 sem] → 2개씩만 실행
스레드 2: ─┘

결과: 최대 2개 동시 실행 (전역 제한)
```

---

## 스레드 안전성 문제

### 공식 문서

> "asyncio primitives are not thread-safe, therefore they should not be used for OS thread synchronization"

### asyncio.Semaphore를 여러 스레드에서 공유하면?

```python
shared_sem = asyncio.Semaphore(1)  # 전역

def thread_func():
    asyncio.run(use_semaphore())  # 각 스레드마다 새 이벤트 루프

# 3개 스레드 실행 → ?
```

**결과: 예측 불가능**

```
스레드 0: ✅ 획득 성공 (Semaphore가 이 루프에 바인딩)
스레드 1: ✅ 또는 ❌ (타이밍에 따라)
스레드 2: ❌ RuntimeError: "bound to a different event loop"
```

### Race Condition 발생 원인

```
asyncio.Semaphore 내부 동작 (atomic하지 않음):
1. 이벤트 루프 바인딩 체크
2. waiter 등록
3. 락 획득 시도

→ 어느 단계에서 다른 스레드가 끼어드느냐에 따라 결과가 달라짐
```

---

## 장단점

### asyncio.Semaphore

| 장점 | 단점 |
|------|------|
| 가벼움 (컨텍스트 스위칭 비용 없음) | 스레드 간 공유 불가 |
| I/O 바운드 작업에 효율적 | 단일 이벤트 루프에서만 사용 |
| `async with` 문법 지원 | CPU 바운드 작업에 부적합 |

### threading.Semaphore

| 장점 | 단점 |
|------|------|
| 스레드 안전 | 컨텍스트 스위칭 오버헤드 |
| 전역 리소스 제한 가능 | GIL로 인해 CPU 바운드에서 성능 제한 |
| 프로세스 간 공유 가능 (BoundedSemaphore) | 상대적으로 무거움 |

---

## 사용 목적별 선택

| 상황 | 선택 |
|------|------|
| 단일 이벤트 루프 내 코루틴 제한 | `asyncio.Semaphore` |
| API rate limit (async 클라이언트) | `asyncio.Semaphore` |
| 멀티스레드 DB 커넥션 풀 | `threading.Semaphore` |
| 파일 동시 접근 제한 (스레드) | `threading.Semaphore` |
| 웹 요청 10개 받아서 각각 async 처리 | 각 요청마다 `asyncio.Semaphore` (독립) |
| 웹 요청 10개의 **전체** 동시 처리 제한 | `threading.Semaphore` 또는 별도 설계 필요 |

---

## 실행 흐름 비교

### asyncio.Semaphore + gather

```
태스크 5개, Semaphore(2)

시간  0s     1s     2s     3s
      │      │      │      │
  A   ████████
  B   ████████
  C          ████████
  D          ████████
  E                 ████████
      └──────┴──────┴──────┘
             2개씩 실행
             총 3초
```

### threading.Semaphore (3스레드 × 3작업)

```
작업 9개, Semaphore(2)

시간  0s     1s     2s     3s     4s    4.5s
      │      │      │      │      │      │
 T0-A ████████
 T1-A ████████
 T2-A        ████████
 T0-B        ████████
 T1-B               ████████
 T2-B               ████████
 T0-C                      ████████
 T1-C                      ████████
 T2-C                             ████████
      └──────┴──────┴──────┴──────┴──────┘
             전역 2개 제한
             총 4.5초
```

---

## 정리

```
┌─────────────────────────────────────────────────────────┐
│  asyncio.Semaphore                                      │
│  ─────────────────                                      │
│  • 코루틴 동기화 전용                                   │
│  • 단일 이벤트 루프 내에서만 사용                       │
│  • 멀티스레드 공유 시 → RuntimeError 또는 예측 불가     │
│                                                         │
│  threading.Semaphore                                    │
│  ───────────────────                                    │
│  • 스레드 동기화 전용                                   │
│  • 스레드 간 안전하게 공유 가능                         │
│  • 전역 리소스 제한에 적합                              │
└─────────────────────────────────────────────────────────┘
```

---

## 관련 파일

- [asyncio-semaphore-comparison.py](./asyncio-semaphore-comparison.py) - Semaphore 유무에 따른 동작 비교
- [asyncio-vs-threading-semaphore.py](./asyncio-vs-threading-semaphore.py) - 멀티스레드에서 두 Semaphore 비교
- [asyncio-semaphore-thread-unsafe-demo.py](./asyncio-semaphore-thread-unsafe-demo.py) - 스레드 안전성 문제 데모

## 참고

- Python 공식 문서: https://docs.python.org/3/library/asyncio-sync.html
- threading 공식 문서: https://docs.python.org/3/library/threading.html#semaphore-objects
