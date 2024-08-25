로컬에서 테스트 서버와 연결된 DB에 접속하기 위해 ssh 터널링을 사용했다.

---

### 현재 상황

테스트 서버와 DB는 모두 AWS에 위치해 있다.  
(EC2, RDS)

이때 RDS의 IP는 퍼블릭 IP가 아닌 프라이빗 IP로 설정되어 있다.

> 퍼블릭 IP로 설정하면 더 편하겠지만,  
> 요금 문제가 있어서 그렇게 하지 않았다.

이때 RDS를 같은 VPC 내의 EC2에서 프라이빗 IP로 접속할 수 있다.

---

### ssh 터널링을 이용한 로컬 포트포워딩

EC2와 연결된 RDS에 접속하기 위해 ssh 터널링 & 포트 포워딩을 사용했다.

`ssh -L {local_port}:{RDS_private_IP}:{RDS_port} {EC2_username}@{EC2_public_IP}`

> -L 옵션은 로컬 포트 포워딩을 의미한다.

이 옵션을 통해  
로컬(클라이언트) 호스트의 지정된 포트(local_port)가  
지정된 호스트(RDS)로 전달되도록 지정한다.

> local과 RDS 사이에 EC2가 중간에서 터널링을 해주는 것이다.

---

### 스프링 데이터 소스 설정

이후 로컬에서 스프링을 실행할 때  
application.yml 파일에 다음과 같이 데이터 소스를 설정했다.

```yml
spring:
  datasource:
    url: jdbc:mysql://localhost:{local_port}/{DB_name}
    username: {DB_username}
    password: {DB_password}
```

> 여기서 DB_username과 DB_password는 RDS의 계정 정보이다.

