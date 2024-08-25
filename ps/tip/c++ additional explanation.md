## 숫자 범위를 항상 체크하자 + 타입이 다른 변수끼리의 연산

항상 input, output 숫자 범위를 체크해주자  
그리고 중간 연산도 항상 체크해주자  
(int 범위를 벗어나는지)

int 타입 변수와 long long 타입 변수의 연산 결과 타입은  
long long 타입이다.  
(작은 타입이 큰 타입으로 승격되어 연산된다)

---

## iterator, reverse_iterator

iterator는 순방향으로 접근할 때 사용한다.  

iterator를 가지고 역방향으로 접근하는 건 매우 비효율적이다.

> iterator를 가지고 역순으로 접근하면, begin을 처리하는 것이 힘들다.  
> iter가 begin에 위치한 상태에서 --를 하면, 에러가 발생한다.
> 
> begin에 있는 원소를 탐색한 뒤에,  
> 따로 begin을 위한 조건을 걸어주어야 한다.

역방향으로 접근할 때는 reverse_iterator를 사용하자  

++ 연산을 하면 이전 원소로 이동하고,  
첫번째 원소 다음에는 rend가 위치한다.  
-> 이를 통해 편하게 처리할 수 있다.

만약 정순 역순 둘 다 사용해야 한다면  
굳이 iterator 한개만 가지고 접근하는 것이 아니라,  
iterator, reverse_iterator 두개를 가지고 접근하는 것이 더 편할 것 같다.  
(물론 두개 동시에 업데이트 해줘야 한다)

---

## type& 선언과 type* 선언의 차이

둘 다 포인터 연산이 된다.

type& - 해당 변수에 대한 참조자를 선언한다.
(별칭을 지정한다고 할 수 있다)

type* - type 변수에 대한 포인터를 선언한다.

둘 다 Call By Reference 이다.

|    | type&                            | type*                      |
|----|----------------------------------|----------------------------|
| 장점 | 포인터보다 코드가 간결하고 직관적이다.            | 동적으로 초기화 가능하다.             |
| -  | 코드의 가독성을 향상시킨다.                  | -                          |
| 단점 | 선언과 동시에 초기화 해야 한다. (이후에는 초기화 불가능) | 코드가 복잡해진다.                 |
| -  | -                                | 포인터 연산이 필요하다 -> 가독성이 떨어진다. |

type& 은 함수의 파라미터를 선언할 떄 자주 사용한다.  
(가리키는 변수를 동적으로 바꿀 필요 없기 때문에)  
```
int add(int& n1, int& n2){
    return n1 + n2;
}
```

type* 은 가리키는 변수를 중간에 바꿔야 할 떄 사용한다.

---

## MyClass() 와 new MyClass() 의 차이

`MyClass()`  
객체를 스택 영역에 저장한다. (스택 프레임 내 지역 변수로 처리)  
함수가 종료되면 해당 객체는 자동으로 파괴된다. (스택 프레임에서 해제)

`new MyClass()`  
객체를 힙 영역에 할당한다.  
프로그래머가 직접 메모리를 해제하기 전까지는 존재한다.  
힙에 할당되므로 프로그램의 어느 위치에서나 접근할 수 있다.  
delete 해주지 않는다면 메모리 누수가 발생한다.

---

## 메서드의 파라미터로 배열이나 컨테이너를 넘길 떄

배열을 메서드의 인자로 넘기는 경우는 무조건 call-by-reference 다.

```cpp
void arrayMethod1(int arr[50]);
void arrayMethod2(int arr[]); // 크기를 명시하지 않아도 된다.
void doubleArrayMethod2(int arr[][50]); // 첫번째만 명시하지 않아도 된다.
```

> 배열의 이름이 배열의 첫번째 요소에 대한 포인터로 해석되기 때문이다.

하지만 컨테이너는 call-by-value, call-by-reference 둘 다 가능하다.

```cpp
void callByValueMethod(vector<int> v);
void callByReferenceMethod(vector<int>& v);
```

첫번째 메서드는 call-by-value라서 인자로 보내주는 vector의 원소들을 복사해서 보내준다.

두번쨰 메서드는 call-by-reference라서 vector의 위치만 보내준다.

> call-by-value로 메서드를 호출하면, 해당 컨테이너의 원소들을 모두 복사해주기 떄문에,  
> 시간초과가 발생할 수 있다.

> call-by-reference로 메서드를 호출할 때는, 해당 컨테이너 내의 값이 바뀔 수 있음을 주의하자.

---

## 커스텀 클래스

### 커스텀 클래스 타입을 사용하는 pair 템플릿

표현해야 할 필드가 많을 때 커스텀 클래스를 많이 쓰는데,  
만약 2차원 배열의 위치만 표현 한다면,  
커스텀 클래스보다는 pair를 쓰는게 좋을 것 같다.

`커스텀 클래스과 비교 했을 때 pair의 장점`

1. 기본적인 operator가 구현되어 있다.
2. make_pair 같은 유틸 메서드가 있다.
3. 생성자와 소멸자가 커스텀 클래스보다 빠르다.

`pair의 first, second는 너무 길다`

이때는 매크로로 편하게 쓰자

```cpp
#define rr first
#define cc second

pair<int, int> p;

// p.first, p.second 대신 p.rr, p.cc
```

rr, cc는 많이 사용하는 변수가 아니기 때문에,  
겹치는 경우가 적어 편하게 쓸 수 있다.

---

### 커스텀 클래스 타입을 요소로 가지는 컨테이너

list, vector 같은 선형 컨테이너의 템플릿 매개변수에 커스텀 클래스를 넣을 때는  
그렇게 주의할 것은 없다.

하지만 비선형 컨테이너의 경우 주의해야 할 것들이 있다.

### set, map의 key로 커스텀 클래스를 사용할 때

set과 map은 트리 기반 컨테이너이기 때문에 key를 기준으로 정렬 되어 있다.

따라서 key에 대한 비교 연산자를 재정의 해줘야 한다.

```cpp
struct Point {
    int x, y;
    bool operator<(const Point& p) const {
        if (x == p.x) return y < p.y;
        return x < p.x;
    }
};

set<Point> s;
map<Point, int> m;
```

### unordered_set, unordered_map의 key로 커스텀 클래스를 사용할 때

unordered_set과 unordered_map은 해시 기반 컨테이너이기 때문에,  
해시 함수와 동등 비교 연산자를 재정의 해줘야 한다.

```cpp
struct Point {
    int x, y;
    bool operator==(const Point& p) const {
        return x == p.x && y == p.y;
    }
};

struct PointHash {
    size_t operator()(const Point& p) const {
        return hash<int>()(p.x) ^ hash<int>()(p.y);
    }
};

unordered_set<Point, PointHash> us;
unordered_map<Point, int, PointHash> um;
```

> 이때 해시 함수는 컨테이너를 정의할 때, 마지막 템플릿 매개변수로 넣어줘야 한다.

> 그리고 해시 함수를 정의할 때, 해시 충돌을 항상 주의해야 한다.

> 비선형 컨테이너의 map과 unordered_map의 value로 커스텀 클래스를 사용할 때는,  
> 따로 주의할 것은 없다.

### unordered_map의 value로 커스텀 클래스를 사용할 때

unordered_map의 value로 커스텀 클래스를 사용할 때는,  
value의 타입이 불완전한 타입이면 안된다.

> visual studio에서는 컴파일 에러가 발생하지 않는다.  
> 하지만 gcc 컴파일러에서는 컴파일 에러가 발생한다.

이를 막기 위해 shared_ptr을 사용하자.

`Class root;` 를  
`shared_ptr<Class> root;` 로 바꿔주자.

맨 처음 root를 초기화 할 때는 make_shared를 사용하자.

`shared_ptr<Class> root = make_shared<Class>();`

> shared_pointer의 사용 방식은 일반 포인터와 비슷하다.  
> (메모리 해제를 신경쓰지 않아도 된다)

