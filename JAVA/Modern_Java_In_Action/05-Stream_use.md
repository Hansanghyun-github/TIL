## 스트림 활용

### 1. 필터링

#### 1-1 Predicate로 필터링

Predicate는 제네릭 변수 T를 받아 불리언을 반환하는 메소드 test를 가지고 있는 함수형 인터페이스

filter() 메서드의 파라미터로 Predicate를 입력해서 필터링한다.

#### 1-2 고유 요소 필터링

distinct() 메서드를 사용하면 고유한 요소만 필터링된다.
> 고유 여부는 스트림에서 만든 객체의 hashCode, equals로 결정된다

### 2. 스트림 슬라이싱

#### 2-1 Predicate를 이용한 슬라이싱

`TAKEWHILE 활용`

정렬된 데이터를 필터링할때 사용하는 메서드

takewhile 메서드를 filter 대신 사용가능
> takewhile을 사용하는 스트림은 정렬되어 있어야 한다.

takewhile은 프레디케이트가 처음으로 거짓이 되는 지점까지 발견된 요소만 필터링한다.

`DROPWHILE 활용`

takewhile과 정반대의 작업을 수행한다.

dropwhile은 프레디케이트가 처음으로 거짓이 되는 지점까지 발견된 요소를 버린다.

> dropwhile은 무한한 남은 요소를 가진 무한 스트림에서도 동작한다.

#### 2-2 스트림 축소

limit(n) 메서드는 주어진 값 이하의 크기를 갖는 새로운 스트림을 반환한다.

#### 2-3 요소 건너뛰기

skip(n) 메서드는 처음 n개 요소를 제외한 스트림을 반환한다.

> n개 이하의 요소를 포함하는 스트림에 skip(n)을 호출하면 빈 스트림이 반환된다.

### 3. 매핑

특정 객체에서 특정 데이터를 선택하는 작업을 매핑이라 한다.

스트림 API의 map과 flatMap 메서드가 이에 해당하는 메서드이다.

#### 스트림 평면화

map을 이용해서 객체에서 특정 데이터를 선택하는 작업을 수행할 수 있다.

이때 ```stream<String[]>``` 을 ```stream<String>``` 으로 변환하고 싶을때 Arrays.stream과 flatMap을 활용한다.

Arrays.stream : array를 스트림으로 변환해주는 함수 ```String[]``` -> ```stream<String>```

flatMap 메서드는 스트림의 각 값을 다른 스트림으로 만든 다음에 모든 스트림을 하나의 스트림으로 연결하는 기능을 수행한다.

일반 map 메서드 활용 => (String)str.stream().map(word -> word.split(" ")) : ```stream<String[]>```

Arrays.stream 활용 => (String)str.stream().map(word -> word.split(" ")).map(Arrays::stream) : ```stream<stream<String>>```

마지막으로 flatMap까지 활용 => (String)str.stream().map(word -> word.split(" ")).flatMap(Arrays::stream) : ```stream<String>```

### 4. 검색과 매칭

```anyMatch``` boolean을 반환하는 최종 연산 메서드. 스트림에서 적어도 한 요소가 일치하는지 확인한다.

```allMatch``` boolean을 반환하는 최종 연산 메서드. 스트림에서 모든 요소가 일치하는지 확인한다.

```noneMatch``` allMatch와 반대 연산 수행(일치하는 요소가 없는지 확인한다)

> 위 세 메서드는 스트림 쇼트서킷 기법, 즉 자바의 &&, ||와 같은 연산을 활용한다.
>
>쇼트서킷: 전체 스트림을 처리하지 않았더라도 결과를 반환하는 프로세스
>>ex) if(a==0 && b==0)에서 a가 0이 아니라면, b의 값과 상관없이 조건문의 결과가 false이므로 b를 체크하기 전에 if문을 탈출한다.

```findAny``` 현재 스트림에서 임의의 요소를 반환하는 최종 연산 메서드

```findFirst``` 스트림의 첫번째 요소를 반환한다.

(일부 스트림에는 논리적인 아이템 순서가 정해져 있을 수 있다)

> 💡 findAny vs findFirst
>
>병렬 실행에서 첫번째 요소를 찾는건 어렵다. 따라서 요소의 반환 순서가 상관없다면 병렬 스트림에서는 제약이 적은 findAny를 써야한다

### 5. 리듀싱

모든 스트림 요소를 처리해서 값으로 도출하는 연산을 리듀싱 연산이라 한다.

reduce 메서드는 (a, b) -> 리턴값 함수를 파라미터로 받는다.

초깃값을 첫 파라미터로 설정 가능

초깃값이 없다면 Optional로 반환됨
> 스트림에 객체가 없을수 있기 때문

> reduce를 이용하면 내부 반복이 추상화되면서 내부 구현에서 병렬로 reduce를 실행할 수 있게 됨

### 6. 스트림 연산: 상태 없음과 상태 있음

map, filter 등은 입력 스트림에서 각 요소를 받아 0 또는 결과를 출력 스트림으로 보낸다.<br>
이 두 메서드들은 보통 상태가 없는, 즉 내부 상태를 갖지 않는 연산이다.(stateless operation)

반면 sorted나 distince 같은 연산은 이전 메서드들과는 다르게, 과거의 이력을 알고 있어야 한다. 이말은 모든 요소가 버퍼에 추가되어 있어야 한다. 이러한 연산은 내부상태를 갖는 연산이다.(stateful operation)

### 7. 숫자형 스트림

일반적인 ```List<Integer> list```의 합계를 구할때는 다음과 같은 스트림을 이용한다.<br>
```list.stream().reduce(0, (a,b) -> a+b) or .reduce(Integer::sum)```

사실 이코드에는 박싱 비용이 숨어있다.<br>
그렇다면 박싱 비용을 피할 수 있는 기능이 있다면 좋지 않을까?

스트림 API는 기본형 특화 스트림을 제공한다.

#### 7-1 기본형 특화 스트림

자바 8에서는 세가지 기본형 특화 스트림을 제공한다.

스트림 API에서는 박싱 비용을 피할 수 있도록 IntStream, DoubleStream, LongStream을 제공한다.

각각의 인터페이스는 숫자 스트림의 sum, max와 같이 자주 사용하는 숫자 관련 리듀싱 연산 수행 메서드를 제공한다.

또한 필요할때 다시 객체 스트림으로 복원하는 기능도 제공한다.

특화 스트림은 오직 박싱 과정에서 일어나는 효율성과 관련 있으며 스트림에 추가 기능을 제공하지는 않는다.

스트림을 특화 스트림으로 변환할 때는 mapToInt, mapToDouble, mapToLong 세가지 메서드를 가장 많이 사용한다.
> mapToInt -> IntStream 반환

> mapToObj -> stream<Object> 반환

`객체 스트림으로 복원하기` - boxed 메서드 사용

`OptionInt`

최댓(솟)값을 구할때 OptionalInt, OptionalDouble, OptionalLong이 반환된다.<br>
```OptionalInt max = menu.stream().mapToInt(Dish::getCalories).max()```

#### 7-2 숫자 범위

IntStream과 LongStream에서는 range와 rangeClosed라는 두가지 static 메서드를 제공한다.<br>
두 메서드 모두 첫번째 인수로 시작값을, 두번쨰 인수로 종료값을 갖는다.

> range 메서드는 시작값과 종료값을 포함하지 않는다.<br>
> rangeClosed 메서드는 시작값과 종료값을 포함한다.

### 스트림 만들기

Stream.of를 이용해서 스트림을 만들 수 있다.

Stream.empty() => 빈 스트림 생성

Arrays.stream(arr) => 배열로 스트림 만들기

iterate(0, n -> n+2) => 무한스트림

generate 메서드 => Supplier를 인수로 받아서 무한스트림 생성

> 무한스트림은 takeWhile, limit 메서드를 이용해서 제한해야 한다.












