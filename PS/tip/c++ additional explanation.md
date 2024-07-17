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

