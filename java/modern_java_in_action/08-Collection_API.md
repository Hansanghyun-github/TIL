# 컬렉션 API 개선

## 1. 컬렉션 팩토리

Arrays.asList() 팩토리 메서드 -> 작은 요소를 포함하는 리스트를 만들어줌<br>
```List<String> list = Arrays.asList("ab", "ac", "bc")```
> 여기서 요소를 갱신하는 작업은 괜찮지만 요소를 추가하려면 UnsupportedOperationException이 발생

> `UnsupportedOperationException이 발생하는 이유`<br>
내부적으로 고정된 크기의 변환할 수 있는 배열로 구현되어있기 때문에

#### Set을 만드는 방법
Arrays.asSet()이라는 팩토리 메서드는 없다.

1. 리스트를 인수로 받는 HashSet 생성자를 사용
    ```new HashSet<>(Arrays.asList("ac", "ab", "bc"))```
2. 스트림 API 사용
    ```Stream.of("ac", "ab", "bc").collect(Collectors.toSet())```

하지만 두 방법 모두 내부적으로 객체 할당을 필요로 한다.

### 1-1 리스트 팩토리

List.of 팩토리 메서드를 이용해서 간단하게 리스트 만들 수 있음
> 요소를 추가하는 것뿐만 아니라, 요소를 바꾸려하면(set 메서드) UnsupportedOperationException이 발생

이 제약이 나쁜것만은 아님 -> 컬렉션이 의도치 않게 변하는 것을 막을 수 있기 때문
> 하지만 요소 자체가 변하는 것을 막을 수 있는 방법은 없다

### 1-2 집합 팩토리

Set.of 를 이용해서 Set을 생성 가능
> set이라서 중복된 요소가 감지되면 IllegalArgumentException이 발생

### 1-3 맵 팩토리
맵을 만드는 것은 리스트나 집합에 비해 복잡하다
> 키와 값이 있어야 하기 때문

Map.of 팩토리 메서드에 키와 값을 번갈하 제공하는 방법으로 맵을 만들 수 있다<br>
```Map.of("key1", "value1", "key2", "value2", ...)```

10개 이하의 키와 값쌍을 가진 맵을 만들떄는 이 메서드가 유용

그 이상은 Map.ofEntries를 사용하자<br>
```Map.ofEntries(entry("", ""), ...)```
> 이 메서드는 키와 값을 감쌀 추가 객체 할당을 필요로 함

---

위 메서드들은 자바 9의 새로운 팩토리 메서드들이다.

---

## 2. 리스트와 집합 처리

자바 8에서는 List, Set 인터페이스에 다음과 같은 메서드를 추가했다.

1. removeIf: Predicate를 만족하는 요소를 제거한다.
2. replaceAll: 리스트에서 이용할 수 있는 기능. UnaryOperator 함수를 이용해 요소를 바꾼다
3. sort: 리스트를 정렬

이들 메서드는 호출한 컬렉션 자체를 바꾼다.
> 새로운 결과를 만드는 스트림 동작과 달리 이들 메서드는 기존 컬렉션을 바꾼다.

컬렉션을 바꾸는 동작은 에러를 유발하여 복잡함을 더한다.

#### `왜 이런 메서드가 추가됐을까?`

### 2-1 removeIf 메서드

```java
for(Transaction transaction: transactions){
    if(Character.isDigit(transaction.getReferenceCode().charAt(0))) 
        transactions.remove(transaction);
}
```

숫자로 시작되는 참조 코드를 가진 트랜잭션을 삭제하는 코드

위 코드는 ConcurrentModificationException을 일으킨다.

`왜그럴까?`

내부적으로 for-each 루프는 Iterator 객체를 사용하므로 위 코드는 다음과 같이 해석된다.

```java
for(Iterator<Transaction> iter = transactions.iterator();iter.hasNext()){
    Transaction transaction = iter.next();
    if(Character.isDigit(transaction.getReferenceCode().charAt(0))) 
        transactions.remove(transaction); // 반복하면서 별도의 두 객체를 통해 컬렉션을 바꾸고 있는 문제
}
```
두 개의 개별 객체가 컬렉션을 관리한다.
1. Iterator 객체 next(), hasNext()를 이용해 소스를 질의한다.
2. Collection 객체 자체 remove()를 호출해 요소를 삭제한다.

`결과적으로 반복자의 상태는 컬렉션의 상태와 서로 동기화되지 않는다.`

Iterator 객체를 명시적으로 사용하고 그 객체의 remove() 메서드를 호출함으로 이 문제를 해결할 수 있다.

```java
for(Iterator<Transaction> iter = transactions.iterator();iter.hasNext()){
    Transaction transaction = iter.next();
    if(Character.isDigit(transaction.getReferenceCode().charAt(0))) 
        iterator.remove();
}
```

이 코드 패턴은 자바 8의 ```removeIf``` 메서드로 바꿀 수 있다.
> 그러면 코드가 단순해질 뿐 아니라 버그도 예방할 수 있다.

```java
transactions.removeIf(transaction -> Character.isDigit(transaction.getReferenceCode().charAt(0)));
```

### 2-2 replaceAll 메서드

스트림 API를 사용하면 문제를 해결할 수 있지만, 새 컬렉션을 만들게 된다.<br>
우리가 원하는 것은 기존 컬렉션을 바꾸는 것이다.

자바 8에 추가된 replaceAll 메서드를 사용하면 간단하게 구현할 수 있다.

```java
referenceCode.replaceAll(code -> "원하는 형태")
```

## 3. 맵 처리

자바 8에서는 Map 인터페이스에 몇 가지 디폴트 메서드를 추가했다.

### 3-1 forEach 메서드

Biconsumer(키와 값을 인수로 받음)를 인수로 받는 메서드

코드를 조금 더 간단하게 구현할 수 있다.

```m.forEach((k,v) -> "원하는 코드")```

### 3-2 정렬 메서드

다음 두개의 새로운 유틸리티를 이용하면 맵의 항목을 값 또는 키를 기준으로 정렬할 수 있다.
1. Entry.comparingByValue
2. Entry.comparingByKey

```java
favoriteMovies
    .entrySet().stream().sorted(Entry.comparingByKey()).forEach()
```

> HashMap 성능
>
> 자바 8에서는 HashMap의 내부 구조를 바꿔 성능을 개선했다.<br>
> 기존의 맵의 항목은 키로 생성한 해시코드로 접근할 수 있는 버켓에 저장했다.<br>
> 많은 키가 같은 해시코드를 반환하는 상황이 되면 O(n)의 시간이 걸리는 LinkedList로 버킷을 반환해야 하므로 성능이 저하된다.<br>
> 최근에는 버킷이 너무 커질 경우 이를 O(logn)의 시간이 소요되는 정렬된 트리를 이용해 동적으로 치환해 충돌이 일어나는 요소 반환 성능을 개선했따. 하지만 키가 String, Number 클래스 같은 Comparable의 형태여야만 정렬된 트리가 지원된다.


### 3-3 getOrDefault 메서드

기존에는 찾으려는 키가 존재하지 않으면 null이 반환된다.

이 메서드는 첫번쨰 인수로 키를 ,두번쨰 인수로 기본값을 받으며 맵에 키가 존재하지 않으면 두번째 인수로 받은 기본값을 반환한다.

> 키가 존재하느냐의 여부에 따라서 두번째 인수가 반환될지 결정된다.

### 3-4 계산 패턴

자바 8에서는 키의 값이 존재하는지 여부를 확인할 수 있는 더 복잡한 몇개의 패턴도 제공한다.

computeIfAbsent: 제공된 키에 해당하는 값이 없으면, 키를 이용해 새 값을 계산하고 맵에 추가한다.

computeIfPresent: 제공된 키가 존재하면 새 값을 계산하고 맵에 추가한다.

compute: 제공된 키로 새 값을 계산하고 맵에 저장한다.

### 3-5 삭제 패턴

자바 8에서는 키가 특정한 값과 연관되었을때만 항목을 제거하는 오버로드 버전 메서드를 제공한다.

m.remove(key, value) - key에 해당하는 value가 두번째 인수와 같다면 해당 키값쌍을 제거
> 기존의 remove 메서드는 첫번쨰 인수만 받아서 첫번쨰 인수에 해당하는 키값쌍을 제거했다.
>
> 이 메서드는 조금더 상세하게 지시할 수 있다.

### 3-6 교체 패턴

replaceAll: BiFunction을 적용한 결과로 각 항목의 값을 교체한다. 
> List의 replaceAll과 비슷한 동작을 수행

Replace: 키가 존재하면 맵의 값을 바꾼다.

### 3-7 합침

두개의 맵을 하나의 맵으로 합칠때 merge 메서드를 이용할 수 있다.

이 메서드는 중복된 키를 어떻게 합칠지 결정하는 BiFunction을 인수로 받는다.

```moviesToCount.merge(movieName, 1L, (key, count) -> count + 1L)```<br>
moviesToCount 맵에 movieName이 key인 키값쌍을 넣는다.

key에 해당하는 value가 없다면 1L이 넣고,<br>
있다면 해당 value와 1L을 더해서 넣는다.

---

지금까지 Map 인터페이스에 추가된 기능을 확인했다. 맵의 사촌인 ConcurrentHashMap의 기능도 개선되었다.

---

## 4. 개선된 ConcurrentHashMap

ConcurrerntHashMap 클래스는 동시성 친화적이며 최신 기술을 반영한 HashMap 버전이다.

이 클래스는 내부 자료구조의 특정 부분만 잠궈(synchronized) 동시 추가, 갱신 작업을 허용한다.

따라서 동기화된 Hashtable 버전에 비해 읽기 쓰기 연산 성능이 월등하다.
> 참고로 표준 HashMap은 비동기로 동작함

### 4-1 리듀스와 검색

ConcurrentHashMap은 스트림에서 봤던 것과 비슷한 종류의 세가지 새로운 연산을 지원한다.

1. forEach: 각 (키,값) 쌍에 주어진 액션을 실행
2. reduce: 모든 (키,값) 쌍에 제공된 리듀스 함수를 이용해 결과로 합침
3. search: null이 아닌 값을 반환할때까지 각 (키,값) 쌍에 함수를 적용

네가지 연산 형태를 지원

1. 키, 값으로 연산(forEach, reduece, search)
2. 키로 연산(forEachKey, reduceKeys, searchKeys)
3. 값으로 연산(forEachValue, reduceValues, searchValues)
4. Map.Entry 객체로 연산(forEachEntry, reduceEntries, searchEntries)

이들 연산은 ConcurrentHashMap의 상태를 잠그지 않고 연산을 수행한다는 점을 주목하자
> 따라서 이들 연산에 제공한 함수는 계산이 진행되는 동안 바뀔 수 있는 객체, 값, 순서등에 의존하지 않아야 한다.

또한 이들 연산에 병렬성 기준값(threshold)을 지정해야 한다.<br>
맵의 크기가 주어진 기준값보다 작으면 순차적으로 연산을 진행한다.

### 4-2 계수

ConcurrentHashMap 클래스는 맵의 매핑 개수를 반환하는 mappingCount 메서드를 제공한다.
> 기존의 size 메서드 대신 새 코드에서는 int를 반환하는 mappingCount 메서드를 사용하는게 좋음
>
> -> 그래야 매핑의 개수가 int 범위를 넘어서는 이후의 상황을 대처할 수 있다.

### 4-3 집합뷰

ConcurrentHashMap을 집합 뷰로 반환하는 keySet이라는 새 메서드를 제공한다.

맵을 바꾸면 집합도 바뀌고 집합을 바꾸면 맵도 영향을 받는다.
> newKeySet이라는 새 메서드를 이용해 ConcurrentHashMap으로 유지되는 집합을 만들수도있다.

---

## 정리

기존 List.asList()를 이용했을때, 요소를 추가하면 예외가 발생했다.

자바 9에서 요소 추가뿐만 아니라 요소를 변경했을때 예외가 발생하는 List.of() 메서드가 추가됨
> 제약이 추가되면서 더 안전

Set.of()는 중복된 값이 들어가면 IllegalArgumentException 발생

Map.of는 키와 값을 순서대로 집어넣어야 함. Map.ofEntries()는 Map.Entry(키, 값)를 이용한 맵 생성

위 컬렉션 팩토리 메서드(자바 9에 추가됨)가 반환한 객체는 만들어진 다음 바꿀 수 없다.

List 인터페이스는 removeIf, replaceAll, sort 세가지 디폴트 메서드를 지원 - 자바 8에 추가됨

Set 인터페이스는 removeIf 디폴트 메서드를 지원 - 자바 8에 추가 됨

Map 인터페이스에 추가된 디폴트 메서드 - 자바 8에 추가 됨
> forEach((k,v) -> {})<br>
> Entry.comparingByValue, Entry.comparingByKey - 키 또는 값을 기준으로 정렬할때 사용<br>
> getOrDefault() -> 첫번째 인수인 키에 해당하는 value가 없다면 두번째 인수반환
> computeIfAbsent, computeIfPresent, compute 제공된 키가 있냐 없냐로 value 생성할지 말지<br>
> remove(key, value) - 해당 value가 있을때만 remove<br>
> merge - 중복되는 키가 있다면 세번쨰 인수를 수행

ConcurrerntHashMap은 MAp에서 상속받은 새 디폴트 메서드를 지원, 스레드 안전성도 제공


















