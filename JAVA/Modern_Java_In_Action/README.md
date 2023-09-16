# 1 자바 8에 큰 변화가 생긴 이유

1. 멀티코어 프로세서의 파워를 충분히 활용해야 한다. 

    빅데이터라는 개념이 나오면서 멀티코어 프로세서나 컴퓨터 클러스터를 이용해서 빅데이터를 효과적으로 처리할 필요성이 커졌다.

2. 데이터 소스를 이용해서 주어진 조건과 일치하는 모든 데이터를 추출하고, 결과에 어떤 연산을 적용하는 등 선언형으로 데이터를 처리하는 방식, 즉 간결하게 데이터 컬렉션을 다루는 것이 추세가 되고 있다.

    함수형 프로그래밍을 도입하기 위해 자바 8에 큰 변화가 생겼다.

# 2 동적 파라미터화

우리가 어떤 상황에서 일을 하든, 소비자의 요구사항은 항상 바뀐다.

동적 파라미터화를 이용하면 자주 바뀌는 요구사항에 효과적으로 대응할 수 있다.

동적 파라미터화란 `아직은 어떻게 실행할 것인지 결정하지 않은 코드 블록`을 의미한다.

```java
public interface ApplePredicate {
	boolean test(Apple apple);
}

public List<Apple> filterApple(List<Apple> apples, ApplePredicate p){
    // ApplePredicate를 파라미터로 받는다.
    // test 함수를 통해 apple들의 값을 비교하면서 filter 수행한다.
    ...
}
```

이렇게 동작 파라미터화, 즉 메서드가 다양한 동작(또는 전략)을 받아서 내부적으로 다양한 동작을 수행할 수 있다.

# 3 람다 표현식

람다 표현식은 `메서드로 전달할 수 있는 익명 함수를 단순화한 것`을 의미한다.

> 익명 클래스 예시
> ```java
> new ApplePredicate<Apple>(){
>     public bool test(Apple a1, Apple a2){   
>         ...
>     }
> }
> ```

람다 표현식은 이름은 없지만, 파라미터 리스트, 바디, 반환 형식, 발생할 수 있는 예외 리스트를 가지고 있다.

### 람다의 특징

1. 익명 - 보통의 메서드와 달리 이름이 없다. 구현해야할 코드가 줄어든다.
2. 함수 - 람다는 메서드처럼 특정 클래스에 종속되지 않으므로 함수라고 부른다.
    > 하지만 메서드처럼 파라미터 리스트, 바디, 반환형식, 가능한 예외 클래스를 포함한다.
3. 전달 - 람다 표현식을 메서드 인수로 전달하거나 변수로 저장할 수 있다.
4. 간결성 - 익명 클래스처럼 많은 코드를 구현할 필요가 없다.

```java
filterApple(apples, (Apple a) -> a.getWeight() > 150);
// apples에서 무게가 150을 넘는 사과만 반환
```

### 함수형 인터페이스

함수형 인터페이스란 `정확히 하나의 추상 메서드를 지정하는 인터페이스`
> Comparaotr, Runnable 등이 있다.

### 람다에서 지역 변수 사용

람다 표현식에서는 자유 변수(외부에서 정의된 변수)를 활용할 수 있다. 이와 같은 동작을 '람다 캡쳐링'이라고 부른다.

자유 변수에는 제약이 있다. 해당 지역 변수는 한번만 할당되어야 한다. - 마치 final처럼

### 메서드 참조

메서드 참조를 이용하면 기존의 메서드 정의를 재활용해서 람다처럼 전달할 수 있다.

```
a.getWeight() => Apple::getWeight
```

# 4 스트림

스트림이란 `데이터 처리 연산을 지원하도록 소스에서 추출된 연속된 요소`

연속된 요소: 특정 요소 형식으로 이루어진 연속된 값 집합의 인터페이스를 제공
> 컬렉션의 주제는 데이터고, 스트림의 주제는 계산이다

소스: 컬렉션 배열 I/O 자원 등의 제공 소스로부터 데이터를 소비한다. 
(리스트로 스트림을 만들면 리스트의 순서가 그대로 유지된다)

데이터 처리 연산: 데이터베이스와 비슷한 연산을 지원한다.
스트림 연산은 순차적으로 혹은 병렬로 실행할 수 있다

스트림을 이용하면 선언형으로 데이터를 처리할 수 있다.
> 선언형: 데이터를 처리하는 임시 구현 코드 대신 짏의형으로 처리하는 것

## 스트림의 특징

1. 파이프파이닝: 대부분의 스트림 연산은 스트림 연산끼리 연결해서 커다란 파이프라인을 구성할 수 있도록 스트림 자신을 반환한다. 그덕분에 lazy 연산, 쇼트서킷 같은 최적화도 얻을 수 있다.

2. 내부 반복: 반복자를 이용해서 명시적으로 반복하는 컬렉션과 달리, 스트림은 내부 반복을 지원한다.
    > 컬렉션은 외부 반복

### 스트림 연산

중간 연산 - filter, map, limit -> lazy 연산

최종 연산 - forEach, collect

# 5 스트림 활용

`filter`, `takewhile`, `dropwhile`

`limit`, `skip`

`map`, `flatMap`

`anyMatch`, `allMAtch`, `noneMatch`, `findAny`, `findFirst`

`reduce`


    스트림 연산에서 상태 없음과 상태 있음

    map, filter 등은 입력 스트림에서 각 요소를 받아 0 또는 결과를 출력 스트림으로 보낸다.<br>
    이 두 메서드들은 보통 상태가 없는, 즉 내부 상태를 갖지 않는 연산이다.(stateless operation)

    반면 sorted나 distince 같은 연산은 이전 메서드들과는 다르게, 과거의 이력을 알고 있어야 한다. 이말은 모든 요소가 버퍼에 추가되어 있어야 한다. 이러한 연산은 내부상태를 갖는 연산이다.(stateful operation)
    -> 이 연산들은 병렬 데이터 처리에서 안좋은 성능을 보여준다.

### 기본형 특화 스트림

`IntStream`, `DoubleStream`, `LongStream`

박싱, 언박싱 문제를 해결해주는 스트림들

# 6 스트림으로 데이터 수집

collect()에서 grouping을 통해 결과를 내가 원하는대로 세팅하는 것

# 7 병렬 데이터 처리

컬렉션에 parallelStream을 호출하면 병렬 스트림이 생성된다.

    iterate()쓰면 병렬 의미 없음!
    오히려 더 느려짐

    IntStream의 range쓰면 병렬 처리 가능

>

### 병렬화 유의할 점
하지만 병렬화가 완전 공짜는 아니라는 사실을 기억하자. 병렬화를 이용하려면 스트림을 재귀적으로 분할해야 하고, 각 서브스트림을 서로 다른 스레드의 리듀싱 연산으로 할당하고, 이들 결과를 하나의 값으로 합쳐야 한다.

멀티코어 간의 데이터 이동은 생각보다 비싸다. 따라서 코어간의 데이터 전송시간보다 훨씬 오래 걸리는 작업만 병렬로 다른 코어에서 수행하는 것이 바람직하다.

그리고 공유 데이터에 동시에 접근하면 문제가 발생한다.

    확신이 서지 않는다면 직접 측정하자

# 8 컬렉션 API 개선

List.of 팩토리 메서드를 이용해서 간단하게 리스트 만들 수 있음
> 요소를 추가하는 것뿐만 아니라, 요소를 바꾸려하면(set 메서드) UnsupportedOperationException이 발생
>
> 기존의 Arrays.asList()는 요소를 추가하는 것만 막는다<br>(요소를 갱신하는 작업은 안막음)

Set.of Map.of Map.ofEntries

List,Set의 removeIf, replaceAll, sort

Map의 forEach, getOrDefault

등등 다양한 편리한 메서드 나옴

# 9 리팩토링, 테스팅, 디버깅

람다 표현식과 스트림 API를 통해 코드의 가독성과 유연성이 많이 개선됨
> 명령형 프로그래밍을 선언형 프로그래밍으로

    유감스럽게도 람다 표현식은 이름이 없기 때문에 복잡한 스택 트레이스가 생성된다.

### 정보 로깅

스트림의 파이프라인에 적용된 각각의 연산(filter, map, limit 등)이 어떤 결과를 도출하는지 확인할 수 있는 스트림 연산이 있다.

`peek`은 스트림의 각 요소를 소비한 것처럼 동작을 실행한다. 하지만 forEach처럼 실제로 스트림의 요소를 소비하지는 않는다. peek은 자신이 확인한 요소를 파이프라인의 다음 연산으로 그대로 전달한다.

# 10 DSL(도메인 전용 언어)

도메인 전용 언어(domain-specific languages, DSL)

DSL은 `특정 비즈니스 도메인의 문제를 해결하려고 만든 언어`
> 특정 비즈니스 도메인을 인터페이스로 만든 API라고 생각할 수 있다

DSL을 개발할 때는 두가지가 필요하다.

1. 의사 소통의 왕: 우리의 코드의 의도가 명확히 전달되어야 하며 프로그래머가 아닌 사람도 이해할 수 있어야 한다.
2. 한 번 코드를 구현하지만 여러 번 읽는다: 가독성은 유지보수의 핵심이다. 항상 우리의 동료가 쉽게 이해할 수 있도록 코드를 구현해야 한다.

> DSL은 코드의 비즈니스 의도를 명확하게 하고 가독성을 높인다는 점에서 약이 된다.
>
> 반면 DSL 구현은 코드이므로 올바르게 검증하고 유지보수해야하는 책임이 따른다.

DSL은 다음과 같은 장점을 제공한다.
1. 간결함
2. 가독성
3. 유지보수
4. 높은 수준의 추상화
5. 집중 - 프로그래머가 특정 코드에 집중할 수 있다. 결과적으로 생산성이 좋아진다.
6. 관심사분리

반면, DSL로 인해 다음과 같은 단점도 발생한다.
1. DSL 설계의 어려움: 간결하게 제한적인 언어에 도메인 지식을 담는 것은 쉬운 작업은 아니다.
2. 개발 비용
3. 추가 우회 계층
4. 새로 배워야 하는 언어
5. 호스팅 언어 한계

    스프링 시큐리티 SecurityConfig 설정할때도 DSL을 활용함

# 11 null 대신 Optional 클래스

null 문제를 해결하기 위해 자바 8에서는 `java.util.Optional<T>`라는 새로운 클래스를 제공한다.

Optional을 활용하면 더 좋은 API를 설계할 수 있다.<br>
사용자는 메서드의 시그니처만 보고도 Optional값이 사용되거나 반환되는지 예측할 수 있다.

# 12 새로운 날짜와 시간 API

자바 8 이전 버전에서 제공하는 기존의 java.util.Date 클래스와 관련 클래스에서는 여러 불일치점들과 가변성, 어설픈 오프셋, 기본값, 잘못된 이름 결정 등의 설계 결함이 존재했다.

새로운 날짜와 시간 API에서 날짜와 시간 객체는 모두 불변이다.

    java.time 패키지

    LocalDate, LocalTime, Instant, Duration, Period

# 13 디폴트 메서드

인터페이스에 새로운 메서드를 추가하면 어떻게 될까.<br>
-> 해당 인터페이스를 구현했던 모든 클래스의 구현도 고쳐야 한다. -> 끔찍하다.

자바 8에서는 기본 구현을 포함하는 인터페이스를 정의하는 두가지 방법을 제공한다.

1. 인터페이스 내부에 정적 메서드를 사용

2. 인터페이스의 기본 구현을 제공할 수 있도록 디폴트 메서드 기능을 사용

디폴트 메서드의 정의는 default 키워드로 시작하며 일반 클래스 메서드처럼 바디를 갖는다.

디폴트 메서드를 이용하면 기존에는 불가능했던 동작 다중 상속 기능도 구현할 수 있다.

# 14 자바 모듈 시스템

//

# 15, 16, 17 CompletableFuture와 리액티브 프로그래밍(Flow API)

다양한 기능을 선언형으로 이용할 수 있도록 자바 8에서 새로 제공하는 CompletableFuture 클래스(Future 인터페이스를 구현한 클래스)

Stream과 CompletableFuture는 비슷한 패턴, 즉 람다 표현식과 파이프라이닝을 활용한다.

    따라서 Future와 CompletableFuture의 관계를 Collection과 Stream의 관계에 비유할 수 있다.

디폴트 메서드를 통해 여러 비동기 동작을 조립하고 조합할 수 있다. (thenApply, thenCompose, thenCombine)

---

Future는 `한번`만 실행해 결과를 제공한다.

반면 리액티브 프로그래밍은 시간이 흐르면서 여러 Future 같은 객체를 통해 여러 결과를 제공한다.

자바 9에서는 java.util.concurrent.Flow의 인터페이스에 발행-구독 모델을 적용해 리액티브 프로그래밍을 제공한다.

# 18, 19 함수형 프로그래밍

프로그램으로 시스템을 구현하는 방식은 크게 두 가지로 구분할 수 있다.

첫번째는 작업을 어떻게 수행할 것인지에 집중하는 방법이 있다. 이처럼 어떻게(how)에 집중하는 프로그래밍 형식은 고전의 객체지향 프로그래밍에서 이용하는 방식이다.

    ex) 리스트에서 가장 비싼 트랜잭션을 계산해라
    1. 리스트에서 트랜잭션을 가져와서 가장 비싼 트랜잭션과 비교
    2. 가져온 트랜잭션이 가장 비싼 트랜잭션보다 비싸다면 가져온 트랜잭션이 가장 비싼 트랜잭션
    3. 리스트의 다음 트랜잭션으로 지금까지의 과정을 반복

때로는 이를 명령형 프로그래밍이라고 부르기도 한다.

'무엇을'에 집중하는 방식을 `선언형 프로그래밍`이라고 부른다. 선언형 프로그래밍에서 우리가 원하는 것이 무엇이고 시스템이 어떻게 그 목표를 달성할 것인지 등의 규칙을 정한다.

    문제 자체가 코드로 명확하게 드러난다는 점이 선언형 프로그래밍의 강점이다.

함수형 프로그래밍은 선언형 프로그래밍의 대표적인 방식이며, 부작용이 없는 계산을 지향한다. '선언형 프로그래밍'과 '부작용을 멀리한다'는 두가지 개념은 좀더 쉽게 시스템을 구현하고 유지보수하는 데 도움을 준다.

### 함수형 프로그래밍 기법

`고차원 함수`<br>
고차원 함수란 한 개 이상의 함수를 인수로 받아서 다른 함수로 반환하는 함수다. 자바에서는 comparing, andThen, compose 등의 고차원 함수를 제공한다.

`커링`<br>
커링은 함수를 모듈화하고 코드를 재사용할 수 있도록 지원하는 기법이다.

`패턴 매칭`

패턴 매칭은 자료형을 언랩하는 함수형 기능이다. 자바의 switch문을 일반화할 수 있다.

f(0) = 1<br>
f(n) = n * f(n-1) // n > 0

위 형식이 패턴 매칭이다.


# 20 OOP와 FP의 조화: 자바와 스칼라 비교

자바와 스칼라는 객체지향과 함수형 프로그래밍 모두를 하나의 프로그래밍 언어로 수용한다. 두 언어 모두 JVM에서  실행되며 넓은 의미에서 상호운용성을 갖는다.

스칼라는 자바에 비해 풍부한 함수 관련 기능을 제공한다. 스칼라는 함수 형식, 지역 변수에 접근할 수 있는 클로저, 내장 커링 형식 등을 지원한다.