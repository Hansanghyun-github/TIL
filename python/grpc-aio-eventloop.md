# gRPC aio와 Event Loop 관리

## 개요

Python gRPC에서 `grpc.aio`를 사용할 때 발생하는 event loop 관련 이슈와 올바른 사용 패턴에 대한 정리.

## 핵심 요약

| 서버 유형 | 적합한 Client | 비고 |
|----------|--------------|------|
| `grpc.server()` (sync) | `grpc.insecure_channel()` | Thread 기반 |
| `grpc.aio.server()` (async) | `grpc.aio.insecure_channel()` | Coroutine 기반 |

**Sync 서버에서 `grpc.aio` 클라이언트를 쓰는 것은 아키텍처 불일치.**

---

## 문제 상황

### 코드 구조

```python
# Sync gRPC 서버
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# Provider에서 async/sync 둘 다 생성
class StatssvcStatisticsProvider:
    def __init__(self, host: str, port: int):
        # sync stub
        self.channel = grpc.insecure_channel(...)
        self.stub = StatsServiceStub(self.channel)

        # async stub - event loop 필요!
        self.aio_channel = grpc.aio.insecure_channel(...)
        self.aio_stub = StatsServiceStub(self.aio_channel)
```

### 문제 1: `asyncio.run()` 사용 시 event loop 닫힘

```python
# asyncio.run()은 실행 후 event loop을 닫음
def async_run_tasks(coroutines, limit):
    return asyncio.run(
        _async_gather_with_semaphore(coroutines, limit)
    )  # 실행 후 loop.close() 호출됨
```

테스트에서 여러 테스트가 순차 실행될 때:

```
Test 1: asyncio.run() → loop 생성 → 실행 → loop 닫힘
Test 2: grpc.aio.insecure_channel() → loop 없음 → RuntimeError!
```

### 문제 2: Event loop mismatch

```python
# aio_channel이 loop A에서 생성됨
self.aio_channel = grpc.aio.insecure_channel(...)  # loop A에 바인딩

# 나중에 asyncio.run()으로 실행하면 새 loop B 생성
asyncio.run(use_aio_channel())  # loop B에서 실행

# aio_channel은 loop A를 기대하지만 현재 loop은 B → 문제!
```

---

## `grpc.aio`의 설계 의도

### Async 서버 구조 (의도된 사용법)

```
┌─────────────────────────────────────────────────────────────┐
│                    Async Server (grpc.aio.server)           │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              Single Event Loop                      │   │
│   │                                                     │   │
│   │   Request 1 ──► coroutine ──┐                       │   │
│   │   Request 2 ──► coroutine ──┼──► aio_channel ───►   │   │
│   │   Request 3 ──► coroutine ──┘    (1개, 공유)        │   │
│   │                                                     │   │
│   └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

- 하나의 event loop
- 여러 coroutine이 동시 실행
- 하나의 aio_channel 공유
- Connection pooling 활용

### Sync 서버 + aio 시도 (문제 있는 구조)

```
┌─────────────────────────────────────────────────────────────┐
│                 Sync Server (grpc.server + ThreadPool)      │
│                                                             │
│   Request 1 ──► Thread 1 ──► asyncio.run() ──► loop A      │
│   Request 2 ──► Thread 2 ──► asyncio.run() ──► loop B      │
│   Request 3 ──► Thread 3 ──► asyncio.run() ──► loop C      │
│                                                             │
│                    aio_channel (어느 loop에 바인딩?)        │
└─────────────────────────────────────────────────────────────┘
```

- 요청마다 다른 thread
- 각 thread에서 `asyncio.run()` 호출 시 다른 event loop
- aio_channel 공유 불가

---

## 해결 방안

### 1. 기존 event loop 재사용 (단기 해결책)

```python
def _async_run_tasks(coroutines, concurrent_tasks_limit):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)  # 전역에 설정, 재사용 가능

    task = loop.create_task(
        _async_gather_with_semaphore(coroutines, concurrent_tasks_limit)
    )
    return loop.run_until_complete(task)  # loop 닫지 않음
```

**장점**: 변경 최소화, 검증된 방식
**단점**: `get_event_loop()` deprecated (Python 3.10+), 전역 상태 의존

### 2. Lazy Initialization

```python
class StatssvcStatisticsProvider:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._aio_channel = None
        self._aio_stub = None
        self._loop_id = None

    def _get_or_create_aio_channel(self):
        current_loop = asyncio.get_running_loop()

        # loop이 바뀌었으면 재생성
        if self._aio_channel is None or self._loop_id != id(current_loop):
            self._aio_channel = grpc.aio.insecure_channel(...)
            self._aio_stub = StatsServiceStub(self._aio_channel)
            self._loop_id = id(current_loop)

        return self._aio_channel, self._aio_stub
```

**장점**: `asyncio.run()` 사용 가능, 올바른 async 패턴
**단점**: 매 요청마다 channel 재생성 가능 → 성능 저하

### 3. aio_stub 제거 + ThreadPoolExecutor 사용

```python
from concurrent.futures import ThreadPoolExecutor

# async 대신 thread로 동시성 확보
def list_finances_concurrent(stub, requests):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(stub.ListUnitFinances, req)
            for req in requests
        ]
        return [f.result() for f in futures]
```

**장점**: 간단, 안정적, event loop 이슈 없음
**단점**: 스레드 오버헤드

### 4. Async 서버로 전환 (장기 해결책)

```python
# grpc.aio.server() 사용
async def serve():
    server = grpc.aio.server()
    billing_pb2_grpc.add_BillingServiceServicer_to_server(
        servicer=AsyncBillingServer(),
        server=server
    )
    await server.start()
    await server.wait_for_termination()

asyncio.run(serve())
```

**장점**: 가장 효율적, 올바른 아키텍처
**단점**: 서버 전체 리팩토링 필요

---

## aio_stub을 쓰는 이유

동시성(concurrency)을 위해:

```python
# sync stub - 순차 실행 (느림)
result1 = stub.ListUnitFinances(request1)  # 100ms
result2 = stub.ListUnitFinances(request2)  # 100ms
result3 = stub.ListUnitFinances(request3)  # 100ms
# 총 300ms

# async stub - 동시 실행 (빠름)
results = await asyncio.gather(
    aio_stub.ListUnitFinances(request1),
    aio_stub.ListUnitFinances(request2),
    aio_stub.ListUnitFinances(request3),
)
# 총 ~100ms
```

---

## gRPC Channel 생성 비용

매 요청마다 channel을 생성하면:

| 항목 | 비용 |
|------|------|
| TCP 연결 수립 | ~1-10ms |
| HTTP/2 핸드셰이크 | 추가 RTT |
| 메모리 할당 | 채널당 수 KB |
| File descriptor | 연결당 1개 |

**Channel은 재사용하는 것이 효율적.**

---

## 실행 환경별 영향

| 환경 | asyncio.run() 문제 |
|------|-------------------|
| Management Command (배치) | 없음 (프로세스 1회 실행) |
| pytest | 있음 (같은 프로세스에서 여러 테스트) |
| gRPC Server | 있음 (여러 요청이 같은 프로세스) |

---

## 결론

1. **Sync 서버에서 `grpc.aio` 사용은 아키텍처 불일치**
2. **`asyncio.run()`은 event loop을 닫으므로 주의 필요**
3. **단기**: 기존 event loop 재사용 방식 유지
4. **장기**: async 서버로 전환 또는 aio_stub 제거 검토

---

## 참고

- [gRPC Python AsyncIO](https://grpc.github.io/grpc/python/grpc_asyncio.html)
- [Python asyncio.run() 문서](https://docs.python.org/3/library/asyncio-runner.html)
- [PEP 492 - Coroutines with async and await syntax](https://peps.python.org/pep-0492/)
