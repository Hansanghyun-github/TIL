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

## 상속과 조합

### 상속(Inheritance)

상속은 부모 클래스의 기능을 자식 클래스가 물려받는 것이다.  
(기존의 클래스에 기능을 추가하거나 재정의하여 새로운 클래스를 정의하는 것)

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

### 상속의 장점

1. 기존에 작성된 클래스를 재활용할 수 있다.
2. 코드의 중복을 줄일 수 있다.  
    (부모 클래스에 공통된 기능을 작성하고, 자식 클래스에서는 추가적인 기능만 작성하면 된다.)
3. 클래스 간의 계층적 관계를 구성함으로써 다형성의 특성을 구현할 수 있다.

### 상속의 문제점

1. 높은 결합도  
    자식 클래스는 부모 클래스의 구현에 의존하기 때문에 변경에 취약하다.  
    (부모 클래스의 구현이 변경되면 자식 클래스도 변경되어야 한다.)
2. 메서드 오버라이딩의 오동작  
    자식 클래스에서 메서드 오버라이딩을 잘못하면 부모 클래스의 기능이 무시되어 버그가 발생할 수 있다.
3. 불필요한 인터페이스 상속  
    부모 클래스의 기능 중 일부만 필요한 경우에도 부모 클래스의 모든 기능을 상속받아야 한다.
4. 클래스 폭발  
    상속을 계속하다 보면 클래스의 수가 무수히 많아지고, 복잡해질 수 있다.

### 조합(Composition)

조합은 클래스 간의 관계를 느슨하게 만들어주는 디자인 패턴이다.  
(클래스 간의 관계를 상속이 아닌 포함을 통해 구현하는 것)

> 기존 클래스를 상속을 통해 확장하는 대신,  
> 필드로 다른 클래스의 인스턴스를 포함시키는 방식

```python
class Person:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(f"안녕하세요, {self.name}입니다.")

class Student:
    def __init__(self, name, school):
        self.person = Person(name)
        self.school = school

    def say_hello(self):
        self.person.say_hello()
        print(f"{self.school}에 다닙니다.")
```

### 조합의 장점

1. 낮은 결합도  
    부모 클래스의 구현에 의존하지 않기 때문에 변경에 유연하다.
2. 내부 구현이 공개되지 않음  
    부모 클래스의 내부 구현이 자식 클래스에 노출되지 않기 때문에 캡슐화를 보장한다.
3. 상속과는 달리, 모든 퍼블릭 메서드를 공개할 필요가 없다.
4. 클래스 간의 관계를 동적으로 변경할 수 있어 유연성이 높아진다.

### 상속과 조합의 선택

코드를 재사용할 뿐만 아니라 부모와 자식의 행동이 호환되는  
다형적인 계층구조를 만들어야 한다면 상속을 사용한다.

하지만, 클래스 간의 관계가 강하게 결합되어 있지 않고,  
부모 클래스의 구현에 의존하지 않는 느슨한 관계를 원한다면 조합을 사용한다.