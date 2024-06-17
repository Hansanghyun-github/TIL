> 스프링은 어떻게 실행 시점에 빈을 주입할 수 있는 걸까요?

> JPA의 Entity는 왜 꼭 기본 생성자를 가져야만 할까요?

# 리플렉션(Reflection)

> JVM은 클래스 정보를 클래스 로더를 통해 읽어와서 해당 정보를 JVM 메모리에 저장한다. 그렇게 저장된 클래스에 대한 정보가 마치 거울에 투영된 모습과 닮아있어, 리플렉션이라는 이름을 가지게 되었다.<br>
(실체=Class, 거울=JVM 메모리영역)

자바에서 리플렉션은 런타임 중에 프로그램의 클래스, 메서드, 필드 및 기타 요소를 검사하고 조작할 수 있는 기능입니다.<br>
런타임에 클래스, 인터페이스, Enum 및 주석의 구조에 대한 정보를 얻을 수 있는 방법을 제공합니다

```java

```

> 어노테이션은 그 자체로는 아무 역할도 하지 않는다. 리플렉션 덕분에 우리가 스프링에서 @Component , @Bean 과 같은 어노테이션을 프레임워크의 기능을 사용하기 위해 사용할 수 있는 것이다.

---

### Class 클래스

리플렉션의 핵심은 ```Class``` 클래스이다.

```Class```는 실행중인 자바 어플리케이션의 클래스와 인터페이스의 정보를 가진 클래스

```Class```의 기능들
1. 클래스에 붙은 어노테이션 조회
2. 클래스 생성자 조회
3. 클래스 필드 조회
4. 클래스 메서드 조회
5. 부모 클래스, 인터페이스 조회

```Class```의 특징
1. public 생성자가 존재하지 않는다.
2. Class 객체는 JVM에 의해 자동으로 생성된다.

Class 객체 획득 방법

```java
Class<Member> aClass = Member.class; // (1)

Member member1 = new Member();
Class<? extends Member> bClass = member1.getClass(); // (2)

Class<?> cClass = Class.forName("hudi.reflection.Member"); // (3)
```

(1) {클래스타입}.class<br>
(2) {인스턴스}.getClass()<br>
(3) Class.forName("{전체 도메인 네임})

---

### getMethods vs getDeclaredMethods

getMethods: 상위 클래스와 상위 인터페이스에서 상속한 메서드를 `포함`하여 `public`인 메서드들을 모두 가져온다.

getDeclaredMethods: `접근 제어자에 관계 없이` 상속한 메서드를 `제외`하고 `직접 클래스에서 선언한` 메서드들을 모두 가져온다.

|-|getXXX|getDeclaredXXX|
|--|--|--|
|접근 제어자|public|관계 없음|
|상속 포함|포함|제외|

---

### 리플렉션 기능

클래스 예시

```java
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Member {
    private static final String CATEGORY = "사람";

    public int age;
    private String name;

    public Member(final String name){
        this.name=name;
        age=0;
    }

}
```

1. 생성자

```java
Class<?> clazz = Class.forName("com.example.demo.Member");
Constructor<?> c1 = clazz.getDeclaredConstructor();
Constructor<?> c2 = clazz.getDeclaredConstructor(String.class);
Constructor<?> c3 = clazz.getDeclaredConstructor(int.class, String.class);
```

위 코드처럼 생성자를 찾을 수 있다.
> 이때 파라미터 순서도 중요함.<br>
> 순서 안맞으면 NoSuchMethodException 발생

```java
Object o1 = c1.newInstance();
Member o2 = (Member)c2.newInstance("WOW");
```

newInstance 메서드를 통해 객체 생성 가능<br>

> 이때 생성자가 private라면 접근이 불가능해 에러 터짐
>
> -> ```c1.setAccessible(true);```를 통해 private에도 접근 가능

2. 필드 정보 조회

```java
Object m1 = c3.newInstance(20, "Hello");

Field[] fields = clazz.getDeclaredFields();
Arrays.stream(fields).forEach(f -> {
    f.setAccessible(true);
    System.out.println(f);
    System.out.println("value: "+f.get(m1));
});
```

필드의 접근제어자, 타입, 네임, 값 등의 정보를 조회할 수 있다.

```java
Object m1 = c3.newInstance(20, "Hello");

Field[] fields = clazz.getDeclaredFields();
Field name = clazz.getDeclaredField("name");
name.setAccessible(true);
System.out.println("기존: "+name.get(m1));
name.set(m1, "World");
System.out.println("변경: "+name.get(m1));
```

private 필드의 값도 변경할 수 있다.

3. 메서드


```java
class Member{
...
    private void MyName(){
        System.out.println("My Name is "+name);
    }
...
}

Method method = clazz.getDeclaredMethod("MyName");
method.setAccessible(true);
method.invoke(m1);

```

메서드를 찾은 후 ```invoke``` 메서드를 통해 해당 메서드를 실행 할 수 있다.

---

### getModifiers

이 메서드는 클래스, 필드, 메서드를 정수로 반환한다.

이를 java.lang.reflect.Modifier 클래스의 정적 메서드를 이용해 해석할 수 있다.

특정 클래스가 public abstract로 선언되었다면,  
`Modifier.isPublic(modifiers)`, `Modifier.isAbstract(modifiers)`는 true를 반환한다.  
그 외는 false를 반환한다.

---

### 리플렉션이 사용되는 곳

라이브러리나 프레임워크에서 많이 사용한다.<br>
(컴파일 시점엔 객체의 타입을 모르기 때문에 리플렉션을 이용한다)

1. JPA
2. Mockito
3. JUnit
등 다양하다.

> 많은 프레임워크나 라이브러리에서 객체의 기본생성자가 필요한 이유
>
> 기본 생성자로 객체를 생성하고, 필드를 통해 값을 넣어주는 것이 가장 간단한 방법이기 때문
>
> 1. 기본 생성자가 없다면, 어떤 생성자를 사용할지 고르기 어렵다.
> 2. 생성자에 로직이 추가되어있다면, 원하는 값을 바로 넣어줄 수 없다.
> 3. 파라미터의 타입이 같은 경우 필드와 이름이 다르면 값을 알맞게 넣어주기 힘들다.

그리고 어노테이션도 리플렉션에 의해 동작한다.<br>
(자세한 건 Annotation에서 참고)

---

### 리플렉션의 단점

1. 일반 메서드 호출보다 성능이 훨씬 떨어진다.
> Reflection API는 컴파일 시점이 아니라 런타임 시점에서 클래스를 분석한다.
>
> => JVM을 최적화할 수 없기 때문에 성능저하 발생
2. 컴파일 시점에서 타입 체크 기능을 사용할 수 없다.
> 리플렉션은 런타임 시점에 클래스 정보를 알게 되기 떄문에, 알맞은 클래스가 아니라면 ClassNotFoundException이 발생한다.
3. 코드가 지저분하고 장황해진다.
4. 내부를 노출해서 추상화를 파괴한다. & 불변성도 지킬 수 없게 된다.

---

### 리플렉션은 아주 제한된 상태로만 사용해야 한다.

