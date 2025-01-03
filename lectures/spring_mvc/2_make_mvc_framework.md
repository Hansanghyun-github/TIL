## v0 - 맨 처음 코드

각각의 컨트롤러가 HttpServlet을 상속받아서,  
`service` 메서드를 오버라이딩하여 구현하고 있다.

```java
@RequiredArgsConstructor
@WebServlet("/member/list")
public class MemberListController implements HttpServlet {
    private final MemberRepository memberRepository;
    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        System.out.println("MvcMemberListServlet.service");
        List<Member> members = memberRepository.findAll();
        request.setAttribute("members", members);
        
        String viewPath = "/WEB-INF/views/members.jsp";
        RequestDispatcher dispatcher = request.getRequestDispatcher(viewPath);
        dispatcher.forward(request, response);
    }
}
```

> `members.jsp` 파일에는 화면을 그리는 코드가 들어있다.

---

MVC 패턴을 적용한 덕분에 컨트롤러의 역할과 뷰를 렌더링하는 역할을 명확하게 구분할 수 있게 되었다.


하지만 위 코드의 아쉬운 점들이 있다.  

### 현재 MVC 컨트롤러의 단점

새로운 컨트롤러를 추가할 때마다 아래의 단점들이 발생한다.

#### 1. 포워드 중복  
뷰로 이동하는 코드가 중복된다.

```
String viewPath = "/WEB-INF/views/members.jsp";
RequestDispatcher dispatcher = request.getRequestDispatcher(viewPath);
dispatcher.forward(request, response);
```

#### 2. ViewPath의 중복

뷰의 경로가 중복된다.

> 만약 jsp가 아닌 thyemleaf로 변경한다면,  
> 모든 컨트롤러의 뷰 경로를 수정해야 한다.

#### 3. 사용하지 않는 코드

HttpServletRequest, HttpServletResponse를 사용하지 않는 컨트롤러도 있다.

> 위 컨트롤러도 HttpServletResponse를 사용하지 않고 있다.

---

## 결국 공통 처리가 어렵다

이 문제를 해결하기 위해 프론트 컨트롤러(Front Controller) 패턴을 도입해보자.

> 입구를 하나로

---

## v1 - 프론트 컨트롤러 패턴

![img.png](../../img/frontcontroller_1.png)

ControllerV1 이라는 인터페이스를 도입하고,  
각 컨트롤러는 이 인터페이스를 구현하도록 변경한다.

```java
public interface ControllerV1 {
    void process(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException;
}
```

그리고 프론트 컨트롤러 서블릿을 도입한다.

```java
@WebServlet(name = "frontControllerServletV1", urlPatterns = "/front-controller/v1/*")
public class FrontControllerServletV1 extends HttpServlet {
    private final Map<String, ControllerV1> controllerMap = new HashMap<>();

    public FrontControllerServletV1() {
        controllerMap.put("/front-controller/v1/members/new-form", new MemberFormControllerV1());
        controllerMap.put("/front-controller/v1/members/save", new MemberSaveControllerV1());
        controllerMap.put("/front-controller/v1/members", new MemberListControllerV1());
    }

    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        System.out.println("FrontControllerServletV1.service");

        String requestURI = request.getRequestURI();

        ControllerV1 controller = controllerMap.get(requestURI);
        if (controller == null) {
            response.setStatus(HttpServletResponse.SC_NOT_FOUND);
            return;
        }

        controller.process(request, response);
    }
}
```

### service()

먼저 request의 URI를 조회해서 실제 호출할 컨트롤러를 찾는다.  
그리고 찾은 컨트롤러를 호출한다.

### v1을 도입하면

프론트 컨트롤러를 도입함으로써 공통 처리가 가능해졌다.

---

### 아직 남은 문제

> 아직 모든 컨트롤러에서 뷰 경로를 직접 지정하고 있다. (중복도 여전히 존재)
>
> ```
> String viewPath = "/WEB-INF/views/members.jsp";
> RequestDispatcher dispatcher = request.getRequestDispatcher(viewPath);
> dispatcher.forward(request, response);
> ```

이 부분을 깔끔하게 분리하기 위해 별도로 뷰를 처리하는 객체를 도입한다.

## v2 - 뷰 분리

![img.png](../../img/mvc_framework_2.png)

기존 v1은 각 컨트롤러에서 직접 뷰를 호출하고 있었다.  
v2에서는 각 컨트롤러가 뷰에 대한 별도의 객체를 반환하도록 변경한다.

```java
public class MyView {
    private final String viewPath;

    public MyView(String viewPath) {
        this.viewPath = viewPath;
    }

    public void render(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        RequestDispatcher dispatcher = request.getRequestDispatcher(viewPath);
        dispatcher.forward(request, response);
    }
}
```

```java
public interface ControllerV2 {
    MyView process(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException;
}
```

```java
public class MemberListControllerV2 implements ControllerV2 {
    private final MemberRepository memberRepository = MemberRepository.getInstance();

    @Override
    public MyView process(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        List<Member> members = memberRepository.findAll();
        request.setAttribute("members", members);
        return new MyView("/WEB-INF/views/members.jsp");
    }
}
```

```java
public class FrontControllerServletV2 extends HttpServlet {
    private final Map<String, ControllerV2> controllerMap = new HashMap<>();

    public FrontControllerServletV2() {
        controllerMap.put("/front-controller/v2/members/new-form", new MemberFormControllerV2());
        controllerMap.put("/front-controller/v2/members/save", new MemberSaveControllerV2());
        controllerMap.put("/front-controller/v2/members", new MemberListControllerV2());
    }

    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        System.out.println("FrontControllerServletV2.service");

        String requestURI = request.getRequestURI();

        ControllerV2 controller = controllerMap.get(requestURI);
        if (controller == null) {
            response.setStatus(HttpServletResponse.SC_NOT_FOUND);
            return;
        }

        MyView view = controller.process(request, response);
        view.render(request, response);
    }
}
```

### v1 -> v2로 변경된 점

딱 한가지다.

기존 컨트롤러들이 더 이상 뷰를 직접 호출하지 않고,  
`MyView` 객체를 반환하도록 변경했다.

뷰를 호출하는 부분은 프론트 컨트롤러에서 처리한다.

> 각 컨트롤러들은 경로만 반환하면 된다.

---

### 아직 남은 문제

> 아직 컨트롤러들은 HttpServletRequest, HttpServletResponse을 의존하고 있다.

컨트롤러들이 위 클래스를 이용하는 경우가 딱 두가지 이다.
1. 요청 파라미터 조회
2. 뷰에 전달할 데이터 전달

이 두가지를 처리하는 코드를 별도의 객체로 분리해보자.

## v3 - Model 추가

`서블릿 종속성 제거`  
HttpServletRequest, HttpServletResponse 대신,  
별도의 객체를 만들어서 사용한다.

`뷰 이름 중복 제거`  
'/WEB-INF/views/new-form.jsp' -> 'new-form'

![img.png](../../img/mvc_framework_3.png)

컨트롤러가 ModelView를 반환하도록 변경한다.

그리고 프론트 컨트롤러는 이를 가지고 뷰를 호출한다.

```java
public class ModelView {
    private String viewName;
    private Map<String, Object> model = new HashMap<>();

    public ModelView(String viewName) {
        this.viewName = viewName;
    }

    public ModelView(String viewName, Map<String, Object> model) {
        this.viewName = viewName;
        this.model = model;
    }

    public String getViewName() {
        return viewName;
    }

    public Map<String, Object> getModel() {
        return model;
    }
}
```

```java
public interface ControllerV3 {
    ModelView process(Map<String, String> paramMap);
}
```

```java
public class MemberListControllerV3 implements ControllerV3 {
    private final MemberRepository memberRepository = MemberRepository.getInstance();

    @Override
    public ModelView process(Map<String, String> paramMap) {
        List<Member> members = memberRepository.findAll();
        ModelView mv = new ModelView("members");
        mv.getModel().put("members", members);
        return mv;
    }
}
```

```java
public class FrontControllerServletV3 extends HttpServlet {
    private final Map<String, ControllerV3> controllerMap = new HashMap<>();

    public FrontControllerServletV3() {
        controllerMap.put("/front-controller/v3/members/new-form", new MemberFormControllerV3());
        controllerMap.put("/front-controller/v3/members/save", new MemberSaveControllerV3());
        controllerMap.put("/front-controller/v3/members", new MemberListControllerV3());
    }

    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        System.out.println("FrontControllerServletV3.service");

        String requestURI = request.getRequestURI();

        ControllerV3 controller = controllerMap.get(requestURI);
        if (controller == null) {
            response.setStatus(HttpServletResponse.SC_NOT_FOUND);
            return;
        }

        Map<String, String> paramMap = createParamMap(request);
        ModelView mv = controller.process(paramMap);

        String viewName = mv.getViewName();
        MyView myView = viewResolver(viewName);
        myView.render(mv.getModel(), request, response);
    }

    private MyView viewResolver(String viewName) {
        return new MyView("/WEB-INF/views/" + viewName + ".jsp");
    }

    private Map<String, String> createParamMap(HttpServletRequest request) {
        Map<String, String> paramMap = new HashMap<>();
        request.getParameterNames().asIterator()
                .forEachRemaining(paramName -> paramMap.put(paramName, request.getParameter(paramName)));
        return paramMap;
    }
}
```

---

## v4 - 단순한 컨트롤러

개발자 입장에서, 항상 ModelView를 생성하고 반환하는 것이 번거롭다.  
-> 모델을 파라미터로 받아서 처리하도록 변경한다.

```java
public interface ControllerV4 {
    String process(Map<String, String> paramMap, Map<String, Object> model);
}
```

> 이외의 코드는 생략한다.  
> (그냥 파라미터로 모델 넘기고, 저 모델 가지고 뷰 렌더링하는 코드)

---

## v5 - 유연한 컨트롤러

v3, v4는 모델을 파라미터로 받냐, 반환하냐의 차이만 있었다.  
(형식만 다를 뿐, 내부 로직은 동일하다)

> 이때 개발자들이 선호하는 방식을 선택할 수 있도록 변경해보자.

어댑터 패턴을 이용해 구현한다.

### 어댑터 패턴

어댑터 패턴이란,  
기존의 코드를 수정하지 않고,  
개발자가 원하는 방식으로 코드를 변경할 수 있도록 하는 패턴이다.

> TMI  
> 
> 예전 핸드폰들은 모두 마이크로 5핀 충전기를 사용했다.  
> (아이폰은 8핀이었지만)
> USB-C가 나오면서 충전기를 바꿔야 하는 번거로움이 있었다.
> 
> 이를 해결하기 위해 마이크로 5핀 -> USB-C 어댑터를 사용하면,  
> 기존의 충전기를 그대로 사용할 수 있었다.
> 
> 여기서 마이크로 5핀이 기존 코드, USB-C가 새로운 코드라고 생각하면 된다.

대신 단점은 각각의 코드마다, 그에 대한 어댑터를 만들어야 한다는 것이다.

### 핵심 코드

> 프론트 컨트롤러는 ModelView를 반환하는 컨트롤러(핸들러)만 처리한다.

이제부턴 컨트롤러 대신 핸들러라고 부르자.

```java
public interface HandlerAdapter {
    boolean supports(Object handler);
    ModelView handle(HttpServletRequest request, HttpServletResponse response, Object handler) throws ServletException, IOException;
}
```

(V3는 규격이 같기 때문에 생략)

```java
public class ControllerV4HandlerAdapter implements HandlerAdapter {
    @Override
    public boolean supports(Object handler) {
        return handler instanceof ControllerV4;
    }

    @Override
    public ModelView handle(HttpServletRequest request, HttpServletResponse response, Object handler) throws ServletException, IOException {
        ControllerV4 controller = (ControllerV4) handler;
        Map<String, String> paramMap = createParamMap(request);
        Map<String, Object> model = new HashMap<>();
        String viewName = controller.process(paramMap, model);
        ModelView mv = new ModelView(viewName);
        mv.setModel(model);
        return mv;
    }

    private Map<String, String> createParamMap(HttpServletRequest request) {
        Map<String, String> paramMap = new HashMap<>();
        request.getParameterNames().asIterator()
                .forEachRemaining(paramName -> paramMap.put(paramName, request.getParameter(paramName)));
        return paramMap;
    }
}
```

```java
public class FrontControllerServletV5 extends HttpServlet {
    private final Map<String, Object> handlerMappingMap = new HashMap<>();
    private final List<HandlerAdapter> handlerAdapters = new ArrayList<>();

    public FrontControllerServletV5() {
        initHandlerMappingMap();
        initHandlerAdapters();
    }

    private void initHandlerMappingMap() {
        handlerMappingMap.put("/front-controller/v5/members/new-form", new MemberFormControllerV4());
        handlerMappingMap.put("/front-controller/v5/members/save", new MemberSaveControllerV4());
        handlerMappingMap.put("/front-controller/v5/members", new MemberListControllerV4());
    }

    private void initHandlerAdapters() {
        handlerAdapters.add(new ControllerV3HandlerAdapter());
        handlerAdapters.add(new ControllerV4HandlerAdapter());
    }

    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        System.out.println("FrontControllerServletV5.service");

        Object handler = getHandler(request);
        if (handler == null) {
            response.setStatus(HttpServletResponse.SC_NOT_FOUND);
            return;
        }

        HandlerAdapter adapter = getHandlerAdapter(handler);
        ModelView mv = adapter.handle(request, response, handler);

        String viewName = mv.getViewName();
        MyView myView = viewResolver(viewName);
        myView.render(mv.getModel(), request, response);
    }

    private Object getHandler(HttpServletRequest request) {
        String requestURI = request.getRequestURI();
        return handlerMappingMap.get(requestURI);
    }

    private HandlerAdapter getHandlerAdapter(Object handler) {
        for (HandlerAdapter adapter : handlerAdapters) {
            if (adapter.supports(handler)) {
                return adapter;
            }
        }
        throw new IllegalArgumentException("handler adapter를 찾을 수 없습니다. handler=" + handler);
    }

    private MyView viewResolver(String viewName) {
        return new MyView("/WEB-INF/views/" + viewName + ".jsp");
    }
}
```

기존 프론트컨트롤러는  
요청 URI에 해당하는 컨트롤러를 조회한 뒤 호출만 하면 끝이었다.

하지만 v5에서는  
요청 URI에 해당하는 핸들러(컨트롤러)를 조회한 뒤,  
해당 핸들러를 처리할 수 있는 어댑터를 찾아서 호출한다.

### 전체 그림

![img.png](../../img/mvc_framework_4.png)