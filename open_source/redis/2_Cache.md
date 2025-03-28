> 레디스를 공부하기 전 먼저 캐시에 대해 알아보자.

# 캐시란?

자주 사용되는 데이터나 명령어를 임시로 저장해 두어, 필요할 때 빠르게 접근할 수 있도록 하는 고속 메모리 저장소이다.

> 기존 데이터를 저장하기 위한 저장소와는 별개로,  
> 더 빠르게 조회할 수 있게 하기 위한 저장소이다.

---

# 캐시 전략

(캐시를 도입하기 전에)  
WAS에서 데이터를 조회하려면 DB에 접근해야 한다.

이때 캐시를 도입함으로써 조회 속도를 높일 수 있다.  
하지만 하나의 데이터를 두 군데에 저장하게 되므로 데이터 일관성을 유지하는 것이 중요하다.  
이를 위한 캐시 전략이 필요하다.

## 읽기 전략

캐시에 데이터가 없을 경우에 대한 전략이다.  
(Cache Miss)

### Look Aside

> 뜻: 옆을 보다  
> 캐시에 데이터가 없을 때 옆(DB)을 보고 데이터를 조회한다.

1. 캐시로 데이터를 조회한다.
2. 캐시에 데이터가 없을 경우 DB로 데이터를 조회한다.
3. DB에서 조회한 데이터를 캐시에 저장한다.

장점: 캐시에 문제가 생겨도 DB에서 데이터를 조회할 수 있다.  
단점: 캐시, DB의 데이터 일관성이 깨질 수 있다.

### Read Through

> 뜻: 통과하다  
> 항상 캐시를 통해 데이터를 조회한다.

1. 캐시로 데이터를 조회한다.
2. 캐시에 데이터가 없을 경우 DB로 데이터를 조회한다.  
   (캐시가 직접 DB에 접근한다)

장점: 캐시, DB 간의 데이터 일관성이 유지된다.  
단점: 캐시가 죽으면 WAS에서 데이터를 조회할 수 없다.

---

여기서는 Read Through라는 개념을 소개했지만,  
내가 사용하는 spring + redis에서는  
Look Aside 방식을 사용하고 있다.

> 기본적으로 redis에서 다른 DB를 조회하는 기능이 없다.

---

## 쓰기 전략

새로운 데이터를 캐시, DB에 저장할 때의 전략이다.

### Wrtie Around

> 뜻: 쓰는 것을 우회하다  

1. 데이터를 DB에 저장한다.
2. (나중에) Cache Miss가 발생하면 캐시에 데이터를 저장한다.

장점: 성능이 좋다.  
단점: 데이터 일관성 유지가 어렵다.  
(캐시, DB 간의 연결점이 없기 때문)

### Write Back

> 뜻: 나중에 쓰다

1. 데이터를 캐시에 저장한다.
2. (나중에) 일정 시간이 지나거나 캐시가 꽉 차면 DB에 데이터를 저장한다.

장점: 쓰기 횟수를 줄일 수 있다.  
단점: 캐시의 데이터 유실이 발생할 수 있다.

> 쓰기 작업을 하지 않은 상태에서  
> 캐시가 죽으면 데이터가 유실될 수 있다.

### Write Through

> 뜻: 통과하다

1. 데이터를 캐시에 저장한다.
2. 데이터를 DB에 저장한다.  
   (캐시가 직접 DB에 데이터를 저장한다)

장점: 데이터 일관성이 유지된다.  
단점: 두번의 쓰기 작업이 필요하다.

---

# 어떤 데이터를 캐시하는 것이 좋을까?

1. 자주 사용되는 데이터
2. 자주 변경되지 않는 데이터
3. 유실되어도 큰 문제가 없는 데이터

---

# 캐시 주의할 점

항상 DB와의 데이터 일관성을 신경써야 한다.