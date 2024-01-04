몇몇 자바 클래스들은 이 클래스를 implements 한다.

```java
public interface Serializable {
}
```

해당 클래스를 implements하면 뭐가 좋을까?

이를 알려면 자바의 직렬화를 알아야 한다.

---

`직렬화(Serialize)`<br>
자바 시스템 내부에서 사용되는 Object 또는 Data를 외부의 자바 시스템에서도 사용할 수 있도록 byte 형태로 데이터를 변환하는 기술.
JVM(Java Virtual Machine 이하 JVM)의 메모리에 상주(힙 또는 스택)되어 있는 객체 데이터를 바이트 형태로 변환하는 기술

`역직렬화(Deserialize)`<br>
byte로 변환된 Data를 원래대로 Object나 Data로 변환하는 기술을 역직렬화(Deserialize)라고 부릅니다.
직렬화된 바이트 형태의 데이터를 객체로 변환해서 JVM으로 상주시키는 형태.

    DB나 파일에 데이터를 넣거나 가져올 때 직렬화와 역직렬화를 사용한다.

직렬화 조건<br>
java.io.Serializable 인터페이스를 상속받은 객체는 직렬화 할 수 있는 기본 조건입니다.

직렬화 방법<br>
java.io.ObjectOutputStream를 사용하여 직렬화를 진행합니다.

역직렬화 방법<br>
java.io.ObjectInputStream를 사용하여 역직렬화를 진행합니다.

---

`transient`

보통 클래스의 멤버변수 전부 직렬화 대상에 해당된다.
하지만 보안 상의 문제나 기타 이유로 멤버 변수의 일부를 제외하고 싶다면 transient를 사용하면 된다.

```java
public class User implements Serializable {
    private String id;
    private transient String password;
    private String email;

    //....
}
```

---

사실 자바의 직렬화는 문제가 많다.

1. 싱글톤을 보장해주지 않는다.
2. 보안상에서도 문제가 있다.

등등 ...

---

바이트스트림으로의 직렬화가 아닌 다른 방법도 있다.

`JSON 직렬화, 역직렬화`

지금까지는 객체 직렬화를 JVM과 ObjectInputStream/ObjectOutputStream에 위임하는 방식이었지만 XML, JSON과 같은 포맷을 이용한 직렬화도 가능하다. 이로 인한 장점은 다른 환경, 다른 언어로 만들어진 어플리케이션과도 통신이 가능해진다는 것이다.
 
JSON 파싱, 처리 라이브러리를 사용하여 자바 객체를 JSON으로 직렬화하거나 JSON 데이터를 자바 객체로 역직렬화할 수 있다. 여기서는 Jackson을 사용한다.(ObjectMapper)

---

`ObjectMapper 사용`

1. Object -> String 문자열 : writeValueAsString

```java
ObjectMapper mapper = new ObjectMapper();
Car car = new Car("K5", "gray");

String text = mapper.writeValueAsString(car); //{"name":"K5","color":"gray"}
```

 

2. String 문자열 -> Object : readValue

```java
Car carObject = mapper.readValue(text, Car.class); //Car{name='k5',color='gary'}
 ```