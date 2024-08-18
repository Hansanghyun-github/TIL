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