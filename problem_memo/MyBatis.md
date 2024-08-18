### MyBatis 관련, NullPointerException 에러

mybatis 로그를 trace로 하고, 요청을 보냈을 때, mybatis 쿼리는 제대로 왔지만,  
이를 제대로 받지 못해 stream 부분에서 NullPointerException가 났다.

그 이유는 mybatis의 결과 클래스의 필드를 변경했는데, 이를 xml 파일에도 반영해줘야 하기 때문

> 쿼리의 결과가 로그로 찍혀도, xml 파일의 변수명이 맞지 않는다면, null 값이 들어갈 수 있다.

---

### InvalidDefinitionException: No serializer found for class {class path} and no properties discovered to create BeanSerializer

그냥 @Getter 없어서 그런것

---

// TODO MyBatis와 JPA 같이 빈 등록하려면 @SpringBootTest 밖에 없나?