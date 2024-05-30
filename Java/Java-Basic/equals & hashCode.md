## equals() & hashCode()

> Java에서 equals() 메서드를 오버라이드할 때 hashCode() 메서드도 함께 오버라이드 해야 하는 이유

Java에서 equals() 메서드를 오버라이드할 때, hashCode() 메서드도 함께 오버라이드하는 것은 중요한 프로그래밍 관례이다.  
이 두 메서드는 객체의 동등성 비교와 해시 기반 컬렉션에서의 효율적인 객체 관리에 관련이 있다.

`equals()와 hashCode()의 연관성`  
동일성과 동등성의 관계: equals() 메서드는 두 객체의 동등성을 확인한다.  
그리고 hashCode() 메서드는 해시 기반 컬렉션에서 객체를 빠르게 찾기 위해 사용된다.

    동일성(identity): 두 객체의 값들 뿐만 아니라, 주소까지 같은지 확인
    동등성(equality): 두 객체의 값들이 같은지 확인

`hashCode() 메서드의 의무`  
두 객체가 equals()에 따라 동등하다면, 두 객체의 hashCode() 값은 같아야 한다.  
이것은 해시 기반 컬렉션에서 객체를 올바르게 찾을 수 있게 한다.

`코드 일관성과 안정성`  
1. `다른 부분에서의 사용 가능성`  
현재 해시 기반 컬렉션을 사용하고 있지 않더라도, 나중에 사용할 수도 있다.  
hashCode()를 오버라이드하지 않으면 나중에 예상치 못한 문제가 발생할 수 있다.
2. `코드 일관성 유지`  
equals()를 오버라이드할 때 hashCode()도 함께 오버라이드하는 것은 Java 프로그래밍의 일반적인 규칙 중 하나이다.  
이것은 코드의 일관성을 유지하고 예기치 못한 버그를 방지하는 데 도움이 된다.

> 그리고 외부 라이브러리에서 hashCode()를 이용해서 구분할 수도 있다.

---

### 예시

```
@AllArgsConstructor
public class TestClass {
        public int age;
        public String name;

        @Override
        public boolean equals(Object obj) {
            if(obj == null) return false;
            if(obj.getClass() != this.getClass()) return false;

            TestClass testClass = (TestClass) obj;
            return (age == testClass.age) && name.equals(testClass.name);
        }
    }
```

이름과 나이를 가지고 있는 `TestClass`가 있다.  
이 클래스는 equals는 오버라이딩 했지만, hashCode는 오버라이딩 하지 않았다.

```
void test(){
    HashSet<TestClass> hashSet = new HashSet<>();
    hashSet.add(new TestClass(10, "name1"));
    hashSet.add(new TestClass(10, "name1"));
    hashSet.add(new TestClass(10, "name1"));
}
```

HashSet에 나이와 이름이 같은 TestClass 인스턴스를 총 3개 넣었다.

```
System.out.println(hashSet.size()); // 결과: 3
```

hashSet의 길이는 3이 나왔다.

> 이름과 나이가 같지만, hashCode()를 오버라이딩 하지 않아서, hashSet이 다른 객체로 인식했기 때문이다.

그래서 추가로 hashCode를 오버라이딩 해준다.

```

public class TestClass{
    ...

    @Override
    public int hashCode() {
        return Objects.hash(age, name);
        // Objects.hash(...)는 파라미터의 값들이 같다면
        //같은 해시코드를 반환한다.
    }
}
```

위 TestClass를 이용해서 다시 HashSet을 세팅하고 길이를 출력해봤다.

```
void test(){
    HashSet<TestClass> hashSet = new HashSet<>();
    hashSet.add(new TestClass(10, "name1"));
    hashSet.add(new TestClass(10, "name1"));
    hashSet.add(new TestClass(10, "name1"));
    
    System.out.println(hashSet.size()); // 결과: 1
}
```

hashCode를 오버라이딩 해서, 객체 내의 값들이 같다면 같은 해시코드가 반환되기 때문에, HashSet이 같은 객체로 판단하여 길이가 1이 나오게 되었다.

---
### 결론

Java에서는 equals()를 오버라이드할 때, hashCode()도 함께 오버라이드하는 것이 좋은 프로그래밍 관행이다.  
두 메서드를 함께 다루면 객체의 동등성과 해시 기반 컬렉션에서의 안정적인 동작을 보장할 수 있다.  
코드의 일관성과 안정성을 유지하기 위해 항상 두 메서드를 함께 다루도록 노력해야 한다.