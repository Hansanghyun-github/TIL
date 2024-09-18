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

