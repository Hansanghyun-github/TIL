# Go에서 인터페이스 만들기, 구조체에 인터페이스 구현하기

## 인터페이스 만들기

`type {name} interface` 구문을 사용하여 인터페이스를 만들 수 있다.

`{}` 안에 메서드를 정의하면, 해당 인터페이스를 구현하는 구조체는 해당 메서드를 구현해야 한다.

```go
package main

import (
    "fmt"
)

type Animal interface {
    Speak() string
}
```

---

## 구조체에 인터페이스 구현하기

> 구조체를 만들 때는, `type {name} struct` 구문을 사용한다.

Go에서는 `implements` 키워드가 없다. 대신, 구조체에 인터페이스를 구현하려면, 해당 인터페이스의 메서드를 구조체에 정의하면 된다.  
(특정 타입이 인터페이스에서 요구하는 메서드를 구현하면, 해당 타입은 해당 인터페이스를 구현한 것으로 간주된다.)

```go
type Dog struct {
    Name string
}

func (d Dog) Speak() string {
    return "Woof!"
}
```

---

### Go에서 Mocking하기

Go에서는 인터페이스를 사용하여 Mocking을 할 수 있다.

```go
type Animal interface {
    Speak() string
}

type MockAnimal struct {
    SpeakFunc func() string
}

func (m MockAnimal) Speak() string {
    return m.SpeakFunc()
}
```

위 방식이 Go에서 Mocking을 하는 일반적인 방법이다.

---

# Go의 구조체 임베딩(Struct Embedding)

Go에서는 클래스 상속이 없다.  
대신, 구조체 임베딩을 통해 다른 구조체의 필드와 메서드를 직접 포함하여 재사용할 수 있다.

> 즉, 구조체 임베딩은 상속과 비슷한 개념이지만, 실제로는 구성(Composition)을 활용한 기능이다.

```go
package main

import (
    "fmt"
)

type Animal struct {
    Name string
}

func (a Animal) Speak() string {
    return "..."
}

type Dog struct {
    Animal // Animal 구조체를 임베딩
    Breed string
}
```

Dog 구조체가 Animal을 익명 필드로 포함(Emedding)하고 있다.  
Dog 내부에서 Animal의 필드와 메서드를 직접 사용할 수 있다. (d.Name, d.Speak())

> 구조체 임베딩과 일반 필드의 차이
> 1. 선언 방식이 다르다.  
>    - 일반 필드: `Name string` // 필드명과 타입을 명시적으로 선언
>    - 임베딩 필드: `Animal` // 필드명을 생략하고 타입만 선언
> 2. 임베딩한 구조체(Animal)를 해당 객체(Dog)를 통해 바로 접근할 수 있다.  
>    (`d.Name`, `d.Speak()` // Animal 구조체의 필드와 메서드에 접근)  
>    일반 필드는 필드명을 통해 접근한다.  
>    (`d.Breed`)

---