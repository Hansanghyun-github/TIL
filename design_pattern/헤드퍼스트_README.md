# 전략 패턴(Strategy Pattern)

여러 오리들을 만들기 위해, 오리에 대한 슈퍼 클래스 Duck를 만들어 놓았다.  
그리고 Duck 클래스를 상속받아 다양한 오리 클래스를 만들었다.

```python
class Duck:
    def quack(self):
        pass

class MallardDuck(Duck):
    def quack(self):
        print("Quack")

class RedheadDuck(Duck):
    def quack(self):
        print("Quack")
```

이때 오리가 날 수 있어야 한다는 요청이 들어왔다.  
이를 위해 Duck 클래스에 fly 메서드를 추가하고, 이를 상속받는 모든 클래스에 fly 메서드를 구현해야 한다.

```python
class Duck:
    def quack(self):
        pass

    def fly(self):
        pass

class MallardDuck(Duck):
    def quack(self):
        print("Quack")

    def fly(self):
        print("Fly")

class RedheadDuck(Duck):
    def quack(self):
        print("Quack")

    def fly(self):
        print("Fly")
```

여기서 못 날 수 있는 오리가 있다.  
이에 대한 클래스는 fly 메서드를 다르게 구현해야 한다.

---

위 과정을 거치면서 경험한 문제점은,  
오리의 행동이 추가될 떄마다 Duck 클래스를 수정해야 한다는 것이다.  
그리고 이를 상속받는 모든 클래스에도 수정이 필요하다.

이 문제를 해결하기 위해  
Duck 클래스에서 quack, fly 메서드를 만들지 않고,  
별도의 인터페이스로 정의할 수도 있다.

```python
class Quackable:
    def quack(self):
        pass

class Flyable:
    def fly(self):
        pass

class MallardDuck(Quackable, Flyable):
    def quack(self):
        print("Quack")

    def fly(self):
        print("Fly")
```

위 코드의 문제점은,  
MallardDuck 클래스가 Quackable, Flyable 인터페이스를 모두 구현해야 한다는 것이다.

> 새로 생성될 수 있는 오리 클래스가 많아진다면,  
> 이를 모두 수정해야 하는 번거로움이 생긴다.

---

이 문제를 해결하기 위해 전략 패턴을 사용할 수 있다.  
(구성(composition)을 사용하여 런타임에 행동을 변경할 수 있다.)

```python

class QuackBehavior:
    def quack(self):
        pass

class FlyBehavior:
    def fly(self):
        pass

class Quack(QuackBehavior):
    def quack(self):
        print("Quack")

class FlyWithWings(FlyBehavior):
    def fly(self):
        print("Fly")

class Duck:
    def __init__(self):
        self.quack_behavior = None
        self.fly_behavior = None

    def perform_quack(self):
        self.quack_behavior.quack()

    def perform_fly(self):
        self.fly_behavior.fly()

class MallardDuck(Duck):
    def __init__(self):
        super().__init__()
        self.quack_behavior = Quack()
        self.fly_behavior = FlyWithWings()

```

이렇게 하면,  
Duck 클래스에서 quack, fly 메서드를 수정할 필요 없이,  
새로운 행동을 추가할 수 있다.

Duck을 상속 받는 새로운 클래스를 만들 때도,  
새로운 행동을 추가하기 위해 Duck 클래스를 수정할 필요가 없다.  
(QuckBehavior, FlyBehavior 클래스를 상속받아 새로운 행동을 만들면 된다.)

---

## 상속보다는 구성을 사용하라

상속은 코드 재사용을 위해 사용되지만,  
상속은 클래스 간의 강한 결합을 만들어낸다.

상속을 사용하면,  
부모 클래스의 변경이 자식 클래스에 영향을 미칠 수 있다.

구성을 사용하면,  
클래스 간의 결합이 약해지고,  
클래스 간의 의존성이 줄어든다.

---

> 전략 패턴(Strategy Pattern)은  
> 알고리즘군을 정의하고 캡슐화해서 각각의 알고리즘군을 수정해서 쓸 수 있게 해준다.  
> 전략 패턴을 사용하면, 클라이언트로부터 알고리즘을 분리해서 독립적으로 변경할 수 있다.

---

# 옵저버 패턴

> 옵저버 패턴(Observer Pattern)은 한 객체의 상태가 바뀌면  
> 그 객체에 의존하는 다른 객체에게 연락이 가고 자동으로 내용이 갱신되는 방식

주제 객체의 상태가 변경되면,  
그 변경을 관찰하는 옵저버 객체들에게 알려주는 패턴이다.

주체 객체는 자신의 변경을 알릴 옵저버들을 관리한다.

각 옵저버 객체들은 주체 객체의 변경을 감지하고,  
해당 변경에 대한 처리를 한다.

이때 특정 옵저버 객체는 주체 객체의 변경을 감지히고 싶지 않을 수도 있다.  
따라서 옵저버 객체는 주체 객체의 변경을 감지할지 말지(subscribe or unsubscribe) 여부를 결정할 수 있다.

---

## 옵저버 패턴을 사용하는 이유

1. 주체 객체와 옵저버 객체의 결합을 느슨하게 만들 수 있다.
2. 주체 객체의 변경에 대한 처리를 독립적으로 추가하거나 삭제할 수 있다.

---

## 옵저버 패턴의 구현

옵저버 패턴은 주체 객체와 옵저버 객체로 구성된다.

```python
class Observer:
    def update(self):
        pass

class Subject:
    def __init(self):
        self.observers = []
        
    def subscribe(self, o: Observer):
        self.observers.append(o)
    
    def unsubscribe(self, o: Observer):
        self.observers.remove(o)
        
    def notify(self):
        for o in self.observers:
            o.update()
```

Subject 클래스의 변경이 발생하면,  
notify 메서드를 호출해서 옵저버 객체들에게 변경을 알린다.  
(옵저버 객체들은 update 메서드를 호출해서 변경에 대한 처리를 한다.)

> 위 방식은 주체가 직접 옵저버들에게 변경 사항을 알리는,  
> 푸쉬 방식이다.
> 
> 옵저버 객체가 주체 객체에게 직접 변경 사항을 요청하는,  
> 풀 방식도 있다.

---

## 느슨한 결합의 위력

옵저버 패턴을 사용하면,  
주체 객체와 옵저버 객체의 결합을 느슨하게 만들 수 있다.

> 결합이 느슨하다:  
> 주체 객체와 옵저버 객체가 서로 독립적으로 변경될 수 있다.

주체는 옵저버가 특정 인터페이스(Observer 인터페이스)를 구현하고 있다는 사실만 알고 있으면 된다.

옵저버는 언제든지 새로 추가하거나 제거할 수 있다.  
(subscribe, unsubscribe 메서드를 통해)

주체와 옵저버는 서로 독립적으로 재사용할 수 있다.

주체나 옵저버가 달라져도 서로에게 영향을 미치지 않는다.

---

# 데코레이터 패턴

> 데코레이터 패턴(Decorator Pattern)은  
> 객체에 추가적인 요소를 동적으로 더할 수 있는 패턴이다.  
> 데코레이터를 사용하면, 서브클래스를 만들 때보다, 유연하게 기능을 확장할 수 있다.

## 데코레이터 패턴을 적용하기 전

카페에 여러 음료가 있다.  
각 음료는 재료도 다르고, 이에 따라 가격도 다르다.

이때 음료를 하나의 클래스로 정의하고,  
음료의 재료를 인스턴스 변수로 추가할 수 있다.

```python
class Beverage:
    def __init__(self):
        self.description = "Unknown Beverage"
    
    def get_description(self):
        return self.description
    
    def cost(self):
        pass

class CafeLatte(Beverage):
    def __init__(self):
        super().__init__()
        self.sugar = 2
        self.milk = 3
        self.bean = 5 
        self.description = "Cafe Latte"
    
    def cost(self):
        return self.sugar + self.milk + self.bean
```

이때 음료의 재료 중 하나의 가격이 변경되면,  
해당 재료를 이용하는 모든 음료의 가격을 변경해야 한다.

---

## 데코레이터 패턴 적용 예시

이때 데코레이터 패턴을 사용하면,  
각 음료의 재료를 독립적으로 확장할 수 있다.

```python
class Beverage:
    def get_description(self):
        pass
    
    def cost(self):
        pass

class CondimentDecorator(Beverage):
    def __init__(self):
        self.beverage = None
    
    def get_description(self):
        pass

class Sugar(Beverage): # 설탕은 원재료로 취급하여 Beverage 클래스를 상속받는다.
    def get_description(self):
        return "Sugar"
    
    def cost(self):
        return 2
    
class CafeLatte(CondimentDecorator): # CafeLatte는 여러 재료를 가지므로 CondimentDecorator 클래스를 상속받는다.
    def __init__(self, beverage):
        super().__init__()
        self.beverage = beverage
    
    def get_description(self):
        return self.beverage.get_description() + ", Cafe Latte"
    
    def cost(self):
        return self.beverage.cost() + 5
```

기존의 구조에서는, 설탕의 가격이 바뀌면,  
모든 음료의 가격을 변경해야 했다.

현재 구조에서는, 설탕의 가격이 바뀌어도,  
Sugar 클래스만 수정하면 된다.

---

## OCP(Open-Closed Principle)

데코레이터 패턴은 OCP를 준수한다.

데코레이터 패턴을 적용하여  
기존의 코드를 수정하지 않고, 새로운 기능을 추가할 수 있다.  
(설탕의 가격을 변경하더라도, 기존의 코드를 수정할 필요가 없다.)

> OCP(Open-Closed Principle):  
> 소프트웨어 요소(클래스, 모듈, 함수 등)는 확장에 대해서는 열려 있어야 하지만,  
> 수정에 대해서는 닫혀 있어야 한다.

---

## 데코레이터 패턴의 단점

데코레이터 패턴을 사용하면,  
자잘한 객체가 매우 많이 추가될 수 있다.  
그리고 코드가 필요 이상으로 복잡해질 수 있다.

> 데코레이터 패턴을 이용하는 특정 객체는,  
> 데코레이터를 사용만 하고 있을 뿐,  
> 해당 데코레이터가 얼마나 많은 객체를 가지고 있는지 알 수 없다.

---

# 팩토리 패턴

## 개요

어떤 인터페이스가 있고 그에 대한 구현 클래스가 있을 때,  
인터페이스를 변수로 선언한다 해도,  
결국 해당 변수를 구현하려면 구현 클래스를 생성해야 한다.

```python
class Pizza:
    def prepare(self):
        pass

class CheesePizza(Pizza):
    def prepare(self):
        print("Cheese Pizza")

pizza: Pizza = CheesePizza()
```

이때 인터페이스에 대한 구현 객체를 생성하는 로직을  
클라이언트 코드로부터 분리하여,  
별도의 클래스로 만들어 관리할 수 있다.

이러한 패턴을 팩토리 패턴이라고 한다.

---

## 팩토리 메서드 패턴

팩토리 메서드 패턴은  
객체 생성을 서브 클래스로 분리하여 처리하는 패턴이다.

```python
class Pizza:
    def prepare(self):
        pass

class PizzaStore:
    def order_pizza(self, pizza_type: str):
        pizza: Pizza = self.create_pizza(pizza_type)
        pizza.prepare()
    
    def create_pizza(self, pizza_type: str) -> Pizza:
        pass

class CheesePizza(Pizza):
    def prepare(self):
        print("Cheese Pizza")

class NYStylePizzaStore(PizzaStore):
    def create_pizza(self, pizza_type: str) -> Pizza:
        if pizza_type == "cheese":
            return CheesePizza()
        else:
            return None
```

`NYStylePizzaStore` 클래스는 `PizzaStore` 클래스를 상속받는다.  
이때 `create_pizza` 메서드를 오버라이딩하여,  
해당하는 피자 객체를 생성한다.

`PizzaStore` 클래스의 구현 객체들은 `order_pizza` 메서드를 변경하지 않고,  
생성하는 메서드(`create_pizza`)만 변경하면 된다.

> 이렇게 되면 서브 클래스는 생성하려는 객체의 종류를 결정한다.

---

## 추상 팩토리 패턴

추상 팩토리 패턴은  
인터페이스를 이용하여 서로 연관된 객체를 생성하는 패턴이다.

위 팩토리 메서드 패턴은  
생성하려는 객체의 종류가 한가지 였지만,  
추상 팩토리 패턴은 여러 종류의 객체를 생성할 때 사용된다.

이때도 생성하려는 객체의 슈퍼 클래스를 인터페이스로 선언하고,  
해당 인터페이스를 구현하는 서브 클래스에서 객체를 생성한다.

---

# 싱글톤 패턴

## 개요

일반적으로 객체는 여러 개 생성할 수 있다.

```python
class Example:
    pass
    
example1 = Example()
example2 = Example()
```

위 두 객체는 다른 객체이다.

이때 어떤 객체는 오직 하나만 생성되어야 할 때가 있다.  
(예: 데이터베이스 연결 객체, 로그 객체 등)

이때 싱글톤 패턴을 사용하면,  
해당 객체를 오직 하나만 생성할 수 있다.

---

## 싱글톤 패턴이란?

싱글톤 패턴(Singleton Pattern)은  
클래스의 인스턴스가 하나만 생성되도록 하는 패턴이다.

싱글톤 패턴을 사용하면,  
클래스의 인스턴스를 하나만 생성하여,  
해당 인스턴스를 여러 곳에서 공유할 수 있다.

---

## 싱글톤 패턴의 구현

기본적으로 생성자는 private으로 선언하고,  
클래스 내부에서 인스턴스를 생성하고,  
해당 인스턴스를 반환하는 메서드를 만든다.

```python
class Singleton:
    __instance = None
    
    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            Singleton()
        return cls.__instance
    
    def __init__(self):
        if Singleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = self
```

위 `get_instance` 메서드를 통해,  
해당 클래스의 인스턴스를 생성하고,  
해당 인스턴스를 반환한다.

---

# 커맨드 패턴

호출하는 객체의 역할과,  
실행하는 객체의 역할을 분리하는 패턴  
(서로가 알 필요가 없다)

## 개요

버튼을 누르면 다른 장치를 실행시키는 리모컨이 있다.

리모컨은 on/off 버튼이 총 7개가 있고,  
각 버튼을 다른 장치들과 연결할 수 있다.

이때 버튼을 누르면,  
불이 켜질 수도 있고 TV가 켜질 수도 있다.

이때 핵심은  
리모컨은 어떤 버튼이 어떤 장치를 실행하는지 알 필요가 없다.  
그리고 장치도 어떤 버튼을 눌러서 실행되었는지 알 필요가 없다.

결국 각자의 역할을 분리하는 것이다.  
이를 분리하고, 둘을 관리하는 객체(커맨더)를 만들어야 한다.  

---

## 커맨드 패턴의 정의

커맨드 패턴은  
요청 내역을 객체로 캡슐화하여,  
요청하는 객체와 수행하는 객체를 분리하는 패턴이다.

---

## 커맨드 패턴의 구성

1. Command: 명령을 나타내는 인터페이스
2. Invoker: 명령을 실행하는 객체
3. Receiver: 명령을 수행하는 객체

> 리모컨: Invoker  
> 버튼: Command  
> TV, Light: Receiver

Invoker 객체는 Command 객체를 가지고 있고,  
Receiver 객체는 Command 객체를 구현한다.

---

## 커맨드 패턴의 구현

```python
class Command:
    def execute(self):
        pass

class Light(Command):
    def execute(self):
        print("Light On")

class TV(Command):
    def execute(self):
        print("TV On")

class Invoker: # 리모컨
    def __init__(self):
        self.command = None
    
    def set_command(self, command: Command):
        self.command = command
    
    def run(self):
        self.command.execute()
```

---

# 어댑터 패턴, 퍼사드 패턴

## 어댑터 패턴

어댑터 패턴은  
클래스의 인터페이스를 사용자가 기대하는 다른 인터페이스로 변환하는 패턴이다.

어댑터 패턴을 이용해 사용하지 못했던 클래스를 사용할 수 있게 된다.

> 대신 변환하려는 클래스의 어댑터를 직접 생성하기 때문에  
> 관리하는 클래스가 많아질 수 있다.

---

## 퍼사드 패턴

퍼사드 패턴은  
복잡한 서브시스템을 간단하게 사용할 수 있도록 하는 패턴이다.

> A, B, C 행동을 전부 이어서 해야 할 때,  
> 이를 a 행동 하나에 저장해서 a만 호출하면 위 3가지를 모두 하게 만들 수 있다.

클라이언트가 여러 객체를 의존하지 않고,  
(여러 객체를 의존하고 있는) 퍼사드 객체 하나만 의존해서  
클라이언트는 간단하게 호출할 수 있게 만든다.

---

## 어댑터 패턴과 퍼사드 패턴

여기서 어댑터 패턴이 여러 클래스를 사용할 수도 있고,  
퍼사드 패턴이 오히려 하나의 클래스만 사용할 수도 있다.

핵심은  
어댑터는 인터페이스를 변환하는 역할을 하고,  
퍼사드는 복잡한 서브시스템을 간단하게 사용할 수 있도록 하는 역할을 한다.

> 두 패턴은 목적에서 차이가 있다.

---

## 최소 지식 원칙

객체 사이의 상호작용은 될 수 있으면 적게 하는 것이 좋다.  
(즉, 객체는 자신이 상호작용하는 객체의 수를 최소화해야 한다.)

> 데메테르 법칙이라고도 한다.

이 원칙의 단점은 메소드 호출을 처리하는  
래퍼 객체가 많아질 수 있다는 것이다.

퍼사드 패턴이 이 원칙을 지키기 위한 방법이 될 수 있다.

---