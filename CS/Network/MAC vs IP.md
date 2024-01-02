# MAC vs IP

MAC 주소 
- `LAN Card`의 주소(디바이스 마다 할당된 물리적인 주소)
- 이더넷을 이용하기 위해 사용

IP 주소 
- `LAN Card에 연결되어 있는 회선(랜선)`의 주소(논리적인 주소)
- 라우팅을 하기 위해 사용

> 라우팅: 네트워크에서 경로를 선택하는 프로세스  
> 이더넷: LAN(근거리 통신망) 구축을 위해 장치를 연결하는 데 널리 사용되는 네트워킹 프로토콜

같은 컴퓨터에서 위치가 달라지면(다른 인터넷망에 접속하면),  
IP 주소는 변하지만, MAC 주소는 변하지 않는다.

## 컴픁터끼리 통신하는 과정

통신을 할 때, MAC 주소와 IP 주소 모두 쓰인다.  

랜선을 찾아가는 라우팅 기법은 패킷에 포함된 IP 주소(즉, 회선의 위치)를 추적해서 최단 경로를 선택해 진행한다.  
IP 주소는 논리적인 주소이기 때문에 이 IP 주소에서 목적지 IP 주소로 네트워크를 추적해서 패킷을 보낸 뒤 그곳에서 그 IP에 등록된 MAC 주소로 변환되어 그 컴퓨터로 패킷을 전송하게 된다. 

> 만약 MAC 주소만 가지고 통신을 한다면, 매우 비효율적일 것이다.  
>
> (MAC 주소만을 이용해) 특정 웹 서버를 찾는다고 가정하면,  
> ISP내의 모든 라우터들은 전세계 모든 서버들의 MAC 주소를 다 가지고 있어야 한다.  
> -> 각각의 MAC 주소에 대해 라우팅 해줘야 한다.  
> (MAC 주소는 변경 불가능한 물리적인 주소이기 때문)

---

## 결론

IP 주소는 최적의 경로를 찾아주는 라우팅을 하기 위한 주소이고 실질적인 통신은 MAC 주소를 이용한다.