### Nginx 설정 파일 위치

`/etc/nginx/nginx.conf` 위치에 nginx 설정 파일이 있다.

<img src="../img/nginx_1.png" width="500">

위 코드를 통해 nginx 로그 파일을 설정할 수 있다.  
(http 블록 안에 있음)

---

### Nginx 로그 파일 설정

이때 error.log 에는 디버그 모드를 설정할 수 있다.

`error_log /var/log/nginx/error.log debug;`  
(디버그 모드로 설정하면 대량의 정보가 기록되어 성능이 저하됨을 유의하자)

> access log에는 디버그 모드를 설정할 수 없다.
>
> access log의 목적  
> 클라이언트 요청에 대한 간단한 기록을 유지하는 것

```
events {
    debug_connection 192.168.1.1;
    debug_connection 192.168.10.0/24;
}
```  
events 블록 안에 특정 IP를 `debug_connection`으로 설정해주면,  
해당 IP 대해서만 디버그 모드를 세팅할 수 있다.

---













