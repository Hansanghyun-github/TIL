### Variable Expected

변수를 입력해야 하는데, 그냥 숫자나 메서드가 입력되었을 때

```cpp
5++; // x
member.getTeam() = temp; // x
```

두번째 예시는 수정 메서드를 만들어서 처리한다.

```cpp
member.setTeam(temp);
```

---

## response의 body 관련 헤더가 로깅이 되지 않는다.

### 개요

스프링 프로젝트에서 http 메시지에 대해 로그를 남기는 필터를 만들었다.

여기서 response의 body 관련 헤더가 로깅이 되지 않는다.

### 원인

로깅을 하기 위해 ContentCachingResponseWrapper 클래스를 사용함으로서,  
response의 body를 write 하는 시기가 변해서 이런 문제가 발생했다.

response의 body 관련 헤더(`Content-Length`, `Content-Type`)가  
response에 입력되는 시점은 responseBody를 write 하는 시점이다.

이때 나는 ContentCachingResponseWrapper를 사용해서 responseBody를 write 하는 시점을  
response의 헤더를 로깅하는 시점보다 늦춰버렸다.

> ContentCachingResponseWrapper는 copyBodyToResponse 메서드를 통해  
> responseBody를 사용자에게 write 한다.
>
> 이때 바디 관련 헤더가 response에 입력된다.

### 해결

헤더를 로깅하는 시점보다 먼저 copyBodyToResponse 메서드를 호출하는 것으로 해결했다.

---

