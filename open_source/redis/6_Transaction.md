## 레디스의 트랜잭션

레디스는 `multi`, `exec`, `discard` 명령어를 통해 트랜잭션을 지원한다.

---

### multi

`multi` 명령어는 트랜잭션을 시작하는 명령어이다.

```bash
> multi
OK
```

### exec

`exec` 명령어는 트랜잭션을 실행하는 명령어이다.

```bash
> exec
1) (integer) 1
```

위 예시는 `multi` 명령어로 트랜잭션을 시작하고,  
명령어 1개를 실행한 후 `exec` 명령어로 트랜잭션을 실행한 결과이다.  
(해당 명령어는 성공적으로 실행되었다)

### discard

`discard` 명령어는 트랜잭션을 취소하는 명령어이다.

```bash
> discard
OK
```

---

### 일반적인 DB의 트랜잭션과 레디스의 트랜잭션의 차이

일반적인 DB의 트랜잭션과 다른 점은  
레디스의 트랜잭션은 `원자성`을 보장하지 않는다는 것이다.  
(DB는 트랜잭션 내의 한 명령어가 실패하면 전체가 실패하지만, 레디스는 실패한 명령어만 실패한다)

> MySQL에서 sql1, sql2, sql3이 트랜잭션으로 묶여있을 때,  
> sql2에서 오류가 발생하면 sql1, sql2, sql3 모두 취소된다.
> 
> 하지만 레디스에서  
> `multi`와 `exec` 사이에 있는 명령어 중 하나가 실패해도,  
> 실패한 명령어만 실패하고 나머지 명령어는 성공한다.

> 레디스 공식문서  
> Redis does not support rollbacks of transactions since supporting rollbacks would have a significant impact on the simplicity and performance of Redis.  
> (Redis는 트랜잭션 롤백을 지원하지 않습니다. 롤백을 지원하면 Redis의 단순성과 성능에 상당한 영향을 미치게 됩니다)

---