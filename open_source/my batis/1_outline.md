### MyBatis

SQL 매퍼 프레임워크,  
자바 언어를 사용하여 RDB의 상호작용을 단순화하는 도구이다.

SQL 쿼리와 자바 객체 간의 매핑을 정의하고 실행하는데 사용된다.

---

### MyBatis의 장점

SQL을 XML에 편리하게 작성할 수 있고,  
동적 쿼리를 매우 편리하게 작성할 수 있다는 점이다.

> vs JdbcTemplate
>
> JdbcTemplate은 스프링에 내장되어 편하게 사용 가능하지만,  
> MyBatis는 약간의 설정이 필요하다.
>
> -> 프로젝트에서 동적 쿼리와 복잡한 쿼리가 많다면 MyBatis를 사용하고,  
> 단순한 쿼리들이 많다면 JdbcTemplate를 사용하는 걸 추천한다고 한다.
>
> ~~그리고 일단 JdbcTemplate보다 MyBatis를 많이 쓰는 것 같다.~~