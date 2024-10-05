# Comparable 인터페이스

객체의 정렬을 위해 사용하는 인터페이스이다.

`compareTo` 메소드를 구현해야 한다.

```java
public interface Comparable<T> {
    public int compareTo(T o);
}
```

`compareTo` 메소드는  
반환되는 값의 0, 양수, 음수에 따라 비교 대상의 순서를 결정한다.

- 0: 같은 값
- 양수: 비교 대상보다 큼
- 음수: 비교 대상보다 작음

```java
public class Student implements Comparable<Student> {
    private int id;
    private String name;

    public Student(int id, String name) {
        this.id = id;
        this.name = name;
    }

    @Override
    public int compareTo(Student o) {
        return this.id - o.id;
    }
}
```

---

# Comparator 인터페이스

`Comparator` 인터페이스는 객체의 정렬 방법을 별도로 구현할 수 있도록 한다.

`compare` 메소드를 구현해야 한다.

```java
public interface Comparator<T> {
    public int compare(T o1, T o2);
}
```

사실 `Comparator` 인터페이스는  
직접 구현하기 보단, 디폴트 메소드를 이용하는 경우가 많다.

---

## Comparator의 디폴트 메소드

> 디폴트 메서드들은 빌더 패턴을 사용하여,  
> 메서드 체이닝을 할 수 있다.  
> (메서드의 반환 타입이 `Comparator` 인터페이스이기 때문)

- `comparing`: 정렬 기준을 지정한다. (`Function` 인터페이스 사용)
- `thenComparing`: 정렬 기준을 추가한다. (`Function` 인터페이스 사용)
- `reversed`: 역순으로 정렬한다.

```java
class Main{
    public static void main(String[] args) {
        List<Student> students = new ArrayList<>();
        students.add(new Student(1, "A"));
        students.add(new Student(3, "C"));
        students.add(new Student(2, "B"));

        // id 오름차순
        students.sort(Comparator.comparing(Student::getId));
        // students.sort(Comparator.comparing(s -> s.getId()));

        // id 내림차순
        students.sort(Comparator.comparing(Student::getId).reversed());

        // id 오름차순, name 오름차순
        students.sort(Comparator.comparing(Student::getId).thenComparing(Student::getName));

        // id 오름차순, name 내림차순
        students.sort(Comparator.comparing(Student::getId).thenComparing(Student::getName).reversed());
    }
}
```

> 메서드 체이닝 시 주의할 점  
> `students.sort(Comparator.comparing(s -> s.getId());`  
> 위 코드만 이용했을 때는 문제가 없지만,  
> `students.sort(Comparator.comparing(s -> s.getId()).reversed());`  
> 처럼, 메서드 체이닝을 사용하면 컴파일 에러가 발생한다.
> 
> 이유는 메서드 체이닝을 사용하면서 제네릭 타입 추론이 제대로 이루어지지 않기 때문이다.  
> 이런 경우, 제네릭 타입을 명시해주면 된다.  
> `students.sort(Comparator.<Student, Integer>comparing(s -> s.getId()).reversed());`