## SQL이란

SQL(Structured Query Language)란 데이터베이스에서  
데이터를 추출하고 조작하는 데 사용하는 데이터 처리 언어

> SQL vs C언어
>
> 목적  
> SQL: DB에서, 데이터를 조작하고 관리하기 위한 언어, DB와 상호작용하는데 사용 됨  
> C언어: 범용 프로그래밍 언어, 다양한 종류의 소프트웨어를 개발하기 위해 사용 됨
> 
> 사용 방식  
> SQL: 비절차적(선언형) 언어(어떤 결과를 얻을 것인지 정의)
> C언어: 절차적(명령형) 언어(명시적으로 어떻게 작업을 수행할 것인지 제어)

---

## SQL의 실행 과정

SQL 작성 - 구문 분석 - 최적화 - 데이터 액세스 - 결과 반환

> 구문 분석(Parsing)
> 
> DBMS가 작성한 SQL을 문법적으로 검사한다.  
> (문장의 구조를 파악, 각 요소가 올바르게 배치되었는지 확인)

> 최적화(Optimization)
> 
> DBMS는 인덱스, 조인 순서 등을 고려하여 실행 계획 생성

---

## SQL의 종류

SQL은 기능에 따라 DDL, DML, DCL로 나눈다.

### DDL(Data Definition Language)

데이터 정의어, 테이블의 구조를 생성, 변경, 삭제 

CREATE, ALTER, DROP, TRUNCATE 등이 있다.

### DML(Data management Language)

데이터 조작어, 테이블의 데이터를 생성, 조회, 수정, 제거

SELECT, INSERT, UPDATE, DELETE가 있다.

> DROP, TRUNCATE, DELETE의 차이점
> 
> DROP과 TRUNCATE는 DDL로 오토 커밋에 해당한다(롤백 불가)  
> DELETE는 DML로, 롤백이 가능하다.

### DCL(Data Control Language)

데이터베이스에 접근하고 데이터들을 사용하도록 권한을 주고 회수하는 명령어

GRANT, REVOKE가 있다.

---

## 참조 무결성과 CASCADE

참조 무결성: 외래키는 참조할 수 없는 값을 가질 수 없다는 규칙

그런데 만약 참조 키가 참조하고 있는 컬럼의 값이 바뀌거나 삭제 된다면?    
-> 해당 컬럼를 참조하고 있는 참조키의 값을 전부 업데이트 해줘야 한다.

이떄 Cascade를 사용한다.

### CASCADE

cascade 옵션을 사용하면,  
특정 컬럼의 값을 삭제하거나 변경했을 때,  
해당 컬럼을 참조하고 있는 컬럼들도 자동으로 삭제/변경 되게 한다.

> cascade 옵션을 사용하여, 참조 무결성을 준수할 수 있게 된다.

```
create table course(
    course
    dept_name varchar(20) 
    foreign key (dept_name) references department
    on delete cascade // 자동 삭제
    on update cascade // 자동 변경
    . . .)    
```

---

## VIEW

뷰(VIEW)란, 다른 테이블로 만들어진 가상 테이블을 말한다.

> 뷰는 실제 테이블처럼, 행과 열을 가지고 있지만, 실제로 데이터를 저장하고 있지 않는다.  
> (특정 데이터를 보여주는 역할만 수행)
> 
> 여러 테이블을 번거롭게 들러서 확인을 해야 할 때 혹은  
> SELECT 문을 겹겹이 사용해서 어려운 쿼리문으로 조회를 수행해야 할 때  
> 이러한 번거로움을 줄여주는 것이 바로 뷰이다.

### 뷰의 장점/단점

장점
1. 특정 사용자에게 테이블 전체가 아닌 필요한 필드만 보여줄 수 있음(보안 관리)
2. 쿼리문을 쉽게 작성할 수 있음

단점
1. 한 번 정의된 뷰는 변경이 불가능
2. 삽입, 삭제, 변경 작업에 따른 오버헤드 발생 가능  
(테이블을 업데이트 하면 뷰도 업데이트 될 수 있음)
3. 뷰는 자신만의 인덱스를 가질 수 없음

---

## SELECT 

데이터베이스에서 데이터를 조회하기 위한 쿼리문



### SELECT 절의 처리순서

```sql
select [distinct] '필드이름1', '필드이름2', ...
from '테이블이름1'
join '테이블이름2' on


```

FROM 절 & JOIN 조건 - WHERE 절 - GROUP BY 절 - HAVING 절 - Window function - SELECT 절 - ORDER BY 절 - LIMIT 절


> SELECT ~ FOR UPDATE
> 
> 선택된 행을 업데이트 하기 위해 잠그는 데 사용된다.
> 
> -> 잠긴 트랜잭션이 완료될 때까지 다른 트랜잭션에서는 해당 행을 수정할 수 없습니다.   
> -> 동시 환경에서의 데이터 일관성을 제어하고 보장하기 위한 메커니즘입니다.

