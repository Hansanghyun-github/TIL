> vector, deque, list   
> queue, priority_queue,   
> set, multiset,   
> map, multimap,   
> unordered_set,   
> unordered_map

원소 조회

원소 삽입

원소 삭제

원소 찾기

> 코테에서 자주 사용할 메서드만 써놓았음

---

### vector

> 동적 배열(배열을 이용하는 컨테이너)

원소 조회  
v.get(i), v[i] - O(1)

원소 삽입  
v.push_back(e) (맨 끝에 삽입) - O(1)

원소 삭제
v.pop_back() (맨 끝 삭제) - O(1)

> 가장 많이 사용하는 컨테이너

---

### deque

> vector처럼 배열 기반이지만,  
> 여러개의 메모리 블록을 할당하고, 이를 하나의 블록처럼 여기는 기능을 제공

원소 조회  
dq[i] - O(1)

원소 삽입  
dq.push_front(e) (맨 앞에 삽입) - O(1)  
dq.push_back(e) (맨 끝에 삽입) - O(1)

원소 삭제  
dq.pop_front() (맨 앞 삭제) - O(1)  
dq.pop_back() (맨 끝 삭제) - O(1)

> 특정 위치 원소 조회를 자주하고  
> 양 끝단의 원소를 자주 삽입하거나 삭제할 때 사용

---

### list

> 이중 연결 리스트

원소 조회  
lt.front() (맨 앞 원소)  
lt.back() (맨 뒤 원소)

원소 삽입  
lt.push_back(e), lt.push_front(e)  
lt.insert(iter, k)

원소 삭제
lt.pop_back(), lt.pop_front()  
lt.erase(iter) // 다음 위치의 iter 반환

> 중간 위치의 원소 삭제/삽입이 잦을 때 사용

> 노드로 연결되어 있기 떄문에,  
> 조회는 iterator를 자주 이용

---

### queue

> deque에서 맨앞 삭제 & 맨뒤 추가 기능 없앤 컨테이너 (FIFO)

원소 조회  
q.front(), q.back() - O(1)

원소 삽입  
q.push(e) (맨 뒤 추가) - O(1)

원소 삭제  
q.pop() (맨 앞 삭제) - O(1)

---

### priority_queue

> 힙을 사용하는 컨테이너
> 
> 원소가 항상 크기순으로 정렬되어있다.

원소 조회  
pq.top() - O(1)

원소 삽입  
pq.push(e) - O(logn)

원소 삭제  
pq.pop() - O(logn)

> 크기 순으로 항상 정렬되어 있을 필요가 있을 때  
> 그리고 항상 가장 높은/낮은 값 필요할 때 사용

---

### set

> 레드-블랙 트리 기반 컨테이너
> 
> key만 저장되어 있다.  
> 항상 정렬되어 있다.
>
> 중복x

원소 삽입  
s.insert(e) - O(logn)

원소 삭제  
s.erase(iter) (다음을 가리키는 iter 반환) - O(logn)  
s.erase(e) - O(logn)

원소 찾기  
s.count(e) (0 or 1 반환) - O(logn)  
s.find(e) (e를 가리키는 iter 반환) - O(logn)

---

### multiset

> 레드-블랙 트리 기반 컨테이너
>
> key만 저장되어 있다.  
> 항상 정렬되어 있다.
>
> 중복 허용

원소 삽입  
ms.insert(e) - O(logn)

원소 삭제  
ms.erase(iter) (다음을 가리키는 iter 반환) - O(logn)  
ms.erase(e) - O(logn)

원소 찾기  
ms.count(e) - O(logn)  
ms.find(e) (e를 가리키는 iter 반환) - O(logn)
---

### map

> 레드-블랙 트리 기반 컨테이너
>
> key, value 쌍이 저장되어 있다.  
> 항상 정렬되어 있다.  
> (키를 기준으로 정렬)
> 
> 중복x

원소 삽입  
m.insert({k,v}) - O(logn)

원소 삭제  
m.erase(iter) (다음을 가리키는 iter 반환) - O(logn)  
m.erase(k) - O(logn)

원소 찾기  
m.count(k) (0 or 1 반환) - O(logn)  
m.find(k) (k를 가리키는 iter 반환) - O(logn)

> [] operator를 이용한 원소 조회/삽입 가능  
> m[k] = v

---

### multimap

> 레드-블랙 트리 기반 컨테이너
>
> key, value 쌍이 저장되어 있다.  
> 항상 정렬되어 있다.  
> (키를 기준으로 정렬)
>
> 중복 허용

원소 삽입  
mm.insert({k,v}) - O(logn)

원소 삭제  
mm.erase(iter) (다음을 가리키는 iter 반환) - O(logn)  
mm.erase(k) - O(logn)

원소 찾기  
mm.count(k) - O(logn)  
mm.find(k) (k를 가리키는 iter 반환) - O(logn)

> [] operator를 이용한 원소 조회/삽입 가능  
> m[k] = v


---

### unordered_set

> 해시 기반 컨테이너
>
> key만 저장되어 있다.  
> 정렬되어 있지 않다.

원소 삽입/삭제 시간복잡도 O(1)

특정 원소 조회 시간복잡도 O(1)

---

### unordered_map

> 해시 기반 컨테이너
>
> key, value 쌍이 저장되어 있다.  
> 정렬되어 있지 않다.
>
> 중복x

원소 삽입  
um.insert({k,v}) - O(1)

원소 삭제  
um.erase(iter) (다음을 가리키는 iter 반환) - O(1)  
um.erase(k) - O(1)

원소 찾기  
um.count(k) - O(1)  
um.find(k) (k를 가리키는 iter 반환) - O(1)

> [] operator를 이용한 원소 조회/삽입 가능  
> m[k] = v

---

> unordered_multimap과 unordered_multiset도 있다.

---

## lower_bound, upper_bound

algorithm 헤더에서 제공하는 메서드

lower_bound: 정렬된 데이터 집합에서 특정 값 이상이 처음으로 나타나는 위치를 반환  
upper_bound: 특정 값보다 큰 값이 처음으로 나타나는 위치를 반환

시퀀스 컨테이너에서 사용가능하다.

> 정렬된 컨테이너를 기준으로 사용하기 때문에,  
> 이분탐색을 이용하여,  
> 시간복잡도는 O(logn)에 해당한다.

> 내부적으로 트리를 사용하는 map이나 set은 자체 내장 메서드가 있다.  
> m.lower_bound(key)  
> s.lower_bound(key)

> 내부적으로 해시테이블을 사용하는 unordered_map이나 unordered_set은 lower_bound를 사용하면 안된다.  
> (정렬이 안되어 있기 때문)  
> 
> 대신 find 메서드를 사용하면 된다.

### find vs lower_bound

find 메서드는 해당 키에 해당하는 iterator를 반환한다.  
만약 해당 키에 대응하는 값이 없다면 end()를 반환한다.

lower_bound는 해당 키값보다 크거나 같은 것들 중에 가장 작은 값을 가리키는 iterator를 반환한다.

```
map<int,int> m;
m[5] = 15;
m.find(4); // m.end() 반환
m.lower_bound(4); // key 5를 가리키는 iterator 반환 
```

그리고 find 메서드는 컨테이너를 순차적으로 탐색하기 때문에 O(n)이라 lower_bound보다 비효율적이다.

> 이분탐색을 이용하는 binary_search 메서드가 있지만,  
> 이 메서드는 해당 값이 있는지 없는지 bool 타입을 반환하므로, 해당 값을 참조할 수 없다.

---

## iterator

컨테이너를 순회할 수 있게 해주는 객체

iterator의 장점
1. 컬렉션에서 요소를 제어하는 기능
2. ++ 및 -- 연산자를 써서 앞뒤로 이동하는 기능  
   (자바는 next(), previous() 메서드)

사용 예시  
```
for(vector<int>::iterator iter = v.begin(); iter != v.end(); iter++)
    cout<<*iter<<' ';
```  
v.begin()이 시작 원소 지점, v.end()가 끝에 있는 원소의 다음 지점

list의 특정 원소를 제거할 때 iter를 사용하면 O(1)에 삭제 가능  
(iter가 list의 원소를 가리키고 있기 때문)  
(물론 원하는 원소가 나올때까지 iter를 이용해서 탐색해야 한다)

> map이나 set도 iterator를 사용할 수 있다.
> 
> 시퀀스 컨테이너처럼 사용 가능하다.  
> (시퀀스 컨테이너와 같이) 모든 노드를 탐색하는데의 시간복잡도는 O(n)  
> (내부적으로 트리의 다음 노드를 탐색하는 것으로 구현되어 있다)
> 
> 사용 예시  
> ```
> for(auto it = m.begin(); it != m.end(); it++)
>   cout<<it->first<<','<<it->second<<' ';
> ```  
> first가 key, second가 value
> 
> (자바는 시퀀스 컨테이너만 iterator 사용가능)  
> (대신 map.entrySet()을 통해서 iterator처럼 사용)

> 주의할 점 
> 
> iterator를 사용해서 컨테이너의 원소를 remove하고, 다음 원소를 탐색할때는  
> 꼭 remove 메서드의 반환값으로 iterator를 업데이트해주자
> 
> ```it = list.remove(it)```
>
> (자바는 자동 업데이트 됨)

