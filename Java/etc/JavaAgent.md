# 자바 에이전트

자바 에이전트는 자바 바이트 코드를 조작하는 프로그램  
에이전트는 자바 가상 머신에 로드되어 실행 중인 프로그램의 바이트 코드를 수정할 수 있다.

> 에이전트는 프로그램의 동작을 모니터링하거나 프로그램의 동작을 수정하는 데 사용됩니다.

> Scouter, Pinpoint 와 Jacoco 등이 자바 에이전트를 사용하여 프로그램의 동작을 모니터링한다.

---

## 자바 에이전트 로드

자바 에이전트를 로드하려면 `java` 명령어에 `-javaagent` 옵션을 사용하여 에이전트 JAR 파일을 지정해야 한다.

```shell
java -javaagent:agent.jar -jar app.jar
```

이때 agent.jar에는 `premain` 메서드가 있는 클래스가 포함되어 있어야 한다.

```java
public class MyAgent {
    public static void premain(String agentArgs, Instrumentation inst) {
        // 에이전트 로직
    }
}
```

그리고 `MANIFEST.MF` 파일에 `Premain-Class` 속성을 추가해야 한다.

```shell
Premain-Class: com.example.MyAgent
Can-Redefine-Classes: true
Can-Retransform-Classes: true
```

---

## 자바 에이전트 로직

자바 에이전트 로직은 `Instrumentation` 인터페이스를 사용하여 구현한다.

```java
public class MyAgent {
    public static void premain(String agentArgs, Instrumentation inst) {
        inst.addTransformer(new MyTransformer());
    }
}
```

`inst.addTransformer` 메서드를 사용하여 `MyTransformer` 클래스를 등록한다.

```java
public class MyTransformer implements ClassFileTransformer {
    @Override
    public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined, ProtectionDomain protectionDomain, byte[] classfileBuffer) {
        // 클래스 변환 로직
    }
}
```

`ClassFileTransformer` 인터페이스를 구현하여 `transform` 메서드를 오버라이드한다.

---

## 클래스 변환

`transform` 메서드에서 클래스를 변환할 수 있다.

```java
public class MyTransformer implements ClassFileTransformer {
    @Override
    public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined, ProtectionDomain protectionDomain, byte[] classfileBuffer) {
        if (className.equals("com/example/MyClass")) {
            // 클래스 변환 로직
        }
        return classfileBuffer;
    }
}
```

`transform` 메서드에서 `className`을 확인하여 특정 클래스만 변환할 수 있다.

> 이때 패키지명을 포함한 전체 클래스명을 사용한다.

---

## 자바 에이전트를 포함한 클래스 로드 순서

1. 에이전트 JAR 파일을 로드한다.
2. 에이전트 JAR 파일에 있는 `premain` 메서드를 호출한다.
3. `premain` 메서드를 통해 `Instrumentation` 객체에 `ClassFileTransformer`를 등록한다.
4. 클래스가 로드될 떄마다 `ClassFileTransformer`의 `transform` 메서드를 호출한다.
5. `transform` 메서드에서 클래스의 바이트 코드를 변환한다.

---

