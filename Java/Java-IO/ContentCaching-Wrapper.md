# ContentCachingRequestWrapper & ContentCachingResponseWrapper

둘 다 `HttpServletRequestWrapper`와 `HttpServletResponseWrapper`를 상속받은 클래스로,  
request와 response의 정보를 캐싱해주는 클래스이다.

> 모든 정보를 캐싱해주는 것은 아니고,  
> 바디의 정보만 캐싱해준다.

---

## 기존 Request/Response body

기존에는 `HttpServletRequest`와 `HttpServletResponse`를 사용했을 때,  
바디의 정보를 읽어오기 위해서는 `request.getInputStream()` 또는 `response.getOutputStream()`을 사용했다.

이때, requestBody의 정보를 읽어오면,  
바디의 정보는 `InputStream`에 저장되어 있기 때문에,  
한 번 읽어오면, 다시 읽을 수 없다.

> HttpServletRequest 객체에서, body를 한번만 읽을 수 있는 이유  
> (스트림 형태로 제공되는 이유)
> 
> HTTP 요청 바디의 크기가 클 수도 있기 때문에,  
> 이를 스트림으로 처리하면 메모리를 효율적으로 사용할 수 있다.
> 
> 그리고 `content-type` 헤더의 value에 따라,  
> request body를 다르게 처리할 수 있기 때문이다.

---

## ContentCachingRequestWrapper의 body 캐싱

기존 InputStream을 이용해 body를 읽을 때,  
내부적으로 ByteArrayOutputStream을 이용해 body를 캐싱한다.

외부에서 request.getInputStream()을 호출하면,  
ContentCachingInputStream 객체를 반환한다.  
(request의 inputStream을 이용해 생성 된다)

ContentCachingInputStream의 read 메서드가 호출되면,  
기존 inputStream의 read 메서드를 호출하고,  
읽은 바이트를 ByteArrayOutputStream에 저장한다.

```java
private class ContentCachingInputStream extends ServletInputStream {

    private final ServletInputStream is;

    private boolean overflow = false;

    public ContentCachingInputStream(ServletInputStream is) {
        this.is = is;
    }

    @Override
    public int read() throws IOException {
        int ch = this.is.read();            // 기존 inputStream의 read 메서드 호출
        if (ch != -1 && !this.overflow) {
            if (contentCacheLimit != null && cachedContent.size() == contentCacheLimit) {
                this.overflow = true;
                handleContentOverflow(contentCacheLimit);
            } else {
                cachedContent.write(ch);    // 읽은 바이트를 ByteArrayOutputStream에 저장
            }
        }
        return ch;
    }
}
```

> 여기서 ContentCachingRequestWrapper 객체를 생성할 때,  
> requestBody를 캐싱할 수 있는 최대 크기를 지정할 수 있다.
> 
> 최대 크기를 넘어서서 read 메서드가 호출되면,  
> ByteArrayOutputStream에 캐싱 하지 않고, 그대로 반환한다.

---

## ContentCachingResponseWrapper의 body 캐싱

기존 OutputStream을 이용해 body를 쓸 때,  
내부적으로 ByteArrayOutputStream을 이용해 body를 캐싱한다.

외부에서 response.getOutputStream()을 호출하면,  
ResponseServletOutputStream 객체를 반환한다.

ResponseServletOutputStream의 write 메서드가 호출되면,  
기존 outputStream의 write 메서드를 호출하지 않고,  
읽은 바이트를 ByteArrayOutputStream에 저장한다.

```java
private class ResponseServletOutputStream extends ServletOutputStream {

    private final ServletOutputStream os;

    public ResponseServletOutputStream(ServletOutputStream os) {
        this.os = os;
    }

    @Override
    public void write(int b) throws IOException {
        content.write(b); // 읽은 바이트를 ByteArrayOutputStream에 저장
    }
}
```

> ContentCachingResponseWrapper를 이용할 때는,  
> 마지막에 copyBodyToResponse 메서드를 호출해야 한다.
> 
> 이 메서드를 통해 캐싱된 body를 response의 outputStream에 쓴다.  
> (만약 호출하지 않는다면 response의 body가 비어있는 상태로 전달된다)

---

