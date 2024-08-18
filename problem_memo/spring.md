## 필터 관련 문제 두가지

### 개요

1. 커스텀 필터를 추가했는데, doFilterInternal 메서드가 두번 호출된다.
2. 첫번째로 호출되는 필터에만 order가 세팅되어 있고, 로깅 관련 설정은 두번쨰로 호출되는 필터에만 세팅되어 있다.  
   ![img_1.png](../img/spring_filter_2.png)
   ![img.png](../img/spring_filter_1.png)

> 해당 필터는 AbstractRequestLoggingFilter 클래스를 상속받은 클래스로  
> 로그 관련 기능을 수행하는 필터이다.

### 원인

ApplicationFilterChain에 등록된 필터 목록을 보니  
내가 만든 필터가 두번 등록되어 있었다.

![img.png](../img/spring_filter_3.png)

첫번째는 Config 파일에서 RegistrationBean을 통해 추가한 필터이고,  
두번째는 직접 추가된 필터인 것으로 확인된다.

이를 보고 해당 필터를 어떻게 스프링 빈으로 등록했는지 확인해보니,  
@Bean, @Component를 동시에 사용하고 있었다.

> 첫번째 필터에만 order가 세팅되어 있고,  
> 두번째 필터에만 로깅 관련 필드가 세팅되어 있는 이유
> 
> 첫번째 필터는 @Bean을 통해 등록했는데 이때 order를 세팅했다.
> 그리고 로깅 관련 필드는 해당 필터 클래스 내부에서 @PostConstruct 를 통해 설정했는데,  
> 해당 메서드는 모든 스프링 빈들이 등록된 이후에 해당 클래스의 필드를 세팅하기 때문에  
> 두번째 필터에만 세팅이 되어 있었던 것이다.

### 해결 방법

결국 @Bean or @Component 둘 중 하나를 삭제해야 한다.

내가 원하는 건 필터의 순서를 위한 order를 세팅하는 것이기 때문에,  
@Component를 삭제하는 것으로 결정했다.

> 로깅 관련 필드 설정은  
> @PostConstruct 를 이용하지 않고,  
> 빈을 등록할 때, 해당 메서드를 직접 호출하는 것으로 해결했다.

위 문제는 인텔리제이 디버깅 덕분에 그나마 빠르게 해결할 수 있었다.

> 위 문제를 해결하면서,  
> 스프링 시큐리티에서 이용하는 필터는  
> DelegateFilterProxyRegistrationBean을 통해 등록하는 것을 알게 됐다.  
> 그리고 해당 필터의 order는 default로 -100 인 것을 알게 됐다.

---

## 로깅 필터는 두번 추가 되서 두번 호출 됐는데, 인증 관련 시큐리티 필터는 @Component, securityFilterChain 두번 추가 됐는데, 한번만 호출된 이유

### 원인

둘다 OncePerRequestFilter를 상속받았는데,
이때 해당 필터는 doFilter 메서드에서
이미 필터가 적용되었는지 확인하는 메서드를 호출한다.

```java
class OncePerRequestFilter {
    public final void doFilter(ServletRequest request, ServletResponse response, FilterChain filterChain) {
        // ...
       
       boolean hasAlreadyFilteredAttribute = request.getAttribute(alreadyFilteredAttributeName) != null;
       
       // ...
       
       if (hasAlreadyFilteredAttribute) {
          if (DispatcherType.ERROR.equals(request.getDispatcherType())) {
             doFilterNestedErrorDispatch(httpRequest, httpResponse, filterChain);
             return;
          }

          // Proceed without invoking this filter...
          filterChain.doFilter(request, response);
       }
       else {
          // Do invoke this filter...
          request.setAttribute(alreadyFilteredAttributeName, Boolean.TRUE);
          try {
             doFilterInternal(httpRequest, httpResponse, filterChain);
          }
          finally {
             // Remove the "already filtered" request attribute for this request.
             request.removeAttribute(alreadyFilteredAttributeName);
          }
       }
    }
}
```

alreadyFilteredAttributeName를 request에 세팅해서  
이미 필터가 적용되었는지 확인하고,  
적용되지 않았다면 필터를 적용하고, // doFilterInternal 메서드 호출  
적용되었다면 필터를 적용하지 않는다. // filterChain.doFilter(request, response) 호출 (다음 필터로 넘어감)

TemporaryAuthFilter는 같은 이름으로 두번 등록되었는데,  
HttpMessageLoggingFilter는 다른 이름으로 두번 등록됐다. // httpMessageLoggingFilter, httpMessageLoggingFilterRegistrationBean
(이름이 다르면, 이미 필터가 적용되었다고 판단하지 않는다)

그래서 HttpMessageLoggingFilter는 두번 호출됐고,  
TemporaryAuthFilter는 한번만 호출됐다.

### 해결

결국 두번 등록된 것이 문제이기 때문에,  
하나만 등록하도록 수정했다.