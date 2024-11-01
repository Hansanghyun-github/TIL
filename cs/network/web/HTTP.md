# HTTP(HyperText Transmission Protocol)

하이퍼텍스트 전송 프로토콜(HTTP)는 HTML 문서와 같은 리소스들을 가져올 수 있도록 해주는 프로토콜

> HTML(HyperText Markup Language)
> 
> 웹을 이루는 가장 기초적인 구성 요소로, 웹 콘텐츠의 의미와 구조를 정의할 때 사용  
> (HyperText란 웹 페이지를 다른 페이지로 연결하는 링크를 말한다)

HTTP는 무상태 프로토콜이며, 서버가 두 요청 간에 어떠한 데이터(상태)도 유지하지 않는다.

## 웹의 리소스 식별 - URL

```scheme://[userinfo@]host[:port][/path][?query][#fragment]```  
([] 는 생략 가능)

```https://www.google.com/search?q=hello&hl=ko```

스키마 (https) - 리소스를 요청하는데 사용하는 프로토콜  
호스트명 (www.google.com) - 도메인 네임 혹은 IP 주소  
포트 번호 (80)  
리소스 경로 (/search)  
query (?q=hello&hl=ko) - key=value 형태, ?로 시작, &로 추가 가능

---

## 웹 브라우저

웹 브라우저란 인터넷을 통해 웹 페이지를 탐색하고 표시하는 소프트웨어이다.

웹 페이지를 표시하기 위해,  
브라우저는 페이지의 HTML 문서를 가져오기 위한 요청을 전송한 뒤,

파일을 구문 분석하여 실행해야 할 스크립트 그리고  
페이지 내 포함된 하위 리소스들(보통 이미지와 비디오)을 잘 표시하기 위한 레이아웃 정보(CSS)에 대응하는 추가적인 요청들을 가져온다.

그런 뒤에 브라우저는 완전한 문서인 웹 페이지를 표시하기 위해 그런 리소스들을 혼합한다.  
브라우저에 의해 실행된 스크립트는 이후 단계에서 좀 더 많은 리소스들을 가져올 수 있으며 브라우저는 그에 따라 웹 페이지를 갱신하게 된다.

---

## HTTP 특징

### 1. HTTP는 확장 가능하다.

HTTP 헤더는 HTTP를 확장하고 실험하기 쉽게 만들어주었다.  
클라이언트와 서버가 새로운 헤더의 시맨틱에 대해 간단한 합의만 한다면, 언제든지 새로운 기능을 추가할 수 있다.

### 2. HTTP는 상태가 없다, but Session은 있다

HTTP는 상태를 저장하지 않는다(Stateless).  
(동일한 연결 상에서 연속하여 전달된 두 개의 요청 사이에는 연결고리가 없다)

하지만, HTTP의 핵심은 상태가 없는 것이지만 HTTP 쿠키는 상태가 있는 세션을 만들도록 해준다.  
헤더 확장성을 사용하여, 동일한 컨텍스트 또는 동일한 상태를 공유하기 위해 각각의 요청들에 세션을 만들도록 HTTP 쿠키가 추가된다.

---

## HTTP 버전 별 특징

### HTTP/0.9

> HTTP 초기 버전에는 버전 번호가 없었다. HTTP/0.9는 이후 버전과 구별하기 위해 0.9로 불리게 됐다.

request는 단일 라인으로 구성되며 리소스에 대한 경로로, 가능한 메서드는 GET이 유일하다.  
서버에 연결되면 프로토콜, 서버 및 포트가 필요하지 않으므로 전체 URL은 포함되지 않았다.

```GET /mypage.html```

response 또한 매우 단순하다.  
파일 내용 자체로만 구성되아있다.

```html
<html>
    very simple page
</html>
```

---

### HTTP/1.0

- 각 요청 안에 버전 정보가 포함되어 전송된다(HTTP/1.0 이 GET 라인에 붙은 형태).  
- 상태 코드 라인 또한 응답의 시작 부분에 붙어 전송된다.  
  브라우저가 요청에 대한 성공과 실패를 알 수 있고 그 결과에 대한 동작(예, 특정 방법으로 로컬 캐시를 갱신하거나 사용)을 할 수 있게 되었다.
- HTTP 헤더 개념은 요청과 응답 둘 다 도입되어, 메타데이터 전송이 가능해졌고, 프로토콜이 극도로 유연하고 확장성이 높아졌다.  
- Content-Type 덕분에, 일반 HTML 파일들 외에 다른 문서들을 전송할 수 있게 되었다.

Request
```
GET /mypage.html HTTP/1.0
User-Agent: NCSA_Mosaic/2.0 (Windows 3.1)
```

Response
```
200 OK
Date: Tue, 15 Nov 1994 08:12:31 GMT
Server: CERN/3.0 libwww/2.17
Content-Type: text/html
<HTML>
A page with an image
  <IMG SRC="/myimage.gif">
</HTML>

```

---

> HTTP/1.0의 아쉬운 점
> 
> 1 Request/Response 1 Connection  
> 커넥션 하나당 요청/응답을 하나만 주고받을 수 있다.  
> (커넥션 맺을 때마다 TCP 3-way handshaking 해야 함)

### HTTP/1.1

- 지속적인 연결을 통해 오버헤드가 감소 되 시간이 절약되었다.  
  단일 원본 문서 내로 포함된 리소스들을 표시하기 위해 더 이상 여러 번 연결을 열 필요가 없기 때문이다.
- 파이프라이닝을 추가하여, 첫번째 요청에 대한 응답이 완전히 전송되기 전에 두번째 요청 전송을 가능케 하여, 통신 지연 시간이 단축되었다.
- 청크된 응답도 지원된다. 
- 추가적인 캐시 제어 메커니즘이 도입되었다.
- 언어, 인코딩 혹은 타입을 포함한 컨텐츠 협상이 도입되어, 클라이언트와 서버로 하여금 교환하려는 가장 적합한 컨텐츠에 대한 합의를 할 수 있습니다. 
- Host 헤더 덕분에, 동일 IP 주소에 다른 도메인을 호스트하는 기능이 서버 배치가 가능해졌습니다.

Request
```
GET /en-US/docs/Glossary/Simple_header HTTP/1.1
Host: developer.mozilla.org
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://developer.mozilla.org/en-US/docs/Glossary/Simple_header
```

Response
```
200 OK
Connection: Keep-Alive
Content-Encoding: gzip
Content-Type: text/html; charset=utf-8
Date: Wed, 20 Jul 2016 10:55:30 GMT
Etag: "547fa7e369ef56031dd3bff2ace9fc0832eb251a"
Keep-Alive: timeout=5, max=1000
Last-Modified: Tue, 19 Jul 2016 00:59:33 GMT
Server: Apache
Transfer-Encoding: chunked
Vary: Cookie, Accept-Encoding

(content)
```

--- 

> HTTP/1.1의 아쉬운점  
> 
> 1. Head Of Line Blocking(맨 처음 요청이 실패하면, 그 뒤의 요청들은 blocking 된다) - 파이프라이닝으로 인해 발생
> 2. 헤더의 중복

> 몇 년에 걸쳐, 웹 페이지는 더욱 복잡해졌습니다.  
> 일부는 그 자체로 애플리케이션이기도 했습니다.  
> 더 많은 시각적 미디어가 표시되고 상호작용을 위한 스크립트 코드의 양과 크기도 증가했습니다.  
> 훨씬 더 많은 HTTP 요청을 통해, 많은 데이터가 전송되었고, 이를 통해 HTTP/1.1 연결에 복잡성과 오버헤드가 많이 발생했습니다.

### HTTP/2.0

HTTP/2.0의 목적: HTTP/1.1의 성능을 높이자!

- HTTP 메시지 전송 방식의 변화(텍스트 -> 바이너리 프레임)  
  속도가 향상되고, 오류율이 줄었다.
- 요청과 응답의 다중화(Multiplexing)  
  (요청/응답이 바이너리 프레임으로 쪼개졌기 때문에 메시지 간의 순서가 사라짐)  
  HOL Blocking 제약을 없앴다.
- 헤더를 압축한다. 요청 집합 간에 유사한 경우가 많으므로, 전송된 데이터의 중복과 오버헤드가 제거된다.  
  (헤더에 대해 허프만 코딩으로 인코딩 시간도 줄였다)
- 서버 푸시 기능(클라이언트가 요청할 데이터를 미리 보내주는 것)

> 다중화(Multiplexing)
> 
> 기존 1.1에선 html, css, js 파일을 따로 요청했다.  
> (지속적인 연결을 하더라도, html 파일을 받아야 css 파일을 받을 수 있었다)
> 
> 하지만 HTTP/2.0에선  
> 하나의 연결에서 `동시에` 여러 파일을 요청할 수 있다.  
> (각 파일을 프레임으로 쪼개어 보내기 때문에, 순서가 보장되지 않는다)

> HTTP/2.0의 바이너리 프레임과 헤더 압축
> 
> 기존 HTTP/1.1에선  
> 데이터가 읽기 쉬운 텍스트 데이터로 전송된다.
> 
> 하지만 HTTP/2.0에선  
> 데이터가 바이너리 프레임으로 전송된다.  
> 이떄 각각의 프레임은 헤더와 데이터로 구성되어 있다.  
> 그리고 헤더 프레임은 헤더를 압축하여 전송한다.
> 
> 헤더 압축은 HPACK 알고리즘을 사용한다.  
> (기존에 많이 사용하는 헤더를 테이블로 만들어, 헤더를 인덱스로 전송한다)  
> (헤더가 중복되는 경우, 인덱스로 전송하면 된다)
> 
> 헤더 압축을 하면서  
> 보내는 데이터의 양이 줄어들어, 속도가 향상된다.
> 

---

> HTTP/2.0의 아쉬운 점
> 
> TCP HOL Blocking(TCP는 순서를 매우 중요하게 생각한다)  
> 특정 패킷이 손실되면, 그 뒤에 패킷들도 전부 Blocking 된다.  
> (뒤의 패킷들이 손실된 패킷과 없을지라도)
> 
> 그리고 HTTPS 를 사용하려면,  
> TCP 연결 이후에 TLS 연결을 한번 더 해줘야 했다. (오버헤드)
> 
> -> 이건 TCP 자체의 문제다

> 기존 HTTP/2.0에선 어플리케이션 레이어에서의 순서를 보장하지 않는다.  
> (프레임을 쪼개어 보내기 때문에, 순서가 보장되지 않는다)
> 
> 하지만 TCP는 순서를 중요하게 생각한다.  
> (특정 패킷이 손실되면, 그 뒤의 패킷들도 전부 Blocking 된다)
> 
> 이를 해결하기 위해, HTTP/3.0이 나왔다.

### HTTP/3.0

(구글에서 아예 전송 계층 프로토콜을 만들었다 - QUIC)

QUIC 위에서 돌아가는 HTTP이다.  
(HTTP/3부터는 TLS(HTTPS) 기본 적용)

- 독립 스트림(요청별로 다른 스트림을 사용한다)  
  -> 앞 패킷이 손실되도, 그와 관련있는 뒷 순서 패킷만 Blocking 된다.  
  (관련 없는 패킷은 Blocking 되지 않는다)
- RTT 최소화(TCP 연결 + TLS 연결 한번에)  
  처음 연결에 QUIC 연결로 TLS까지 전부 연결한다.  
  그리고 각 연결마다 connection ID를 부여  
  -> 클라이언트의 IP 주소가 변해도 QUIC 연결 없이 바로 데이터를 주고받을 수 있다.  
  (클라이언트가 이 ID를 캐싱까지 한다)

