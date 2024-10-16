## 스프링 DI(Dependency Injection)

스프링 DI(Dependency Injection, 의존성 주입)는 객체 간의 의존 관계를 스프링 프레임워크가 자동으로 설정해주는 기능이다.  

이를 통해 객체 간의 결합도를 낮추고,  
코드의 유연성과 테스트 용이성을 높일 수 있다.

### 주요 개념

1. 의존성(Dependency): 한 객체가 다른 객체를 필요로 하는 관계.
2. 주입(Injection): 필요한 객체를 외부에서 제공하는 방식.

### DI의 종류

1. 생성자 주입(Constructor Injection): 생성자를 통해 의존성을 주입.
2. 세터 주입(Setter Injection): 세터 메서드를 통해 의존성을 주입.
3. 필드 주입(Field Injection): 필드에 직접 의존성을 주입.

### 예제

#### 생성자 주입

```java
@Component
public class MyService {
    private final MyRepository myRepository;

    @Autowired
    public MyService(MyRepository myRepository) {
        this.myRepository = myRepository;
    }
}
```

> 생성자가 하나만 존재할 경우 `@Autowired` 어노테이션을 생략할 수 있다.

#### 세터 주입

```java
@Component
public class MyService {
    private MyRepository myRepository;

    @Autowired
    public void setMyRepository(MyRepository myRepository) {
        this.myRepository = myRepository;
    }
}
```

#### 필드 주입

```java
@Component
public class MyService {
    @Autowired
    private MyRepository myRepository;
}
```

### 장점

- 결합도 감소: 객체 간의 의존 관계를 외부에서 설정해주므로 결합도가 낮아짐.
- 유연성 증가: 객체의 변경이 용이해짐.
- 테스트 용이성: Mock 객체를 주입하여 테스트할 수 있음.

스프링 DI를 통해 객체 간의 관계를 설정하고 관리함으로써 코드의 유지보수성과 확장성을 높일 수 있습니다.

### 3가지 주입 방식 중 생성자 주입을 권장하는 이유

1. 불변성(Immutability): 생성자 주입을 사용하면 필드를 `final`로 선언할 수 있어 불변성을 보장할 수 있다.
2. 의존성 주입을 강제화: 객체 생성 시점에 의존성을 주입받기 때문에, 객체의 사용 전에 의존성이 주입되었는지 확인할 수 있다.
3. 순환 참조 방지: 생성자 주입을 사용하면 순환 참조를 방지할 수 있다.  
   (객체 생성 시점에 의존성을 주입받기 때문에, 순환 참조가 발생하면 런타임 에러가 발생한다. 따라서 미리 방지할 수 있다.)