# 세그먼트 트리

> N개의 원소를 가진 배열의 누적 합을 구하는 알고리즘의 시간복잡도는 O(n)이다.
> 
> 누적 합을 한번만 구한다면 문제가 되지 않지만, 
> 특정 범위의 값을 업데이트하는 행위와, 누적 합을 구하는 행위가  
> 빈번히 반복된다면
> 
> 누적 합 알고리즘으로 위 문제를 풀었을 때의 시간복잡도는 O(n^2)이 될 것이다.
> 
> 이떄 세그먼트 트리를 이용하면 시간복잡도를 O(nlogn)으로 줄일 수 있다.

## 방법

특정 범위의 원소의 합을 구한다면,  
일일이 더하지 말고,  
2, 4, 8, ..., $2^k$개의 원소를 더한 블록을 저장해놓는다.
이를 이용해 시간복잡도를 줄인다.

<img src="../../img/segTree_1.png" width="700">

> 1 2 3 4 5 6 7 의 합을 구한다.  
> -> 1+2+3+4 5+6 7 합을 저장  
> -> 3번의 연산 만으로 합을 구할 수 있다.
> (이건 그냥 간단한 예시)

$2^k$개의 원소를 더한 블록을 트리의 구조를 이용해 저장한다.

<img src="../../img/segTree_2.png" width="700">

## buildTree - 트리를 만드는 과정

트리를 표현할 벡터의 원소의 개수를 4n개로 설정해준다.(n = 입력 배열의 사이즈)  
(사실 대부분 2n개도 충분하지만, 원소의 개수가 2의 배수가 아닐 때를 생각해서 4n개로 설정해준다고 한다)

```cpp
int SegTree::merge(int a, int b) {
	return a + b; // 지금은 합을 구하는 트리, min이나 max도 가능하다. (gcd(최대공약수), lcm(최소공배수)도 가능하다)
}

int SegTree::buildTree(const int arr[], int index, int nodeLeft, int nodeRight) {
	// arr: 입력 원소 배열
	// index: 벡터에서 현재 노드의 번호
	// nodeLeft: 현재 노드가 포함하는 원소의 시작 번호
	// nodeRight: 현재 노드가 포함하는 원소의 마지막 번호
	if (nodeLeft == nodeRight)
		return node[index] = arr[nodeLeft];

	int mid = nodeLeft + (nodeRight - nodeLeft) / 2; // overflow 막는 계산(그냥 더하면 오버플로우 날 수 있음)
	
	int leftSum = buildTree(arr, index * 2, nodeLeft, mid);
	int rightSum = buildTree(arr, index * 2 + 1, mid + 1, nodeRight);
	return node[index] = merge(leftSum, rightSum);
}
```

맨 처음 buildTree를 호출할 때
index = 1 (세그먼트 트리의 root index)  
nodeLeft = 0 (입력 배열의 첫번째 인덱스)  
nodeRight = N-1 (입력 배열의 마지막 인덱스)

> buildTree 메서드의 시간복잡도는 O(n)이다.

---

## query

```cpp
int SegTree::query(int left, int right, int index, int nodeLeft, int nodeRight) {
	// left: 쿼리의 시작 값, right: 쿼리의 끝 값
	// index: 벡터에서 현재 노드의 번호
	// nodeLeft: 현재 노드가 포함하는 원소의 시작 번호
	// nodeRight: 현재 노드가 포함하는 원소의 마지막 번호

	// 재귀함수에서
	// left, right는 바뀌지 않음
	// index, nodeLeft, nodeRight는 계속 바뀜

	if (left > nodeRight || right < nodeLeft) // 쿼리가 현재 노드를 포함하지 않는다
		return 0; // sum일 때 default value
	// min, max면 그때 그때 달라져야 함 
	// min->엄청 큰값, max->엄청 작은 값

	if (left <= nodeLeft && right >= nodeRight) // 쿼리가 현재 노드에 있는 모든 값들을 전부 포함한다
		return node[index];

	int mid = nodeLeft + (nodeRight - nodeLeft) / 2;

	return merge(query(left, right, index * 2, nodeLeft, mid)
		, query(left, right, index * 2 + 1, mid + 1, nodeRight));
}
```

> query 메서드의 시간복잡도는 O(logn)이다.

---

## range update

```cpp
int SegTree::rangeUpdate(int left, int right, int value, int index, int nodeLeft, int nodeRight){
	// left: update할 원소의 시작 값, right: update할 원소의 끝 값
	// value: 업데이트 할 값(그냥 update가 아니라 + - 도 할 수 있다)
	// index: 벡터에서 현재 노드의 번호
	// nodeLeft: 현재 노드가 포함하는 원소의 시작 번호
	// nodeRight: 현재 노드가 포함하는 원소의 마지막 번호

    if(left > nodeRight || right < nodeLeft) // 이 영역은 업데이트하지 않는 영역
        return node[index];
        
    if(nodeLeft == nodeRight) // 하나의 원소만 업데이트 하면 된다.
        return node[index] = value;
        
    
	int mid = nodeLeft + (nodeRight - nodeLeft) / 2;
	int leftSum = buildTree(left, right, value, index * 2, nodeLeft, mid);
	int rightSum = buildTree(left, right, value, index * 2 + 1, mid + 1, nodeRight);
	return node[index] = merge(leftSum, rightSum);
}
```

> 현재 rangeUpdate 메서드의 시간복잡도는 O(n)이다.  
> (범위에 해당하는 모든 노드를 업데이트 하기 때문)

---

> 결국 세그먼트 트리가 누적 합보다 유용할 경우는  
> 특정 범위의 값을 업데이트하는 행위와, 누적 합을 구하는 행위가  
> 빈번히 반복될 때 유용하다.
> (구간 합을 한번만 구한다면 그냥 누적합을 사용하는 것이 나을 것이다)
> 
> 그런데 특정 범위의 값을 업데이트 해주는 rangeUpdate 메서드의 시간복잡도는 O(n)이다.  
> 이를 줄일려면 lazy propagation 알고리즘이 필요하다.

---

## Lazy Propagation

> Lazy Propagation의 목적:  
> 최대한 업데이트를 미뤄보자(query가 일어날 때까지)

만약 [a,b]를 c로 업데이트 하는데,  
a <= nodeLeft && nodeRight <= b 라고 가정해보자  
-> 현재 노드는 업데이트 구간에 완전히 포함되는 노드이다.

-> 완전히 포함되는 노드에 업데이트되는 값을 mark 해놓자  
그리고 나중에 계산하자

<img src="../../img/segtree_3.png" width="700">

여기서 추가적인 update 요청이 들어오거나, query 요청이 들어왔을 때  
현재 요청의 범위와 이전 update 범위와 다르다면,  
-> 다른 곳만 push down 해준다.  
(value를 아래 노드로 옮겨주자)

### Lazy Propagation 코드 구현

먼저 해당 노드에 lazy value가 있는지 체크해야한다.

```cpp
vector<bool> lazyExist;
vector<int> lazyValue;
```

그리고 lazy propagation을 적용하기 위해  
rangeUpdate 메서드와 query 메서드에 코드를 추가 해줘야 한다.

```cpp
int SegTree::pushDown(int value, int index, int nodeLeft, int nodeRight){
    if(nodeLeft == nodeRight)
        return node[index] = value;
        
    lazyExist[index] = true;
    lazyValue[index] = value;
    
    return node[index] = (nodeRight - nodeLeft + 1) * value;
    // 여기선 특정 범위의 원소들을 value로 바꾸기 때문에 & sum을 구하기 때문에, 위 공식이 나온 것
}

int SegTree::rangeUpdate(int left, int right, int value, int index, int nodeLeft, int nodeRight){
    if(left > nodeRight || right < nodeLeft) // 이 영역은 업데이트하지 않는 영역
        return node[index];
        
    if(nodeLeft == nodeRight) // 하나의 원소만 업데이트 하면 된다.
        return node[index] = value;
        
    // ------------------------- 새로운 코드 ---------------------------//
    // 현재 노드가 포함하는 원소의 범위가 업데이트 범위에 포함되기 때문에, 현재 노드에 lazyValue를 넣어준다.
    if(left <= nodeLeft && nodeRight <= right){ 
        lazyExist[index] = true;
        lazyValue[index] = value;
        return node[index] = (nodeRight - nodeLeft + 1) * value;
    }  
    // ------------------------- 새로운 코드 끝 -------------------------//
    
    
	int mid = nodeLeft + (nodeRight - nodeLeft) / 2;
	
	// ------------------------- 새로운 코드 ---------------------------//
	// 현재 노드가 포함하는 원소의 범위와 업데이트 범위와 다르기 떄문에, pushDown 해줘야 한다.
	if(lazyExist[index] == true){
	    lazyExist[index] = false;
	    pushDown(lazyValue[index], index * 2, nodeLeft, mid);
	    pushDown(lazyValue[index], index * 2 + 1, mid + 1, nodeRight);
	}
	// ------------------------- 새로운 코드 끝 ------------------------//
	
	int leftSum = rangeUpdate(left, right, value, index * 2, nodeLeft, mid);
	int rightSum = rangeUpdate(left, right, value, index * 2 + 1, mid + 1, nodeRight);
	return node[index] = merge(leftSum, rightSum);
}

int SegTree::query(int left, int right, int index, int nodeLeft, int nodeRight) {
	if (left > nodeRight || right < nodeLeft)
		return 0;

	cout << index << ' ';

	if (left <= nodeLeft && right >= nodeRight)
		return node[index];

	int mid = nodeLeft + (nodeRight - nodeLeft) / 2;

    // ------------------------- 새로운 코드 --------------------------//
	// 현재 노드가 포함하는 원소의 범위와 업데이트 범위와 다르기 떄문에, pushDown 해줘야 한다.
    if(lazyExist[index] == true){
        lazyExist[index] = false;
        pushDown(lazyValue[index], index * 2, nodeLeft, mid);
        pushDown(lazyValue[index], index * 2 + 1, mid + 1, nodeRight);
    }
    // ------------------------- 새로운 코드 끝 ------------------------//

	return merge(query(left, right, index * 2, nodeLeft, mid)
		, query(left, right, index * 2 + 1, mid + 1, nodeRight));
}
```

> lazy propagation을 적용한 rangeUpdate 메서드의 시간복잡도는 O(logn)이 된다.

---

> 세그먼트 트리는 단순히 배열의 구간 합을 구할 때만 사용되는 자료 구조가 아니라,  
> 배열의 특정 범위의 min, max, gcd(최대공약수), lcm(최소공배수)를 구할 때도 유용한 자료 구조이다.

> 세그먼트 트리는 배열의 길이가 고정일 때 사용 가능한 자료 구조이다.
> 
> 배열의 길이가 가변이라면 팬윅트리를 사용해야 한다. 