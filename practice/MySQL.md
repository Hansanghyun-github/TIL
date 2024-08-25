### MySQL 서버의 현재 구성된 시스템 변수를 보는 방법

```SHOW [ GLOBAL  | SESSION ] VARIABLES```

이 값들을 이용해 서버의 동작 및 구성을 확인할 수 있다.

### MySQL 서버의 현재 상태 정보를 보는 방법

```SHOW [ GLOBAL  | SESSION ] STATUS```

이 값들을 이용해 모니터링 할 수 있다.

> 특정 변수만 보고 싶다면 뒤에 `LIKE 'A%'` 를 붙여주면 된다.

> [ GLOBAL | SESSION ] 을 붙이지 않으면,  
> 자동으로 SESSION으로 인식한다.

---

### show engine innodb status

InnoDB 스토리지 엔진의 현재 상태를 보여주는 정보를 반환하는 명령어

이를 이용해 현재 몇개의 레코드가 lock이 걸렸는지,  
트랜잭션 별로 undo log에 레코드가 몇개 있는지,  
등등 현재 상태에 대한 다양한 정보를 알 수 있다.

`이미지 예시`

<img src="../img/mysql_practice_!.png" width="700">

현재 9894번 id인 트랜잭션이 4개의 레코드 락을 걸고 있고,  
3개의 undo log를 갖고 있다.

---

### Performance_schema DB의 data_locks 테이블

현재 잠금이 걸린 레코드에 대한 정보를 보여주는 테이블

몇가지 중요한 칼럼
- engine_transaction_id: 현재 락을 걸고 있는 트랜잭션의 id
- object_name: 락을 걸고 있는 레코드가 있는 테이블의 이름
- index_name: 락이 걸린 인덱스의 이름
- lock_mode: 어떤 락이 걸렸는지 보여준다.
  (S: 공유 락, X: 배타 락, GAP: 갭락)
- lock_data: 레코드의 정보(값)

---

특정 범위에 대해 락을 걸면  
MySQL InnoDB는 그 다음 레코드도 락을 건다.  
(갭 락)