# asyncio.gather() 사용 여부에 따른 동작 차이

## 핵심 요약

| 방식 | 실행 | 총 시간 |
|------|------|--------|
| gather 미사용 | 순차 (sequential) | 각 작업 시간의 **합** |
| gather 사용 | 동시 (concurrent) | **가장 긴** 작업 시간 |

---

## 코드 비교

### gather 미사용 (순차 실행)

```python
async def without_gather():
    result1 = await task("A")  # 1초 대기
    result2 = await task("B")  # 1초 대기
    result3 = await task("C")  # 1초 대기
    return [result1, result2, result3]
```

### gather 사용 (동시 실행)

```python
async def with_gather():
    results = await asyncio.gather(
        task("A"),  # 동시에
        task("B"),  # 동시에
        task("C"),  # 동시에
    )
    return results
```

---

## 실행 흐름 비교

### gather 미사용 (순차)

```
시간  0s        1s        2s        3s
      │         │         │         │
  A   ██████████
  B             ██████████
  C                       ██████████
      │         │         │         │
      └─────────┴─────────┴─────────┘
                    총 3초
```

**출력:**
```
A 시작
A 완료      ← A 끝나야 B 시작
B 시작
B 완료
C 시작
C 완료
```

### gather 사용 (동시)

```
시간  0s        1s
      │         │
  A   ██████████
  B   ██████████
  C   ██████████
      │         │
      └─────────┘
        총 1초
```

**출력:**
```
A 시작
B 시작      ← A, B, C 동시 시작
C 시작
A 완료
B 완료      ← 거의 동시 완료
C 완료
```

---

## 이벤트 루프 관점

### gather 미사용

```
이벤트 루프:
  1. A 실행 → await sleep → A 대기
  2. (대기 중 아무것도 안 함)
  3. (1초 후) A 재개 → A 완료
  4. B 실행 → await sleep → B 대기
  5. (대기 중 아무것도 안 함)
  6. (1초 후) B 재개 → B 완료
  7. C 실행 ...
```

**A가 대기 중일 때 B, C는 시작조차 안 함**

### gather 사용

```
이벤트 루프:
  1. A 실행 → await sleep → A 대기 (Task로 등록)
  2. B 실행 → await sleep → B 대기 (Task로 등록)
  3. C 실행 → await sleep → C 대기 (Task로 등록)
  4. (1초 후) A, B, C 모두 재개 → 완료
```

**A가 대기할 때 B, C도 실행 시작 → I/O 대기 시간이 겹침**

---

## 왜 이런 차이가 나는가?

### await의 의미

```python
result = await task("A")
```

`await`는 **"이 코루틴이 끝날 때까지 여기서 기다려"**라는 의미.

- gather 미사용: 각 await에서 완료까지 대기 → 다음 줄로 진행
- gather 사용: 모든 코루틴을 **Task로 등록** 후 동시에 대기

### gather의 역할

```python
await asyncio.gather(task("A"), task("B"), task("C"))
```

1. A, B, C를 각각 **Task로 생성** (이벤트 루프에 등록)
2. 세 Task가 **동시에 실행** 시작
3. **모두 완료될 때까지** 대기
4. 결과를 **리스트로 반환** (순서 보장)

---

## 실제 예시: API 3개 호출

```python
# 순차: 3초
async def fetch_sequential():
    user = await fetch_user()          # 1초
    posts = await fetch_posts()        # 1초
    comments = await fetch_comments()  # 1초
    return user, posts, comments

# 동시: 1초
async def fetch_concurrent():
    user, posts, comments = await asyncio.gather(
        fetch_user(),      # 1초
        fetch_posts(),     # 1초  ← I/O 대기 겹침
        fetch_comments(),  # 1초
    )
    return user, posts, comments
```

---

## 언제 gather를 사용하는가?

| 상황 | 사용 여부 |
|------|----------|
| 독립적인 I/O 작업 여러 개 | ✅ gather |
| 작업 간 의존성 있음 (A 결과로 B 호출) | ❌ 순차 |
| 결과 순서 보장 필요 | ✅ gather (순서 보장됨) |
| 하나 실패해도 나머지 결과 필요 | ✅ gather + `return_exceptions=True` |

---

## 참고

- 예시 코드: [asyncio-gather-comparison.py](./asyncio-gather-comparison.py)
- Python 공식 문서: https://docs.python.org/3/library/asyncio-task.html#asyncio.gather
