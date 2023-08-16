형식

#### ERROR, WARN 내용

`발생이유`:

`해결방법`:

---

#### 2023-08-06 18:47:12.758  WARN 2272 --- [l-1 housekeeper] com.zaxxer.hikari.pool.HikariPool        : HikariPool-1 - Thread starvation or clock leap detected (housekeeper delta=1m6s828ms665µs608ns).

`발생이유`: 클라이언트의 request를 스레드 풀에서 스레드를 할당받아서 서버를 돌려야 하는데,  스레드가 부족함

ec2 모니터링을 보니, 이때 CPU 가동률이 100% 가까이였음. cpu가 스왑하느라 바빠서 서버쪽 스레드풀에 스레드 전달을 못해줌

`해결방법`: cpu나 메모리 성능을 높여야지

---

#### 2023-08-06 18:49:18.985 ERROR 2272 --- [nio-8080-exec-1] o.a.c.c.C.[Tomcat].[localhost]           : Exception Processing ErrorPage[errorCode=0, location=/error]
#### org.apache.catalina.connector.ClientAbortException: java.io.IOException: Broken pipe

`발생이유`: Receiver 에서 송신 받은 데이터를 제때 처리하지 못하는 상황(네트워크가 느리거나 CPU 가 max 인 경우)에서 Sender 가 계속 보내는 경우 발생한다.

`해결방법`: request 후 response 기다리기, 그냥 exception 무시하기, 중복요청막기

---

#### 2023-08-06 19:24:28.655 ERROR 2272 --- [onnection adder] com.zaxxer.hikari.pool.HikariPool        : HikariPool-1 - Error thrown while acquiring connection from data source
#### com.mysql.cj.jdbc.exceptions.CommunicationsException: Communications link failure
#### The last packet successfully received from the server was 30,943 milliseconds ago. The last packet sent successfully to the server was 33,417 milliseconds ago.

`발생이유`: 일반적으로 데이터베이스에 대한 연결을 설정하거나 유지하는 데 문제가 있을 때

> DB를 잘못세팅했을때도 있지만, 대부분 네트워크 문제, 나는 ec2 인스턴스가 꺼져서 그런듯

`해결방법`: 네트워크 상태 잘 확인하고, 로깅 잘해야함

---


