## JVisaulVM 원격 연결이 되지 않는다.

### 개요

JVisualVM을 이용하여 다른 컴퓨터에서 실행되는  
Java 프로세스에 연결하려고 하였으나 연결이 되지 않았다.

### 원인

JVisualVM은 JMX를 이용하여 연결을 한다.

이를 위해 자바 프로그램을 실행할 때  
설정해줘야 하는 옵션이 있는데,  
여기서 몇개를 빼먹어서 연결이 되지 않았다.

```shell
java \
        -Dcom.sun.management.jmxremote=true \
        -Djava.rmi.server.hostname={ip_address} \
        -Dcom.sun.management.jmxremote.port={port} \
        -Dcom.sun.management.jmxremote.rmi.port={port} \
        -Dcom.sun.management.jmxremote.authenticate=false \
        -Dcom.sun.management.jmxremote.ssl=false \
        -Dcom.sun.management.jmxremote.local.only=false \
        -jar target/your-jar-file.jar
```

위 옵션들을 설정해줘야 한다.

여기서 빼억은 옵션은  
```shell
-Djava.rmi.server.hostname={ip_address} \
-Dcom.sun.management.jmxremote.rmi.port={port} \
```

이 두가지 이다.

`-Djava.rmi.server.hostname` 옵션을 통해 원격에서 실행되는  
자바 프로그램의 IP 주소를 설정해줘야 한다.

> 여기서 IP 주소를 지정해주지 않았을 때 발생하는 문제는
> 
> 1. 잘못된 IP 주소 선택:  
>    서버가 여러 네트워크 인터페이스를 가지고 있거나 NAT(Network Address Translation) 뒤에 있을 때, 잘못된 IP 주소가 선택될 수 있습니다. 이는 클라이언트가 서버에 연결하는 데 실패할 수 있다. 
> 2. DNS 문제:  
>    자동으로 감지된 호스트명이 DNS에 등록되어 있지 않거나 올바르지 않을 경우, 클라이언트가 RMI 서버를 찾지 못할 수도 있다.

`-Dcom.sun.management.jmxremote.rmi.port` 옵션을 통해  
RMI(Remote Method Invocation) 포트를 설정해줘야 한다.

> 이미 JMX 포트를 지정해줬는데, 굳이 RMI 포트를 지정해줘야 하는 이유는 무엇일까?
> 
> RMI 포트를 지정해주지 않으면,  
> 자바 프로그램이 동적으로 포트를 할당하게 된다.  
> 이때 JMX 포트가 아닌 다른 포트를 할당할 수도 있다.
> 
> 여기서 나는 자바 프로그램을 AWS EC2에서 실행했는데,  
> EC2는 보안 그룹을 통해 포트를 제어하기 때문에  
> 동적으로 할당된 포트를 열어주지 않을 수도 있다.

### 해결

위 옵션들을 설정해주고 다시 실행하니  
JVisualVM과 연결이 잘 되었다.

---

// todo

1. RMI 포트와 JMX 포트의 관계 -> RMI, JMX 공부 
2. ip 주소 설정해주지 않았을 때 발생하는 문제 분석