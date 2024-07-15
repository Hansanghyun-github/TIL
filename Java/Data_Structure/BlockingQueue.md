# BlockingQueue

// 한국말로 설명한다.
// 1. BlockingQueue의 개념
// 2. BlockingQueue의 구현체
// 3. 구현체들의 차이점

## 1. BlockingQueue의 개념

BlockingQueue는 Queue 인터페이스를 구현한 클래스로,  
멀티스레드 환경에서 사용할 수 있는 큐이다.  
(thread-safe한 큐)

요소를 검색할 때 대기열이 비어 있지 않을 때까지 기다리고, (blocking)  
요소를 저장할 때 대기열에서 공간을 사용할 수 있을 때까지 기다리는 작업을 추가로 지원하는 대기열입니다.  

BlockingQueue 메소드는 즉시 충족될 수 없는  
(나중에는 성공할 수 있는)  
작업을 처리하는 다양한 방법을 포함하는 네 가지 형식으로 제공한다.  

하나는 예외를 발생시키고,  
두 번째는 special value를 반환시키고,  
세 번째는 작업이 성공할 때까지 현재 스레드를 무기한 대기시키고,  
네 번째는 포기하기 전에 지정된 최대 시간 제한 동안만 차단합니다.

|-|throw exception|special value|block|timeout|
|---|---|---|---|---|
|Insert|add(e)|offer(e)|put(e)|offer(e, time, unit)|
|Remove|remove()|poll()|take()|poll(time, unit)|
|Examine|element()|peek()|N/A|N/A|

---

## 2. BlockingQueue의 구현체

BlockingQueue 인터페이스를 구현한 구현체로는 다음과 같은 것들이 있다.  
- ArrayBlockingQueue
- LinkedBlockingQueue
- PriorityBlockingQueue
- DelayQueue
- SynchronousQueue
- LinkedTransferQueue

// TODO


---

## 3. 구현체들의 차이점

