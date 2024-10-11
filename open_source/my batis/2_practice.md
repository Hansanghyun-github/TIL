### MyBatis 설정

MyBatis를 사용하기 위해 `application.properties` 파일에 설정을 추가해야 한다.

> 테스트의 `application.properties`도 추가해야 한다.

`mabatis.type-aliases-package`: 패키지 이름을 생략하기 위해 사용  
(MyBatis에서 타입 정보를 사용할 때는 패키지 이름을 적어줘야 한다)

`mybatis.configuration.map-underscore-to-camel-case=true`  
언더바를 카멜로 자동 변경해주는 기능

> 자바 객체에는 주로 camelCase을 사용한다. (첫글자 소문자, 다음 단어 첫글자 대문자)  
> 반면에 RDB에서는 주로 snake_case를 사용한다. (소문자, 언더바로 단어 구분)

> 컬럼 이름과 객체 이름이 완전히 다른 경우에는 조회 SQL에서 별칭을 사용하면 된다.

---

### MyBatis 실습1 - 인터페이스 생성

```java
@Mapper
public interface ItemMapper{
    Optional<Item> findById(Long id);
    List<Item> findAll(ItemSearchCond itemSearch);
}
```

`@Mapper` 애노테이션을 붙여줘야, MyBatis에서 인식할 수 있다.

---

### MyBatis 실습2 - XML 생성

같은 위치에 실행할 SQL이 있는 XML 매핑 파일을 만들어줘야 한다.

> 자바 코드가 아니라서,  
> `src/main/resources` 하위에서, 패키지 위치를 맞춰서 만들어야 한다.
>
> 만약 XML 파일을 원하는 위치에 두고 싶다면,  
> `application.properties`에 다음 설정을 추가해야 한다.  
> `mybatis.mapper-locations=classpath:mapper/**/*.xml`

```xml
<mapper namespace="hello.itemservice.repository.mybatis.ItemMapper">
    <select id="findById" resultType="Item">
        select id, item_name, price, quantity
        from item
        where id = #{id}
    </select>
    
    <select id="findAll" resultType="Item">
        select id, item_name, price, quantity
        from item
        <where>
            <if test="itemName != null and itemName != ''">
                and item_name like concat('%',#{itemName},'%')
            </if>
            <if test="maxPrice != null">
                and price &lt;= #{maxPrice}
            </if>
        </where>
    </select>
</mapper>
```

`id`: 매퍼 인터페이스에 설정한 메서드 이름을 지정하면 된다.  
`#{}`: 파라미터를 지정한다.  
`resultType`: 반환 타입을 명시할 때 사용한다.
`where`: 적절하게 where 문장을 만들어준다.
`if`: 해당 조건이 만족되면 구문을 추가한다.

> `if`가 모두 실패하면 SQL where를 만들지 않는다.

> XML에서는 데이터 영역에 특수 문자(>, <)를 사용할 수 없다.  
> 대신 &lt(<), &gt(>)를 사용해야 한다.

---

### MyBatis 실습3 - 구현 객체 생성

```java
@Repository
@RequiredArgsConstructor
public class MyBatisItemRepository {
    private final ItemMapper itemMapper;
    
    public Optional<Item> findById(Long id) {
        return itemMapper.findById(id);
    }
    
    public List<Item> findAll(ItemSearchCond cond) {
        return itemMapper.findAll(cond);
    }
}
```

---

### Mapper 인터페이스

위 코드를 보면 ItemMapper 인터페이스의 구현체가 없다.

이 부분은 MyBatis 스프링 연동 모듈에서 자동으로 처리해준다.  
XML 파일을 보고, 인터페이스의 구현체를 스프링이 직접 만들어준다.

---

### MyBatis의 SQL injection

사용자의 입력으로 쿼리를 생성할 때,  
입력 문자열 자체를 이용해 쿼리를 만들 수도 있다.

> `#{}`: 파라미터 바인딩
> `${}`: 문자열 그대로 사용

이때 `${}`을 사용하면 SQL injection 문제가 발생할 수 있다.

> `#{}`은 Prepared Statement 기능을 제공한다.
>
> Prepared Statement  
> 입력을 문자열이 아닌 매개변수로 취급하여, SQL 쿼리의 일부로 간주되지 않게 한다.  
> 따라서 사용자 입력이 쿼리의 구조를 변경하거나 악의적인 명령어를 삽입하는 공격을 방지한다.

---

MyBatis가 어떻게 쿼리의 테이블과 자바 클래스를 매핑할까

mybatis에 파라미터를 보낼떄, 두개 이상이면 `@Param("{이름}")` 으로 구분해줘야 한다.






