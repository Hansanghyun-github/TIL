# Socket, ServerSocket

> 둘 다 TCP/IP 통신을 기반으로 한다.  
> (UDP 통신 기반 소켓은 따로 있음 DatagramSocket)

## ServerSocket

서버 측 소켓을 담당하는 클래스
클라이언트의 연결 요청을 수락하고, 클라이언트와의 통신을 담당한다.
특정 포트에서 클라이언트의 연결 요청을 수신하는 데 사용된다.

### 서버 소켓 생성

```ServerSocket server = new ServerSocket(portNumber,queueLength);```

ServerSocket 생성자를 호출하면 생성자의 매개변수에는 portNumber 와 queueLength를 가진 소켓을 생성한다.  
- queueLength : 서버에 연결되기를 기다리는 클라이언트의 최대 개수  
- portNumber : 포트번호로 클라이언트가 서버 컴퓨터에서 서버 애플리케이션을 찾기 위해 필요.  

### 클라이언트 소켓과 통신

```Socket socket = serverSocket.accept()```

서버는 클라이언트가 연결을 시도하기를 기다린다.  

accept() 메소드는 클라이언트와 연결이 되면 새로운 Socket 객체를 생성하여 반환한다.  
이 새로운 Socket 객체를 통해 서버는 클라이언트와 상호작용할 수 있다.

이전 단계에서의 portNumber에 연결된 소켓은 다른 클라이언트의 연결을 위하여 그냥 두어야한다

(accept() 메서드에 의해 생성된 소켓의 포트 번호는 서버 소켓의 포트 번호와 같다)

---

## Socket

클라이언트 소켓을 담당하는 클래스

클라이언트가 서버에게 요청을 보내거나 서버로부터 응답을 받기 위해 사용된다.

특정 호스트의 특정 포트에 연결할 수 있도록 해준다.

### 클라이언트 소켓의 생성

```Socket socket = new Socket(String host_IP_address, int port_number);```

네트워크 통신을 진행 할 서버의 IP 주소, 포트 번호를 생성자의 파라미터로 넘겨야 한다.

이때 해당 IP주소/포트번호 유효하지 않다면(해당 서버가 존재하지 않는다면)  
IOException이 발생한다.

---

## 클라이언트-서버 소켓을 이용한 통신

클라이언트 소켓은 `getInputStream()`, `getOutputStream()` 메서드를 가지고 있다.

위 메서드는 InputStream/OutputStream을 반환하는데,  
이들을 이용해 데이터를 주고받는다.

---

둘다 사용을 마치면 close() 메서드를 호출해 닫아줘야 한다.