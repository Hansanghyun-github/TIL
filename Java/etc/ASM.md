# ASM 라이브러리

ASM은 바이트 코드 조작 라이브러리로, 바이트 코드를 직접 조작할 수 있다.  
ASM을 사용하면 클래스 파일을 직접 생성하거나 수정할 수 있다.

---

## ClassReader 클래스

바이트 코드를 읽어오는 클래스  
`byte[]` 형태의 바이트 코드를 읽어와서 `accept` 메서드를 통해 `ClassVisitor`를 통해 바이트 코드를 분석 & 변환한다.


### accept 메서드

바이트 코드를 분석하는 메서드  
`ClassVisitor`를 통해 바이트 코드를 분석 & 변환한다.

---

## ClassVisitor 클래스

바이트 코드를 분석하고 변환하는 클래스

> ClassVisitor 클래스는 체인 형태로 연결할 수 있다.  
> (이때, 체인 형태로 연결된 ClassVisitor는 순차적으로 호출된다)

`visitMethod` 메서드, `visitAnnotation` 메서드 등을 통해 바이트 코드를 변환할 수 있다.  
(반환 객체(MethodVisitor)를 바꿔서 바이트 코드를 변환한다)

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
    @Override
    public AnnotationVisitor visitAnnotation(String desc, boolean visible) {
        AnnotationVisitr av = super.visitAnnotation(desc, visible);
        // 어노테이션 바이트 코드 변환 로직
        return av;
    }
}
```

### visiteMethod 메서드

메서드에 해당하는 MethodVisitor를 반환한다.  
이때 메서드의 바이트 코드를 변환할 수 있다.

클래스에 있는 모든 메서드를 순회하며 호출된다.  
특정 메서드만 변환하려면 `visitMethod` 메서드에서 특정 메서드만 변환하도록 구현해야 한다.

### visitAnnotation 메서드

어노테이션에 해당하는 AnnotationVisitor를 반환한다.  

이때 desc는 어노테이션의 이름을 나타낸다.

---

## ClassWriter 클래스

바이트 코드를 작성하는 클래스  
(바이트 코드 조작 결과를 저장하는 클래스)

> ClassVisitor 클래스를 상속 받는 클래스이다.  
> 
> ClassWriter 클래스는 ClassVisitor 체인의 마지막 클래스로 사용된다.  
> 이때 그전에 방문한 모든 ClassVisitor들이 조작한 결과를 받아서 최종적인 바이트 코드를 생성한다.

### toByteArray 메서드

바이트 코드를 반환하는 메서드

> 이 메서드를 이용해 바이트코드를 조작하려면,
> 1. ClassReader로 바이트 코드를 읽어온다.
> 2. ClassReader의 accept 메서드로 ClassVisitor를 통해 바이트 코드를 분석 & 변환한다.
>
> 위 과정을 거친 후, ClassWriter의 toByteArray 메서드로 바이트 코드를 반환한다.

---

## MethodVisitor 클래스

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

### visitCode 메서드
메서드의 시작 지점에 호출된다.  
메서드의 시작 지점에 바이트 코드를 추가하려면 이 메서드를 오버라이드한다.

### visitInsn 메서드
메서드의 각 명령어에 호출된다.  
메서드의 각 명령어에 바이트 코드를 추가하려면 이 메서드를 오버라이드한다.

> opcode는 명령어 코드를 나타낸다.

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

---

## AnnotationVisitor 클래스

어노테이션을 분석하는 클래스

visit, visitArray, visitEnum 등의 메서드를 통해 어노테이션의 필드를 분석할 수 있다.

`visit()` - primitive 타입의 어노테이션 필드를 방문한다.
`visitEnum()` - enum 타입의 어노테이션 필드를 방문한다.
`visitAnnotation()` - 어노테이션 타입의 어노테이션 필드를 방문한다.
`visitArray()` - 배열 타입의 어노테이션 필드를 방문한다.

> 예를 들어 @GetMapping 어노테이션의 value 필드를 분석하려면  
> `visit` 메서드를 사용하여 value 필드를 분석할 수 있다.

---