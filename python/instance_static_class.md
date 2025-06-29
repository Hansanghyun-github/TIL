# 클래스 내 메서드 정리

Python에서 메서드는 **인스턴스**, **클래스**, **스태틱** 세 가지로 나뉩니다.  
아래 표와 함께 각각의 문법·특징·권장 용도를 정리했습니다.

| 구분 | 암묵 인자 | 접근 범위 | 대표 용도 |
|------|-----------|-----------|-----------|
| **인스턴스 메서드** | `self` (인스턴스) | 인스턴스 속성 / 클래스 속성 | 객체 상태 변경·조회 |
| **클래스 메서드**<br>`@classmethod` | `cls` (호출한 실제 **클래스**) | 클래스 속성 / 다른 classmethod | 대안 생성자, 팩토리, 레지스트리 |
| **스태틱 메서드**<br>`@staticmethod` | _(없음)_ | 전달된 인자만 | 유틸 함수, 상태 비의존 로직 |

---

## 인스턴스 메서드

```python
class Counter:
    def __init__(self):
        self.value = 0      # 인스턴스 속성

    def inc(self, n=1):
        self.value += n     # self 로 상태 변경
```

* **암묵 인자**: `self`  
* 객체마다 다른 상태를 읽거나 쓸 때 사용.

---

## 클래스 메서드

```python
class Date:
    def __init__(self, y, m, d):
        self.y, self.m, self.d = y, m, d

    @classmethod
    def from_iso(cls, s: str):   # cls → 호출한 서브클래스 유지
        y, m, d = map(int, s.split("-"))
        return cls(y, m, d)      # 서브클래스일 경우 그 타입으로 생성
```

### 특징
* 첫 번째 인자로 **`cls`(호출 주체 클래스)** 가 자동 주입된다.
* 서브클래스가 호출해도 `cls` 가 해당 서브클래스를 가리켜 다형성(Polymorphism) 보장.
* **클래스 변수만 다룰 때도 유용** — 인스턴스를 만들 필요 없이 전역 카운터·설정값 등을 읽거나 수정할 수 있다.

### 대표 용도
1. **대안 생성자 / 팩토리** (`from_json`, `clone`, `load_from_db` …)  
2. **클래스 레지스트리 패턴**  
3. **클래스 변수 조작** (전역 카운터 증가, 설정 값 변경 등)

```python
class Shape:
    _registry = {}

    @classmethod
    def register(cls, subclass):
        cls._registry[subclass.__name__] = subclass
```

---

## 스태틱 메서드

```python
class Math:
    @staticmethod
    def dot(a, b):
        return sum(x * y for x, y in zip(a, b))
```

* **암묵 인자 없음** → 인스턴스·클래스 상태를 건드리지 않는다.
* “이 클래스와 주제가 같은 **순수 함수**”를 네임스페이스에 묶어 둘 때 편리.
* 호출 오버헤드가 가장 적음.

---

## 언제 각 메서드를 사용하나?

| 체크포인트 | 인스턴스 | 클래스 | 스태틱 |
|------------|---------|--------|--------|
| **객체 상태가 필요한가?** | ✔ | ✖ | ✖ |
| **서브클래스-aware 팩터리가 필요한가?** | ✖ | ✔ | ✖ |
| **그냥 유틸리티 함수인가?** | △ (가능하나 과하다) | △ | ✔ |

> **실전 규칙**  
> * **상태 의존** → 인스턴스 메서드  
> * **타입 다형성 필요** → 클래스 메서드  
> * **상태·타입 둘 다 불필요** → 스태틱 메서드

---

## 요약

```text
self  → 객체 자신
cls   → 호출한 실제 클래스 (다형성)
없음  → 순수 함수, 네임스페이스 목적
```

메서드 선언 전 *“이 로직이 객체 상태·타입에 의존하는가?”* 를 먼저 자문하면 자연스럽게 세 가지 중 하나가 결정됩니다.

---

## 참고

인스턴스 메서드에서도 cls를 사용할 수 있다.

```python
class C1:
    def method1(self):
        cls = self.__class
```