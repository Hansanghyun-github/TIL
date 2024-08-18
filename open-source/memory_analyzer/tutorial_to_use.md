(MemoryAnalyzer의 공식 문서를 참고하여 작성했다)

---

## Memory Analyzer를 사용하기 위한 기본 지식

### 힙 덤프

힙덤프는 자바 프로세스의 메모리의 스냅샷이다.

힙영역의 자바 객체와 클래스에 대한 정보를 가지고 있다.

힙 덤프에서 찾을 수 있는 일반적인 정보
- 모든 객체
- 모든 클래스
- GC Roots(객체가 살아있게 유지하는 것들)
- Thread Stacks and Local Variables(스레드의 콜 스택)

> 힙 덤프에는 할당 정보가 포함되어 있지 않으므로 누가 개체를 생성했는지, 어디서 생성되었는지와 같은 질문들을 해결할 수 없다.

모든 객체에는 해당 타입의 reference와 클래스 로더를 가지고 있다.

> reference가 field, array elements, 또는 hidden reference 일 수 있다.

---

### Shallow Heap vs Retained Heap

shallow heap은 한 객체가 소비하는 메모리를 의미한다.

> 객체 하나에게 필요한 것  
> reference 당 32/64 bits(OS 아키텍쳐에 따라 다름)  
> int 4 byte, long 8 byte 등 ...

Retained set of X  
GC가 발생할 때, 같이 삭제되는 모든 객체들의 집합(참조하고 있는 것들인가?)

Retained heap of X  
X에 의해 유지되는 메모리, X에 포함된 모든 객체의 shallow size의 합

minimum retained size는 힙 덤프의 객체의 수가 아니라,  
검사된 집합의 객체의 수에 의존한다.

---

처음 힙덤프를 열었을 때 나오는 오른쪽 위는,  
덤프의 사이즈, 클래스 수, 객체 수, 클래스 로더 수가 나온다.

// todo 이미지 추가

만약 사이즈가 실제 힙 덤프보다 많이 작다면  
이는 garbage objects가 빠졌기 때문이다.  
(MAT default 설정이 garbage objects는 빼고 표시해줌)

### get the histogram

histogram icon을 클릭하면  
클래스 별로 인스턴스 수, shallow size, retained size가 표로 나열되어 있다.

> Memory Analyzer는 default retained size를 display 한다.  
> 전체를 측정하고 싶다면, 계산기 아이콘을 통해 측정해야 한다.

특정 객체에 대해 outgoing/incoming reference와 함께 list 할 수 있다.

이 프로그램의 중요한 기능은, 클래스들을 grouping 할 수 있다는 것이다.
(class 별로, class loader 별로, package 별로, superclass 별로)

### view the domiator tree

dominator tree는  
힙덤프의 biggest objects를 display 한다.

그다음으로 garbage objects를 나열한다?

이 기능을 통해, 어떤 객체가 다른 객체를 살아있게 유지하는지 조사한다.
?

// todo 자세히 파악하기

### Path to GC Roots

GC Roots 옵션은 VM에 의해 살아있는 객체들을 표시한다.

이곳에는 현재 실행중인 스레드의 스레드 객체, stack trace에 있는 객체,  
시스템 클래스 로더에 로드된 클래스가 포함된다.

처음에는 최단 경로에 도달한 GC 루트가 선택된다.

### Generate the Leak Report

이 프로그램은 힙덤프로부터, leak suspects를 조사한다.

---

## Memory Analyzer 유의할 점

이 프로그램도 메모리를 사용하기 때문에,  
큰 힙 덤프를 열 때는 주의해야 한다.

> 이 프로그램에 default로 할당된 힙 사이즈는 1GB이다.

만약 1GB보다 큰 힙 덤프를 열려면,  
.ini 파일에서 `-Xmx` 옵션을 사용하여 힙 사이즈를 늘려야 한다.