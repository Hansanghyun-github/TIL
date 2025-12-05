

---

ttl 에 해당하는 필드는
굳이 테라폼 정의에 넣을 필요 없다.

타입은 무조건 N(Number)이어야 한다.
-> UNIX epoch(초 단위를 넣어야 한다.)

---

point_in_time_recovery 는 DynamoDB Point-In-Time Recovery(PITR) 설정

최근 몇일간의 기록을 그대로 저장해서  
백업할 수 있는 기능  
(대신 그만큼 비용이 증가한다.)

---

