스핀로그 프로젝트의 API 서버에서 처리하는 메인 API의 성능 개선 과정을 다룹니다.

---

## API 서버 구성

API 서버는 1대의 AWS EC2 서버와 1대의 DB 서버로 구성되어 있다.

```mermaid
graph LR
    Client --> nginx
    nginx --> WAS
    WAS --> DB
    
    subgraph AWS EC2
        WAS
        nginx
    end
    
    subgraph RDS 
        DB
    end
```

> WAS - Spring Boot  
> DB - MySQL

### 하드웨어 스펙

- AWS EC2
    - vCPU: 1
    - Memory: 1GB
- AWS RDS
    - vCPU: 2
    - Memory: 1GB

---

## 메인 API란?

스핀로그 사이트에서 로그인을 한 유저는 메인 페이지에 들어가면,  
한 달 동안 작성한 일기들과 오늘 작성한 일기들을 볼 수 있다.

<img src="../img/PerfTest_211.png" width="300">  

(위 데이터들을 가져오는 API)

메인 API는 사용자가 로그인 한 뒤에 항상 호출되는 API이다.  

> 스핀로그에서 가장 많이, 자주 호출되는 API 이다.

따라서 이 API의 성능이 중요하다.

---

## 기존 메인 API 부하 테스트 결과

> nGrinder를 이용해 100명의 vuser가 20분 동안 메인 API를 호출했다.

TPS는 30으로 나왔다.

(VisualVM으로 확인한 결과)  
WAS 서버의 CPU 사용량 - 97%, 그 중 GC가 차지하는 비율 - 20%~35%  
<img src="../img/PerfTest_212.png" width="600">

(AWS CloudWatch를 통해 확인한 결과)  
DB 서버의 CPU 사용량 - 약 20%  
<img src="../img/PerfTest_213.png" width="500">

---

## 원인 분석

병목은 WAS 서버에서 발생하고 있었다.

### 1. WAS 서버의 병목 원인

htop 명령어 & 스레드 덤프를 이용해 스레드별 CPU 사용량 분석 결과  
`VM Thread`와 `C2 CompilerThread0` 스레드의 CPU 사용량이 높게 나타났다.  
(GC 스레드와 JIT 컴파일러 스레드 -> API 호출의 빈도 수과 관계없이 항상 사용되는 스레드들)

그 외 스레드들은 모두 0%~2% 점유율을 보였다.  
그리고 0%~2% 점유율을 보이는 스레드들이 약 100개 정도 존재했다.

> 특정 스레드가 병목을 발생시키는 것이 아니라,  
> 단순히 부하가 많아 CPU 사용량이 높게 나온 것으로 보인다.

### 2. GC 점유율 높은 이유

WAS 서버의 CPU 사용량이 높은 이유 중 하나는 많은 GC 때문인 것도 있다.  
메모리 누수가 있는지 확인하기 위해 그라파나에서 GC Count 그래프를 확인했다.  
(테스트 중 GC가 몇 번 수행되었는지 확인)

![img.png](../img/gc_count.png)

만약 메모리 누수가 발생했다면 GC 횟수가 증가해야 하는데,  
GC 횟수는 일정 횟수를 유지했다.

> 즉, 메모리 누수는 발생하지 않았다고 판단된다.

그리고 Majar GC보다 Minor GC가 더 많이 발생했다.  
(Old 영역이 아닌 Young 영역에서 GC가 더 많이 발생했다)

> 따라서 특정 API 요청이 병목을 발생시키는 것이 아니라,  
> 한번의 API 요청을 처리할 때 많은 GC가 발생하는 것으로 보인다.

그 다음, 잦은 GC의 원인을 알아보기 위해  
Main API를 호출하기 전/후의 Heap Dump를 뽑아봤다.

> GC 대상 객체가 얼마나 증가 했는지를 확인하기 위해  
> 힙 덤프에서 GC Roots를 확인했다.

(API 호출 전 Heap Dump)  
![img_1.png](../img/hd_before.png)

(API 호출 후 Heap Dump)  
![img.png](../img/iap_1.png)

> 위 사진은 100명의 vuser가 1번씩 메인 API를 호출한 후의 Heap Dump이다.

여기서 핵심은 Unreachable Object의 증가량이다.

Main API 호출 전 5.74MB에서,  
Main API 호출 후 1.32GB로 증가했다.

그리고 약 860만개의 Unreachable Object가 생성되었다.

이 객체들 중 DB 조회와 관련된 객체들이 많이 생성되었다.
1. `com.mysql.cj.result.StringValueFactory` - 130만개
2. `org.hibernate.persister.entity.AbstractEntityPersister` - 16만개

> 이를 통해, 메인 API 호출 시 많은 DB 조회가 발생하고  
> 많은 양의 Unreachable Object가 생성되었음을 알 수 있다.

---

## 성능 개선

### 1. 불필요한 커넥션 소모 방지

사용자가 요청 했을 때,  
요청에 대한 비즈니스 로직을 수행하기 전,  
`SessionAuthFilter`에서 세션 검증 과정을 거친다.

세션 검증 과정을 수행할 때 DB에 조회를 하는데,  
이로 인해 (비즈니스 로직과 별개의) 트랜잭션이 발생한다.  

> 비즈니스 로직 외의 추가적인 DB 커넥션이 소모된다.

```mermaid
sequenceDiagram
    title API 요청 수행 과정(세션 인증 성공 시 케이스)
    actor Client
    participant SessionAuthFilter
    participant BusinessLogic
    participant Database
        
    Client->>SessionAuthFilter: API 요청
    SessionAuthFilter->>Database: 세션 검증 (connection 1)
    Database-->>SessionAuthFilter: 세션에 해당하는 데이터 반환
    SessionAuthFilter->>BusinessLogic: 요청 전달
    BusinessLogic->>Database: 데이터 조회 (connection 2)
    Database-->>BusinessLogic: 데이터 반환
    BusinessLogic-->>Client: 응답
```

따라서 세션 인증 단계에서는 DB 조회는 하지 않고,  
세션의 존재 여부만 확인하도록 변경했다.  
(connection 1을 제거)

그리고 비즈니스 로직에서  
DB를 통해 세션 검증을 수행하는 로직을 추가했다.  
(connection 2에서 세션 검증)

이로 인해 불필요한 커넥션 소모가 방지된다.

> 모든 비즈니스 로직에서 세션에 대해 검증을 수행하기 때문에  
> 세션 인증 필터에서 세션 검증은 하지 않아도 된다고 판단했다.

### 2. DB에서 데이터를 가져올 때, 필터링하는 작업 추가

메인 API는 DB로부터 한달치 articles와 오늘 articles를 가져와야 한다.

현재 스프링 코드를 확인해보니,  
DB로부터 해당 유저의 모든 articles를 가져온 뒤,  
WAS에서 날짜에 대한 필터링 작업을 수행하는 코드를 발견했다.

```mermaid
sequenceDiagram
    title API 요청에 대한 데이터 조회 과정
    actor Client
    participant WAS
    participant Database

    Client->>WAS: API 요청
    WAS->>Database: 유저의 모든 articles 조회
    Database-->>WAS: 모든 articles 데이터 반환
    WAS->>WAS: 날짜에 따른 필터링 작업 수행(!)
    WAS-->>Client: 응답
```

WAS에서 필터링 작업을 수행하면서,  
실제로 응답하는 데이터보다 많은 양의 Garbage Object가 생성되고 있다.

> 이 때문에 GC가 많이 발생하고, WAS 서버의 CPU 사용량이 높게 나타나는 것으로 보인다.

따라서 DB에서 필터링 작업을 수행하도록 변경했다.

> DB에서 필터링 작업을 하는 것이  
> WAS에서 필터링 작업을 하는 것보다 효율적이다.
> 
> 1. DB에서 인덱스를 이용해 최적화가 가능하다.
> 2. DB의 CPU 스펙이 WAS보다 좋다.  
>    (DB vCPU: 2, WAS vCPU: 1)

### 3. DB 인덱스 활용

현재 한달치 articles을 조회하는 쿼리를 인덱스를 이용하기 위해  
쿼리를 변경했다.

변경 전 쿼리
```sql
select *
from articles a1_0
where
    a1_0.user_id = ? and 
    date_format(a1_0.spend_date, '%Y-%m') = ?; -- '2024-07' 형태로 넘어온다.
```

변경 후 쿼리
```sql
select *
from articles a1_0
where 
    a1_0.user_id = ? and 
    a1_0.spend_date between ? and ?; -- '2024-07-01 00:00:00' 형태로 넘어온다.
```

> 인덱스를 사용하기 위해 칼럼을 변형 시키는 부분을 제거했다.

그리고 인덱스는 (user_id, spend_date)로 생성했다.  
((spend_date, user_id) 인덱스는 (user_id, spend_date) 인덱스보다 비효율적이기 때문에)

<details>
<summary>(spend_date, user_id) 인덱스가 (user_id, spend_date) 인덱스보다 비효율적인 이유</summary>

현재 메인 API에서 한달치 articles를 조회하기 위해 사용하는 SQL  
```sql
select *
from articles a1_0
where 
    a1_0.user_id = ? and 
    a1_0.spend_date between ? and ?;
```

user_id 필드는 동등 비교 조건으로 사용되었고,  
spend_date 필드는 범위 조건으로 사용되었다.

#### (spend_date, user_id) 인덱스

만약 인덱스가 (spent_date, user_id)로 생성되었다면,  
해당 인덱스에서 첫 번째 칼럼(spend_date)이 범위 검색을 수행할 때,  
뒤 칼럼(user_id)은 인덱스를 타지 못한다.

> 뒤 칼럼들은, 해당 조건을 이용해 인덱스의 범위를 결정할 수 없다.  
> (인덱스를 통해 읽은 레코드들이 맞는지 확인만 한다)

> 첫번째 칼럼만 작업 범위 결정 조건이 되고,  
> 그 이후의 칼럼들은 체크 조건이 된다.

#### (user_id, spend_date) 인덱스

하지만 (user_id, spend_date) 인덱스에서  
user_id을 동등 비교 조건으로 사용하기 때문에  
user_id, spend_date 모두 범위 검색을 수행한다.

> 이때는 두 칼럼 모두 작업 범위 결정 조건이 된다.

#### 두 인덱스 성능 비교 그래프

<img src="../img/sql_compare_index.png" width="400">

위 사진은 동일한 쿼리에 대해 두 인덱스를 사용했을 때의 평균 실행 시간을 비교한 것이다.  
(100명의 유저에 대해 1달치 데이터를 조회하는 쿼리)

(user_id, spend_date) 인덱스를 이용한 쿼리가 더 빠르게 실행된다.

> 동등 비교 조건으로 사용되는 칼럼이 먼저 오도록 인덱스를 생성하는 것이 효율적이다.

</details>

---

## 성능 개선 결과

> WAS 서버의 안정성을 위해,  
> cgroup을 이용해 자바 프로그램의 CPU 사용량을 60%로 제한했다.

TPS: 30 -> 205 로 증가했다.

(VisualVM으로 확인한 결과)  
![img.png](../img/PerfTest_231.png)

WAS 서버의 CPU 사용량은 60%로 제한했음에도 불구하고  
TPS가 증가했다.

그리고 GC가 차지하는 비율도 5%로 대폭 감소했다.

---

## 추가 개선

### 4. 비즈니스 로직 개선

메인 API는 DB에 2개의 쿼리를 수행한다.  
1. 한 달치 articles 조회
2. 오늘 articles 조회

여기서 2번 쿼리는 1번 쿼리의 결과에 속한다.  
따라서 2번 데이터를 위한 DB 조회를 수행하지 않고,  
1번 쿼리의 결과에서 오늘 articles를 추출하도록 변경했다.

```mermaid
sequenceDiagram
    title 기존 로직
    actor Client
    participant WAS
    participant Database

    Client->>WAS: API 요청
    WAS->>Database: 한 달치 articles 조회
    Database-->>WAS: 한 달치 articles 반환
    WAS->>Database: 오늘 articles 조회
    Database-->>WAS: 오늘 articles 반환
    WAS-->>Client: 응답
```

```mermaid
sequenceDiagram
    title 변경된 로직
    actor Client
    participant WAS
    participant Database

    Client->>WAS: API 요청
    WAS->>Database: 한 달치 articles 조회
    Database-->>WAS: 한 달치 articles 반환
    WAS->>WAS: 오늘 articles 추출
    WAS-->>Client: 응답
```

> 이로 인해 DB에 대한 요청이 1번으로 줄어든다.

---

## 추가 개선 결과

TPS: 205 -> 230 로 증가했다.

WAS 서버와 DB 서버의 CPU 사용량은 이전과 비슷한 수준을 유지했다.

### 최적화 이후 힙 덤프 결과

(최적화 전 API 호출 후 Heap Dump)  
![img.png](../img/iap_1.png)

(최적화 후 API 호출 후 Heap Dump)  
![img.png](../img/iap_2.png)

최적화 후 Unreachable Object의 증가량이  
1.32GB -> 379MB로 감소했다.

---

## 결론

1. 불필요한 커넥션 소모 방지
2. DB에서 데이터를 가져올 때, 필터링하는 작업 추가
3. DB 인덱스 활용
4. 비즈니스 로직 개선

위의 개선을 통해  
WAS 서버의 CPU 사용량을 97%에서 60%로 낮추면서  
TPS를 30에서 230으로 증가시켰다.

---

### 남은 문제

지금도 여전히 WAS 서버에서 병목이 발생한다.  
(WAS 서버의 CPU 사용량: 60%)  
(DB 서버의 CPU 사용량: 22%)

이것은 단순히 부하가 많아서 발생하는 것으로 보인다.  
(특정 스레드가 병목을 발생시키는 것이 아니라, 여러 스레드가 CPU 사용량을 나눠 가지고 있기 때문)

> 이를 해결하려면 스케일 업이나 스케일 아웃이 필요한 것으로 보인다.

---