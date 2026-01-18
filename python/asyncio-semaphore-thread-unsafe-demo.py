"""
asyncio.Semaphore를 여러 스레드에서 사용할 때 발생하는 문제 데모

공식 문서:
"asyncio primitives are not thread-safe, therefore they should
not be used for OS thread synchronization"
"""

import asyncio
import threading

print("=" * 60)
print("asyncio.Semaphore 스레드 안전성 문제 데모")
print("=" * 60)

# =============================================================================
# 테스트: 같은 asyncio.Semaphore를 여러 스레드에서 공유
# =============================================================================

print("""
[테스트] 같은 asyncio.Semaphore(1)을 3개 스레드에서 공유
──────────────────────────────────────────────────────────
- Semaphore(1) = 한 번에 1개만 획득 가능
- 3개 스레드가 동시에 획득 시도
- 타임아웃 2초 설정 (데드락 감지용)
""")

# 전역 asyncio.Semaphore
shared_sem = asyncio.Semaphore(1)

results = {
    "success": 0,
    "timeout": 0,
    "error": 0,
}
results_lock = threading.Lock()


def try_acquire_in_thread(thread_id: int):
    """다른 스레드에서 공유 asyncio.Semaphore 획득 시도"""

    async def acquire_with_timeout():
        try:
            print(f"  [스레드 {thread_id}] 획득 시도...")

            # 타임아웃 2초 설정
            await asyncio.wait_for(shared_sem.acquire(), timeout=2.0)

            print(f"  [스레드 {thread_id}] ✅ 획득 성공!")
            await asyncio.sleep(0.5)  # 작업 수행
            shared_sem.release()
            print(f"  [스레드 {thread_id}] 해제 완료")

            with results_lock:
                results["success"] += 1

        except asyncio.TimeoutError:
            print(f"  [스레드 {thread_id}] ⏰ 타임아웃! (2초 대기 후 포기)")
            with results_lock:
                results["timeout"] += 1

        except Exception as e:
            print(f"  [스레드 {thread_id}] ❌ 에러: {type(e).__name__}: {e}")
            with results_lock:
                results["error"] += 1

    # 각 스레드에서 새 이벤트 루프 생성
    asyncio.run(acquire_with_timeout())


print("실행 중...")
print("-" * 50)

# 3개 스레드 동시 시작
threads = []
for i in range(3):
    t = threading.Thread(target=try_acquire_in_thread, args=(i,))
    threads.append(t)
    t.start()

# 모든 스레드 완료 대기
for t in threads:
    t.join()

print("-" * 50)
print(f"""
결과:
  성공: {results["success"]}개
  타임아웃: {results["timeout"]}개
  에러: {results["error"]}개
""")

# =============================================================================
# 분석
# =============================================================================

print("=" * 60)
print("분석")
print("=" * 60)

if results["error"] > 0:
    print("""
❌ RuntimeError 발생!

원인:
- asyncio.Semaphore는 첫 acquire() 시 해당 이벤트 루프에 바인딩됨
- 다른 스레드(= 다른 이벤트 루프)에서 접근하면 RuntimeError 발생
- "is bound to a different event loop" 에러 메시지
""")
elif results["timeout"] > 0:
    print("""
⏰ 타임아웃 발생! (데드락)

원인:
- asyncio.Semaphore는 특정 이벤트 루프에 바인딩됨
- 다른 스레드의 이벤트 루프에서는 release() 신호를 받지 못함
- 결과: 영원히 대기 (데드락)
""")
elif results["success"] == 3:
    print("""
🤔 모두 성공했지만...

- 이것은 각 스레드가 독립적인 이벤트 루프를 가져서
- Semaphore가 실제로 공유되지 않았기 때문
- 전역 제한이 작동하지 않음!
""")

print("""
해결책:
─────────
스레드 간 동기화가 필요하면 → threading.Semaphore 사용
코루틴 간 동기화가 필요하면 → asyncio.Semaphore 사용 (단일 이벤트 루프)
""")
