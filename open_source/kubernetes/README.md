### pod

pod - 도커의 여러 컨테이너들을 관리하는 하나의 단위

> 쿠버네티스에서 하나의 pod는,  
> 컨테이너를 하나만 가질 수 있고,  
> 여러 개의 컨테이너를 가질 수도 있지만,  
> 이 컨테이너들은 하나의 pod 내에서 동작한다.

---

### multipod

여러 개의 pod를 관리하는 단위

multipod 내 여러 컨테이너들은 같은 pod 이름 & IP를 가진다.

> 쿠버네티스 리스트를 띄웠을 때,  
> multipod는 runnings pod의 개수만큼 나타난다.

그리고 `kubectl` 명령어를 입력할 때도,  
mutlipod는 -c 옵션을 통해 특정 컨테이너를 지정할 수 있다.

일반적인 `kubectl` 명령어  
`kubectl get pods`

multipod에서 특정 컨테이너를 지정하는 `kubectl` 명령어  
`kubectl get pods -c <CONTAINER_NAME>`