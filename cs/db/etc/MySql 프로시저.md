# MySql 프로시저

## 프로시저란?

데이터베이스에서 실행할 수 있는 일련의 SQL 명령문들을 하나의 이름으로 묶어놓은 것이다.  
데이터베이스에 저장되어 있으며, 필요할 때마다 호출하여 사용할 수 있다.  
데이터베이스 내에서 실행되므로 네트워크 트래픽을 줄일 수 있고, 실행 속도가 빠르다는 장점이 있다.

---

## 프로시저의 이점

1. 네트워크 트래픽 감소
2. 실행 속도 향상
3. 재사용성
4. 보안성
5. 코드의 모듈화
6. 트랜잭션 처리

---

## 프로시저 예시

```sql
DELIMITER //
CREATE PROCEDURE 'sp_select_all'()
BEGIN
    SELECT * FROM user;
END //
DELIMITER ;
```

DELIMITER - 구분자를 변경하는 명령어  
CREATE PROCEDURE - 프로시저 생성 명령어  
sp_select_all - 프로시저 이름  
BEGIN - 프로시저 시작  
SELECT * FROM user; - 프로시저 내용  
END - 프로시저 종료

## 프로시저 반복문 예시

```sql
DELIMITER //
CREATE PROCEDURE `create_articles_using_period`(input integer)
BEGIN
	DECLARE v1 INT;

	SET v1 = 1;
	WHILE v1 <= input DO
		CALL create_random_article(v1);
		SET v1 = v1 + 1;
END WHILE;
END
DELIMITER ;
```

{변수이름} {변수타입} - 변수 선언  
DECLARE - 변수 선언  
SET - 변수에 값 할당  
WHILE {조건문} DO - 반복문 시작  
END WHILE - 반복문 종료