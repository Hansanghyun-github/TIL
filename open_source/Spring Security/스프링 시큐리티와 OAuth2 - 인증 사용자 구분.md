OAuth2 인증은
1. 사용자가 Application에 로그인을 시도하면, Application은 사용자를 인증 서버로 리다이렉트한다.
2. 사용자가 인증 서버에 로그인을 성공하면, 인증 서버는 권한 부여 승인 코드를 Application으로 전달한다.
3. Application은 권한 부여 승인 코드를 이용해 Access Token을 요청한다.
4. Access Token을 받으면, Application은 리소스 서버에 Access Token을 전달하여 원하는 리소스를 요청한다.

이 글에서는 1,2번 과정에서 스프링 시큐리티가 사용자를 어떻게 구분하는지 알아본다.

---

## 스프링 시큐리티의 OAuth2 관련 처리 필터 클래스

스프링 시큐리티는 OAuth2 인증을 처리하기 위해  
OAuth2AuthorizationRequestRedirectFilter 클래스와  
OAuth2LoginAuthenticationFilter 클래스를  
이용한다.

### OAuth2AuthorizationRequestRedirectFilter

사용자가 Application에 로그인을 시도했을 때, 인증 서버로 리다이렉트 시키는 필터이다.

### OAuth2LoginAuthenticationFilter

사용자가 인증 서버에 로그인을 성공한 이후에, 권한 부여 승인 코드를 사용자로부터 받아  
3,4 과정을 처리하는 필터이다.

---

## AuthorizationRequestRepository

스프링 시큐리티에서 AuthorizationRequest를 관리하는 인터페이스

default 구현체로 HttpSessionOAuth2AuthorizationRequestRepository 클래스를 사용한다.  
![spring_security_oauth2_1.png](..%2F..%2Fimg%2Fspring_security_oauth2_1.png)

> HttpSessionOAuth2AuthorizationRequestRepository  
> 
> 서블릿의 세션을 이용해 AuthorizationRequest를 관리하는 클래스

Oauth2AuthorizationRequestRedirectFilter에서  
AuthorizationRequest를 생성하고,  
state 값을 파라미터로 전달할 때 이용한다.

OAuth2LoginAuthenticationFilter에서  
사용자의 세션으로부터 AuthorizationRequest를 가져오고,  
사용자로부터 받은 state 값을 이용해  
AuthorizationRequest를 검증할 때 이용한다.

> 결국 OAuth2 로그인을 진행할 때,  
> 각 사용자를 구분해줘야 한다.  
> 
> 이때 사용자를 구분하기 위한 값이 state이다.

---

## HttpSessionOAuth2AuthorizationRequestRepository 클래스를 이용한 OAuth2 (사용자-Application)인증 과정

### state 발급 과정

1번의 리다이렉트 URL을 설정할 때, 쿼리 파라미터로 state를 설정한다.  
(AuthorizationRequest에 state를 설정한다)  
(이 과정을 담당하는 필터는 OAuth2AuthorizationRequestRedirectFilter)

HttpSessionOAuth2AuthorizationRequestRepository 클래스의 saveAuthorizationRequest 메서드를 통해  
사용자의 세션에 AuthorizationRequest를 저장한다.

```java
class HttpSessionOAuth2AuthorizationRequestRepository {
    @Override
    public void saveAuthorizationRequest(OAuth2AuthorizationRequest authorizationRequest, HttpServletRequest request,
                                         HttpServletResponse response) {
        Assert.notNull(request, "request cannot be null");
        Assert.notNull(response, "response cannot be null");
        if (authorizationRequest == null) {
            removeAuthorizationRequest(request, response);
            return;
        }
        String state = authorizationRequest.getState();
        Assert.hasText(state, "authorizationRequest.state cannot be empty");
        request.getSession().setAttribute(this.sessionAttributeName, authorizationRequest); // 사용자의 세션에 AuthorizationRequest를 저장한다.
    }
}
```

위 코드에서 서블릿 세션 생성 시, JSESSIONID 쿠키를 사용자에게 전달한다.

### state 검증 과정

그리고 (사용자가 인증 서버에 로그인을 성공한 후)  
code & state 쿼리 파라미터를 Application에게 전달한다.  
(이 과정을 담당하는 필터는 OAuth2LoginAuthenticationFilter)

OAuth2LoginAuthenticationFilter 클래스는 HttpSessionOAuth2AuthorizationRequestRepository 클래스의 loadAuthorizationRequest 메서드를 통해  
사용자로부터 받은 state 값과 사용자의 세션에 저장된 state 값을 비교한다.

```java
class HttpSessionOAuth2AuthorizationRequestRepository {
    @Override
    public OAuth2AuthorizationRequest loadAuthorizationRequest(HttpServletRequest request) {
        Assert.notNull(request, "request cannot be null");
        String stateParameter = getStateParameter(request); // request 에서 state 파라미터를 가져온다.
        if (stateParameter == null) {
            return null;
        }
        OAuth2AuthorizationRequest authorizationRequest = getAuthorizationRequest(request); // request 에서 AuthorizationRequest를 가져온다. (사용자의 세션에 저장된 값)
        return (authorizationRequest != null && stateParameter.equals(authorizationRequest.getState()))  // 사용자로부터 받은 state 값과 사용자의 세션에 저장된 state 값을 비교한다.
                ? authorizationRequest : null;
    }
}
```

이 값이 틀리면 OAuth2LoginAuthenticationFilter 클래스는 OAuth2AuthenticationException 에러를 발생시킨다.  
![spring_security_oauth2_2.png](..%2F..%2Fimg%2Fspring_security_oauth2_2.png)

```java
class OAuth2LoginAuthenticationFilter {
    private void attemptAuthentication(HttpServletRequest request, HttpServletResponse response) {
        // ...
        OAuth2AuthorizationRequest authorizationRequest = this.authorizationRequestRepository
                .removeAuthorizationRequest(request, response); // 내부적으로 loadAuthorizationRequest 메서드를 호출한다.
        if (authorizationRequest == null) {
            OAuth2Error oauth2Error = new OAuth2Error(AUTHORIZATION_REQUEST_NOT_FOUND_ERROR_CODE);
            throw new OAuth2AuthenticationException(oauth2Error, oauth2Error.toString());
        }
        // ...
    }
}
```

> 결국 위 검증 과정을 통과하려면,  
> (사용자가 인증 서버에서 로그인을 성공한 후)  
> 사용자가 Application에 권한 부여 승인 코드를 전달할 때  
> 올바른 state 파라미터 값과 JSESSIONID 쿠키를 전달해야 한다.

