### 커스텀 클래스 

표현해야 할 필드가 많을 때 커스텀 클래스를 많이 쓰는데,  
만약 2차원 배열의 위치만 표현 한다면,  
커스텀 클래스보다는 pair를 쓰는게 좋을 것 같다.

### 커스텀 클래스과 비교 했을 때 pair의 장점

1. 기본적인 operator가 구현되어 있다.
2. make_pair 같은 유틸 메서드가 있다.
3. 생성자와 소멸자가 커스텀 클래스보다 빠르다.

### pair의 first, second는 너무 길다

이때는 매크로로 편하게 쓰자

```cpp
#define rr first
#define cc second

pair<int, int> p;

// p.first, p.second 대신 p.rr, p.cc
```

rr, cc는 많이 사용하는 변수가 아니기 때문에,  
겹치는 경우가 적어 편하게 쓸 수 있다.