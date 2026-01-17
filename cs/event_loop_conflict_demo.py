"""
이벤트 루프 충돌 데모

하나의 스레드에서 두 개의 이벤트 루프를 동시에 실행하면 어떻게 되는지 보여줌
"""

import asyncio


async def task_a():
    print("Task A: 시작")
    await asyncio.sleep(1)
    print("Task A: 완료")


async def task_b():
    print("Task B: 시작")
    await asyncio.sleep(1)
    print("Task B: 완료")


def demo_conflict():
    """두 개의 이벤트 루프를 동시에 실행 시도"""

    print("=" * 60)
    print("시나리오: 두 개의 이벤트 루프를 동시에 실행하려고 시도")
    print("=" * 60)
    print()

    # 첫 번째 이벤트 루프 생성 및 실행
    loop1 = asyncio.new_event_loop()
    asyncio.set_event_loop(loop1)

    print("[Loop 1] 이벤트 루프 생성됨")
    print("[Loop 1] task_a 실행 시작...")
    print()

    # loop1이 실행 중인 상태에서 loop2를 실행하려고 시도
    async def nested_loop_attempt():
        print("  [Loop 1 내부] task_a 실행 중...")

        # 여기서 새로운 이벤트 루프를 만들어 실행하려고 시도
        print("  [Loop 1 내부] 새로운 이벤트 루프(Loop 2)를 실행하려고 시도...")
        print()

        try:
            # 이미 실행 중인 루프가 있는데 asyncio.run() 호출
            asyncio.run(task_b())  # RuntimeError 발생!
        except RuntimeError as e:
            print(f"  ❌ 에러 발생: {e}")
            print()
            print("  → 이미 이벤트 루프가 실행 중이라 새 루프를 시작할 수 없음!")

        await asyncio.sleep(0.1)

    loop1.run_until_complete(nested_loop_attempt())
    loop1.close()


def demo_why_this_matters():
    """왜 이게 문제인지 설명"""

    print()
    print("=" * 60)
    print("왜 이게 문제인가?")
    print("=" * 60)
    print("""
가상의 상황:
─────────────────────────────────────────────────────────────

[기존 Twisted 애플리케이션]

    from twisted.internet import reactor

    def main():
        # Twisted의 이벤트 루프 (reactor)가 실행 중
        reactor.run()  # ← 이벤트 루프 A 실행 중

        # 여기서 새로운 asyncio 라이브러리를 쓰고 싶다면?
        # asyncio.run(some_new_library())
        # ↑ 에러! 이미 Twisted reactor가 돌고 있음

─────────────────────────────────────────────────────────────

문제:
• Twisted reactor = 이벤트 루프 A
• asyncio        = 이벤트 루프 B
• 하나의 스레드에서 두 이벤트 루프를 동시에 돌릴 수 없음!

─────────────────────────────────────────────────────────────

해결책 (Python이 선택한 방식):
• 이벤트 루프를 교체 가능(pluggable)하게 만듦
• Twisted가 asyncio의 이벤트 루프를 사용하도록 설정 가능
• 또는 asyncio가 Twisted의 reactor를 사용하도록 설정 가능
• → 두 프레임워크가 같은 이벤트 루프를 공유!
""")


def demo_single_loop_works():
    """하나의 이벤트 루프에서 여러 작업은 문제없음"""

    print()
    print("=" * 60)
    print("정상 케이스: 하나의 이벤트 루프에서 여러 코루틴 실행")
    print("=" * 60)
    print()

    async def main():
        print("[단일 Loop] 여러 코루틴을 동시에 실행...")
        await asyncio.gather(task_a(), task_b())
        print("[단일 Loop] 모든 작업 완료!")

    asyncio.run(main())


if __name__ == "__main__":
    demo_conflict()
    demo_why_this_matters()
    demo_single_loop_works()
