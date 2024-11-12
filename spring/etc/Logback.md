아무런 설정도 하지 않고 스프링을 실행하면,
로그는 stdout에 출력된다.

이때 logback-spring.xml 파일을 resources 디렉토리에 추가하면,  
로그를 원하는 대로 설정할 수 있다.

---

### logback-spring.xml

이 이름으로 파일을 만들어서 resources 디렉토리에 넣어주면 알아서 설정된다.

> 다른 이름의 파일을 생성했다면,  
> ```logging.config=classpath:{파일명}.xml```
> 을 추가 해줘야 한다.

---

## <appender>

로그를 어디에 출력할지 설정한다.

name 속성으로 appender의 이름을 지정한다.
class 속성으로 어떤 appender를 사용할지 지정한다.

> class 속성에는 다음과 같은 appender가 있다.
> - ConsoleAppender: 콘솔에 출력
> - FileAppender: 파일에 출력
> - RollingFileAppender: 파일에 출력 하되, 파일을 규칙에 따라서 나눠서 저장

---

### <encoder>

로그를 어떻게 출력할지 설정한다.

pattern 속성으로 출력할 로그의 형식을 지정한다.

```xml
<encoder>
    <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
</encoder>
```

---

### <filter>

로그를 어떻게 필터링할지 설정한다.

class 속성으로 어떤 필터를 사용할지 지정한다.
- ThresholdFilter: 로그 레벨을 지정해서 출력
- TurboFilter: 로그를 필터링해서 출력
- DynamicThresholdFilter: 로그 레벨을 동적으로 변경해서 출력
- LevelChangePropagator: 로그 레벨을 변경해서 출력

```xml
<filter class="ch.qos.logback.classic.filter.LevelFilter">
    <level>INFO</level>
    <onMatch>ACCEPT</onMatch>
    <onMismatch>DENY</onMismatch>
</filter>
```  
(이 필터는 INFO 레벨 로그만 출력)

---

## RollingFileAppender 관련 설정

### <rollingPolicy>

파일을 어떻게 나눌지 설정한다.

class 속성으로 어떤 정책을 사용할지 지정한다.
- TimeBasedRollingPolicy: 시간에 따라 파일을 나눔
- SizeAndTimeBasedRollingPolicy: 시간과 파일 크기에 따라 파일을 나눔
- FixedWindowRollingPolicy: 파일을 일정 개수만큼 나눔

### SizeAndTimeBasedRollingPolicy - <fileNamePattern>

파일 이름을 어떻게 지을지 설정한다.

```xml
<fileNamePattern>${user.home}/error.%d{yyyy-MM-dd}.%i.log.gz</fileNamePattern>
```  
(이 설정은 error.2022-01-01.0.log.gz, error.2022-01-01.1.log.gz, ... 형식으로 파일을 나눈다)

> %d{yyyy-MM-dd} - 날짜를 나타낸다.  
> %i - 파일을 나눌 때 사용하는 인덱스를 나타낸다.  
> .gz - 파일을 압축한다.  
> ${user.home} - 사용자의 홈 디렉토리를 나타낸다.

### SizeAndTimeBasedRollingPolicy - <maxFileSize>

파일을 얼마나 크게 나눌지 설정한다.

### SizeAndTimeBasedRollingPolicy - <maxHistory>

파일을 몇 개까지 나눌지 설정한다.

### SizeAndTimeBasedRollingPolicy - <totalSizeCap>

모든 파일의 크기가 얼마가 되면 삭제할지 설정한다.  
(모든 로그 파일의 크기의 합을 제한할 때 사용)

---

## <root>

어떤 로그를 출력할지 설정한다.

level 속성으로 어떤 레벨의 로그를 출력할지 지정한다.

```xml
<root level="INFO">
    <appender-ref ref="CONSOLE"/>
</root>
```  
(이 설정은 INFO 레벨 이상의 로그를 CONSOLE appender에 출력)

appender-ref 속성으로 어떤 appender를 사용할지 지정한다.

---

## <logger>

특정 패키지의 로그를 어떻게 출력할지 설정한다.

