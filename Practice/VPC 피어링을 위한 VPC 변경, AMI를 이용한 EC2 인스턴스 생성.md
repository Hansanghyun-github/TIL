### 문제 발생 - AWS Data Transfer 요금 왜 나옴?

-> public IP를 이용해서 EC2끼리 통신하면 데이터 통신한 만큼 요금 나온다고 한다.  
(지역, AZ 같더라도)

> 데이터 통신을 public IP를 이용한 이유  
> -> 어떻게든 요금 아끼려고 프리티어 다계정을 이용해 EC2 인스턴스 여러개 썼다.  
> (dev, monitoring, test 계정들)

-> VPC peering을 이용하면 요금을 없앨 수 있다고 한다.  
(이걸 쓰면 public IP가 아닌 private IP로 통신 가능하다)

### VPC 피어링을 위한 CIDR 설정

그런데 VPC peering을 하려면 CIDR이 달라야 한다고 한다.  
(CIDR: 서브넷팅을 위해(IP 주소 효율적으로 사용하기 위해))

> 문제는 나는 EC2 만들때 VPC 설정을 기본으로 해서, 각각의 계정들의 인스턴스의 VPC CIDR이 다 같았다.

결국 새로 VPC를 생성해야 했다.

---

### VPC 피어링

새로 VPC를 생성하고, VPC 피어링을 했다.

---

