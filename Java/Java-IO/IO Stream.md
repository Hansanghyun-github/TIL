자바의 Socket 클래스는 데이터를 InputStream과 OutputStream을 이용해 주고받는다.

---

## InputStream & OutputStream

### InputStream

다른 매체로부터 바이트로 데이터를 읽을 때 사용되는 스트림

```read()``` - 단일 바이트 반환(없으면 -1)  
```readAllBytes()``` - 스트림의 모든 바이트들을 반환 (byte[])

### OutputStream

다른 매체에 바이트로 데이터를 쓸 때 사용되는 스트림

```write(byte b)``` - 바이트 한 개만 쓴다  
```write(byte[] bytes)``` - bytes 전체를 쓴다(효율적)

### flush() 메서드

이 메서드를 사용하면 버퍼가 가득 차지 않았어도 강제로 버퍼의 내용을 받는다/전송한다.

> Stream은 동기(synchronous)로 동작하기 때문에 버퍼가 찰 때까지 기다리면  
> 데드락(deadlock) 상태가 되기 때문에 flush로 해제해야 한다.

### close() 메서드

스트림 사용이 끝나면 항상 close() 메서드를 호출하여 스트림을 닫는다.
 
> 장시간 스트림을 닫지 않으면 파일, 포트 등 다양한 리소스에서 누수(leak)가 발생한다.

> try-with-resources (자바 9 이상)
> 
> try 옆의 괄호에 try 이후에 닫을 변수들을 넣으면,  
> 자동으로 close 된다.

---

## 필터스트림(FilterStream)

전달하는/받은 데이터를 필터링할 때 사용되는 스트림

필터스트림은 바이트를 다른 데이터 형식으로 변환하거나, (Reader/Writer)  
빠르게 읽기위해 사용된다. (BufferedStream)

### Buffered Input/Output Stream

내부적으로 버퍼링을 통해 데이터를 임시로 저장한다.  
이는 입출력 작업을 수행할 때 데이터를 한 번에 큰 덩어리로 처리함으로써 입출력 속도를 향상시킨다.

> 작은 단위로 데이터를 읽으면/쓰면 그때마다 시스템콜이 발생 해 오버헤드가 커지기 떄문이다.

### Reader/Writer

자바의 기본 문자열은 UTF-16 유니코드 인코딩을 사용한다.  
문자열이 아닌 바이트 단위로 처리하려니 불편하다.  
그리고 바이트를 문자(char)로 처리하려면 인코딩을 신경 써야 한다.  
reader, writer를 사용하면 입출력 스트림을 바이트가 아닌 문자 단위로 데이터를 처리하게 된다.

> InputStream/OutputStream은 데이터를 바이트 단위로 읽는데/쓰는데,  
> 이를 편하게 읽기/쓰기 위해(문자 단위로 읽기/쓰기 위해),  
> Reader/Writer를 사용한다.

---

> 이 외에도 FilterStream은 압축, 암호화 등에도 쓰인다.  
> (결국 받은/전달하는 데이터를 변환하는 것이 필터의 핵심)

> 코테에서는 입력 값을 문자열 단위로 빠르게 읽기 위해 BufferedReader를 사용하는 것 같다.  
> ```InputStreamReader isr = new InputStreamReader(System.in);```  
> ```BufferedReader br = new BufferedReader(isr);```

