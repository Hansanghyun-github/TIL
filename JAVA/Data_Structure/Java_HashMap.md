# HashMap

https://d2.naver.com/helloworld/831311 참조



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

|--|HASHMAP|HASHTABLE|CONCURRENTHASHMAP|
|--|--|--|--|
|key와 value에 null 허용|O|X|X|
|동기화 보장(Thread-safe)|X|O|O|
|추천 환경|싱글 쓰레드|멀티 쓰레드|멀티 쓰레드|