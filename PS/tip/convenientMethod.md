## lower_bound, upper_bound

algorithm 헤더에서 제공하는 메서드

lower_bound: 주어진 값 이상을 처음으로 만나는 위치를 반환  
upper_bound: 주어진 값보다 큰 값을 처음으로 만나는 위치를 반환

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

> 그리고 lower_bound, find 메서드를 사용할 때
> 
> 해당 컨테이너의 원소의 타입이 기본 값이 아니라면,  
> 추가로 기본 생성자와 < operator를 선언해줘야 한다.

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

그리고 find 메서드는 컨테이너를 순차적으로 탐색하기 때문에 O(n)이라  
정렬된 컨테이너를 탐색할 때는 lower_bound가 더 효율적이다.  
(map, set 컨테이너의 find 메서드는 O(logn))

> 이분탐색을 이용하는 binary_search 메서드가 있지만,  
> 이 메서드는 해당 값이 있는지 없는지 bool 타입을 반환하므로, 해당 값을 참조할 수 없다.

> 연결리스트는 lower_bound, binary_search의 효과를 볼 수 없다.  
> 실행은 되지만 비효율적이다 - O(n) not O(logn)  
> 임의 접근이 안되기 때문에 순차적으로 탐색한다.

### find, binary_search, lower_bound 정리

| 시간 복잡도 표 |find|binary_search|lower_bound| 비고  |
|------|--|--|--|-----|
| array, vector |O(n)|O(logn)|O(logn)||
| list |O(n)|O(n)|O(n)|임의 접근이 불가능해서 전부 O(n)|
|map, set|O(logn)|x|O(logn)|algorithm 헤더가 아닌 내장 메서드를 이용한다|

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
> 모든 노드를 탐색하는데의 시간복잡도는 O(nlogn)  
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
> ```it = list.remove(it)```  
> (자바는 자동 업데이트 됨)
> 
> iterator를 사용하다 보면 에러를 자주 만날 수 있다.
> 1. end()에서 ++ 연산을 했을 때
> 2. begin()에서 -- 연산을 했을 때
> 3. remove한 iterator를 사용할 때
> 
> 항상 주의하자
> 

---

### next_permutation

(algorithm 헤더에서 제공하는 메서드)

n개의 원소를 가지고 있는 컨테이너(배열도 가능)의  
(오름차순 기준) 다음 순열을 구해주는 함수

항상 오름차순으로 정렬되어 있는 컨테이너를 기준으로 한다.

파라미터
(첫번째 원소의 위치, 마지막 원소의 다음 위치) - (v.begin(), v.end())  
(첫번째 원소의 위치, 마지막 원소의 다음 위치, 비교 함수) - (v.begin(), v.end(), compare)

비교 함수  
해당 컨테이너의 원소가 기본타입이 아닐때(or 특정 조건으로 비교할 때)  
이를 비교해주기 위한 비교 함수가 필요하다.  
```
bool compare(Infor i1, Infor i2){
   return i1.x < i2.x;
   // 오른쪽이 클 때 true를 반환해야 오름차순으로 순열 제공 됨
}
```

`언제 사용할까`  
역시 순열이 필요할 때 사용한다.  
이 메서드를 실행하면 다음 순열이 컨테이너에 입력되기 때문에, do-while문을 주로 사용  
```
do{
   // 제공된 순열(v) 이용해 코딩
} while(next_permutation(v.begin(), v.end(), compare));
```

조합은 어떻게 만들까?  
방법은 있지만, 조합은 그냥 for문으로 일일이 구해주는게 나는 편하다.  
```
// arr의 원소를 이용해 조합 결과를 result에 넣음

void combination(int n, int r) { // 몇번째 원소부터 시작하는지, 몇번째 선택인지
	if (r == R) {
		// result를 가지고 코딩		
		return;
	}
	for (int i = n; i < N; i++) {
		result.push_back(arr[i]);
		permutation(i + 1, r + 1); // i+1번째 원소부터 시작, r+1만큼 뽑았다고 표시
		result.pop_back();
	}
}
```

> 내림차순 순열을 구해주는 prev_permutation 메서드도 있지만,  
> next_permutation만 생각하는게 편하다고 생각함
> 
> 1. 둘다 생각하면 헷갈려서 오히려 시간 낭비 될 수 있음
> 2. 컨테이너가 내림차순 된 상태에서 next_permutation을 실행하기 위해,  
>    정렬을 해도 시간복잡도는 괜찮음 - O(nlgn)  
>    (오히려 순열 구하는 시간복잡도가 더 높음 - O(n!))

