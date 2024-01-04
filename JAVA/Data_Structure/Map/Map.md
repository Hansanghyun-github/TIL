# Map

> map은 mapping의 map을 의미함  
> (mapping: 하나의 값을 다른 값에 대응하다)

> 자바 Map 인터페이스는, Dictionary abstract 클래스를 대체한다.  
> (Dictionary는 자바1에 등장했고, Map은 자바2에 등장했다)  
> (HashTable은 지금도 Dictionary를 상속 받고 있다)

`Map<K, V>`  
키(Key)와 값(Value) 한 쌍으로 이루어진 자료형  
키를 값에 매핑하는 object

> 값은 중복될 수 있지만, 키는 고유한 값을 가져야 한다.

Map interface는 3개의 컬렉션 뷰를 제공한다.  
(keys set, values collection, key-value mappings set)  
(키는 고유한 값을 가지기 때문에 set으로 제공되지만, value는 중복이 허용 되기 때문에 collection으로 제공된다)

TreeMap 클래스와 같은 일부 맵 구현 클래스는 순서를 보장한다.  
HashMap 클래스는 순서를 보장하지 않는다.

---

> mutable 객체를 키로 사용할 때는 주의 해야 한다.  
> (가변 객체가 맵의 키로 있는 동안 값이 변경되면, map의 동작을 예상하기 힘들다)
>
> & 맵의 키로 사용되는 객체는 equals & hashcode 메서드를 잘 정의 해놔야 한다.

> 모든 맵 구현 클래스는 빈 생성자와, 동일한 인수(Map<K, V>)를 받는 생성자 두가지를 정의해놔야 한다.  
> (후자는 동등(equal)한 Map을 반환)

---

## Map의 구현체들

1. HashTable
2. HashMap
3. TreeMap
4. ConcurrentHashMap

...