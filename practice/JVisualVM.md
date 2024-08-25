# JVisualVM

JVisualVM은 Java VisualVM의 약자로, Java 애플리케이션의 성능을 모니터링하고 프로파일링하는 도구이다.

## JVisualVM을 사용하는 이유

- Java 애플리케이션의 CPU 사용량, 메모리 사용량, 스레드 개수 등을 확인할 수 있다.
- 스레드 덤프를 뜨거나, 힙 덤프를 뜨는 등의 작업을 할 수 있다.
- Sampler, Profiler 를 이용해 성능을 분석할 수 있다.

## JVisualVM 사용법

JVisualVM은 JDK에 포함되어 있으므로 별도로 설치할 필요가 없다.  
대신 JMX를 이용하여 연결을 해야한다.

### JMX 설정

JMX를 이용하여 연결하기 위해서는 자바 프로그램을 실행할 때 설정해줘야 하는 옵션이 있다.

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

> JMX는 해당 포트를 통해 TCP 연결을 하기 때문에, 방화벽에서 해당 포트를 열어줘야 한다.

### JMX 인증 설정

모든 사용자가 JMX에 접근할 수 있다면, 이는 보안상 위험하다.  
이를 막기 위해 access, password 파일을 생성하여 접근을 제한할 수 있다.

```shell
java \
        -Dcom.sun.management.jmxremote=true \
        -Dcom.sun.management.jmxremote.port={port} \
        -Dcom.sun.management.jmxremote.rmi.port={port} \
        -Dcom.sun.management.jmxremote.authenticate=true \ # default: true
        -Dcom.sun.management.jmxremote.ssl=false \
        -Dcom.sun.management.jmxremote.password.file=jmxremote.password \
        -Dcom.sun.management.jmxremote.access.file=jmxremote.access \
        -jar target/your-jar-file.jar
```

jmxremote.password 파일  
```shell
monitorRole 123456
controlRole 123456
```

> {role} {password} 형식으로 작성한다.

jmxremote.access 파일  
```shell
monitorRole readonly
controlRole readwrite
```

> {role} {readonly or readwrite} 형식으로 작성한다.
> 
> readonly: 읽기만 가능  
> readwrite: 읽기, 쓰기 가능 (모든 권한)

### 클라이언트 연결

JVisualVM을 실행하고, remote를 선택하여 연결한다.  
JMX를 이용하여 연결할 때, `{ip_address}:{port}` 형식으로 연결한다.

> 위의 설명은 원격 모니터링에 대한 설명이다.  
> 만약 로컬에서 실행하는 경우, JMX 설정을 하지 않아도 된다.