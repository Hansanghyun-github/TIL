## 기본적인 Commands

`DEL {key}` - 키 삭제  
`EXISTS {key}` - 키 존재 여부 확인  
(`EXISTS` 명령어는 키가 존재하면 1, 존재하지 않으면 0을 반환한다.)

`TTL {key}` - 키의 TTL(Time To Live) 조회  
(`TTL` 명령어는 키의 TTL을 초 단위로 반환한다.)  

> `TTL` 명령어의 결과가 -1이면,  
> 키에 TTL이 설정되어 있지 않다는 의미이다.  
> (영원히 존재하는 키)

`TYPE {key}` - 키의 데이터 타입 조회

---

# Redis Data Types and Commands

레디스는 Data Structure Server로서,  
레디스는 다양한 데이터 구조를 지원하며 각 데이터 구조는 특정한 목적에 맞게 사용된다.

---

## 1. Strings

레디스의 문자열은 바이트의 배열로서,  
텍스트를 포함하거나 직렬화된 객체 그리고 이진 데이터를 저장하는데 사용된다.

### Strings Commands

```bash
> SET key value
OK
> GET key
"value"
> GET key2
(nil)
```

`SET` 명령어를 사용할 때 키가 이미 존재하는 경우,  
기존 값이 대체된다는 점을 주의해야 한다.

```bash
> SET key value
OK
> SET key value2
OK
> GET key
"value2"
```

value는 모든 종류의 데이터를 저장할 수 있으며,  
최대 512MB까지 저장할 수 있다.

> `SET`의 옵션  
> 
> - `NX` : 키가 존재하지 않을 때만 설정한다.
> - `XX` : 키가 존재할 때만 설정한다.
> 
> ```bash
> > SET key value NX
> OK
> > SET key value XX
> OK
> > SET key value NX
> (nil)
> ```

---

## 2. Lists

레디스의 리스트는 문자열 value들을 링크드 리스트로 저장한다.

### Lists Commands

`LPUSH` - 리스트의 맨 앞에 데이터 추가  
`RPUSH` - 리스트의 맨 뒤에 데이터 추가
`LPOP` - 리스트의 맨 앞 데이터 제거  
`RPOP` - 리스트의 맨 뒤 데이터 제거

`LRANGE` - 리스트의 범위 데이터 조회  
`LINDEX` - 리스트의 인덱스 데이터 조회

```bash
> LPUSH key value1
1 # 리스트의 길이를 반환한다.
> LPUSH key value2
2
> LRANGE key 0 -1
1) "value2"
2) "value1"
```

> `LPUSH` 명령어를 사용할 때,  
> 키가 존재하지 않는 경우 새로운 리스트를 생성하고 value를 추가한다.

---

## 3. Sets

레디스의 셋은 유니크한 문자열 value들을 저장한다.  
셋은 중복된 데이터를 허용하지 않으며 순서가 없다.

### Sets Commands

`SADD` - 셋에 데이터 추가  
`SREM` - 셋에서 데이터 제거  
`SMEMBERS` - 셋의 모든 데이터 조회

```bash
> SADD key value1
1 # 셋에 추가된 데이터의 수를 반환한다.
> SADD key value1
0 # 이미 존재하는 데이터는 추가되지 않는다.
> SADD key value2 value3
2
> SMEMBERS key
1) "value1"
2) "value2"
3) "value3"
```

`SISMEMBER` - 셋에 데이터 존재 여부 확인

```bash
> SISMEMBER key value1
1 # 존재하면 1, 존재하지 않으면 0을 반환한다.
```

---

## 4. Hashes

레디스의 해시는 키와 값의 맵을 저장한다.

> 이전의 Set은 해당 키의 존재 여부만을 확인할 수 있었지만,  
> Hash는 키의 존재 여부와 값을 확인할 수 있다.  
> (키에 대한 값을 같이 저장하기 때문)

### Hashes Commands

`HSET` - 해시에 필드와 값을 추가  
`HGET` - 해시의 필드 값 조회  
`HGETALL` - 해시의 모든 필드와 값을 조회

```bash
> HSET key field1 value1
1 # 새로운 필드를 추가하면 1을 반환한다.
> HSET key field1 value2
0 # 이미 존재하는 필드는 추가되지 않는다.
> HSET key field2 value3
1
> HGET key field1
"value2"
> HGETALL key
1) "field1"
2) "value2"
3) "field2"
4) "value3"
```

---