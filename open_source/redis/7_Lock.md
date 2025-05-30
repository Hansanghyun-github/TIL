# 레디스 락

싱글 스레드로 작동하며 기본적으로 하나의 명령어가 순차적으로 실행되기 때문에  
일반적인 상황에서는 락이 필요 없다.

하지만 여러 클라이언트가 동시에 접근하는 경우,  
데이터의 일관성을 유지하기 위해 레디스 락을 사용할 수 있다.

## 싱글 인스턴스에서 레디스 락을 사용하는 방법

### 락 획득

`SET NX PX` 명령을 사용하여 레디스 락을 구현할 수 있다.

```
SET lock_key random_value NX PX 30000
```

- `NX`: 해당 key가 존재하지 않을 때만 실행
- `PX {milliseconds}`: {milliseconds} 동안만 해당 key가 존재

A 클라이언트가 위 명령을 실행하고  
B 클라이언트가 같은 명령을 실행하면  
이미 `lock_key`가 존재하기 때문에 실패한다.  
-> A가 락을 획득한 상태 유지

> 여기서 random_value는 랜덤한 값이다.  
> (락을 해제할 때, 해당 값과 일치하는지 확인하기 위해 사용)  
> (UUID나 timestamp 등을 사용한다)

### 락 해제

`EVAL` 명령을 사용하여 레디스 락을 해제한다.

```lua
if redis.call("GET", KEYS[1]) == ARGV[1] then
    return redis.call("DEL", KEYS[1])
else
    return 0
end
```

> 그냥 `DEL` 명령을 사용하면,  
> 다른 클라이언트가 락을 획득한 상태에서 락을 해제할 수 있다.  
> 
> -> 이를 방지하기 위해, 락을 해제할 때 랜덤한 값과 일치하는지 확인한다.

---

## 분산 환경에서 레디스 락을 사용하는 방법

### 분산 환경의 정의

여기서 설명하는 레디스의 분산 환경은  
각각이 독립적인 마스터 레디스 인스턴스로 구성된 경우를 가정한다.

### Redlock 알고리즘

여러 인스턴스에서 레디스 락을 사용할 때,  
Redlock 알고리즘을 사용하여 레디스 락을 구현할 수 있다.

Redlock 알고리즘은 위 문제를 해결하기 위해,  
여러 레디스 인스턴스에 락을 획득하고 해제하는 방법을 제공한다.

### Redlock 알고리즘의 구현

1. 현재 시간을 ms 단위로 가져온다.
2. 모든 인스턴스에서 순차적으로 잠금을 획득하려고 시도한다.
3. 클라이언트는 (현재 시간 - 1단계에서 얻은 타임스탬프)를 통해 잠금을 획득하기 위해 경과한 시간을 계산한다.  
   클라이언트가 과반이 넘는(N/2 + 1) 인스턴스에서 잠금을 획득했고,  
   총 경과 시간이 잠금 유효 시간보다 적다면 분산락을 획득한 것으로 간주한다.
4. 분산락을 획득한 경우, 잠금 유효 시간은 3단계에서 계산한 시간으로 간주한다.
5. 분산락을 획득하지 못한 경우(과반이 넘는 인스턴스를 잠글 수 없거나 유효 시간이 음수인 경우),  
   클라이언트는 모든 인스턴스에서 잠금을 해제하려고 시도한다.

### Redlock 알고리즘의 문제점

Clock Drift로 인한 문제  
RedLock 알고리즘은 노드들 간에 동기화된 시계(synchronized clock)는 없지만, 로컬 시간이 거의 동일한 속도로 갱신된다는 가정에 의존한다.  
하지만 현실에서는 클럭이 정확한 속도로 갱신되지 않는 Clock Drift 문제가 발생할 수 있다.

> 자바에서 사용하는 `Redisson` 라이브러리는  
> Redlock 알고리즘을 사용하며,  
> Clock Drift 문제를 해결하기 위해  
> 주기적 TTL 갱신, 클럭 동기화 등의 방법을 사용한다.  
> (NTP(Network Time Protocol)를 사용하여 클럭 동기화를 수행한다)

### 인스턴스 장애로 인한 문제

장애로 인해 동시에 락을 획득할 수 있는 경우가 있다.

(인스턴스 A,B,C가 있다고 가정)
1. 클라이언트 A가 인스턴스 A,B의 락을 획득해서  
   모든 레디스 인스턴스에 락을 획득한 상태
2. 인스턴스 B가 장애로 인해 레디스 인스턴스가 다운된다.
3. 인스턴스 B가 복구되고, 클라이언트 B가 락을 획득하려고 시도한다.  
   인스턴스 B, C에 락을 획득하고, A에는 락이 없는 상태  
   이때도 락을 획득한 것으로 간주할 수 있다.
4. 두 클라이언트가 모두 락을 획득한 상태로 동시에 작업을 수행할 수 있다.

> 이를 방지하기 위한 방법들은  
> 인스턴스가 다운된 경우 락을 해제하거나,  
> 락을 획득할 때 인스턴스의 상태를 확인하는 등의 방법이 있다.