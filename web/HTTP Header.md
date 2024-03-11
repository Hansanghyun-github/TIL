# HTTP 헤더(Header)

HTTP 전송에 필요한 모든 부가정보(Metadata)

헤더 구조

{field-name}: {field-value}
(: 옆에 띄어쓰기 할 수도 있고 안 할 수도 있음)

---

## 헤더 분류

### General 헤더

메시지 전체에 적용되는 정보

### Request 헤더

요청 정보

### Response 헤더

응답 정보

### Representation 헤더

메시지 바디(표현 데이터)를 해석할 수 있는 정보

---

## Representation 헤더 종류

### Content-Type: 표현 데이터의 형식 설명

미디어 타입, 문자 인코딩

`text/html; charset=UTF-8`  
`application/json`  
`image/png`

### Content-Encoding: 표현 데이터 인코딩

표현 데이터를 압축하기 위해 사용

> 데이터 전달하는 쪽에서 압축 후 인코딩 헤더 추가
> 데이터를 읽는 쪽에서 인코딩 헤더의 정보로 압축 해제

`gzip`, `delfate`, `identity`

### Content-Language: 표현 데이터의 자연 언어

`ko`, `en`, `en-US`

### Content-Length: 표현 데이터의 길이

바이트 단위

> 응답에서 잔송 방식으로 Transfer-Encoding을 사용하면 Content-Length를 사용하면 안됨

---

## Request 헤더 - 협상(Accept) 헤더

클라이언트가 선호하는 표현(Representation)을 요청한다.

Accept: 클라이언트가 선호하는 미디어 타입 전달
Accept-Charset: 클라이언트가 선호하는 문자 인코딩 전달
Accept-Encoding: 클라이언트가 선호하는 압축 인코딩 전달
Accept-Language: 클라이언트가 선호하는 자연 언어 전달

### 협상과 우선순위

> 선호한다는 걸 요청해도, 해당 서버가 선호하는 방식이 지원이 안될 수 있다.  
> -> 다른 것들의 우선순위를 정한다.

1. Quality Values(q) 값 사용  
0~1 클 수록 높은 우선순위 (생략하면 1)  
`Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7`

2. 구체적인 것이 우선  
`Accept: text/*, text/plain, text/plain;format=flowed, */*`

---

## Representation 헤더 - 전송 방식

### Content-Length: 단순 전송(그냥 데이터의 길이)

### Content-Encoding: 압축 전송

### Transfer-Encoding: 분할 전송

여기서는 Content-Length가 들어가면 안된다.

### Range, Content-Range: 분할 전송

---

(요청)

From: 유저 에이전트의 이메일 정보

Referer: 이전 웹 페이지 주소  
(리다이렉트 했을 때, 이전 웹 페이지 주소)

User-Agent: 유저 에이전트 애플리케이션 정보  
(웹 브라우저)

Host: 요청한 호스트 정보(도메인)
(하나의 서버가 여러 도메인을 처리해야 할 때 사용)

Location:   
3XX 응답 결과에 이 헤더가 있다면 자동 리다이렉트  
201 응답 결광 이 헤더가 있다면, 요청에 의해 생성된 URI를 의미한다.

(응답)

Server: 요청을 처리하는 오리진 서버의 SW 정보

Data: 데이터가 생성된 날짜

Retry-After: 유저 에이전트가 다음 요청을 하기까지 기다려야 하는 시간  
(503 응답 헤더에 실린다)

---

## 쿠키 관련 헤더

`Set-Cookie`: 서버에서 보내는 쿠키

`Cookie`: 클라이언트에서 보내는 쿠키  
(모든 요청에 쿠키가 자동 포함된다)

### 쿠키의 생명주기

`Set-Cookie`에서 expires(만료 날짜)나 max-age(만료 남은 시간)를 보내면 영속 쿠키  
보내지 않으면 세션 쿠키(브라우저 종료시까지만 유지)

### 쿠키의 도메인, 경로

`Set-Cookie`에서 domain을 보내면 명시한 도메인에 요청 보낼 때만 쿠키를 보낸다.  
(생략하면 현재 도메인)

`Set-Cookie`에서 path를 보내면 명시한 경로에 요청 보낼 때만 쿠키를 보낸다.  
(일반적으로 루트 '/' 경로)

---

## 캐시 관련 헤더

`Cache-Control` 헤더를 통해 캐시에 유효 시간을 설정할 수 있다.

캐시 유효 시간이 지나면, 해당 데이터를 서버에 다시 요청하고, 캐시를 갱신한다.

`Cache-Control`의 값    
max-age - 초 단위

### 캐시 된 데이터 검증 - 조건부 요청

케시 유효 시간이 지나 클라이언트가 다시 데이터를 요청했을 때,  
서버에서는 해당 데이터가 변경됐을 수도 있다.

그리고 만약 안바꼈다면, 캐시된 데이터를 그냥 쓰는게 효율적이다.
(중복 데이터 또 받는 시간은 아깝다)

이제 서버는 데이터를 보낼 때  
`Last-Modified` 헤더를 통해 해당 데이터가 마지막에 수정된 시간을 알려준다.

그리고 캐시 유효 시간이 지났을 때, 클라이언트는  
`if-modified-since` 헤더를 통해, 현재 캐싱이 만료된 데이터의 마지막 수정된 시간을 확인한다.  

만약 변경되지 않았다면, 서버는 `304 Not Moodofied`를 응답으로 보낸다(데이터 없음 - 실용적)  
변경 됐다면, 데이터를 포함하여 `200 OK`를 응답을 보낸다.

> `if-modified-since` & `Last-Modified` 방식의 아쉬운 점
> 
> 만약 데이터가 수정된 날짜는 갱신됐지만,  
> 데이터 자체에는 변화가 없다면?
> 
> -> 데이터에 이름을 붙이자(ETag)
> (ETag가 같다면 원본 유지, 다르면 다시 받기)

서버가 데이터를 보내면서 `Last-Modified` 대신 `ETag`를 보낸다면  
클라이언트는 데이터와 ETag를 저장  
그리고 캐시 유효 시간이 만료되면, `If-None-Match`를 보낸다.
(이걸 보고 변경됐는지 확인한다)

> 데이터의 수정 날짜는 `if-modified-since` 요청 & `Last-Modified` 응답  
> 데이터의 해시 값은 `If-None-Match` 요청 & `etag` 사용
> 
> (`If-Unmodified-Since`, `If-Match`도 있음)



---

### 프록시 캐시

웹 브라우저와 원(origin) 서버 사이에 프록시 서버가 있을 수 있다.

이 프록시 서버들에게 어떻게 캐싱할지 지정해주는 헤더들이 있다.

> 여기서 웹 브라우저에 캐시를 private 캐시라 하고  
> 프록시 서버의 캐시를 public 캐시라 한다.

`Cache-Control` 지시어
public - 프록시 서버에서 캐싱 가능
private - 웹 브라우저(클라이언트)만 캐싱 가능(default)
s-maxage - 프로시 캐시에 적용되는 max-age

---

### 캐시 무효화

`Cache-Control`  
no-cache - 데이터는 캐시해도 되지만, 항상 원 서버에 검증하고 사용해야 함  
no-store - 캐시 금지  
must-revalidate - 캐시 만료후 최초 조회시에 원 서버에서 검증해야 함
(원 서버에 접근 실패시 `504 Gateway Timeout`)

> 원 서버와 프록시 서버 사이의 네트워크가 단절됐을 때
> 
> no-cache는 캐시 서버 설정에 따라서,  
> 프록시 서버에 있는 캐시로 응답할 수도 있다.
> 
> 하지만 must-revalidate는 504 응답을 보낸다.

> 그냥 민감한 정보는 위 3개 다 써놓자

---

## Keep-Alive

하나의 TCP 연결을 통해 여러 개의 HTTP 요청과 응답을 주고받을 수 있도록 해주는 기능

HTTP/1.0에서 지속적인 연결 기능을 지원하기 위해 Connection, Keep-Alive 헤더가 등장했다.

> Connection: `Keep-Alive`(계속 연결), `close`(닫는다)  
> Keep-Alive: `timeout={t}, max={m}`  
> (송신자가 연결에 대한 타임아웃과 요청 최대 개수를 어떻게 정했는지에 대해 알려준다)

HTTP/1.1부터는 기본적으로 지속적인 연결을 지원하기 때문에, Keep-Alive 헤더는 쓰이지 않는다.  
(Connection 헤더 만으로 연결을 유지하거나 닫는다(default는 Keep-Alive))

HTTP/2.0부터는 자동으로 지속적인 연결을 보장해 Connection, Keep-Alive 헤더 둘 다 쓰이지 않는다.