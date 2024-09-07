## 직접 url 입력하는 건 성공하지만, AWS ALB의 health check는 계속 실패했다.

이유는 nginx의 server_name 설정 떄문이다.

나는 nginx의 site-available 설정을 두가지를 했다.
1. default 설정(server_name: _)
2. dev 설정(직접 만듬)(server_name: {내가 지정한 도메인})

내가 직접 url을 입력할 때는, 내가 설정한 도메인 네임을 직접 입력하기 때문에  
2번 설정을 통해 프로시 기능을 수행했는데,  

AWS ALB가 요청하는건, 내가 설정한 도메인 네임으로 요청하지 않기 떄문에,  
1번 설정을 통해 프록시 기능을 수행했다.  
-> 내가 설정한 스프링 서버로의 프록시 기능이 수행되지 않았다.

### 해결 방법

nginx에서 sites-enabled에 있는 default 심볼릭 링크를 없애 주었다.

<img src="../img/nginx_problem_1.png" width="300">

default 심볼릭 링크를 없애줌으로써,  
내가 실행시킨 스프링 서버로 올바르게 라우팅 되었다.

---

## nginx: [emerg] "set" directive is not allowed here in {nginx 설정 파일 경로}.inc

### 개요

conf 파일에서 포트 번호를 지정해주기 위해 추가로 inc 파일을 include 했는데,  
inc 파일에서 set을 사용하려고 하니 에러가 발생했다.

### 원인

conf 파일에서 inc 파일을 include 해줄 때,  
include 디렉티브의 위치 때문에 발생한 문제이다.

> include 디렉티브가 위치한 영역에서  
> set 디렉티브가 동작한다.  

set 디렉티브는 http 블록에서 사용할 수 없다.  
server 블록이나 location 블록에서 사용해야 한다.

### 해결

inc 파일을 include 하는 위치를 변경해주었다.  
(http 블록에서 server 블록으로 변경)

```nginx
server {
    listen 80;
    server_name {도메인 네임};

    include {inc 파일 경로};
}
```