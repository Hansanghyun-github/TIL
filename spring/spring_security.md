# Spring Security

스프링 시큐리티가 username/password를 인증하는 방식
1. Basic 인증
2. Form 인증
3. 다이제스트 인증
> 다이제스트는 다른 두가지 방식에 비해 거의 안쓰이므로 다루지 않겠음

## Basic 인증
> SecurityConfig에서 httpBasic()을 통해 설정한다.

1. 클라이언트는 Authorization 헤더에 Base64로 인코딩된 username/password 값을 입력하고 request를 보낸다

> 예시 - POSTMAN
![img.png](../image/basic_login1.png)
![img.png](../image/basic_login2.png)

2. request를 받은 서버는 BasicAuthenticationFilter에서 Authorization 헤더에 있는 값을 받아서 디코딩한 후 해당 유저가 있는지 확인한다
- 2-1. 해당 유저가 있다면 SecurityContext에 해당 유저의 Authentication 정보를 입력하고, 새로운 SESSIONID 쿠키 값을 response로 전달한다.
- 2-2. 해당 유저가 없다면 WWW-Authenticate 헤더를 포함하여 response를 보낸다.

---

## Form 인증
> SecurityConfig에서 formLogin()을 통해 설정한다.

// TODO

---

## 스프링 시큐리티의 Authentication 객체

// TODO