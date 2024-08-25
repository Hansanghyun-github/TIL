# agent.java

자바 프로그램을 모니터링하는데 사용된다.

> -javaagent 옵션을 사용하여 agent.jar를 실행하면,  
> agent.jar에 포함된 premain 메서드가 실행된다.

## agent.java premain 메서드의 동작 과정

## 1. 먼저 ClassFileTransformer를 등록한다.

AgentTransfomer 객체를 Instrumentation에 등록한다.  
(AgentTransformer 다른 파일에서 설명)

이떄 JavaAgent에서 inst라는 static 변수에 Instrumentation을 저장한다.

## 2. AsyncRunner를 통해 비동기로 AgentBoot를 실행한다.

AgentBoot 클래스의 boot 메서드를 실행한다.

### AsyncRunner

Thread 클래스를 상속받아, 비동기로 실행된다.

여러가지 작업을 비동기로 실행하는데,  
이 작업들을 RequestQueue에 저장하고,  
AsyncRunner가 이 작업들을 꺼내서 실행한다.

> RequestQueue는 직접 구현한 클래스  
> LinkedList를 사용하여 구현했다.

### AgentBoot

premain 메서드를 통해 AsyncRunner를 생성한 뒤에,  
AgentBoot 클래스의 run 메서드를 실행한다.

> AgentBoot의 run 메서드는 boot 메서드를 실행하는데,  
> 이 메서드는 전체 생명주기 중에 딱 한번만 실행된다.

boot 메서드는  
`CounterExecutingManager.load()`  
`ReqestHandlingProxy.load(ReqestHandlingProxy.class)`  
를 실행한다.

> CounterExecutingManager.load() 메서드는  
> @Counter 나 @InteractionCounter가 있는 메트릭 관련 클래스들을  
> static 필드에 저장하는 작업을 한다.

> ReqestHandlingProxy.load(ReqestHandlingProxy.class) 메서드는  
> @RequestHandler 어노테이션이 있는 클래스들을  
> static 필드에 저장하는 작업을 한다.

### CounterExecutingManager.load()

`scouter.agent.counter.task` 패키지에 있는 모든 클래스들을 찾아서,  
클래스마다 Counter, InteractionCounter 어노테이션이 있는지 검사하고,  
있다면 CounterExecutingManager에 등록한다.

### agent.java의 default task

`scouter.agent.counter.task` 패키지에 있는 모든 클래스들은,  
agent.java가 수집하는 메트릭에 대한 클래스들이다.

### BackJobs

AsyncRunner와 비슷한 역할을 한다.  

이 클래스는 로깅 작업만 수행한다.

