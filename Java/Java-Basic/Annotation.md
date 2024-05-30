# Annotation

### 어노테이션이란?

어노테이션은 다른 프로그램에게 유용한 정보를 제공하기 위해 사용되는 것으로 주석과 같은 의미를 가진다.

---

### 어노테이션의 역할
- 컴파일러에게 문법 에러를 체크하도록 정보를 제공한다.
- 프로그램을 빌드할 때 코드를 자동으로 생성할 수 있도록 정보를 제공한다.
- 런타임에 특정 기능을 실행하도록 정보를 제공한다.

---

### 어노테이션의 구성

```
@Target(ElementType.{적용대상})
@Retenttion(RetentionPolicy.{정보유지되는 대상})
public @interface {어노테이션명}{
    ...
}
```

@Retention: 주석 보존 기간을 지정한다.
1. SOURCE: 컴파일 전까지만 유효
2. CLASS: 컴파일러가 클래스를 참조할 때까지 유효
3. RUNTIME: 컴파일 이후 런타임 시기에도 JVM에 의해 참조가 가능(리플렉션)

@Target: 주석이 나타날 수 있는 구문 위치를 나타낸다.
1. TYPE: 타입 선언
2. FIELD: 멤버 변수 선언
3. CONSTRUCTOR: 생성자 선언
4. METHOD: 메서드 선언

등등 많이 있다.


@Target별 예시  
```
@TypeAnnotation // (1)
Class Example{
    @FieldAnnotation // (2)
    private int exampleField

    @ConstructorAnnotation // (3)
    public Example(int i){ ... }

    @MethodAnnotation // (4)
    public methodExample( ... ){ ... }
}
```

---

### 어노테이션이 동작하는 원리

(Source 기준)  
대표적으로 롬북의 어노테이션들이 있는데,  
어노테이션이 붙어 있는 클래스들에 롬북이 직접 바이트 코드를 넣어준다.

(Runtime 기준)  
어노테이션은 리플렉션에 의해 동작한다.

1. 리플렉션을 통해 클래스나 메서드, 파라미터 정보를 가져온다.
2. 리플렉션의 getAnnotation(s), getDeclaredAnnotation(s) 등의 메서드를 통해 원하는 어노테이션이 붙어 있는지 확인한다.
3. 어노테이션이 붙어 있다면 원하는 로직을 수행한다.

---

### 커스텀 @Autowired를 통해 어노테이션 동작 원리 이해하기

직접 코딩해봐서 알아보자

```java
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Autowired {
}
```
직접 만든 커스텀 Autowired<br>
멤버 변수 앞에서만 선언 가능하다

```java
public class OrderService {
    @Autowired
    public OrderRepository orderRepository;
}

public class OrderRepository {
}
```

OrderService가 OrderRepository를 의존하고 있다.

이떄 커스텀 @Autowired를 이용해서 주입해줘야 한다.

```java
public class ApplicationContext {

    public static <T> T getInstance(Class<T> clazz) throws Exception{
        T instance = createInstance(clazz);
        Field[] fields = clazz.getDeclaredFields();
        for (Field field : fields) {
            if(field.getAnnotation(Autowired.class) != null){
                Object fieldInstance = createInstance(field.getType());
                field.setAccessible(true);
                field.set(instance, fieldInstance);
            }
        }
        return instance;
    }

    private static <T> T createInstance(Class<T> clazz) throws Exception{
        return clazz.getConstructor().newInstance();
    }
}
```

```createInstance```<br>
인자로 받은 클래스를 생성해주는 메서드<br>
(리플렉션 API을 통해 직접 생성자로 생성한다)

```getInstance```<br>
인자로 받은 클래스 타입에 맞는 인스턴스를 생성하고, 그 인스턴스의 필드들을 순회한다.<br>
필드들을 순회하면서, 커스텀 @Autowired 어노테이션이 붙어있다면, 그 필드에 맞는 인스턴스를 생성 & 해당 필드에 주입<br>
(여기서 private일 수 있으므로, setAccessible을 통해 접근 가능하게 함)<br>
마지막으로 해당 인스턴스를 반환한다.


```
OrderService orderService = ApplicationContext.getInstance(OrderService.class);
assertNotNull(orderService);
assertNotNull(orderService.orderRepository);
```

테스트 코드의 일부

```ApplicationContext```의 ```getInstance```를 이용해서 OrderService를 받아온다.<br>
이때 커스텀 @Autowired 덕분에 OrderRepository를 주입 받은 OrderService 인스턴스를 받아온다.

---

