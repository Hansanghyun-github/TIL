"""
asyncio.gather() 사용 여부에 따른 실행 시간 비교

- gather 미사용: 순차 실행 → 3초
- gather 사용: 동시 실행 → 1초
"""

import asyncio
import time


async def task(name: str) -> str:
    """1초 걸리는 비동기 작업"""
    print(f"  {name} 시작")
    await asyncio.sleep(1)
    print(f"  {name} 완료")
    return name


async def without_gather() -> list[str]:
    """gather 미사용: 순차 실행"""
    result1 = await task("A")
    result2 = await task("B")
    result3 = await task("C")
    return [result1, result2, result3]


async def with_gather() -> list[str]:
    """gather 사용: 동시 실행"""
    results = await asyncio.gather(
        task("A"),
        task("B"),
        task("C"),
    )
    return list(results)


if __name__ == "__main__":
    print("=" * 50)
    print("asyncio.gather() 사용 여부에 따른 실행 시간 비교")
    print("=" * 50)

    # 1. gather 미사용 (순차 실행)
    print("\n[1] gather 미사용 (순차 실행)")
    print("-" * 30)
    start = time.perf_counter()
    results1 = asyncio.run(without_gather())
    elapsed1 = time.perf_counter() - start
    print(f"결과: {results1}")
    print(f"소요 시간: {elapsed1:.2f}초")

    # 2. gather 사용 (동시 실행)
    print("\n[2] gather 사용 (동시 실행)")
    print("-" * 30)
    start = time.perf_counter()
    results2 = asyncio.run(with_gather())
    elapsed2 = time.perf_counter() - start
    print(f"결과: {results2}")
    print(f"소요 시간: {elapsed2:.2f}초")

    # 결과 비교
    print("\n" + "=" * 50)
    print("결과 비교")
    print("=" * 50)
    print(f"""
gather 미사용: {elapsed1:.2f}초 (1초 × 3 = 순차)
gather 사용:   {elapsed2:.2f}초 (1초 × 1 = 동시)

→ gather를 사용하면 I/O 대기 시간이 겹쳐서
  총 실행 시간이 "가장 긴 작업 시간"이 된다.
""")
