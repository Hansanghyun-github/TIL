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

## s