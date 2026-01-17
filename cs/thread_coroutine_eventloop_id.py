"""
스레드, 코루틴, 이벤트 루프 ID 확인 스크립트

- 2개의 스레드에서 같은 코루틴 실행
- 각 코루틴 내부에서 Thread ID, Coroutine ID, Event Loop ID 출력
"""

import asyncio
import threading


async def my_coroutine(name: str) -> None:
    """코루틴: Thread ID, Coroutine ID, Event Loop ID 출력"""

    # Thread ID
    thread_id = threading.get_ident()

    # Coroutine ID (Task를 통해 접근)
    task = asyncio.current_task()
    coroutine_id = id(task.get_coro())

    # Event Loop ID
    loop = asyncio.get_running_loop()
    event_loop_id = id(loop)

    print(f"[{name}]")
    print(f"  Thread ID:     {thread_id}")
    print(f"  Coroutine ID:  {coroutine_id}")
    print(f"  Event Loop ID: {event_loop_id}")
    print()

    await asyncio.sleep(0.1)


def run_in_thread(thread_name: str) -> None:
    """스레드에서 이벤트 루프 생성 후 코루틴 실행"""
    asyncio.run(my_coroutine(thread_name))


if __name__ == "__main__":
    print("=" * 50)
    print("2개의 스레드에서 같은 코루틴 실행")
    print("=" * 50)
    print()

    # 스레드 2개 생성
    thread1 = threading.Thread(target=run_in_thread, args=("Thread-1",))
    thread2 = threading.Thread(target=run_in_thread, args=("Thread-2",))

    # 스레드 시작
    thread1.start()
    thread2.start()

    # 스레드 종료 대기
    thread1.join()
    thread2.join()

    print("=" * 50)
    print("결과 분석")
    print("=" * 50)
    print("""
- Thread ID:     다름 (각각 별도의 OS 스레드)
- Coroutine ID:  다름 (호출할 때마다 새 코루틴 객체 생성)
- Event Loop ID: 다름 (각 스레드마다 별도의 이벤트 루프)
""")
