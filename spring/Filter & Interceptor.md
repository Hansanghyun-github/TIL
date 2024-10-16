로그인 등 애플리케이션 여러 로직에서 공통으로 관심이 있는 것을 공통 관심사(cross-cutting concern)라고 한다.

> 거의 대부분의 모든 로직에서 사용하는 로직을 따로 관리한다면,  
> 해당 로직의 수정을 하기 위해서는 모든 로직을 수정해야 한다.  
> -> 너무 번거롭다.

이러한 문제는 스프링에서 제공하는 AOP라는 기능을 활용할 수도 있지만,  
서블릿 필터 또는 스프링 인터셉터를 사용하여 해결할 수 있다.

## 서블릿 필터

서블릿이 지원하는 기능으로,  
필터를 적용하면 필터가 호출된 다음에 서블릿이 호출된다.

> 여기서 말하는 서블릿은  
> (스프링 기준) DispatcherServlet을 말한다.

필터는 특정 URL 패턴에 대해서만 적용할 수 있다.

### 필터 흐름

> 필터에서 로그인 기능을 구현했다고 가정

1. 인증 성공한 사용자: HTTP 요청 -> 필터 -> 서블릿 -> 컨트롤러
2. 인증 실패한 사용자: HTTP 요청 -> 필터(인증 실패, 서블릿 호출 X)

적절하지 않은 요청은 필터에서 걸러낼 수 있다.

### 필터 체인

흐름  
HTTP 요청 -> 필터1 -> 필터2 -> 필터3 -> 서블릿 -> 컨트롤러

필터는 체인으로 구성되고, 순서를 지정할 수 있다.

> FilterRegistrationBean을 사용하여 필터를 등록할 수 있다.  
> 이때 순서와 URL 패턴을 지정할 수 있다.

> FilterRegistrationBean을 사용하지 않고,  
> @Filter 어노테이션을 사용하여 필터를 등록할 수도 있다.  
> (이때는 순서를 지정할 수 없다)

### 필터 인터페이스

```java
public interface Filter {
    public default void init(FilterConfig filterConfig) throws ServletException {}
    
    public void doFilter(ServletRequest request, ServletResponse response,
    FilterChain chain) throws IOException, ServletException;
    
    public default void destroy() {}
}
```

- init: 필터 초기화, 서블릿 컨테이너가 생성될 때 호출
- doFilter: 필터 로직, 매 요청마다 호출
- destroy: 필터 종료, 서블릿 컨테이너가 종료될 때 호출

필터 인터페이스를 구현하고 등록하면 된다.  
-> 서블릿 컨테이너가 필터를 싱글톤으로 생성하고 관리한다.

> doFilter 메서드에서  
> chain.doFilter(request, response)를 호출해야 다음 필터(or 서블릿)로 넘어간다.

---

## 스프링 인터셉터

스프링 MVC가 제공하는 기능으로,  
필터와 비슷하게 공통 관심사를 처리할 수 있지만,  
필터와 다르게 적용되는 순서와 범위, 그리고 사용방법이 다르다.

### 인터셉터 흐름

HTTP 요청 -> 필터 -> 서블릿 -> 인터셉터 -> 컨트롤러

서블릿과 컨트롤러 사이에서 동작한다.

> 인터셉터는 스프링 MVC가 제공하는 기능이기 때문에,  
> DispatcherServlet 이후에 동작한다.  
> (스프링 MVC의 시작점이 DispatcherServlet이라고 봐도 무방하다)

### 인터셉터 체인

HTTP 요청 -> 필터 -> 서블릿 -> 인터셉터1 -> 인터셉터2 -> 인터셉터3 -> 컨트롤러

필터와 마찬가지로 체인으로 구성되고, 순서를 지정할 수 있다.

### 인터셉터 인터페이스

```java
public interface HandlerInterceptor {
    default boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {}
    
    default void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, @Nullable ModelAndView modelAndView) throws Exception {}
    
    default void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, @Nullable Exception ex) throws Exception {}
}
```

- preHandle: 컨트롤러 호출 전 호출
- postHandle: 컨트롤러 호출 후 호출 (뷰 렌더링 전, 핸들러 어댑터 호출 후)
- afterCompletion: 요청 완료 이후 호출 (뷰가 렌더링 된 후)

컨트롤러에서 예외가 발생하면 afterCompletion 메서드만 호출된다.  
(postHandle은 호출되지 않는다)

### 인터셉터 등록

- WebMvcConfigurer 인터페이스를 구현하여 addInterceptors 메서드를 오버라이딩한다.
- addInterceptors 메서드에서 InterceptorRegistry를 사용하여 인터셉터를 등록한다.

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new CustomInterceptor())
             .order(1)
            .addPathPatterns("/path1")
            .excludePathPatterns("/path2");
    }
}
```

---

## 필터 vs 인터셉터

필터는 DispatcherServlet에 들어가기 전인 Web Application의 모든 요청에 대해 동작한다.  
Web Application 단의 기능만 사용할 수 있다.

> 필터는 스프링의 기능을 사용할 수 없다.

> 필터는 인코딩 변환 처리, XSS 방어 등의 기능을 구현할 때 사용한다고 한다.  
> (위 기능을 인터셉터에서도 구현할 수 있지만, 필터가 더 적합하다고 한다.)

인터셉터는 DispatcherServlet 다음에 동작한다.  
(Spring Application에서 동작한다.)

> 인터셉터는 스프링의 기능을 사용할 수 있다.



---

## 언제 AOP를 사용하고, 언제 필터 & 인터셉터를 사용할까?

// TODO