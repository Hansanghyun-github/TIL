### Thread 클래스

`Thread.currentThread()` 현재 실행 중인 스레드의 객체 반환  
(메인 메서드 실행 중인 스레드 이름 - main)

Thread 클래스를 상속받아 run 메서드를 오버라이딩 하고,  
해당 객체의 start 메서드를 실행하면,  
직접 작성한 run 메서드를 병렬로 실행한다.  
(새로운 스레드를 생성하여 실행)

> run 메서드가 아닌 start 메서드를 호출해야  
> 새로운 스레드로 실행된다.

`스레드 간 실행 순서는 보장하지 않는다`

---

### Runnable 인터페이스

위는 Thread를 상속받는 방법  
이제부터는 Runnable 인터페이스를 구현하는 방법 (실무에선 이 방법 많이 쓴다)

똑같이 run 메서드를 오버라이딩하여 구현하면 된다.  
(Thread 클래스가 Runnable 인터페이스를 구현한 클래스)

대신 스레드 객체를 생성할 때, 실행할 작업을 생성자로 전달해야 한다.

```java
class Thread {
    public static void main(String[] args) {
        Thread thread = new Thread(() -> System.out.println("hello thread"));
    }
}
```

---

### Thread 상속 vs Runnable 구현 차이점

자바는 단일 상속만 허용하기 때문에, Thread 상속받으면 다른 클래스를 상속받을 수 없다.  
or (만약 기존 클래스가 상속받았다면) Thread 상속을 위해 기존 클래스를 새로 만들어야 한다.

> 그리고 Thread를 상속받아도, 해당 메서드의 기능을 거의 사용하지 않는다.

그리고 Runnable 인터페이스에는 실행할 작업(run 메서드)만 있다.  
-> 코드의 분리  
(Thread 클래스에는 많은 다른 메서드가 있기 때문)

그리고 Runnable 객체를 공유할 수 있다 -> 자원 관리 효율적  
(하나의 Runnable 객체를 가지고 여러 Thread 생성 가능)

대신 코드가 약간 복잡해짐

> 그냥 Runnable 써라  
> (만약 Thread 클래스의 기능들을 사용해야 한다면 그때는 Thread를 상속 받겠지)
