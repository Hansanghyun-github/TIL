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