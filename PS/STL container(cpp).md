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
s.insert(e) - O(logn)

원소 삭제  
s.erase(iter) (다음을 가리키는 iter 반환) - O(logn)

원소 찾기  
s.count(e) - O(logn)  
s.find(e) (e를 가리키는 iter 반환) - O(logn)
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
s.insert({k,v}) - O(logn)

원소 삭제  
s.erase(iter) (다음을 가리키는 iter 반환) - O(logn)

원소 찾기  
s.count(k) (0 or 1 반환) - O(logn)  
s.find(k) (k를 가리키는 iter 반환) - O(logn)

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
s.insert({k,v}) - O(logn)

원소 삭제  
s.erase(iter) (다음을 가리키는 iter 반환) - O(logn)

원소 찾기  
s.count(k) - O(logn)  
s.find(k) (k를 가리키는 iter 반환) - O(logn)

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

원소 삽입/삭제 시간복잡도 O(1)

특정 원소 조회 시간복잡도 O(1)