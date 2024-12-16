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

### 클래스의 생성자 - __init__ & __new__

__init__ 메서드는 클래스 오브젝트에 메모리를 할당하지 않는다.

실제로 메모리를 할당하는 메서드는 __new__ 메서드 이다.

> 실제로 __init__를 호출하면 __new__ 메서드가 먼저 실행된다.

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