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