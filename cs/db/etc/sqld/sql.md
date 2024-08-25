# SQL(Structed Query Language)

sql이란 데이터를 관리하기 위해 설계된 특수 목적의 프로그래밍 언어이다.

<img src="../../../../img/images_alicesykim95_post_e12c29bf-f5ba-4c5d-9905-50e1ba60c443.png" width=650>

---

## DDL(Data Definition Language, 데이터 정의어) - Auto Commit

DB 구조 또는 스키마를 정의하는데 사용

> 주의: 직접 DB의 테이블에 영향을 미치기 때문에 DDL 명령어를 입력하는 순간, <br>
> 명령어에 해당하는 작업이 `즉시 커밋`된다는것을 기억하자

`CREATE` - 데이터베이스의 객체를 생성

※SCHEMA, DOMAIN, TABLE, VIEW, INDEX를 정의하거나 변경 또는 삭제할 때 사용하는 언어

※데이터 베이스 관리자나 데이터베이스 설계자가 사용

👉 CREATE 규칙

- 객체를 의미하는 것이므로 단수형으로 이름을 짓는걸 권고한다.
- 유일한 이름으로 명명해야 한다.
- 테이블 내의 컬럼명 또한 중복되지 않는 유일한 이름으로 명명해야 한다.
- 정의할 때 각 컬럼은 ,으로 구분하며 테이블 생성문의 마지막은 ;이다.
- 컬럼명은 데이터 표준화 관점에서 일관성 있게 사용해야 한다.
- 컬럼 뒤에 데이터 유형을 반드시 지정해야 한다.
- 테이블과 컬럼명은 반드시 문자로 시작한다.
- 대소문자 구분을 하지 않지만, 기본적으로 대문자로 만들어진다.

    CREATE TABLE 테이블이름 (
        필드이름1 필드타입1,
        필드이름2 필드타입2,
    )

    제약조건 - NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, DEFAULT 기본값

    default를 설정해도 직접 null을 넣으면 null이 들어가네

`ALTER` - 데이터베이스의 구조를 변경

👉 ALTER: 컬럼 변경 문법

|명령어|내용|
|--|--|
|ADD COLUMN|컬럼을 추가하는 역할|
|DROP COLUMN|컬럼을 삭제하는 역할|
|MODIFY COLUMN|컬럼을 수정하는 역할|
|RENAME COLUMN|컬럼 이름을 변경하는 역할|
|DROP CONSTRAINT|컬럼을 제약조건을 기반해서 삭제하는 역할|

    ALTER TABLE 테이블이름 ADD 필드명 필드타입;
    ALTER TABLE 테이블이름 DROP 필드명;
    ALTER TABLE 테이블이름 MODIFY 필드명 필드타입;

`DROP` - 데이터베이스의 객체를 삭제 (테이블의 모든 데이터와 구조를 삭제)

    DROP TABLE 테이블명;

`TRUNCATE` - 테이블을 초기화
    > 테이블 내의 스키마는 남겨놓고, 태이블 내의 데이터 만을 지울때 사용

    TRUNCATE TABLE 테이블명;

`RENAME` - 데이터베이스의 객체 이름 변경

`COMMENT` - 데이터에 주석등을 추가

---

## DML(Data Manipulation Language)

정의된 데이터베이스에 입력된 레코드를 조회하거나 수정하거나 삭제하는 등의 역할을 하는 언어

`SELECT`	데이터베이스에서 데이터를 검색하는 역할

    SELECT문 실행 순서 예제<br>
    5 SELECT<br>
    1 FROM<br>
    (start with, connected by)
    2 WHERE<br>
    3 GROUP BY<br>
    4 HAVING<br>
    6 ORDER BY<br>

    FROM - (start with, connect by) - WHERE - GROUP BY - HAVING - SELECT - ORDER BY

`INSERT`	테이블에 데이터를 추가하는 역할

    INSERT INTO 테이블명(필드명_1, 필드명_2, 필드명_3, ...)
    VALUES (필드값_1, 필드값_2, 필드값_3, ...), (필드값_1, 필드값_2, 필드값_3), ...;

    insert할때 default로 설정된곳은 굳이 안넣어도 에러안남, PK여도 가능

    삽입 컬럼을 명시하지 않았을 경우 모든 컬럼을 삽입해야 한다

`UPDATE`	테이블 내에 존재하는 데이터를 수정하는 역할

    UPDATE 테이블명
    SET 필드명_1=필드값_1, 필드명_2=필드값_2, ...
    WHERE 필드명_1=필드값_1, 필드명_2=필드값_2, ...;

`DELETE`	테이블에서 데이터를 삭제하는 역할

    DELETE FROM 테이블명
    WHERE 필드명_1=필드값_1, 필드명_2=필드값_2, ...;

---

## DCL(Data Control Language)

데이터를 관리 목적으로 보안, 무결성, 회복, 병행 제어 등을 정의하는데 사용한다. DCL을 사용하면 데이터베이스에 접근하여 읽거나 쓰는 것을 제한할 수 있는 권한을 부여하거나 박탈할 수 있고 트랜잭션을 명시하거나 조작할 수 있다.

`GRANT` - 권한을 정의할때 사용하는 명령어

    GRANT 시스템 권한명 [, 시스템 권한명 ... | 롤명]<br>
    TO 유저명 [, 유저명... | 롤명 ... |PUBLIC | ​[WITH ADMIN OPTION]];

`REVOKE` - 권한을 삭제할때 사용하는 명령어

    REVOKE { 권한명 [, 권한명...] ALL}
    ON 객체명
    FROM {유저명 [, 유저명...] | 롤명(ROLE) | PUBLIC} 
    [`CASCADE CONSTRAINTS`]

|종류|설명|
|--|--|
|WITH GRANT OPTION|자신이 부여받은 권한에서 다른 사용자에게 권한 부여 가능, 권한을 회수할 경우 연쇄적으로 권한이 회수된다.|
|CASCADE|권한제거 명령어 로 부여된 권한 트리를 모두 제거한다.|
|RESTRICT|권한제거 명령어 로 지정한 권한을 제거 할 경우 타 사용자에게 영향이 가면 실패 하도록 처리하는 명령어|

---

## TCL (Transaction Control Language)

DCL과 비슷한 맥락이지만 데이터를 제어하는 언어가 아닌 트랜잭션을 제어할때 사용한다. 논리적인 작업 단위를 묶어 DML에 의해 조작된 결과를 트랜잭션 별로 제어한다.

`COMMIT`	모든 작업을 정상적으로 처리하겠다는 명령어

`ROLLBACK`	모든 작업을 다시 돌려 놓겠다는 명령어

`SAVEPOINT`	Commit 전에 특정 시점까지만 반영하거나 Rollback하겠다는 명령어

    SAVEPOINT 이름이 같을때 마지막에 저장한 값으로 ROLLBACK 한다.

---

## 그룹 함수

    그룹 함수는 기존의 결과를 그룹별로 `나누는`거다.

    group by 1,2, ... 있으면 1로 나누고 그 다음 2로 나누고 진행하면됨

    그룹함수는 그냥 집계를 도와주는 함수라고 생각하자

|구분|설명|
|--|--|
|ROLLUP|- 총계와 소그룹 간의 소계를 계산하는 ROLLUP 함수|
|--|- 인수는 계층 구조이므로 인수 순서가 바뀌면 수행 결과도 바뀌게 되므로 인수의 순서에도 주의|
|--|예) GROUP BY ROLLUP (DEPTNO); → DEPTNO 합계(소계), 총계를 조회|
|CUBE|- CUBE는 제시한 칼럼에 대해서 결합 가능한 모든 집계를 계산한다.|
|--|- 다차원 집계를 제공하여 다양하게 데이터를 분석할 수 있다.|
|--|예) GROUP BY CUBE(DEPTNO, JOB); → DEPTNO 합계, JOB 합계, DEPTNO & JOB 합계, 총계를 조회, 조합할 수 있는 모든 경우의 수가 조합된다. *시스템에 부하를 많이 주는 단점이 있음|
|GROUPING SETS|- 원하는 부분의 소계만 손쉽게 추출하여 계산할 수 있는 GROUPING SETS 함수|

`GROUPING` : Subtotal과 GRand total의 행이 어디인지 0,1값으로 알려줌

- ROLLUP이나 CUBE에 의한 소계가 계산된 결과(해당 COLUMN이 NULL인 곳)에는 GROUPING(EXPR) = 1 이 표시되고,
- 그 외의 결과에는 GROUPING(EXPR) = 0 이 표시

>

    ROLLUP과 CUBE에 여러 column을 넣으면, 
    
    ROLLUP은 마지막 column에 대한 집계, 다음 column에 대한 집계(마지막을 제외하고), ... 첫번째 column에 대한 집계(뒤쪽을 전부 제외하고)를 보여주면

    CUBE는 마지막 column에 대한 집계, 다음 column에 대한 집계, ... 첫번째 column에 대한 집계, 전체 집계를 보여준다.

    그래서 CUBE는 순서가 의미가 없음
>
    ROLLUP(A,B) = GROUPING SETS((A,B), A, ())
    ROLLUP(A) = GROUPING SETS(A, ())
    CUBE(A,B) = GROUPING SETS((), B, A, (A,B))
    ROLLUP(A), A = A집계 두번한것
>
    mysql은 with rollup, grouping 사용가능
