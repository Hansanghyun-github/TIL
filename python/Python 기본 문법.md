## 파이썬의 문법

### 변수 처리

파이썬은 자료형을 명시하지 않아도 되기 때문에 변수를 선언할 때 자료형을 지정하지 않아도 된다.  
변수에 값을 할당할 때 자료형이 결정된다.

```python
a = 10 # 정수형
b = 3.14 # 실수형
c = 'hello' # 문자열
```

> 내부적으로 알아서 자료형을 결정해주기 때문에 동적 타이핑 언어라고 한다

---

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

---

### 타입 힌트

파이썬은 동적 타이핑 언어이기 때문에 변수의 자료형을 명시하지 않아도 된다.  
하지만, 타입 힌트를 사용하면 변수의 자료형을 명시할 수 있다.

> Python 3.5부터 타입 힌트를 지원한다.

```python
def add(a: int, b: int) -> int:
    return a + b
```

---

`a: int` 는 `a` 변수의 자료형이 `int`라는 것을 의미하고,  
`-> int` 는 함수의 반환값이 `int`라는 것을 의미한다.

### 함수 정의

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

### * 연산자 & ** 연산자

### * 연산자 (Positional Argumentsm, 리스트/튜플 언패킹)

`*` 연산자는 주로  
(1) 위치 인자를 받을 때 사용하거나,  
(2) 리스트/튜플을 언패킹할 때 사용한다.

> 여러 개의 인자 혹은 리스트/튜플을 받을 때 사용한다.

```python
def add(*args):
    for arg in args:
        print(arg)

add(1, 2, 3, 4, 5) # 여러 개의 인자 전달
# 1
# 2
# 3
# 4
# 5
```

여기서 `* args`는 (1, 2, 3, 4, 5) 라는 튜플로 처리된다.

```python
numbers = [1, 2, 3, 4, 5]
add(*numbers) # 리스트 언패킹
# 1
# 2
# 3
# 4
# 5
```

여기서 `*numbers`는 (1, 2, 3, 4, 5) 라는 튜플로 처리된다.

> Iterable 언패킹도 `*` 연산자를 사용한다.
>
> ```a, *b = [1, 2, 3, 4, 5]```  
> `a`에는 1이 할당되고, `b`에는 [2, 3, 4, 5]가 할당된다.

### ** 연산자 (Keyword Arguments, 딕셔너리 언패킹)

`**` 연산자는 주로 키워드 인자를 받을 때 사용하거나,  
딕셔너리를 언패킹할 때 사용한다.

```python
def print_kwargs(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_kwargs(name="Alice", age=25, country="USA")
# 출력:
# name: Alice
# age: 25
# country: USA
```

여기서 `kwargs`는 {'name': 'Alice', 'age': 25, 'country': 'USA'}라는 딕셔너리로 처리된다.

```python
info = {'name': 'Alice', 'age': 25, 'country': 'USA'}
print_kwargs(**info) # 딕셔너리 언패킹
# 출력:
# name: Alice
# age: 25
# country: USA
```

---

### 패키지와 모듈

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

### 컴프리헨션

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

### 람다

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