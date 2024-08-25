# 스프링 데이터 JPA에서 페이징과 정렬

`반환 타입`  
Page 인터페이스 - 내가 세팅한 페이징 쿼리와 추가 count 쿼리 결과를 포함한다.
Slice - 내가 세팅한 페이징 쿼리만 보낸다.

> Slice는 추카 count 쿼리를 보내지 않기 때문에, 내부적으로 limit + 1로 조회한다.  
> (다음 페이지가 존재하는지 알기 위해)  
> (Page는 count 쿼리를 통해 다음 페이지가 존재하는지 알 수 있다)

```List<Member> findByUsername(String name, Pageable pageable);```

Pageable - Sort를 포함한 페이징 기능이 있는 파라미터(인터페이스)  
(PageRequest가 대표적인 구현체이다.)

```
PageRequest pageRequest = PageRequest.of(0, 3, Sort.by(Sort.Direction.DESC,
"username"));
Page<Member> page = memberRepository.findByUsername("han", pageRequest);
```

```Page의 메서드들```  
page.getContent() - 조회된 데이터를 반환  
page.getNumber() - 페이지 번호를 반환(0부터 시작)  
page.isFirst() - 현재 페이지가 첫번째 항목인지 반환  
page.hasNext() - 다음 페이지가 있는지 반환  
page.getTotalElements() - 전체 데이터 수를 반환  
page.getNumberOfElements() - 현재 페이지의 데이터들의 수를 반환  

---

```최적화를 위한 count 쿼리 분리```

```java
@Query( value = “select m from Member m”,
        countQuery = “select count(m.username) from Member m”)
Page<Member> findMemberAllCountBy(Pageable pageable);
```