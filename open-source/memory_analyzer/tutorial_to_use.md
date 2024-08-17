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