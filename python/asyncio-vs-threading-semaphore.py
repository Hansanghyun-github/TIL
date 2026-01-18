"""
asyncio.Semaphore vs threading.Semaphore 멀티스레드 비교

- asyncio.Semaphore: 스레드 안전하지 않음 → 각 스레드별 독립
- threading.Semaphore: 스레드 안전 → 전역 제한 가능
"""

import asyncio
import threading
import time

# 공유 카운터 (동시 실행 중인 작업 수 추적)
current_running = 0
max_running = 0
lock = threading.Lock()


def track_start():
    """작업 시작 시 카운터 증가"""
    global current_running, max_running
    with lock:
        current_running += 1
        max_running = max(max_running, current_running)


def track_end():
    """작업 종료 시 카운터 감소"""
    global current_running
    with lock:
        current_running -= 1


def reset_counters():
    """카운터 초기화"""
    global current_running, max_running
    current_running = 0
    max_running = 0


# =============================================================================
# 1. asyncio.Semaphore - 각 스레드별 독립 (전역 제한 안 됨)
# =============================================================================

def run_with_asyncio_semaphore(thread_id: int, limit: int):
    """각 스레드에서 asyncio.Semaphore 사용"""

    async def task(name: str):
        track_start()
        print(f"  [{thread_id}] {name} 시작 (현재 동시 실행: {current_running})")
        await asyncio.sleep(0.5)
        print(f"  [{thread_id}] {name} 완료")
        track_end()

    async def main():
        # 각 스레드마다 새로운 Semaphore 생성됨!
        sem = asyncio.Semaphore(limit)

        async def limited_task(name: str):
            async with sem:
                await task(name)

        await asyncio.gather(
            limited_task("A"),
            limited_task("B"),
            limited_task("C"),
        )

    asyncio.run(main())


# =============================================================================
# 2. threading.Semaphore - 전역 제한 (스레드 안전)
# =============================================================================

# 전역 threading.Semaphore
global_threading_sem = None


def run_with_threading_semaphore(thread_id: int):
    """각 스레드에서 전역 threading.Semaphore 사용"""

    def task(name: str):
        with global_threading_sem:  # 전역 Semaphore 공유
            track_start()
            print(f"  [{thread_id}] {name} 시작 (현재 동시 실행: {current_running})")
            time.sleep(0.5)
            print(f"  [{thread_id}] {name} 완료")
            track_end()

    threads = []
    for name in ["A", "B", "C"]:
        t = threading.Thread(target=task, args=(name,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


# =============================================================================
# 메인 실행
# =============================================================================

if __name__ == "__main__":
    LIMIT = 2  # 동시 실행 제한
    NUM_THREADS = 3  # 스레드 수

    print("=" * 70)
    print("asyncio.Semaphore vs threading.Semaphore 멀티스레드 비교")
    print("=" * 70)
    print(f"설정: Semaphore limit={LIMIT}, 스레드 {NUM_THREADS}개, 각 스레드에서 3개 작업")
    print(f"예상 총 작업 수: {NUM_THREADS * 3} = 9개")

    # =========================================================================
    # 테스트 1: asyncio.Semaphore
    # =========================================================================
    print("\n" + "=" * 70)
    print("[테스트 1] asyncio.Semaphore (스레드별 독립)")
    print("=" * 70)
    print(f"예상: 각 스레드가 독립적인 Semaphore → {NUM_THREADS} × {LIMIT} = {NUM_THREADS * LIMIT}개 동시 실행 가능")
    print("-" * 70)

    reset_counters()
    start = time.perf_counter()

    threads = []
    for i in range(NUM_THREADS):
        t = threading.Thread(target=run_with_asyncio_semaphore, args=(i, LIMIT))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed1 = time.perf_counter() - start
    print("-" * 70)
    print(f"결과: 최대 동시 실행 수 = {max_running}")
    print(f"소요 시간: {elapsed1:.2f}초")

    # =========================================================================
    # 테스트 2: threading.Semaphore
    # =========================================================================
    print("\n" + "=" * 70)
    print("[테스트 2] threading.Semaphore (전역 공유)")
    print("=" * 70)
    print(f"예상: 전역 Semaphore 공유 → 최대 {LIMIT}개만 동시 실행")
    print("-" * 70)

    reset_counters()
    global_threading_sem = threading.Semaphore(LIMIT)
    start = time.perf_counter()

    threads = []
    for i in range(NUM_THREADS):
        t = threading.Thread(target=run_with_threading_semaphore, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed2 = time.perf_counter() - start
    print("-" * 70)
    print(f"결과: 최대 동시 실행 수 = {max_running}")
    print(f"소요 시간: {elapsed2:.2f}초")

    # =========================================================================
    # 결과 비교
    # =========================================================================
    print("\n" + "=" * 70)
    print("결과 비교")
    print("=" * 70)
    print(f"""
┌─────────────────────────────────────────────────────────────────────┐
│                    asyncio.Semaphore vs threading.Semaphore         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  asyncio.Semaphore (스레드별 독립)                                  │
│  ─────────────────────────────────                                  │
│  • 각 스레드마다 새 Semaphore 생성                                  │
│  • 최대 동시 실행: {NUM_THREADS} 스레드 × {LIMIT} limit = {NUM_THREADS * LIMIT}개                        │
│  • 소요 시간: {elapsed1:.2f}초 (빠름, 제한 안 됨)                            │
│                                                                     │
│  threading.Semaphore (전역 공유)                                    │
│  ───────────────────────────────                                    │
│  • 모든 스레드가 동일한 Semaphore 공유                              │
│  • 최대 동시 실행: {LIMIT}개 (전역 제한)                                    │
│  • 소요 시간: {elapsed2:.2f}초 (느림, 제한 적용됨)                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

→ asyncio.Semaphore는 스레드 간 공유 불가 (각자 독립)
→ threading.Semaphore는 스레드 간 공유 가능 (전역 제한)
""")
