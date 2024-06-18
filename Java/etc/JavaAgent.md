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

> transform 메서드는  
> 클래스 로더에 로드되는 모든 클래스에 대해 호출된다.  
> (javaagent 관련 클래스 포함)
> 
> 따라서 특정 클래스만 변환하기 위해 `className`을 확인하여 변환할 클래스를 선택해야 한다.

---

## 자바 에이전트를 포함한 클래스 로드 순서

1. 에이전트 JAR 파일을 로드한다.
2. 에이전트 JAR 파일에 있는 `premain` 메서드를 호출한다.
3. `premain` 메서드를 통해 `Instrumentation` 객체에 `ClassFileTransformer`를 등록한다.
4. 클래스가 로드될 떄마다 `ClassFileTransformer`의 `transform` 메서드를 호출한다.
5. `transform` 메서드에서 클래스의 바이트 코드를 변환한다.

---

## ClassFileTransformer의 transform 메서드 & asm 라이브러리

transform 메서드는 클래스의 바이트 코드를 변환하는 메서드이다.

이때 바이트 코드를 변환할 때는 `asm`, `Javassist` 등의 라이브러리를 사용한다.

(아래는 `asm` 라이브러리를 사용한 예시)  
```java
public class MyTransformer implements ClassFileTransformer {
    @Override
    public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined, ProtectionDomain protectionDomain, byte[] classfileBuffer) {
        ClassReader cr = new ClassReader(classfileBuffer);
        ClassWriter cw = new ClassWriter(cr, ClassWriter.COMPUTE_MAXS);
        ClassVisitor cv = new MyClassVisitor(cw);
        cr.accept(cv, 0);
        return cw.toByteArray();
    }
}
```

`cr.accept(cv, 0);` 를 통해 바이트 코드를 변환하고, 해당 바이트 코드를 `cw.toByteArray()`로 반환한다.

### ClassReader 클래스

바이트 코드를 읽어오는 클래스  
`byte[]` 형태의 바이트 코드를 읽어와서 `accept` 메서드를 통해 `ClassVisitor`를 통해 바이트 코드를 분석한다.

### ClassWriter 클래스

바이트 코드를 작성하는 클래스

### ClassVisitor 클래스

바이트 코드를 분석하는 클래스  
`visitMethod` 메서드를 오버라이드하여 메서드를 분석할 수 있다.

```java
public class MyClassVisitor extends ClassVisitor {
    public MyClassVisitor(ClassVisitor cv) {
        super(Opcodes.ASM9, cv);
    }

    @Override
    public MethodVisitor visitMethod(int access, String name, String desc, String signature, String[] exceptions) {
        MethodVisitor mv = super.visitMethod(access, name, descriptor, signature, exceptions);
        // 메서드 바이트 코드 변환 로직
        return mv;
    }
}
```

> visiteMethod 메서드
> - 메서드에 해당하는 MethodVisitor를 반환한다.  
>   이때 메서드의 바이트 코드를 변환할 수 있다.
> - 클래스에 있는 모든 메서드를 순회하며 호출된다.  
>   특정 메서드만 변환하려면 `visitMethod` 메서드에서 특정 메서드만 변환하도록 구현해야 한다.

### MethodVisitor 클래스

메서드의 바이트 코드를 분석하는 클래스

```java
public class MyMethodVisitor extends MethodVisitor {
    public MyMethodVisitor(MethodVisitor mv) {
        super(Opcodes.ASM9, mv);
    }

    @Override
    public void visitCode() {
        super.visitCode();
        // 메서드 바이트 코드 변환 로직
    }
    
    @Override
    public void visitInsn(int opcode) {
        // 메서드 바이트 코드 변환 로직
        super.visitInsn(opcode);
    }
}
```

`visitCode` 메서드
- 메서드의 시작 지점에 호출된다.
- 메서드의 시작 지점에 바이트 코드를 추가하려면 이 메서드를 오버라이드한다.

`visitInsn` 메서드
- 메서드의 각 명령어에 호출된다.
- 메서드의 각 명령어에 바이트 코드를 추가하려면 이 메서드를 오버라이드한다.
- opcode는 명령어 코드를 나타낸다.

opcode를 이용해 메서드의 끝을 확인할 수 있다.  
```java
public class MyMethodVisitor extends MethodVisitor {
    public MyMethodVisitor(MethodVisitor mv) {
        super(Opcodes.ASM9, mv);
    }

    @Override
    public void visitInsn(int opcode) {
        if ((opcode >= Opcodes.IRETURN && opcode <= Opcodes.RETURN) || opcode == Opcodes.ATHROW) {
            // 메서드의 끝에 호출
        }
        super.visitInsn(opcode);
    }
}
```

visitMethodInsn 메서드를 이용해 바이트 코드를 변환할 수 있다.  
```java
public class MyMethodVisitor extends MethodVisitor {
    public MyMethodVisitor(MethodVisitor mv) {
        super(Opcodes.ASM9, mv);
    }

    @Override
    public void visitInsn(int opcode) {
        if ((opcode >= Opcodes.IRETURN && opcode <= Opcodes.RETURN) || opcode == Opcodes.ATHROW) {
            mv.visitMethodInsn(Opcodes.INVOKESTATIC, "com/example/MethodTimeRecorder", "end", "()V", false);
        }
        super.visitInsn(opcode);
    }
}
```

// TODO visitMethodInsn 설명 추가

### AnnotationVisitor 클래스

어노테이션을 분석하는 클래스  

visit, visitArray, visitEnum 등의 메서드를 통해 어노테이션의 필드를 분석할 수 있다.

`visit()` - primitive 타입의 어노테이션 필드를 방문한다.
`visitEnum()` - enum 타입의 어노테이션 필드를 방문한다.
`visitAnnotation()` - 어노테이션 타입의 어노테이션 필드를 방문한다.
`visitArray()` - 배열 타입의 어노테이션 필드를 방문한다.

> 예를 들어 @GetMapping 어노테이션의 value 필드를 분석하려면  
> `visit` 메서드를 사용하여 value 필드를 분석할 수 있다.  
> 

---