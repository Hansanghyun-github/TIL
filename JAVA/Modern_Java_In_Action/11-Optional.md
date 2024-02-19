# 11. null 대신 Optional 클래스

## 11.1 값이 없는 상황

null을 참조하려고 할대 NullPointerException이 발생한다.

**`null 때문에 발생하는 문제`**

1. 에러의 근원이다.

2. 코드를 어지럽힌다.

3. 아무 의미가 없다.

4. 자바 철학에 위배된다.
    > 자바는 개발자로부터 모든 포인터를 숨겼다. 하지만 null 포인터는 예외다.

5. 형식 시스템에 구멍을 만든다
    > 모든 참조 형식에 null을 할당할 수 있다. - 이게 문제

null 문제를 해결하기 위해 자바 8에서는 `java.util.Optional<T>`라는 새로운 클래스를 제공한다.

## 11.2 Optional 클래스 소개

Optional은 선택형값을 `캡슐화`하는 클래스이다.

    Optional<Car>은 해당 객체 안에 Car가 있을 수 있고 null(?)이 있을 수 있다.

값이 있으면 Optional 클래스는 값을 감싼다.<br>
반면 값이 없으면 Optional.empty 메서드로 Optional을 반환한다.

    Optional.empty 특별한 싱글턴 인스턴스를 반환하는 정적 팩토리 메서드

---

    그렇다고 무조건 null 참조를 Optional로 대처하는 것은 바람직하지 않다.

    Optional의 역할은 더 이해하기 쉬운 API를 설계하도록 돕는 것이다.

    ex) 
    메서드의 반환 타입이 String이라면 무조건 문자열이 있다고 예측할 수 있고,
    메서드의 반환 타입이 Optional<String>이라면 문자열이 있을수도 있고 없을수도 있다고 예측할 수 있다.

    -> 메서드의 시그니처만 보고도 선택형값인지 여부를 구별할 수 있다.

---

## 11.3 Optional 적용 패턴

### 11.3.1 Optional 객체 만들기

`빈 Optional` - Optional.empty()

`null이 아닌 값으로 Optional 만들기` - Optional.of(object)

`null 값으로 Optional 만들기` - Optional.ofNullable(object)<br>
(object가 null이면 빈 Optional 객체가 반환된다.)

### 11.3.2 맵으로 Optional의 값을 추출하고 변환하기

Optional의 get 메서드를 이용하면 해당 객체 안의 값을 받을 수 있는데, <br>
이 경우는 null을 사용할 때와 다른게 없다.

이런 유형의 패턴에 사용할 수 있도록 Optional은 map 메서드를 지원한다.

```java
Optional<Insurance> optInsurance = Optional.ofNullable(insurance);
Optional<String> name = optInsurance.map(Insurance::getName);
```

Optional의 메서드는 스트림의 map 메서드와 개념적으로 비슷하다.

    스트림의 map은 스트림의 각 요소에 제공된 함수를 적용하는 연산
    Optional 객체를 최대 요소의 개수가 한개이하인 데이터 컬렉션이라고 생각할 수 있음

Optional이 비어있으면 아무 일도 일어나지 않는다.

### 11.3.3 flatMap으로 Optional 객체 연결

만약 위코드에서 optInsurance.map(Insurance::getName)다음으로 추가 메서드를 설정하려고 하는데,<br>
Insurance 클래스의 name의 타입이 `Optional<String>`이라면 어떻게 될까?

```java
Optional<Optional<String>> name = optInsurance.map(Insurance::getName);
```

이처럼 `Optional<Optional<String>>`이 반환된다.

Optional 클래스가 두번 감싸져있기 때문에, 다음으로 추가 메서드를 설정하는건 매끄럽지 못할 것이다.

이때 `flatMap`을 사용하면 매끄럽게 대처가능하다.

```java
Optional<String> name = optInsurance.flatMap(Insurance::getName);
```

(스트림의 flatMap처럼) 생성된 모든 Optional이 하나의 Optional로 병합되어 평준화된다.

    flatMap 역시 내부 객체가 null이라면 Optional.empty가 반환된다.

---

    '도메인 모델에 Optional을 사용했을 때 데이터를 직렬화할 수 없는 이유'

    자바 언어 아키텍트는 Optional의 용도가 선택형 반환값을 지원하는 것이라고 명확하게 못박았다.

---

### 11.3.4 Optional 스트림 조작

```java
public Set<String> getCarInsuranceNames(List<Person> persons) {
    return persons.stream()
     .map(Person::getCar) // Person -> Optional<Car>
     .map(optCar -> optCar.flatMap(Car::getInsurance)) // Optional<Car> -> Optional<Insurance> (1)
     .map(optInsurance -> optInsurance.map(Insurance::getName)) // Optional<Insurance> -> Optional<String>
     .flatMap(Optional::stream) // Optional<String> -> Stream<String> (2)
     .collect(toSet()); // Stream<String> -> Set<String>
}
```

(1) flatMap을 통해 `Optional<Optional<Insurance>>`을 `Optional<Insurance>`로 평준화

(2) Optional이 stream() 메서드를 지원하기 때문에, Optional -> Stream으로 변환

    여기서 Optional 내의 객체가 비어있다면 Optional.empty를 반환,
    null 걱정없이 안전하게 Stream으로 변환 가능하다.

하지만 빈 Optional이 있을 수도 있기 떄문에, 이를 제거해야 한다.

```java
Stream<Optional<String>> stream = ...
Set<String> result = stream.filter(Optional::isPresent) // 빈 Optional은 여기서 멈춤
                            .map(Optional::get)
                            .collect(toSet());
```

위 코드처럼 빈 Optional을 제거할 수 있다.

### 11.3.5 디폴트 액션과 Optional 언랩

Optional 클래스는 Optional 인스턴스에 포함된 값을 읽는 다양한 방법을 제공한다.

`get()` - 값을 읽는 메서드. 가장 간단한 메서드

    값이 없으면 NoSuchElementException이 발생한다.

`orElse(T other)` Optional이 값을 포함하지 않을 때 기본값을 제공한다.

`orElseGet(Supplier<? extends T> other)` orElse 메서드의 게으른 버전. Optional에 값이 없을때만 Supplier가 실행된다.

`orElseThrow(Supplier<? extends X> exceptionSupplier)` Optional이 비어있을 때 예외를 발생시킨다. get과 비슷, 하지만 이 메서드는 발생시킬 예외의 종류를 선택할 수 있다.

`ifPresent(Consumer<? extends T> consumer)` 값이 존재할 때 인수로 넘겨준 동작을 실행

`ifPresentOrElse(Consumer<? super T> action, Runnable emptyAction)` (자바 9에 추가됨) Optional이 비어있을때 Runnable을 실행

### 11.3.6 두 Optional 합치기

그냥 if문으로 두 Optional이 present라면 값넣어주고, 아니라면 Optional.empty 반환함

## 11.4 Optional을 이용한 실용 예제

1. 잠재적으로 null이 될수 있는 대상을 Optional로 감싸기

    맵에 키에 해당하는 value가 있을 지 모른다면 Optional로 감싸준다.

2. 예외와 Optional 클래스

    문자를 정수로 변환할때 NumberFormatException이 발생할 수 있음
    이를 try, catch와 Optional.empty를 이용해 안전하게 전달 가능
    ```java
    try{
        return Optional.of(Integer.parseInt(s));
    } catch(NumberFormatException e){
        return Optional.empty();
    }
    ```

    굳이 이렇게 감싸지 않아도, OptionalUtility.stringToInt를 쓰면 간단하게 사용가능하다.

3. 기본형 Optional은 사용하지 말자

    OptionalInt, OptionalLong, OptionalDouble은 filter, map 등을 못쓴다. 별로임

## 11.5 마치며

자바 8에서는 값이 있거나 없음을 표현할 수 있는 `java.util.Optional<T>` 클래스를 제공한다.

Optional.empty, Optional.of, Optional.ofNullable 등을 이용해서 Optional 객체를 만들 수 있다.

Optional 클래스는 스트림과 비슷한 연산을 수행하는 map, flatMap, filter 등의 메서드를 제공한다.

Optional을 이용하면 예상치 못한 null 예외를 방지할 수 있다.

Optional을 활용하면 더 좋은 API를 설계할 수 있다.<br>
사용자는 메서드의 시그니처만 보고도 Optional값이 사용되거나 반환되는지 예측할 수 있다.

























