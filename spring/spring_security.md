# Spring Security

**목차**
1. 스프링 시큐리티 전체적인 과정
2. 기본적인 인증 과정(form 로그인 & basic 로그인 & AuthenticationManger.authenticate 메소드)
3. Authentication Architecture (유저 인증될때 사용되는 클래스의 구조)
4. SessionManagementFilter
5. ExceptionTranslationFilter가 인증 & 인가 관련 Exception을 처리하는 과정 ( +AnonymousAuthenticationFilter )
6. FilterSecurityInterceptor ( 권한 인증을 처리하는 필터 )
7. (Appendix) 기존 세션방식에서 jwt로 바꾸는 과정 
8. (Appendix) 로그인된 유저정보를 가져오기 ( @AuthenticationPrincipal )

---

## 1. 스프링 시큐리티 전체적인 과정

스프링 시큐리티는 필터를 이용해서 인증, 인가를 처리한다.

---

## 2. 전체적인 인증 과정

![simple login process.png](..%2Fimage%2Fsimple%20login%20process.png)

// TODO 정확한 이미지로 교체

1. AuthenticationFilter가 request를 받음
2. 받은 request에 있는 username/password를 이용해 UsernamePasswordAuthenticationToken 생성
3. Token을 AuthenticationManager에게 보내면서 인증 진행 (대표적인 구현 객체는 ProviderManager)
4. ProviderManager는 현재 Token을 인증을 할 수 있는 AuthenticationProvider를 search & 해당 Provider에게 Token 보냄
5. 해당 Provider는 UserDetailsService에게 Token에 있는 username으로 DB 조회 요청
6. UserDetailsService는 username를 통해 DB로부터 사용자 정보를 조회한다. & 해당 사용자 정보로 UserDetails 생성
7. AuthenticationProvider는 UserDetailsService로부터 받은 UserDetails를 통해 사용자 인증 진행
8. 인증 성공하면 해당 사용자 정보 객체(Authentication 객체)를 AuthenticationManager로 반환
9. Authentication 객체 AuthenticationFilter로 반환
10. 받은 Authentication 객체를 SecurityContext에 저장

> SecurityContext에 있는 Authentication을 이용해서 권한 인증(인가)를 진행한다.

> AuthenticationFilter는 interface가 아니라 인증을 진행하는 필터를 의미한다.
> UsernamePasswordAuthenticationFilter, BasicAuthenticationFilter가 이에 해당한다.

AuthenticationFIlter를 통해 인증하는 방법은 여러가지가 있다.
1. Basic 인증 - BasicAuthenticationFilter
2. Form 인증 - UsernamePasswordAuthenticationFilter
3. 다이제스트 인증
> 다이제스트는 다른 두가지 방식에 비해 거의 사용되지 않되므로 다루지 않겠음

---

### 2-1 Form 인증
> SecurityConfig에서 formLogin()을 통해 설정한다.

// TODO

---

### 2-2 Basic 인증
> SecurityConfig에서 httpBasic()을 통해 설정한다.

클라이언트는 Authorization 헤더에 Base64로 인코딩된 username/password 값을 입력하고 request를 보낸다

> 예시1 - POSTMAN
>
> ![img.png](../image/basic_login1.png)
> ![img.png](../image/basic_login2.png)

> 예시2 - 크롬
> 
> ![basic_login_chrome.png](..%2Fimage%2Fbasic_login_chrome.png)

> request
> 
> ![basic_login_request.png](..%2Fimage%2Fbasic_login_request.png)

클라이언트의 request에서 Authorization 헤더를 찾아서, 해당 값을 디코딩 진행 

-> request의 헤더로부터 username/password를 추출한다.

-> username/password를 이용해 UsernamePasswordAuthenticationToken 생성

-> UsernamePasswordTokenAuthenticationManager의 authenticate 메서드를 호출한다. (Token도 같이 보낸다)

> 만약 헤더가 없다면 response에 WWW-Authenticate 헤더를 담아서 클라이언트에게 보낸다 
> 
> ![basic_login_response.png](..%2Fimage%2Fbasic_login_response.png)

### 2-3 AntityManger의 authenticate 메서드

AuthenticationManager는 interface이다.

스프링 시큐리티에서 다른 설정을 하지 않았다면 기본적으로 ProviderManager가 구현 객체로 주입된다.

그리고 ProviderManager는 인증을 위해 AuthenticationProvider의 authenticate 메서드를 호출한다.

AuthenticationProvider는 역시 interface이다.

스프링 시큐리티에서 다른 설정을 하지 않았다면 기본적으로 DaoAuthenticationProvider가 구현 객체로 주입된다.

그리고 DaoAuthenticationProvider는 인증하는 중간에 UserDetailsService의 loadUserByUsername 메서드를 호출한다.

해당 메서드를 통해 입력받은 username에 해당하는 사용자가 DB에 있는지 조회한다.

없다면 Exception 호출

username에 해당하는 사용자가 DB에 있다면, 해당 사용자 정보와 password를 비교해서 인증을 진행한다.

인증에 성공하면 마지막으로 AuthenticationFilter에서 SecurityContext에 Authentication을 set한다.

전체적인 과정
![login process class diagram.png](..%2Fimage%2Flogin%20process%20class%20diagram.png)

위의 사진과 비교하면, 여기서 AuthenticationFilter는 UsernamePasswordAuthenticationFilter가 된다. 

---

## 3. Authentication Architecture (유저 인증될때 사용되는 클래스의 구조)

---

## 4. SessionManagementFilter

---

## 5. ExceptionTranslationFilter가 인증 & 인가 거부를 처리하는 과정 ( +AnonymousAuthenticationFilter )

---

## 6. FilterSecurityInterceptor

---

## 7. (Appendix) 기존 세션방식에서 jwt로 바꾸는 과정

---

## 8. (Appendix) 로그인된 유저정보를 가져오기 ( @AuthenticationPrincipal )


---

로그인을 할때 parent로 왜 다시 try하는 거지?