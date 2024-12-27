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