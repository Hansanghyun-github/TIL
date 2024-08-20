# cgroup을 이용한 리소스 제한

## cgroup이란?

cgroup은 리눅스 커널의 기능 중 하나로, 프로세스 그룹에 대한 리소스 사용량을 제한하는 기능을 제공한다.  

cgroup은 리소스 제한 기능을 그룹 단위로 제공하기 때문에, 여러 프로세스를 그룹으로 묶어서 리소스 제한을 할 수 있다.

---

## cgroup 실습

cgroup을 이용해 특정 프로그램의 CPU 사용량을 제한하는 실습을 진행해보자.

> 현재 테스트하는 환경은 ubuntu 20.04이다.  
> (cgroup-v2를 사용하고 있다)

### cgroup 마운트 확인

먼저 cgroup이 마운트 되어 있는지 확인한다.

```bash
mount -l | grep cgroup
# cgroup2 on /sys/fs/cgroup type cgroup2 (rw,nosuid,nodev,noexec,relatime)
```

위와 같이 출력되면 cgroup이 마운트 되어 있는 것이다.

### cgroup 컨트롤러 확인

`/sys/fs/cgroup/cgroup.controllers` 파일을 통해 cgroup이 사용하는 컨트롤러를 확인할 수 있다.

```bash
cat /sys/fs/cgroup/cgroup.controllers
# cpuset cpu io memory pids
```

위와 같이 출력되면 cgroup이 사용하는 컨트롤러로 `cpuset`, `cpu`, `io`, `memory`, `pids`가 있다.  
-> 이 말은 cgroup을 통해 CPU, 메모리, I/O, 프로세스 개수 등을 제한할 수 있다는 뜻이다.

> 내가 사용한 서버는 싱글 코어이기 때문에 `cpuset` 컨트롤러를 사용할 수 없다.  
> (결과에 `cpuset`이 없다)

// todo cpuset 설명

### 하위 그룹 컨트롤러 설정

`echo "+cpu" | tee /sys/fs/cgroup/cgroup.subtree_control` 

위 명령어를 통해 하위 그룹에 cpu 컨트롤러를 사용할 수 있도록 설정한다.

// todo tee 설명

### 
