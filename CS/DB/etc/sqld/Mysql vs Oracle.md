# Mysql vs Oracle

구조적 차이

    오라클 : DB 서버가 통합된 하나의 스토리지를 공유하는 방식

    MYSQL : DB 서버마다 독립적인 스토리지를 할당하는 방식

 

조인 방식의 차이

    오라클 : 중첩 루프 조인, 해시 조인, 소트 머지 조인 방식을 제공함.

    MYSQL : 중첩 루프 조인 방식을 제공함.

 

확장성의 차이
    
    오라클 : 별도의 DBMS을 설치해 사용할 수 없음

    MYSQL : 별도의 DBMS을 설치해 사용할 수 있음

 

메모리 사용율의 차이
    
    오라클 : 메모리 사용율이 커서 최소 수백MB 이상이 되어야 설치 가능함.

    MYSQL : 메모리 사용율이 낮아서 1MB 환경에서도 설치가 가능함.

 
파티셔닝

    오라클 : Local Partion Index, Global Partion Index를 지원

    MYSQL : Local Partion index만 지원

 

힌트 방식

    오라클 : 힌트에 문법적 오류가 있으면 힌트를 무시하고 쿼리를 수행한다.

    MYSQL : 힌트에 문법적 오류가 있으면 오류를 발생시킨다.

 

SQL 구문의 차이

NULL 대체

    [오라클]
    NVL(열명, '대체값')

    [MYSQL]
    IFNULL(열명, '대체값')

SELECT 결과 갯수 제한(페이징처리)

    [오라클]
    ROWNUM <= 숫자

    [MYSQL]
    LIMIT 숫자, OFFSET 숫자
    // OFFSET 숫자위치부터 LIMIT의 숫자만 큼 row 가져옴

가상테이블 DUAL

    [오라클]
    SELECT 1 FROM DUAL;

    [MYSQL]
    SELECT 1;
 

현재날짜

    [오라클]
    SELECT SYSDATE FROM DUAL;

    [MYSQL]
    SELECT NOW();


조건식 (IF)

    [오라클]
    //칼럼이 값과 일치하면 TRUE, 일치하지 않으면 FALSE
    SELECT DECODE(칼럼, 값, TRUE일때 출력할 값, FALSE일때 출력할 값) FROM TABLE;

    [MYSQL]

    SELECT IFNULL(조건식, TRUE일때 값, FALSE일때 값) FROM TABLE;

날짜 형식

    [오라클]
    SELECT TO_CHAR(SYSDATE, 'YYYY-MM-DD') FROM DUAL;
    
    [MYSQL]

    SELECT DATE_FORMAT(NOW(), '%Y-%m-%d');
 
시퀀스

    [오라클]

    CREATE SEQUENCE [시퀀스명]
    INCREMENT BY [증감숫자]
    START WITH [시작숫자]
    NOMINVALUE / MINVALUE [최소값]
    NOMINVALUE / MINVALUE [최소값]
    CYCLE / NOCYCLE
    CACHE / NOCACHE
    INSERT TABLE
    (SEQ_NBR)
    VALUES
    (시퀀스명.NEXTVAL)
    ;

    [MYSQL]
    CREATE TABLE
    ( SEQ_NBR INT NOT NULL AUTO_INCREMENT PRIMARY KEY);
    * INSERT 시 자동으로 값이 생성되어 들어감.

 

문자열 합치기

    [오라클]
    SELECT "A" || "B" FROM DUAL;
    SELECT CONCAT("A", "B") FROM DUAL;

    [MYSQL]
    SELECT CONCAT("A", "B") FROM DUAL;

문자열 자르기

    [오라클]
    SELECT SUBSTR( 문자열/칼럼, 시작위치, 잘라낼 문자열의 길이) FROM DUAL;

    [MYSQL]
    SELECT SUBSTRING(문자열/칼럼, 시작위치, 잘라낼 문자열의 길이);

---

# Oracle의 계층형 쿼리

오라클은 계층형 쿼리를 종종 사용하게 된다.

`계층형 쿼리`란 테이블에 계층형 구조 즉, 수직적 구조가 존재할 때 이를 조회하기 위한 쿼리

    예시 - 회사에는 조직도가 있다
        사장 밑에 뭐 부장, 차장, 과장, ...
        잘모름..

    Oracle DB에서 사장을 시작으로 부하직원들을 탐색할 때 사용하는 쿼리를 계층형 쿼리라 한다.

    계층형 쿼리로 전개한 뒤에 where절이 수행된다.

---

`START WITH` 어떤 레코드를 최상위 레코드로 정할지 결정한다.

`CONNECT BY` 연결고리를 만든다. 서브쿼리 사용못함

    CONNECT BY PRIOR 부서번호 = 상위부서번호

`LEVEL` 계층 구조 쿼리에서 수행 결과의 Depth를 표현하는 의사컬럼
    
    현재 행이 몇번째인지
    그러니까 몇등인지 알려주는 `모조 컬럼`

`ORDER SIBLINGS BY` 계층끼리 정렬 진행

    계층간의 구조는 유지
>
    start with를 지정했는데 루트노드가 2개 이상이라면

    루트노드1
    하위노드1
    하위노드2
    루트노드2
    하위노드3
    ...

    이런식으로 조회됨

---

LPAD("값", "총 문자길이", "채움문자")<br>
왼쪽에 채움문자를 문자길이에서 값의 길이를 뺸만큼 채움

RPAD도 있다.

---

    오라클 NULL은 가장 큰값으로 인식되므로 ASC로 정렬할경우 맨 마지막에 나오게 된다.