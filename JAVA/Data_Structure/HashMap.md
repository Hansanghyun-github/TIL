# HashMap

https://d2.naver.com/helloworld/831311 참조

> HashMap 성능
>
> 자바 8에서는 HashMap의 내부 구조를 바꿔 성능을 개선했다.<br>
> 기존의 맵의 항목은 키로 생성한 해시코드로 접근할 수 있는 버켓에 저장했다.<br>
> 많은 키가 같은 해시코드를 반환하는 상황이 되면 O(n)의 시간이 걸리는 LinkedList로 버킷을 반환해야 하므로 성능이 저하된다.<br>
> 최근에는 버킷이 너무 커질 경우 이를 O(logn)의 시간이 소요되는 정렬된 트리를 이용해 동적으로 치환해 충돌이 일어나는 요소 반환 성능을 개선했따. 하지만 키가 String, Number 클래스 같은 Comparable의 형태여야만 정렬된 트리가 지원된다.

### HashMap
key와 value에 null을 허용한다.
동기화를 보장하지 않는다.
> thread-safe하지 않아 싱글스레드 환경에서 사용하는게 좋다<br>
>동기화 처리를 하지 않기 때문에 데이터를 탐색하는 속도가 빠르다

> -> HashTable과 ConcurrentHashMap보다 데이터를 찾는 속도는 빠르지만, 신뢰성과 안정성이 떨어진다.

### HashTable
key와 value에 null을 허용하지 않는다.
동기화를 보장한다.
> thread-safe하기 때문에, 멀티 쓰레드 환경에서 사용할 수 있다

> 데이터를 다루는 메소드에 synchronized가 붙어있다<br>
이 키워드는 메소드를 호출하기전에 쓰레드간 락을 건다.

> 멀티쓰레드 환경에서도 무결성을 보장하지만, 락 때문에 성능이 안좋음

### ConcurrentHashMap
key와 value에 null을 허용하지 않는다.
동기화를 보장한다.
> thread-safe하기 때문에, 멀티 쓰레드 환경에서 사용할 수 있다

HashMap의 동기화 문제를 보완하기 위한 자료구조

어떤 Entry를 조작하는 경우에 해당 Entry에 대해서만 락을 건다.

-> HashTable보다 데이터를 다루는 속도가 빠르다.

>즉, Entry 아이템별로 락을 걸어 멀티 쓰레드 환경에서의 성능을 향상시킨다.

>ConcurrerntHashMap 클래스는 동시성 친화적이며 최신 기술을 반영한 HashMap 버전이다.
>
>이 클래스는 내부 자료구조의 특정 부분만 잠궈(synchronized) 동시 추가, 갱신 작업을 허용한다.
>
>따라서 동기화된 Hashtable 버전에 비해 읽기 쓰기 연산 성능이 월등하다.
>> 참고로 표준 HashMap은 비동기로 동작함

---

|--|HASHMAP|HASHTABLE|CONCURRENTHASHMAP|
|--|--|--|--|
|key와 value에 null 허용|O|X|X|
|동기화 보장(Thread-safe)|X|O|O|
|추천 환경|싱글 쓰레드|멀티 쓰레드|멀티 쓰레드|