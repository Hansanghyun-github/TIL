# SQL (Structured Query Language)

RANK() - 중복값은 중복등수, 등수 건너뜀
DENSE_RANK() - 중복값은 중복등수, 등수 안 건너뜀
ROW_NUMBER() - 중복값이 있어도 고유 등수 부여

START WITH
CONNECT BY

오라클이 지원하느 질의 방법으로 계층형 구조를 탐색할 수 있다.

순위함수 사용시 ORDER BY를 입력해야 한다.

 ORDER SIBLINGS BY 를 수행하면 전체 테이블이 아니라 계층형으로 된 데이터값(특정 칼럼) 기준으로 정렬된다

|구분|설명|
|--|--|
|ROLLUP|- 전체합계와 소그룹 간의 소계를 계산하는 ROLLUP 함수|
|--|예) GROUP BY ROLLUP (DEPTNO); → DEPTNO 합계(소계), 전체 합계를 조회|
|CUBE|- CUBE는 제시한 칼럼에 대해서 결합 가능한 모든 집계를 계산한다.|
|--|- 다차원 집계를 제공하여 다양하게 데이터를 분석할 수 있다.|
|--|예) GROUP BY CUBE(DEPTNO, JOB); → DEPTNO 합계, JOB 합계, DEPTNO & JOB 합계, 전체 합계를 조회, 조합할 수 있는 모든 경우의 수가 조합된다. *시스템에 부하를 많이 주는 단점이 있음|
|GROUPING SET|- 원하는 부분의 소계만 손쉽게 추출하여 계산할 수 있는 GROUPING SETS 함수|

### 인덱스 생성
UNIQUE SCAN : 유일한 값 하나 찾기 (예: 고객아이디) *한개의 행

RANGE SCAN : 어떠한 조건에서 한 범위를 찾기 (예:주문번호)

FULL SCAN : 전체 데이터 *전체 행

---

문자형과 숫자형을 비교 시 문자형을 숫자형으로 묵시적 변환하여 비교한다.

CHAR는 길이가 서로 다르면 짧은 쪽에 스페이스를 추가하여 같은 값으로 판단한다. 같은 값에서 길이만 서로 다를 경우 다른 값으로 판단하는 것은 VARCHAR(가변길이 문자형 : 입력한 크기만큼 할당 )로 비교하는 경우이다

---

메인쿼리의 값을 서브쿼리에서 주입을 받아서 비교를 하는것으로 상호연관 서브쿼리(CORRELATED SUB QUERY) 이다.

---

칼럼의 변경은 ALTER TABLE ~ MODIFY 문을 사용하면 된다. 칼럼은 데이터 타입 및 길이를 변경 할 수 있다.

추가(ADD), 삭제(DROP)

---

서브쿼리에 있는 칼럼을 자유롭게 사용할수 없다

---

(오라클 DB에서)
오늘 날짜를 구하기 위해서 SYSDATE+1을 해주면된다. 단, 데이트 타입을 문자열 TO_CHAR 로 변환해주어야 한다.

---

ROLE은 데이터베이스에서 OBJECT(테이블, 프로시저, 뷰) 등의 권한을 묶어서 관리할 수 있다.

---

GRANT(권한부여), REVOKE(권한회수)

-시스템 권한 부여(GRANT) 기본 문법

`GRANT` 시스템 권한명 [, 시스템 권한명 ... | 롤명]<br>
`TO` 유저명 [, 유저명... | 롤명 ... |PUBLIC | ​[`WITH ADMIN OPTION`];

-객체 권한의 회수 (Revoke) 기본 문법 

`REVOKE` { 권한명 [, 권한명...] ALL}

`ON` 객체명

`FROM` {유저명 [, 유저명...] | 롤명(ROLE) | PUBLIC} 

[`CASCADE CONSTRAINTS`]

---

### SELECT의 논리적인 수행 순서

FROM - WHERE - GROUP BY - HAVING - SELECT - ORDER BY

---

## 조인 수행 원리
 
조인이란 두 개 이상의 테이블을 하나의 집합으로 만드는 연산이다.

FROM 절에 세 개의 테이블이 존재하더라도 세 개의 테이블이 동시에 조인이 수행되는 것은 아니다.<br>
세 개의 테이블 중에서 먼저 두 개의 테이블에 대해 조인이 수행된다. 그리고 먼저 수행된 조인 결과와 나머지 테이블 사이에서 조인이 수행된다. 

### 1. Nested Loop Join

중첩for문 방식

inner table에 인덱스가 걸려있지 않으면 굉장히 비효율적
> outer table에서 한건한건 조회할때마다 inner table을 full scan해야 하기 떄문

대량의 테이블을 조인하는 방식으로 적절하지 않다

크기가 작은 테이블이 outer table이 되야 성능에 유리하다
> 1:n이라면 1이 outer table로

### 2. Sort Merge Join

NL join에서 두 테이블을 우선 조인컬럼을 기준으로 정렬을 진행하고 조인을 진행한다.

> inner table에 적절한 인덱스가 없어서 NL join을 쓰기에 너무 비효율적일때 사용한다.

equal join이 아니라 범위로 join을 할때 적절한 수행 원리라고 할 수 있다.

table random access가 일어나지 않고 sorting 작업이 PGA영역에서 수행되기 떄문에

경합이 발생하지 않아 성능에 유리한 이점이 있다.

### 3. Hash Join

배치에서 쓰기 좋은 수행원리

대용량 테이블을 조인할떄 쓰기 좋은 조인

PGA영역에 해시 영역을 생성

첫번째 테이블을 해시 테이블에 넣는다.

그리고 두번쨰 테이블이 읽히면서 조인이 되는 원리

해쉬 영역에 올라갈때 JoinColumn을 기준으로 hash function이 적용되기 때문에

key 컬럼에 중복값이 없을수록 성능에 유리하다

> equal join만 가능하다. 범위 조인 x

> sort merge join처럼 random access 부하가 없다.

> 유의할점
>
> 해시영역에 들어가는 테이블의 크기가 충분히 작아야 성능에 유리하다.
>
> 너무 커지면 디스크 영역을 사용하게 되어 성능이 안좋아진다.

수행빈도가 높은 OLTP 환경에서 이 조인을 사용하게 되면<br>
오히려 CPU나 메모리의 사용량이 늘어서 성능이 안좋아질수있다.