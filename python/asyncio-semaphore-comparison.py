"""
asyncio.gather()에서 Semaphore 사용 여부에 따른 동작 비교

- Semaphore 미사용: 5개 동시 실행 → 1초
- Semaphore(2) 사용: 2개씩 실행 → 3초
"""

import asyncio
import time


async def task(name: str) -> str:
    """1초 걸리는 비동기 작업"""
    print(f"  {name} 시작 (time: {time.perf_counter() - start:.1f}s)")
    await asyncio.sleep(1)
    print(f"  {name} 완료 (time: {time.perf_counter() - start:.1f}s)")
    return name


async def without_semaphore() -> list[str]:
    """Semaphore 미사용: 전부 동시 실행"""
    results = await asyncio.gather(
        task("A"),
        task("B"),
        task("C"),
        task("D"),
        task("E"),
    )
    return list(results)


async def with_semaphore(limit: int) -> list[str]:
    """Semaphore 사용: 최대 limit개만 동시 실행"""
    semaphore = asyncio.Semaphore(limit)

    async def limited_task(name: str) -> str:
        async with semaphore:
            return await task(name)

    results = await asyncio.gather(
        limited_task("A"),
        limited_task("B"),
        limited_task("C"),
        limited_task("D"),
        limited_task("E"),
    )
    return list(results)


if __name__ == "__main__":
    print("=" * 60)
    print("asyncio.gather()에서 Semaphore 사용 여부에 따른 동작 비교")
    print("=" * 60)

    # 1. Semaphore 미사용 (전부 동시 실행)
    print("\n[1] Semaphore 미사용 (5개 전부 동시 실행)")
    print("-" * 40)
    start = time.perf_counter()
    results1 = asyncio.run(without_semaphore())
    elapsed1 = time.perf_counter() - start
    print(f"결과: {results1}")
    print(f"소요 시간: {elapsed1:.2f}초")

    # 2. Semaphore(2) 사용 (2개씩 동시 실행)
    print("\n[2] Semaphore(2) 사용 (최대 2개만 동시 실행)")
    print("-" * 40)
    start = time.perf_counter()
    results2 = asyncio.run(with_semaphore(limit=2))
    elapsed2 = time.perf_counter() - start
    print(f"결과: {results2}")
    print(f"소요 시간: {elapsed2:.2f}초")

    # 3. Semaphore(3) 사용 (3개씩 동시 실행)
    print("\n[3] Semaphore(3) 사용 (최대 3개만 동시 실행)")
    print("-" * 40)
    start = time.perf_counter()
    results3 = asyncio.run(with_semaphore(limit=3))
    elapsed3 = time.perf_counter() - start
    print(f"결과: {results3}")
    print(f"소요 시간: {elapsed3:.2f}초")

    # 결과 비교
    print("\n" + "=" * 60)
    print("결과 비교")
    print("=" * 60)
    print(f"""
태스크: 5개 (각 1초)

Semaphore 없음:  {elapsed1:.2f}초  │ A,B,C,D,E 동시 → 1초
Semaphore(2):    {elapsed2:.2f}초  │ [A,B] → [C,D] → [E] → 3초
Semaphore(3):    {elapsed3:.2f}초  │ [A,B,C] → [D,E] → 2초

실행 흐름 (Semaphore=2):
┌────────────────────────────────────────┐
│ 시간  0s     1s     2s     3s          │
│       │      │      │      │           │
│   A   ████████                         │
│   B   ████████                         │
│   C          ████████                  │
│   D          ████████                  │
│   E                 ████████           │
│       │      │      │      │           │
│       └──────┴──────┴──────┘           │
│              2개씩 실행                 │
└────────────────────────────────────────┘

→ Semaphore는 동시 실행 개수를 제한한다.
→ 리소스 보호 (DB 연결, API rate limit 등)에 사용.
""")
