## nGrinder + Spring Security + OAuth2 인증 - 쿠키 관련 레이스 컨디션 문제

### 개요

nGrinder를 이용해서 100명의 vuser로 성능테스트를 해봤는데  
(프로세스 1개, 스레드 100개)

실제 API 테스트 전의 OAuth2 인증에서 문제가 발생했다.

100명의 vuser에서 절반정도만 인증에 성공하고, 나머지는 실패했다.

여기서 특이한 점은 100명의 유저 중에서,  
초반에 요청한 유저들만 인증에 실패하고  
나중에 요청한 유저들은 인증에 성공했다.

> 이 테스트를 실행할 때마다 성공/실패 한 유저의 수가 다르게 나왔다.  
> -> 멀티 스레드 환경에서 발생하는 문제일 것으로 예상했다.

---

### 원인 1 - 어떤 시점에 vuser의 요청이 서버에서 종료됐는지 확인

스카우터를 이용해 인증에 실패한 유저의 로그를 확인해보니,  
OAuth2 인증을 위한 액세스 토큰 요청, userInfo 요청을 하지 않고 바로 종료됐다.

성공한 인증 요청의 플로우  
(내부에서 액세스 토큰 요청, userInfo 요청을 모두 성공적으로 수행했다)  
![img.png](../img/cookie_race_condition_1.png)

실패한 인증 요청의 플로우  
(내부에서 아무 요청도 하지 못했다)  
![img_1.png](../img/cookie_race_condition_2.png)

---

그리고 인증에 실패한 요청을 에러 로그로  
authorization_request_not_found 라는 에러 메시지를 확인했다.  
![spring_security_oauth2_2.png](..%2Fimg%2Fspring_security_oauth2_2.png)

해당 로그 메시지가 어디서 발생했는지 알아보기 위해  
OAuth2LoginAuthenticationFilter 클래스의 attemptAuthentication 메서드를 디버깅 해봤다.

해당 메시지는 맨처음 요청을 검증하는 단계에서 발생한 것으로 확인했다.  
```java
class OAuth2LoginAuthenticationFilter {
    @Override
    public Authentication attemptAuthentication(HttpServletRequest request, HttpServletResponse response) throws AuthenticationException {
        // ... 
        OAuth2AuthorizationRequest authorizationRequest = this.authorizationRequestRepository.removeAuthorizationRequest(request, response);
        if (authorizationRequest == null) {
            OAuth2Error oauth2Error = new OAuth2Error("authorization_request_not_found");
            throw new OAuth2AuthenticationException(oauth2Error, oauth2Error.toString()); // 여기서 에러 발생
        }
        // ...
    }
}

```

위 두가지 사실로 보아,  
이 문제는 인증 서버, 리소스 서버와의 통신에서 문제가 발생한 것이 아니라  
맨 처음, 사용자가 Application에 권한 부여 승인 코드를 전달하는, 요청을 검증하는 단계에서 문제가 발생한 것으로 확인했다.

---

### 원인 2 - 인증에 실패한 이유

인증에 실패한 유저들의 http 메시지 로그를 확인해보니,  
사용자가 Application에 권한 부여 승인 코드를 전달하는 요청의  
Cookie 헤더에 JSESSIONID가 없었다.

이로 인해 세션이 없어서 인증에 실패했다.  

> OAuth2 인증 프로세스
> 
> 맨 처음 사용자는 Applicaiton에 로그인을 시도했을 때,  
> 인증 서버로 리다이렉트 되도록 302 응답을 받는다.  
> 이때 Location 헤더의 url에서 쿼리 파라미터로 state 값을 전달한다.  
> (이때 세션에 state 값을 저장한다)
> 
> 이 다음 사용자가 인증 서버로부터 로그인을 성공하면,  
> 권한 부여 승인 코드(code)와 state 값을 Application으로 전달한다.
> 
> 이때 Applicaiton은 state 값을 이용해 사용자를 검증한다.  
> (요청에 있는 state 파라미터를 세션의 state와 비교한다)

이때 내가 만든 Application은 OAuth2 인증을 위해 스프링 시큐리티를 사용했다.  

스프링 시큐리티는 사용자의 세션을 이용해서 state를 검증하는데,  
인증에 실패한 유저들은 (JSEESIONID 쿠키를 요청에 담지 않아서) 세션이 생성되지 않아서 인증에 실패한 것이다.

---

### 원인 3 - JSESSIONID 쿠키를 요청에 담지 못한 이유

사용자가 Application에게 권한 부여 승인 코드를 전달하는 요청을 보낼 때  
JSESSIONID 쿠키가 요청에 담기지 않았다.

그런데 이전에 사용자가 Application으로부터 인증 서버로 리다이렉트 되었을 때,  
JSESSIONID 쿠키가 응답에 (Set-Cookie 헤더로) 담겨 있었다.

결국 문제는 쿠키를 받고 나서,  
이를 nGrinder vuser가 Application에 요청할 때, 쿠키를 담지 못한 것이 문제였다.

---

### 원인 4 - nGrinder의 쿠키 관리

먼저 nGrinder에서 맨 처음 요청의 쿠키가 잘 담겨있는지 확인해보기 위해  
로그로 확인해봤다.

모든 스레드가 JSESSIONID 쿠키를 잘 받았지만,  
몇몇 쿠키의 도메인이 (Application 서버가 아닌) 다른 도메인으로 나왔다.

> 해당 도메인은 OAuth2 인증을 위한 모의 인증 서버의 도메인이었다.

여기서 테스트를 매번할때마다 쿠키의 도메인이 다르게 나온 것은 아니다.  
다른 테스트와 똑같이 인증에 실패한 vuser가 있었지만, 해당 vuser의 쿠키의 도메인은 올바르게 나온 케이스도 있었다.

이를 보고 이 문제는 nGrinder에서 쿠키를 관리할 때 레이스 컨디션이 발생한 것으로 판단했다.

---

### 원인 5 - 쿠키 관련 레이스 컨디션 (HTTPRequest 클래스의 CookieOrigin 필드)

이를 알아보기 위해 nGrinder의 쿠키 관리 코드를 확인했다.

nGrinder의 HTTPRequest 객체는 쿠키를 ThreadLocal로 관리한다.  
(각 스레드마다 쿠키를 관리한다)

따라서 쿠키 자체에는 문제가 없었다.

이떄 HTTPRequest 클래스는 내부적으로 CookieOrigin이라는 인스턴스 변수를 사용하는데,  
이 클래스는 쿠키의 기본 정보(호스트, 포트 번호, path, secure)를 저장해놓는 클래스이다.

문제는 내가 인증을 하기 위해 dev 서버와 mock 서버 (인증 서버) 둘 다 요청을 하는데,  
이때 스레드 별로 각각 요청을 하면서, cookieOrigin 필드가 계속 다른 도메인으로 바뀌었다.  
(레이스 컨디션 발생)

이로 인해 dev에서 발급한 쿠키의 도메인이 mock 서버의 도메인으로 저장될 때도 있고,  
쿠키의 도메인이 dev 서버로 제대로 저장이 되도, 검증하는 코드에서는 mock 서버의 도메인으로 검증을 하게 되었다.

---

### 레이스 컨디션으로 인해 쿠키가 요청에 담기지 않는 두가지 예시

#### 첫번째 케이스

HTTPReqeust GET 메서드  
-> createRequestWithParam 메서드  
-> createRequest 메서드  
-> getMatchedCookies 메서드  
(-> doRequest 메서드로 요청한다)

getMatchedCookieds 메서드 코드  
```java
class HTTPRequest {
   private static final CookieStore COOKIE_STORE = ThreadContextCookieStore.INSTANCE; // 스레드 별로 쿠키를 관리하는 CookieStore
    private CookieOrigin cookieOrigin; // 쿠키의 기본 정보를 저장하는 클래스 (인스턴스 변수 - 모든 스레드가 공유)
    
    private List<Header> getMatchedCookies(String uriString) {
        // ...

        cookieOrigin = new CookieOrigin(uri.getHost(), port, uri.getPath(), isSecure); // 새로운 CookieOrigin 생성

        final List<Cookie> cookies = COOKIE_STORE.getCookies();
        // Find cookies matching the given origin
        final List<Cookie> matchedCookies = new ArrayList<>();
        final Date now = new Date();
        boolean expired = false;
        for (final Cookie cookie : cookies) {
            if (!cookie.isExpired(now)) {
                if (COOKIE_SPEC.match(cookie, cookieOrigin)) { // 해당 쿠키가 CookieOrigin에 맞는지 확인
                    if (LOGGER.isDebugEnabled()) {
                        LOGGER.debug("Cookie {} match {}", cookie, cookieOrigin);
                    }
                    matchedCookies.add(cookie);
                }
            } 
            // ...
        }
        // ...
    }
}
```

현재 uri을 이용해 CookieOrigin 생성한다.
CookieManage에 있는 쿠키들을 요청에 담는데, 이때 새로 생성한 CookieOrigin과 매칭시켜서
맞는 쿠키만 요청에 담는다.

> 이때 Race Condition이 발생할 수 있다.

(두개의 스레드 thx1, thx2가 있다고 가정)  
(OAuth2 인증을 위해 API 서버(1) -> Mock 서버 -> API 서버(2) 순서로 요청을 보내는 경우)
0. [thx1] API 서버(1) 요청 후 쿠키를 CookieManager에 담는다, Mock 서버 요청을 수행한다,  
   [thx2] API 서버(1) 요청을 수행한다.
1. [thx1] API 서버(2) 요청에서 cookieOrigin = new CookieOrigin(uri.getHost(), port, uri.getPath(), isSecure); 실행  
   (API 서버의 도메인을 CookieOrigin에 담는다)
2. [thx2] Mock 서버 요청에서 cookieOrigin = new CookieOrigin(uri.getHost(), port, uri.getPath(), isSecure); 실행  
   (Mock 서버의 도메인을 CookieOrigin에 담는다)
3. [thx1] if (COOKIE_SPEC.match(cookie, cookieOrigin)) 수행 -> 바뀐 CookieOrigin으로 인해 쿠키 담기지 못함
4. [thx1] 스레드의 인증이 실패한다.

thx1 스레드가 다른 스레드와 비교했을 때, 요청들을 너무 빨리 수행해서  
레이스 컨디션이 발생했다.

---

#### 두번째 케이스

HTTPRequest 클래스의 doRequest 메서드는  
요청을 수행한 후 processResponseCookies 메서드를 수행한다.  
이 메서드를 통해 응답으로 받은 쿠키를 CookieManager에 저장한다.

processResponseCookies 메서드 코드  
```java
class HTTPRequest {
   private CookieOrigin cookieOrigin;
   
   // ...
   
   private void processResponseCookies(Iterator<Header> iterator) {
       iterator.forEachRemaining(header -> {
           try {
               List<Cookie> cookies = COOKIE_SPEC.parse(header, cookieOrigin); // 헤더에 있는 Set-Cookie 헤더를 파싱해서 쿠키로 변환 & CookieOrigin의 정보를 이용해 쿠키를 생성
              // ...
           } catch (Exception ex) {
               // ...
           }
       });
       // ...
   }
}

```

(두개의 스레드 thx1, thx2가 있다고 가정)  
(OAuth2 인증을 위해 API 서버(1) -> Mock 서버 -> API 서버(2) 순서로 요청을 보내는 경우)
0. [thx2] API 서버(1) 요청을 수행한다.
1. [thx1] API 서버(1) 요청의 cookieOrigin = new CookieOrigin(uri.getHost(), port, uri.getPath(), isSecure); 실행
2. [thx2] Mock 서버 요청의 cookieOrigin = new CookieOrigin(uri.getHost(), port, uri.getPath(), isSecure); 실행
3. [thx1] doRequest에서 요청 수행
4. [thx1] processResponseCookies 메서드 수행  
   (thx2가 생성해서 초기화 한 mock 서버의 CookieOrigin으로 인해 API 서버의 쿠키의 도메인이 Mock 서버로 세팅된다)
5. [thx1] 이후 API 서버(2) 요청에서 쿠키가 담기지 않아서 인증에 실패한다.  
   (API 서버(1)의 쿠키가 Mock 서버의 도메인으로 설정되어 있기 때문)

thx1 스레드가 다른 스레드와 비교했을 때, 요청들을 너무 느리게 수행해서  
레이스 컨디션이 발생했다.

---

### 해결

이를 막기 위한 방법
1. HTTPRequest 클래스를 공유하지 않고, ThreadLocal로 관리한다. x
2. API 서버에 요청할 때, Mock 서버에 요청할 때, API 서버에 요청할 때  
   각각의 요청을 모든 스레드가 동시에 수행하고 동시에 끝나도록 synchronize 처리한다.

1번은 불가능하다.  
nGrinder가 HTTPRequest를 스레드에서 관리하면 에러를 발생시킨다.

> 정확히는 스레드 별로 수행하는 메서드에서  
> new HTTPRequest()를 통해 새로운 HTTPRequest 객체를 생성하면 에러가 발생한다.

2번을 선택했다.  
스레드 사이의 sync를 맞추는 작업은 성능 상의 이슈가 있을 수 있지만,  
이 작업은 성능 테스트 전 인증을 위한 작업이므로,  
성능 상의 이슈는 크게 중요하지 않다고 판단했다.

Thread Synchronezation을 처리하기 위해 CountDownLatch를 사용했다.

CountDownLatch의 핵심 메서드  
0. 생성자: count를 초기화한다.  
   (스레드의 수를 count로 설정한다)
1. `await()` : count가 0이 될 때까지 대기한다.
2. `countDown()` : count를 1 감소시킨다.

각각의 요청 사이마다 CountDownLatch를 이용해 스레드 동기화를 처리했다.

```java
// 간단하게 표현한 코드
class TestRunner {
   private CountDownLatch latch1 = new CountDownLatch(100); // 100개의 스레드
   private CountDownLatch latch2 = new CountDownLatch(100);
   private HTTPRequest httpRequest = new HTTPRequest();

   @Test
   public void request1() {
      request.GET("{API 서버}");
      
      latch1.countDown();
      latch1.await();
      
      request.GET("{Mock 서버}");
      
      latch1.countDown();
      latch1.await();

      request.GET("{API 서버}");
   }
}
```

위 코드를 추가해줌으로써 모든 스레드들이 동시에 같은 서버에만 요청을 보내도록 처리했다.

이로 인해 레이스 컨디션 문제가 해결되었고,  
인증에 실패한 유저들이 없어졌다. ^^

### 그 외의 해결 방법

1. 도메인별로 HTTPRequest를 관리한다.  
   (API 서버 요청, Mock 서버 요청을 각각의 HTTPRequest 객체로 관리한다)
2. OAuth2 인증을 수행할 때, 서블릿 세션이 아닌 다른 방법으로 세션을 관리한다.  
   (AuthorizationRequestRepository 클래스를 내가 직접 구현하는 것)

---

### 이 문제를 통해 얻은 것들

멀티스레딩 환경에서의 디버깅은 매우 어렵다.  
(매번 실행할 때마다 결과가 다르게 나온다)