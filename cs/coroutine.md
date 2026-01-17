# 코루틴 (Coroutine)

## 정의

### 최초 정의 (1963년, Melvin Conway)

> Coroutines are autonomous subroutines operating at the same level, communicating through discrete information along fixed, one-way paths **without a central master program**.

코루틴은 **중앙 마스터 프로그램 없이** 동일한 수준에서 작동하며, 고정된 단방향 경로를 따라 개별 정보를 통해 통신하는 자율적인 서브루틴이다.

**출처**: Conway, M. E. "Design of a Separable Transition-Diagram Compiler" (Communications of the ACM, 1963)

### Python 공식 문서 정의

> A coroutine object is created when calling an async def function, but **it only executes when explicitly awaited**. Calling a coroutine without awaiting it does not run its code.

코루틴 객체는 `async def` 함수를 호출할 때 생성되지만, **명시적으로 await될 때만 실행**된다. await 없이 코루틴을 호출하면 코드가 실행되지 않는다.

**출처**: https://docs.python.org/3/library/asyncio-task.html

### Kotlin 공식 문서 정의

> Coroutines are often called **lightweight threads** because you can run code on coroutines, similar to how you run code on threads.

코루틴은 스레드에서 코드를 실행하는 것과 유사하게 코루틴에서 코드를 실행할 수 있기 때문에 종종 **경량 스레드**라고 불린다.

**출처**: https://kotlinlang.org/docs/coroutines-basics.html

---

## 핵심 특징

### 1. 앱(유저 레벨)에서 관리

| 구분 | 스레드 | 코루틴 |
|------|--------|--------|
| 관리 주체 | OS (커널) | 앱 (이벤트 루프/런타임) |
| 다른 이름 | 네이티브 스레드, OS 스레드 | 유저 스레드, 그린 스레드 |

```
OS (커널)
    │
    └── 네이티브 스레드 관리

앱 (유저 레벨)
    │
    └── 코루틴 관리 (이벤트 루프/런타임)
```

### 2. 경량 (Lightweight)

**Kotlin 공식 문서**:
> A thread is managed by the operating system. Each thread usually needs **a few megabytes of memory**, and typically the JVM can only handle **a few thousand threads** at once.

스레드는 운영체제가 관리하며, 각 스레드는 보통 **수 MB의 메모리**가 필요하고, JVM은 보통 **수천 개**의 스레드만 처리할 수 있다.

**Go 공식 문서**:
> A newly minted goroutine is given **a few kilobytes**, which is almost always enough. It is practical to create **hundreds of thousands of goroutines** in the same address space.

새 고루틴은 **수 KB**만 할당받으며, 같은 주소 공간에서 **수십만 개의 고루틴**을 만드는 것이 실용적이다.

**출처**: https://go.dev/doc/faq

| 구분 | 메모리 | 동시 실행 가능 수 |
|------|--------|-----------------|
| 스레드 | ~MB | 수천 개 |
| 코루틴 | ~KB | 수십만 개 |

### 3. 협력적 스케줄링 (Cooperative Scheduling)

**스레드 (선점형)**: OS가 강제로 실행 중단 가능
**코루틴 (협력형)**: 코루틴이 자발적으로 `await`에서 양보

```python
async def task():
    x = 0
    for i in range(1000000):
        x += 1  # ← 여기서는 절대 전환 안됨
    await something()  # ← 오직 여기서만 전환
    return x
```

### 4. 특정 스레드에 바인딩되지 않음

**Kotlin 공식 문서**:
> A **coroutine isn't bound to a specific thread**. It can suspend on one thread and resume on another.

**코루틴은 특정 스레드에 바인딩되지 않는다**. 한 스레드에서 suspend하고 다른 스레드에서 resume할 수 있다.

**출처**: https://kotlinlang.org/docs/coroutines-basics.html

---

## 언어별 구현

| 언어 | 용어 | 관리 주체 |
|------|------|----------|
| Python | Coroutine | asyncio 이벤트 루프 |
| JavaScript | Promise/async function | 이벤트 루프 |
| Kotlin | Coroutine | Kotlin 런타임 |
| Go | Goroutine | Go 런타임 스케줄러 |
| Java 21+ | Virtual Thread | Java 런타임 |

---

## 역사

| 연도 | 사건 |
|------|------|
| 1958 | Melvin Conway가 "coroutine" 용어 최초 사용 (미발표 메모) |
| 1963 | 공식 논문 발표 (Communications of the ACM) |
| 1968 | Knuth가 "The Art of Computer Programming"에서 인용 |

---

## 이벤트 루프와의 관계

```
이벤트 루프 : 코루틴 = 1 : N

┌─────────────────────────────────────┐
│            이벤트 루프               │
│            (스케줄러)               │
│                                     │
│   코루틴1  코루틴2  코루틴3  ...     │
│            (Worker)                 │
└─────────────────────────────────────┘
```

- **이벤트 루프**: 스케줄러 (관리자) - 누가 실행될지 결정
- **코루틴**: Worker (일꾼) - 실제 비즈니스 로직 수행

---

## 참고 자료

- Conway, M. E. "Design of a Separable Transition-Diagram Compiler" (1963)
- Python asyncio 문서: https://docs.python.org/3/library/asyncio-task.html
- Kotlin Coroutines 문서: https://kotlinlang.org/docs/coroutines-basics.html
- Go FAQ: https://go.dev/doc/faq
