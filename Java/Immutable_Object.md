# 불변객체(Immutable Object)

불변객체는 `재할당은 가능하지만, 한번 할당하면 내부 데이터를 변경할 수 없는 객체`

자바에서 String, Integer 등이 있다

> String str="a"를 str="b"로 해준다고 str 내부의 값이 변한게 아니다
>
> "b"라는 새로운 String을 str에 할당한 것

### 불변 객체 예시

```java
class MutableObject {
    public int cnt;
    public String name;
    
    public MutablePerson(int cnt, String name) {
        this.cnt = cnt;
        this.name = name;
    }
}
```

위 클래스는 외부에서 cnt나 name을 변경할 수 있다.

-> 불변이 아닌 클래스이다.

```java
class ImmutableObject {
    public final int cnt;
    public final String name;
    
    public ImmutablePerson(int cnt, String name) {
        this.cnt = cnt;
        this.name = name;
    }
}
```

위 클래스는 외부에서 cnt나 name을 변경할 수 없다.

### 불변 객체의 장단점

장점
1. 객체에 대한 신뢰도가 높아진다. 
2. 생성자, 접근메소드 때문에 객체 내의 메소드에서 필드 값이 변할 걱정을 할 필요가 없다.
3. 멀티스레드 환경에서 동기화 처리없이 객체를 공유할 수 있다.

단점 -  성능저하 가능
> 재할당 할때마다 새로운 객체가 필요하기 때문

### 불변 객체 만들어보기

Immutable Object를 만드는 기본적인 아이디어는 필드에 final을 사용하고, Setter를 구현하지 않아야 한다.<br>
이 아이디어는 불변객체의 필드가 모두 원시 타입일 경우에만 가능하고, 참조 타입일 경우엔 추가적인 작업이 필요하다.

#### 원시 타입만 있는 경우

원시 타입인 필드에 ```final```을 선언해주면 됨<br>
-> setter 자동 불가능

#### 참조타입이 있는 경우

원시 타입과는 다르게 ```final```만으로 불변객체를 만들 수 없다.

```java
class Person{
    private final Information information;
    ...
}

class Information{
    private String name;
    private int age;
    ...
}
```

위 Person 클래스는 Information 필드 자체는 변경할 수 없지만, Information 필드 내의 값을 변경할 수 있다.

참조타입인 경우는 객체를 참조(1), Array(2), List(3)이 있다.

1. 참조변수가 일반 객체일 경우 - 일반 객체도 불변객체여야 함

2. 참조변수가 Array일 경우

    생성자에서 배열을 받아 copy해서 저장하고, getter에서 clone을 반환
    > getter 이후 외부에서 배열 내부값을 변경시킬 수 없도록

    ```java
    public class ArrayObject {

        private final int[] array;

        public ArrayObject(final int[] array) {
            this.array = Arrays.copyOf(array,array.length);
        }


        public int[] getArray() {
            return (array == null) ? null : array.clone();
        }
    }
    ```

3. 참조변수가 List일 경우

    List인 경우에도 Array와 마찬가지로 생성시 생성자 인자를 그대로 참조하지 않고, 새로운 List를 만들어 값을 복사하도록 해야합니다. 그리고 getter를 통해 값 추가/삭제가 불가능하도록 Collection의 unmodifiableList 메서드를 사용한다.

    ```java

    public class ListObject {

        private final List<Animal> animals;

        public ListObject(final List<Animal> animals) {
            this.animals = new ArrayList<>(animals);
        }

        public List<Animal> getAnimals() {
            return Collections.unmodifiableList(animals);
        }
    }
    ```

---

### 결론

불변객체는 한번 할당하면 필드 값을 변경할 수 없는 객체<br>
하지만 재할당은 가능<br>
필드가 원시 타입일 경우엔 final 사용으로 불변객체를 만들 수 있고, 참조 타입일 경우엔 추가적인 작업이 필요하다 (copy, clone, unmodifiableList)
