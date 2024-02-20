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

랜선을 찾아가는 라우팅 기법은  
패킷에 있는 목적지 IP 주소를 이용하여 최단 경로를 선택해 진행한다.  
(다음 라우터를 결정한다)

라우팅을 거친 후에 해당 패킷은 L2로의 캡슐화 과정을 거치는데,  
이떄 출발지/목적지 MAC 주소는 라우터를 거칠 떄마다 변한다.

처음 송신자가 패킷을 보냈을 떄의 MAC 주소:  
내 컴퓨터의 MAC 주소 -> 내부망에 있는 게이트웨이의 MAC 주소

라우터에서 라우팅을 거치고 나서의 MAC 주소:  
현재 라우터의 MAC 주소 -> 다음 라우터의 MAC 주소

> 이떄 프레임(L2 데이터 단위)의 헤더 정보는  
> 라우터를 거칠 때마다 변하지만,  
> 
> 프레임 내에 있는 패킷의 정보는 변하지 않는다.  
> (IP 주소 포함)

결국 IP 주소를 이용해 다음 목적지의 MAC 주소가 결정된다.

---

> (내 생각)  
> MAC 주소는 기기마다 부여된 고유한 주소이고,  
> IP 주소는 위치?마다 부여된 고유한 주소라고 생각
> 
> 위치별로 주소가 어느정도 정해져 있기 때문에,  
> 라우팅이 가능하다  
> (IP 주소를 이용해 최적의 경로를 찾을 수 있다)
> 
> 만약 MAC 주소로 목적지 컴퓨터를 찾아야 한다면  
> 불가능 한건 아니지만, 매우 비효율적일 것이다.  
> (MAC 주소와 위치는 관계가 없기 때문)

---

### 결론

IP 주소는 최적의 경로를 찾아주는 라우팅을 하기 위한 주소이고 실질적인 이동은 MAC 주소를 이용한다.