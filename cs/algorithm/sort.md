## 버블 정렬

첫번째 원소부터 인접한 원소와 비교하며 자리를 바꾸면서 맨 끝부터 정렬하는 방식

> 정렬 방식이 마치 물속에서 올라오는 물방울과 같다고 하여 버블 정렬이라는 이름이 붙여졌다.

```cpp
void bubbleSort(vector<int>& v){
    for(int i = v.size() - 1;i > 0; i--){
        for(int j=0;j < i;j++){
            if(v[j] > v[j+1]) {
                swap(v[j], v[j+1]);
            }
        }
    }
}
```

매 턴마다  
첫번째 위치부터 i번째 위치까지  
값이 큰 원소를 오른쪽으로 스왑하면서 순회한다.  
(i는 size-1 부터 1까지 진행)


### 시간 복잡도

best case/average case/worst case: $O(n^2)$

### 특징

모든 케이스의 시간복잡도가 $O(n^2)$라는 단점이 있다.

---

## 선택 정렬

매 탐색마다  
배열의 최솟값을 찾아 선택하여 정렬하는 방식

```cpp
void selectionSort(vector<int>& v){
    for(int i=0;i < v.size();i++){
        int minI = i;
        for(int j = i+1;j < v.size();j++){
            if(v[minI] > v[j]){
                minI = j;
            } 
        } 
        swap(v[i], v[minI]);
    }
}
```

i번째 턴에서  
i 위치 이후에 있는 원소들 중 가장 작은 원소의 위치 minI를 찾은 다음  
i번째 위치에 있는 원소와 minI 위치에 있는 원소를 스왑한다.  
(i는 0부터 size-1 까지)


### 시간 복잡도

best case/average case/worst case: $O(n^2)$

### 특징

버블 정렬처럼 모든 케이스의 시간복잡도가 $O(n^2)$라는 단점이 있다.

---

## 삽입 정렬

((i-1)번째 원소까지는 모두 정렬된 상태)  
i번째 원소보다 작은 값이 발견되면 그 위치에 i원소를 삽입하는 방식

```cpp
void insertionSort(vector<int>& v){
    for(int i = 1;i < v.size();i++){
        int value = v[i];
        int j = i-1;
        while(j >= 0 && v[j] > v[i]){
            v[j+1] = v[j];
            j--;
        }
        v[j + 1] = value;
    }
}
```

(i는 1부터 size-1 까지)  
i번째 원소를 value 원소에 넣고,  
i이전의 원소들을 backward로 순회하면서  
if v[j] > value, v[j+1] = v[j];  
else, break and v[j+1] = value;

> i 위치 이전의 원소들은 항상 정렬되어 있다는 것을 가정하고  
> 정렬을 진행한다.

### 시간 복잡도

best case: $O(n)$  
average case/worst case: $O(n^2)$

### 특징

best case에서는 시간복잡도가 위의 다른 정렬보다 좋다는 장점이 있다.

---

## 퀵 정렬

분할 정복(divide and conquer) 방법을 이용한 정렬

하나의 pivot(축)을 정해서, 이 pivot보다 작은 값은 왼쪽에, 큰 값은 오른쪽에 위치시킨다.  
그리고 pivot을 기준으로 왼쪽 부분을 재귀 호출하고, 오른쪽 부분을 재귀 호출하면서 정렬시킨다.  
(재귀 호출이 한번 진행될때마다 최소한 하나의 원소는 최종적으로 위치가 정해진다)

```cpp
int partition(vector<int>& v, int start, int end){
    int pivot = arr[end];
    int i = start; // 피벗보다 작은 원소들이 위치할 인덱스
    for(int j = start;j < end;j++){
        if(arr[j] < pivot){
            swap(arr[i], arr[j]);
            i++;
        }
    } 
    
    swap(arr[i], arr[end]); // 피벗을 중간으로 옮김
    return i;
}

void quickSort(vector<int>& v, int start, int end){
    if(start >= end) break;
    
    int pivot = partition(v, start, end);
    quickSort(v, start, pivot - 1);
    quickSort(v, pivot + 1, end);
}
```

### 시간 복잡도

best case/average case: $O(nlogn)$  
worst case: $O(n^2)$

### 특징

정렬된 배열에 대해서는 시간복잡도가 오래 걸린다.

---

## 병합 정렬(merge sort)

(분할 정복을 이용한 정렬)
1. 배열을 절반으로 나눈다.
2. 나눈 왼쪽/오른쪽 배열들을 재귀적으로 호출한다.  
   (원소의 개수가 1개라면 그대로 종료)
3. 양쪽의 배열들을 크기순으로 정리한다.

```cpp
void merge(vector<int>& v, int start, int end, int mid) {
	vector<int> left(mid - start);
	vector<int> right(end - mid);

	for (int i = start; i < mid; i++)
		left[i - start] = v[i];
	for (int i = mid + 1; i <= end; i++)
		right[i - mid - 1] = v[i];

	int i = 0, j = 0, k = start;
	while (i < mid - start && j < end - mid) {
		if (left[i] < right[j]) {
			v[k] = left[i];
			i++;
		}
		else {
			v[k] = right[j];
			j++;
		}
		k++;
	}
	while (i < mid - start) {
		v[k] = left[i];
		i++;
		k++; 
	}
	while (j < end - mid) {
		v[k] = right[j];
		j++;
		k++;
	}
}

void mergeSort(vector<int>& v, int start, int end) {
	if (start >= end) return;

	int mid = (start + end) / 2;
	mergeSort(v, start, mid);
	mergeSort(v, mid, end);

	merge(v, start, end, mid);
}
```

`start`: 시작 점, `end`: 끝 점의 다음 위치  
left는 start부터 mid 전까지,  
right는 mid부터 end 전까지 정렬한 다음,  
두 배열을 정렬한다.

### 시간 복잡도

best case/average case/worst case: $O(nlogn)$

### 특징

모든 케이스에 대해 시간복잡도 효율이 좋다.  
하지만 정렬을 하는 배열의 추가적인 임시 배열이 필요하다. (추가 메모리)

---

## 힙 정렬

힙을 이용한 정렬

배열의 모든 원소를 힙에 넣고,  
한개씩 빼면서 정렬된 배열을 얻는다.

### 특징

모든 케이스에 대해 시간복잡도가 O(nlogn)이라 효율적이지만,  
힙 정렬보다 오래걸린다.
(모든 원소를 힙에 넣는데 O(nlogn) + 힙의 모든 원소를 빼는데 O(nlogn))

---

## 안정(Stable) 정렬/불안정(Unstable) 정렬

정렬 알고리즘의 안정성을 나타내는 용어

> 안정 정렬: 정렬 전에 같은 값의 원소가 있을 때, 정렬 후에도 순서가 유지되는 정렬 방식  
> 불안정 정렬: 정렬 전에 같은 값의 원소가 있을 때, 정렬 후에 순서가 유지되지 않는 정렬 방식

- 버블 정렬, 삽입 정렬, 병합 정렬은 안정 정렬
- 선택 정렬, 퀵 정렬, 힙 정렬은 불안정 정렬

```
// Pair(int, String)에서 int를 기준으로 정렬

{(1, "a"), (2, "b"), (1, "c")} -> {(1, "a"), (1, "c"), (2, "b")}
// 안정 정렬 - 같은 키를 가지는 a와 c의 순서가 유지됨

{(1, "a"), (2, "b"), (1, "c")} -> {(1, "c"), (1, "a"), (2, "b")}
// 불안정 정렬 - 같은 키를 가지는 a와 c의 순서가 유지되지 않음
```