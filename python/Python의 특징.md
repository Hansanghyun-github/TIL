## 파이썬의 기본 문법

### 변수 처리

파이썬은 자료형을 명시하지 않아도 되기 때문에 변수를 선언할 때 자료형을 지정하지 않아도 된다.  
변수에 값을 할당할 때 자료형이 결정된다.

```python
a = 10 # 정수형
b = 3.14 # 실수형
c = 'hello' # 문자열
```

> 내부적으로 알아서 자료형을 결정해주기 때문에 동적 타이핑 언어라고 한다

### 데이터 타입

기본 타입: `int`, `float`, `str`, `bool`, `NoneType` (`null` 대신 `None` 사용)  
컬렉션 타입: `list` (배열), `tuple` (불변 배열), `set` (집합), `dict` (맵)

```python
# list
a = [1, 2, 3, 4, 5]

# tuple
b = (1, 2, 3, 4, 5)

# set
c = {1, 2, 3, 4, 5}

# dict
d = {'a': 1, 'b': 2, 'c': 3}
```

## 파이썬의 주요 특징

### 코드가 간결하고 가독성이 좋다

중괄호(`{}`) 대신 들여쓰기로 코드 블록을 구분하기 때문에 가독성이 좋다.

```python
for i in range(10):
    print(i)
```

### 자료형 변환이 자유롭다

```java
class Main{
    public static void main(String[] args){
        int a = 10;
        String b = Integer.toString(a);
    }
}
```

```python
a = 10
b = str(a)
```

### 문자열 처리가 편리하다

```python
a = 'hello'
print(f"안녕하세요, {a}")  # f-string
```

---

## 파이썬의 함수

파이썬은 `def` 키워드로 함수를 정의한다.

```python
def add(a, b):
    return a + b
```

람다 함수로 간단히 함수를 정의할 수 있다.

```python
add = lambda a, b: a + b
```

---

## 클래스와 객체 지향

파이썬은 객체 지향 언어이다.

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        print(f"안녕하세요, {self.name}입니다.")
```

> 파이썬은 자바처럼 `public`, `private` 키워드가 없고,  
> 모든 멤버 변수와 메소드는 `public`이다.
> 
> 대신 `_`이나 `__`로 시작하는 변수는 `protected`나 `private`처럼 사용할 수 있다.  
> (접근을 암시적으로 제한하는 것이지, 실제로 제한하는 것은 아니다)

### 클래스 메서드 & 인스턴스 메서드

클래스 메서드는 클래스 자체에 속해있는 메서드이고,  
인스턴스 메서드는 인스턴스에 속해있는 메서드이다.

```python
class Person:
    count = 0

    def __init__(self, name):
        self.name = name
        Person.count += 1

    @classmethod
    def get_count(cls):
        return cls.count

    def say_hello(self):
        print(f"안녕하세요, {self.name}입니다.")


p1 = Person('홍길동')
p1.say_hello()  # 안녕하세요, 홍길동입니다.
print(p1.get_count())  # 1
print(Person.get_count())  # 1
```

인스턴스 메서드는 `self`를 통해 인스턴스 변수에 접근할 수 있고,  
클래스 메서드는 `cls`를 통해 클래스 변수에 접근할 수 있다.

그리고 인스턴스 메서드는 각 인스턴스 별로 다른 값을 가질 수 있지만,  
클래스 메서드는 모든 인스턴스가 공유하는 값이다.  

클래스 메서드는 각 객체나 클래스를 통해 호출할 수 있다.  
인스턴스 메서드는 객체를 통해서만 호출할 수 있다.

> 파이썬의 클래스 메서드는  
> 자바의 `static` 메서드와 비슷하다.

### 클래스의 생성자 - __init__ & __new__

__init__ 메서드는 클래스 오브젝트에 메모리를 할당하지 않는다.

실제로 메모리를 할당하는 메서드는 __new__ 메서드 이다.

> 실제로 __init__를 호출하면 __new__ 메서드가 먼저 실행된다.

__new__ 메서드는 `cls`를 인자로 받아서 객체를 생성하고,  
__init__ 메서드는 `self`를 인자로 받아서 객체를 초기화한다.

```python
class Person:
    def __new__(cls, *args, **kwargs):
        print("new")
        return super().__new__(cls)

    def __init__(self, name):
        print("init")
        self.name = name
```

### 상속

부모 클래스를 상속받아 자식 클래스를 만들 수 있다.  
(자바와 동일하게 `super()`를 사용하여 부모 클래스의 생성자를 호출할 수 있다.)

```python
class Person:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(f"안녕하세요, {self.name}입니다.")

class Student(Person):
    def __init__(self, name, school):
        super().__init__(name)
        self.school = school

    def say_hello(self):
        print(f"안녕하세요, {self.name}입니다. {self.school}에 다닙니다.")
```

> 자바와 다르게 파이썬은 다중 상속을 지원한다.


---

## 패키지와 모듈

파이썬에서 모듈은 `.py` 확장자를 가진 파일 하나를 의미하고,  
패키지는 여러 모듈을 모아놓은 디렉토리를 의미한다.

```python
# my_module.py
def add(a, b):
    return a + b
```

```python
# main.py
import my_module

print(my_module.add(1, 2))
```

---

## 타입 힌트

파이썬은 동적 타이핑 언어이기 때문에 변수의 자료형을 명시하지 않아도 된다.  
하지만, 타입 힌트를 사용하면 변수의 자료형을 명시할 수 있다.

> Python 3.5부터 타입 힌트를 지원한다.

```python
def add(a: int, b: int) -> int:
    return a + b
```

`a: int` 는 `a` 변수의 자료형이 `int`라는 것을 의미하고,  
`-> int` 는 함수의 반환값이 `int`라는 것을 의미한다.

---

## 컴프리헨션

컴프리헨션(Comprehension)은 리스트나 딕셔너리를 간결하고 직관적으로 생성할 수 있는 파이썬의 문법

리스트 컴프리헨션을 만들기 위한 방법  
-> `[표현식 for 요소 in 반복가능한객체 if 조건]`

딕셔너리 컴프리헨션을 만들기 위한 방법  
-> `{키: 값 for 요소 in 반복가능한객체 if 조건}`

```python
# list comprehension
a = [i for i in range(10)]
print(a) # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# dictionary comprehension
b = {i: i * i for i in range(10)}
print(b) # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64, 9: 81}
```

> 컴프리헨션을 통해 코드를 간결하게 작성할 수 있다.  
> (기존 방식은 빈 리스트를 만들고 반복문을 통해 요소를 추가하는 방식)

---

## 람다

람다는 익명 함수를 생성하기 위한 표현식  
이름이 없는 함수를 한 줄로 정의할 때 사용한다.

람다 문법  
-> `lambda 매개변수: 표현식`

```python
add = lambda a, b: a + b
print(add(1, 2)) # 3
```

람다 표현식은 보통 map, filter, sorted와 같은 함수에서 활용된다.  

```python
numbers = [1, 2, 3, 4, 5]

# map: 각 요소를 제곱
squared = list(map(lambda x: x**2, numbers))

# filter: 홀수만 선택
odds = list(filter(lambda x: x % 2 != 0, numbers))
```

---

## 비동기 프로그래밍 - async & await

파이썬은 비동기 프로그래밍을 지원한다.

### async 키워드

`async` 키워드를 사용하면 함수를 비동기 함수(코루틴)로 만들 수 있다.

```python
import asyncio

async def hello():
    print('Hello')
```

### await 키워드

`await` 키워드를 사용하면 비동기 함수의 실행이 완료될 때까지 기다릴 수 있다.

> `await` 키워드는 `async` 함수 내에서만 사용할 수 있다.

`await`를 만나면 제어권이 이벤트 루프로 돌아가고, 작업이 완료될 때까지 다른 작업을 수행할 수 있다.

```python
import asyncio

async def hello():
    await asyncio.sleep(1)
    print('Hello')

asyncio.run(hello())
```

---

## asyncio 모듈

`asyncio` 모듈은 비동기 프로그래밍을 위한 모듈이다.

`asyncio.run()` 함수를 사용하면 비동기 함수를 실행할 수 있다.

```python
import asyncio

async def hello():
    await asyncio.sleep(1)
    print('Hello')

asyncio.run(hello())
```

> `asyncio.run()`은 최상위 진입점에서 코루틴을 실행하는 함수이다.  
> 따라서 `await` 키워드를 사용하지 않는다.

여러 코루틴을 실행할 때는 `asyncio.gather()` 함수를 사용한다.

```python
import asyncio

async def hello():
    await asyncio.sleep(1)
    print('Hello')

async def world():
    await asyncio.sleep(1)
    print('World')

async def main():
    await asyncio.gather(hello(), world())

asyncio.run(main())
```

> `asyncio.gather` 함수는 여러 코루틴을 동시에 실행하고,  
> 모든 코루틴이 완료될 때까지 기다린다.

---

## 코루틴

비동기 프로그래밍을 쉽게 구현할 수 있도록 설계된 프로그래밍 개념  
일반적인 함수와는 다르게 실행 흐름을 중단(suspend)하고, 이후 다시 재개(resume)할 수 있는 기능을 제공한다.

### 코루틴의 특징

1. 중단과 재개  
    코루틴은 실행 중인 함수를 중단하고, 이후 다시 재개할 수 있다.  
    (예를 들어, 파일 다운로드, 데이터베이스 쿼리와 같은 I/O 작업 중 코루틴을 멈추고, 다른 작업을 진행한 뒤 다시 재개할 수 있다.)
2. 경량 스레드  
    코루틴은 스레드와 유사하게 동작하지만, 훨씬 더 가볍다.  
    한 개의 스레드에서 수천 개의 코루틴을 실행할 수 있다.  
    일반 스레드는 운영 체제에 의해 관리되지만, 코루틴은 프로그램 런타임(예: Python의 asyncio, Kotlin의 Coroutine 등)이 관리합니다.
3. 비동기 작업 처리  
    코루틴은 비동기 작업을 직관적이고 구조적으로 처리할 수 있도록 도와준다.  
    async/await 키워드를 통해 비동기 작업을 순차적으로 작성할 수 있어 코드 가독성이 높아진다.


### 코루틴의 장점

1. 효율적인 자원 사용  
    스레드보다 메모리와 CPU 자원을 덜 사용하므로, 대규모 비동기 작업을 처리할 때 유리하다.
2. 가독성  
    비동기 작업을 순차적으로 작성할 수 있어 가독성이 높다.
3. 비동기 작업의 간소화  
    콜백(callback) 기반 비동기 프로그래밍의 복잡함(콜백 헬)을 줄이고, 명확한 코드 흐름을 제공한다.

### 파이썬 코루틴

파이썬에서 코루틴은 `async def` 키워드를 사용하여 정의한다.

그리고 `asyncio` 모듈을 사용하여 코루틴을 실행한다.

```python
import asyncio

async def coro():
    print('start')
    await asyncio.sleep(1)
    print('end')

asyncio.run(coro())
```