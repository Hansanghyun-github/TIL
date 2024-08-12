# 프록시

클라이언트는 서버에 필요한 것을 요청하고,  
서버는 클라이언트의 요청을 처리하는 역할을 한다.

클라이언트와 서버 개념에서 일반적으로 클라이언트가 서버를 직접 호출하고,  
처리 결과를 직접 받는다.  
(직접 호출)

여기서 클라이언트가 요청한 결과를 서버에 직접 요청한 것이 아니라  
어떤 대리자를 통해서 대신 간접적으로 서버에 요청할 수 있다.  
(간접 호출)

여기서 대리자를 프록시(Proxy)라고 한다.

프록시를 통해 여러 가지 일을 할 수 있다.  
1. 접근 제어(권한에 따른 차단, 캐싱, 지연 로딩)
2. 로깅

---

객체에서 프록시가 되려면,  
프록시 객체는 실제 객체와 같은 인터페이스를 구현해야 한다.

그리고 클라이언트가 사용하는 서버 객체를  
프록시 객체로 변경해도 클라이언트 코드를 변경하지 않고 동작할 수 있어야 한다.

---

## 프록시를 이용하는 GOF 디자인 패턴

프록시를 이용한 디자인 패턴은 두가지가 있다.

1. 프록시 패턴: 접근 제어가 목적
2. 데코레이터 패턴: 새로운 기능 추가가 목적

둘 다 프록시를 사용하는 방법이지만 GOF 디자인 패턴에서는  
이 둘을 의도(intent)에 따라서 구분한다.

> 디자인 패턴에서 핵심은 의도이다.

---

## 인터페이스 기반 프록시

클라이언트가 서버 인터페이스를 의존하고 있다면,  
프록시 객체는 서버 인터페이스를 구현함으로써  
클라이언트가 서버 객체를 사용하는 것과 동일하게 사용할 수 있다.

```java
public interface IService {
    String runSomething();
}

public class RealService implements IService {
    @Override
    public String runSomething() {
        return "서비스 짱!!!";
    }
}

public class ProxyService implements IService {
    private IService service;
    
    public ProxyService(IService target) {
        this.service = target;
    }

    @Override
    public String runSomething() {
        System.out.println("호출에 대한 흐름 제어가 주목적, 반환 결과를 그대로 전달");
        return service.runSomething();
    }
}

public class ProxyPattern {
    public static void main(String[] args) {
        IService proxy = new ProxyService(new RealService());
        System.out.println(proxy.runSomething());
    }
}
```

---

## 클래스 기반 프록시

클라이언트가 서버 클래스를 의존하고 있다면,  
프록시 객체는 서버 클래스를 상속함으로써  
클라이언트가 서버 객체를 사용하는 것과 동일하게 사용할 수 있다.

```java
public class RealService {
    public String runSomething() {
        return "서비스 짱!!!";
    }
}

public class ProxyService extends RealService {
    @Override
    public String runSomething() {
        System.out.println("호출에 대한 흐름 제어가 주목적, 반환 결과를 그대로 전달");
        return super.runSomething();
    }
}

public class ProxyPattern {
    public static void main(String[] args) {
        RealService proxy = new ProxyService();
        System.out.println(proxy.runSomething());
    }
}
```

> 이때 기존 서버 클래스가 기본 생성자가 아닌  
> 매개변수를 받는 생성자만 가지고 있다면,  
> 프록시 클래스도 매개변수를 받는 생성자를 만들어야 한다.  
> (안하면 컴파일 에러 발생)

---

## 인터페이스 기반 프록시 vs 클래스 기반 프록시

인터페이스 기반 프록시는 인터페이스를 구현하기 때문에  
별도의 인터페이스가 필요하다.

클래스 기반 프록시는 상속을 사용하기 떄문에 몇가지 제약이 있다.

1. 부모 클래스의 생성자가 호출되어야 한다.
2. 클래스에 final 키워드를 사용할 수 없다.  
   (붙으면 상속이 불가능하기 때문에)
3. 메서드에 final 키워드를 사용할 수 없다.  
   (붙으면 오버라이딩이 불가능하기 때문에)

---