## Thread 클래스의 getContextClassLoader() 메서드

Thread.currentThread().getContextClassLoader() 메서드는 현재 스레드의 컨텍스트 클래스 로더를 반환한다.

이때 컨텍스트 클래스 로더와 일반 클래스 로더의 차이점은 무엇일까?

---

### 클래스 로더의 정의

클래스 로더란 JVM에서 클래스 파일을 읽어들여 메모리에 로딩하는 역할을 하는 컴포넌트 이다.

이는 클래스 파일을 찾고, 읽고, 메모리에 로딩하여, JVM에서 사용할 수 있도록 하는 역할을 한다.

---

### 일반적인 클래스 로더

{Object}.class.getClassLoader() 메서드를 통해 얻을 수 있는 클래스 로더는  
일반적인 클래스 로더로,  

해당 클래스를 로딩한 클래스 로더를 반환한다.

---

### 컨텍스트 클래스 로더

컨텍스트 클래스 로더는  
Thread.currentThread().getContextClassLoader() 메서드를 통해 얻을 수 있는 클래스 로더로,  

해당 스레드에서 사용하는 클래스 로더를 반환한다.

> 스레드를 처음 실행할 때,  
> 해당 스레드의 컨텍스트 클래스 로더는 부모 스레드의 컨텍스트 클래스 로더를 상속받는다.
> 
> 그래서 대부분의 경우,  
> 'Thread.currentThread().getContextClassLoader()' 메서드를 통해 얻을 수 있는 클래스 로더는  
> 부모 스레드의 컨텍스트 클래스 로더를 반환하기 때문에,  
> 일반 클래스로부터 얻는 클래스 로더와 동일하다.

---

스레드 별로 얻는 컨텍스트 클래스 로더가 다른 경우는,  
스레드를 실행하고 나서,  
스레드의 컨텍스트 클래스 로더를 변경한 경우이다.

> `setContextClassLoader(ClassLoader cl)` 메서드를 통해  
> 스레드의 컨텍스트 클래스 로더를 변경할 수 있다.

---

https://stackoverflow.com/questions/39849690/when-to-use-thread-currentthread-getcontextclassloader-in-webapplications

위 사이트에서는  
기존 클래스 로더를 변수에 저장하고 새로운 클래스 로더를 등록하는 코드를 보여준다.