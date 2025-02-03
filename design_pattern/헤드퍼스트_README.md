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