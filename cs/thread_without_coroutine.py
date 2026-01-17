"""
코루틴 없이 스레드만 실행하는 스크립트

- 2개의 스레드에서 일반 함수 실행 (async 아님)
- Thread ID, Coroutine ID, Event Loop ID 출력 시도
"""

import asyncio
import threading


def my_function(name: str) -> None:
    """일반 함수 (코루틴 아님): 3개 ID 출력 시도"""

    # Thread ID
    thread_id = threading.get_ident()

    # Coroutine ID - 코루틴이 없으므로 None
    try:
        task = asyncio.current_task()
        coroutine_id = id(task.get_coro()) if task else None
    except RuntimeError:
        coroutine_id = None

    # Event Loop ID - 이벤트 루프가 없으므로 None
    try:
        loop = asyncio.get_running_loop()
        event_loop_id = id(loop)
    except RuntimeError:
        event_loop_id = None

    print(f"[{name}]")
    print(f"  Thread ID:     {thread_id}")
    print(f"  Coroutine ID:  {coroutine_id}")
    print(f"  Event Loop ID: {event_loop_id}")
    print()


if __name__ == "__main__":
    print("=" * 50)
    print("코루틴 없이 스레드만 실행")
    print("=" * 50)
    print()

    # 스레드 2개 생성
    thread1 = threading.Thread(target=my_function, args=("Thread-1",))
    thread2 = threading.Thread(target=my_function, args=("Thread-2",))

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
- Thread ID:     있음 (OS 스레드는 존재)
- Coroutine ID:  None (코루틴 없음)
- Event Loop ID: None (이벤트 루프 없음)

→ 스레드는 이벤트 루프 없이도 실행 가능
→ 스레드 : 실행 중인 이벤트 루프 = 1 : 0~1 (동시 실행 기준)
""")
