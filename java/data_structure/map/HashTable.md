# HashTable

키(key)를 값(value)에 매핑하는 Map 인터페이스의 구현체이다.

(null이 아닌 모든 객체는 키나 값으로 사용될 수 있다)

> HashTable에서 객체를 성공적으로 저장 or 조회하려면 키로 사용되는 객체는 
> equals & hashcode 메서드를 구현해야 한다.

해시 테이블의 인스턴스에는 성능에 영향을 미치는 두개의 파라미터, initial capacity & load factor가 있다.

capacity: 해시 테이블에 있는 버킷의 수  
(initial capacity는 처음 해시 테이블이 생성 됐을 때의 버킷의 수)

load factor: 해시 테이블의 용량이 자동으로 증가하기 전에 얼마나 가득 차도록 허용되는지를 측정하는 척도

> 실제 HashTable은 capacity라는 변수가 있지 않고, threshold 라는 변수가 있다.  
> (threshold = capacity * load factor) 
> 
> 처음 HashTable을 생성할 때 입력한 capacity로 table의 크기를 결정하고,  
> threshold로 재해시 여부를 결정한다.
> 
> 재해시할 때, 새 capacity는 (기존 capacity * 2 + 1)로 결정한다.

---

## HashTable의 메서드들

> HashTable의 대부분의 메서드(Map의 메서드를 오버라이딩하는 메서드) 앞에 synchronized라는 단어가 붙어 있다.
>
> > 심지어 size(), isEmpty() 메서드에도 synchronized가 붙어 있다.
>
> 그래서 thread-safe 지만, (다른 Map 구현체보다) 성능이 안좋다.

boolean containsKey(K key) - key가 테이블에 있는지 반환, O(1)

boolean containsValue(V value) - value가 테이블에 있는지 반환, O(n) (n = 테이블의 크기)

> 모든 테이블을 조회 함(키로 조회할 수 없기 때문에)

V get(Object key) - key에 해당하는 값을 반환, O(1)

V put(K key, V value) - `<K, V>` 엔트리를 HashTable에 추가, O(1)  
, 키에 해당하는 자리에 값이 있다면 그 자리를 차지하고 그 값을 반환, 없다면 null 반환

> 만약 현재 size가 threshold보다 커지면 재해시 한다. -> O(n) (n = 테이블의 크기)

Object remove(K key) - key에 해당하는 엔트리 삭제, O(1)  
삭제하는 value를 반환

---

## HashTable의 iterator

HashTable의 메서드에서 반환하는 iterator는 fail-fast다.

> fail-fast: iterator를 통해 조회하다가, 다른 스레드가 HashTable을 수정한다면, 빠르게 예외를 발생시키고 동작을 중단시킨다.

하지만 이 예외를 가정하고 프로그램을 만드는 것은 잘못된 것이라고 한다.

> (해시테이블의 메서드에서 반환되는 `열거형(Enumeration)`은 fail-fast가 아니다)

---

## HashTable의 충돌 전략(Optional)

키 값은 다르지만, 해시 값이 같을 때  
(해시 충돌이 일어난 상황)  
separate chainning 방식(연결 리스트 방식)으로 값이 추가된다.