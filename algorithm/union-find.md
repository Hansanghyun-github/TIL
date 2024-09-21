# union-find 알고리즘

## Disjoin Set (분리 집합)
분리집합이란 교집합이 존재하지 않는 두개 이상의 집합을 뜻한다.

> {1,2,3}, {4} 두 집합은 분리집합
>
> {1,2}, {2,3,4} 두 집합은 분리집합이 아니다 (2가 겹침) 

---

## Union-Find 알고리즘이란

Union-Find란 분리집합을 표현하기 위한 알고리즘

분리집합 연산은 두가지가 있음

1. find(x)

    x가 속한 집합의 대표값(루트노드)을 반환

    -> x가 어떤 집합에 속해있는지 찾는 연산

2. union(x, y) // x, y는 노드의 번호

    합집합 연산

    x가 속한 집합과 y가 속한 집합을 합친다.


---

## Union-Find 실제 코드

실제 코드에서, Union-Find 알고리즘을 트리로 구현한다.

자식노드가 부모노드를 가리키게 되어 있다.

```cpp
int parent[MAX_NODE];
// 인덱스 번호가 자식노드의 번호, 배열의 값은 해당 노드의 부모노드를 의미함

parent[0] = 0;  // 루트노드 (인덱스 번호와 해당 값이 같음)
parent[1] = 0;  // 부모노드가 0
parent[2] = 0;  // 부모노드가 0
parent[3] = 3;  // 루트노드 (인덱스 번호와 해당 값이 같음)

// 여기서 {0,1,2}와 {3}은 분리집합
```

```cpp
// 맨처음 parent 배열의 값들은 자기 자신의 번호로 초기화 되어있음
int parent[MAX_NODE];

int find(int x) {
    if (x == parent[x]) {
        return x;
    } else {
        return find(parent[x]);
    }
}

void union(int x, int y){
    x = find(x);
    y = find(y);

    parent[y] = x;
}

```

---

### 각 메서드의 시간복잡도

find(x) - $O(lgn)$

해당 노드가 속합 집합(트리)의 대표값(루트노드)를 반환하는 메서드

최대 트리의 높이만큼 걸린다.

union(x) - $O(lgn)$

find() 메서드를 2번 사용

---

## 추가적인 Union-Find 알고리즘 최적화

분리집합은 두 집합사이의 관계에만 의미가 있다.
> 두 집합이 분리집합인지 아닌지

한 집합 내에서, 원소들끼리의 관계는 의미가 없다.

-> 이를 이용해서 트리의 높이를 낮춰서 시간복잡도를 줄일 수 있다.

### 1 - Find 메서드 최적화

Find 메서드를 실행할때 특정 원소의 부모노드를 루트노드로 바꿔주면서 트리의 높이를 낮춰줄 수 있다.

```cpp
int find(int x) {
    if (x == parent[x]) {
        return x;
    } else {
        return parent[x] = find(parent[x]); 
        // x의 부모노드를 루트노드로 변환
        // -> x가 리프노드라면 해당 트리의 높이가 낮아질 수 있다
        // -> 다음 Find 메서드를 호출할때 시간복잡도가 감소한다.
    }
}
```

### 2 - Union 메서드 최적화

Union 메서드를 실행할때, 마지막에서, 높이가 더 낮은 트리를 높은 트리

-> 항상 높이가 더 낮은 트리를, 더 높은 트리 밑에 넣는다

-> 전체 트리의 높이가 낮아져서 시간복잡도를 줄일 수 있음

```cpp
// nodeCount는 해당 노드가 속한 트리의 높이를 저장한 배열, 초깃값은 0

void Union(int x, int y) {
	int rx = Find(x);
	int ry = Find(y);

	if (nodeCount[rx] < nodeCount[ry]) {
		parent[rx] = ry;
	}
	else {
		parent[ry] = rx;

		if (nodeCount[rx] == nodeCount[ry])
			nodeCount[rx]++;
	}
}
```

> union 메서드를 최적화하는건 트레이드오프가 있다.
>
> 트리의 높이를 낮춰서 시간복잡도를 줄이지만, 각각의 노드마다 트리의 높이를 저장하는 배열을 추가적으로 선언해줘야 하기때문에, 공간복잡도가 조금 증가한다.

> 그냥 `rx < ry` 같은 간단한 비교로도 충분히 시간복잡도를 줄일 수 있다.

---

## 최종 코드

```cpp
vector<int> parent; // 초깃값 해당 인덱스 값 ( ex) parent[1]=1, parent[3]=3 )

int Find(int x) {   // 해당 노드의 루트노드를 반환하는 메서드
	if (x == parent[x])
		return x;
	else return parent[x] = Find(parent[x]);
}

void Union(int x, int y) {  // 두 노드가 속한 트리를 합하는 과정 (합집합)
	int rx = Find(x);
	int ry = Find(y);

	if (rx < ry)
		parent[rx] = ry;
	else
		parent[ry] = rx;
}
```