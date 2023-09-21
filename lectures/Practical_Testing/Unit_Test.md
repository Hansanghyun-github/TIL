# 단위 테스트

다음과 같은 테스트 코드가 있다

```java
@Test
public void test1(){
    Americano americano = new Americano();
    Cafe cafe = new Cafe();

    cafe.add(americano);
    System.out.println("커피 이름: "+ cafe.getAll().get(0).getName());
    System.out.println("커피 가격: "+ cafe.getAll().get(0).getPrice());
}
```

위 테스트는 실패가 없다.<br>
그리고 그냥 결과를 콘솔창에 출력해서 사람이 직접 확인한다.

이런 코드는 자동화가 된 것이 아니다.

그리고 다른 팀원이 와서 이 코드를 실행해봐도 뭐가 맞는 것인지 모를 것이다.

---

### JUnit, AssertJ

JUnit

단위 테스트를 위한 프레임워크

AssertJ

테스트 코드 작성을 원활하게 돕는 테스트 라이브러리<br>
풍부한 API, 메서드 체이닝 지원

JUnit과 AssertJ를 이용해서 테스트 코드를 작성하면

```java
public void test1_Auto(){
    Americano americano = new Americano();
    Cafe cafe = new Cafe();

    cafe.add(americano);
    Assertions.assertThat(cafe.getAll().get(0).getName()).isEqualTo("아메리카노");
    Assertions.assertThat(cafe.getAll().get(0).getPrice()).isEqualTo(4000);
}
```

    JUnit도 Assertions가 있지만, AssertJ의 Assertions를 쓰자

이렇게 하면 assertThat에서 실패했을때 코드가 실패한다.

테스트 코드를 자동화할 수 있다.