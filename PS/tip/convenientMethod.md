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

