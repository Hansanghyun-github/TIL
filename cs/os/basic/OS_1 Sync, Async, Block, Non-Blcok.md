# Sync, Async, Block, Non-Blcok

Blocking/Non-Blocking은 작업을 기다리는 동안 시스템 자원(CPU)을 어떻게 사용하는지에 대한 것  
(제어권이 있는지 없는지)

Synchronous/Asynchronous는 작업을 호출한 쪽이 작업이 끝나기를 기다리는지 여부에 대한 것  
(시간적 관점에서 요청과 응답의 처리 순서)

## Blocking vs Non-Blocking

### Blocking I/O
 
호출한 작업이 끝나기 전까지 다른 작업을 수행하지 않는 것  
(제어권이 없다)  
(자원을 사용하지 않는다)

### Non-Blocking I/O

호출한 작업이 끝나지 않아도 다른 작업을 수행하는 것  
(제어권이 있다)  
(자원을 사용한다)

## Synchronous vs Asynchronous

> 2개 이상의 것들(스레드/메소드)이 시간을 맞추냐 안 맞추냐  
> (synchronous = Sync(함께) + Chrono(시간))

### Synchronous

동기(Synchronous) 방식은 메서드 리턴과 결과를 전달받는 시간이 일치하는 명령 실행 방식

2개 이상의 스레드가 동시에 시작해서, 동시에 끝나면 동기  
메소드의 결과를 받아서, 바로 처리하면 동기

> 자바에서 synchronized, BlockingQueue가 있다

### Asynchronous

비동기(Asynchronous) 방식은 여러 개의 처리가 함께 실행되는 방식  
(함꼐 시간을 맞추지 않는다)

메소드의 결과를 받아도, 바로 처리하지 않는다.  
(리턴 시간과 맞추지 않는다)

> 비동기는 언제 끝날지 모른다.

> 동기 방식에 비해 단위 시간 당 많은 작업 처리 가능

---

## block, non-block, sync, async 섞은 예시

sync + non-block - 게임 로딩 화면  
(맵이 로딩 돼야 캐릭터 플레이 가능(sync), 로딩 하는 동안 로딩화면 보여줌(non-block))

sync + block - fprintf, scanf  
(함수 끝나야 실행되고, 끝나기 전까지 아무것도 못함)

async + non-block - 콜백