# String 클래스

`String` 클래스는 자바에서 문자열을 다루기 위한 클래스이다.

> `int`, `boolean` 같은 기본형이 아니라 참조형이다.

`String` 클래스는 `new` 키워드를 사용하지 않고도 객체를 생성할 수 있다.

쌍따옴표로 문자열을 감싸면 자바 언어에서  
자동으로 `String` 객체를 생성해준다.

```java
public class String {
    public static void main(String[] args) {
        String str = "Hello, World!";               // 기존
        String str2 = new String("Hello, World!");  // 변경
    }
}
```

---

## String 클래스 구조

```java
public final class String {
    private final char[] value; // 자바 9 이전
    private final byte[] value; // 자바 9 이후
}
```

value 필드에 실제 문자열 값이 보관된다.  

> 영어, 숫자는 1byte로 표현 가능하지만,  
> 나머지(한글 등)의 경우 2byte인 UTF-16 인코딩을 사용한다.
> 
> 따라서 자바 9 이후 byte[] 타입을 사용한다.  
> (메모리를 더 효율적으로 사용하기 위함)

---

## 문자열 풀

자바에서는 문자열 리터럴을 사용하면  
자바 컴파일러가 자동으로 문자열 풀에 저장한다.

따라서 문자열 리터럴을 사용하는 경우 같은 참조값을 가지므로  
`==` 연산자로 비교하면 `true`가 나온다.

```java
public class String {
    public static void main(String[] args) {
        String str1 = "Hello, World!";
        String str2 = "Hello, World!";
        String str3 = new String("Hello, World!");

        System.out.println(str1 == str2);  // true
        System.out.println(str1 == str3);  // false
    }
}
```

이때 `new` 키워드를 사용하여 String 객체를 생성하면  
새로운 객체를 생성하므로 참조값이 달라진다.

```java
public class String {
    public static void main(String[] args) {
        String str1 = "Hello, World!";
        String str2 = "Hello, World!";
        String str3 = new String("Hello, World!");

        System.out.println(System.identityHashCode(str1));  // 366712642
        System.out.println(System.identityHashCode(str2));  // 366712642
        System.out.println(System.identityHashCode(str3));  // 1829164700 - different
        
        // hashcode() 메서드는 모두 같은 값을 반환한다.
        // System.identityHashCode() 메서드는 객체의 고유한 참조값을 반환한다.
    }
}
```

따라서 String 클래스를 비교할 때는  
`equals()` 메서드를 사용하는 것이 안전하다.



---

## 불변 객체인 String 클래스

```java
public class String {
    public static void main(String[] args) {
        String str = "Hello, World!";
        str.concat("Java");  // "Hello, World!Java" 반환

        System.out.println(str); // "Hello, World!"
    }
}
```

`String` 클래스는 불변 객체이다.  
따라서 `concat()` 메서드를 호출해도  
원본 문자열은 변경되지 않는다.

### String이 불변으로 설계된 이유

문자열 풀에 있는 String 인스턴스의 값이 변경되면  
다른 참조하는 변수들도 같이 변경되기 때문이다.

---

## StringBuilder - 가변 String

> 불변 객체인 String 클래스는 내부 값을 변경할 수 없다.  
> 문자를 더하거나 변경할 때마다 계속해서 새로운 객체를 생성한다.  
> (메모리 낭비 & 잦은 GC 발생)
>
> 대신 간단한 문자열의 `+` 연산은 자바 컴파일러가  
> 내부적으로 문자열 리터를 더하는 부분을 자동으로 합쳐준다.

`StringBuilder` 클래스는 가변 객체로  
문자열을 변경할 때마다 새로운 객체를 생성하지 않는다.

```java
public class StringBuilder {
    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder("Hello, World ");
        sb.append("Java");

        System.out.println(sb.toString());  // "Hello, World Java"
        
        sb.insert(5, "Java ");
        System.out.println(sb.toString());  // "Hello Java, World Java"
        
        sb.delete(0, 5);
        System.out.println(sb.toString()); // "Java, World Java"
        
        sb.reverse();
        System.out.println(sb.toString()); // "avaJ dlroW ,avaJ"
    }
}
```

1. StringBuilder 객체 생성
2. `append()` 메서드로 문자열 추가
3. `insert()` 메서드로 특정 위치에 문자열 삽입
4. `delete()` 메서드로 특정 위치의 문자열 삭제
5. `reverse()` 메서드로 문자열 뒤집기

### StringBuilder의 메서드 체이닝

`append()`, `insert()`, `delete()`, `reverse()` 메서드는  
객체 자신을 반환하므로 메서드 체이닝이 가능하다.

```java
public class StringBuilder {
    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder("Hello, World ");
        sb.append("Java").insert(5, "Java").delete(0, 5).reverse();

        System.out.println(sb.toString());  // "avaJ dlroW ,avaJ"
    }
}
```

---

## StringBuffer

`StringBuffer` 클래스는 `StringBuilder`와 같은 기능을 제공하지만  
멀티 스레드 환경에서 동기화를 지원한다.

따라서 멀티 스레드 환경에서는 `StringBuffer`를 사용하는 것이 안전하다.

```java
public class StringBuffer {
    public static void main(String[] args) {
        StringBuffer sb = new StringBuffer("Hello, World ");
        sb.append("Java").insert(5, "Java").delete(0, 5).reverse();

        System.out.println(sb.toString());  // "avaJ dlroW ,avaJ"
    }
}
```

실제로 내부 메서드들에 `synchronized` 키워드가 붙어있다.

```java
public final class StringBuffer {
    public synchronized StringBuffer append(String str) {
        // ...
    }
}
```

---