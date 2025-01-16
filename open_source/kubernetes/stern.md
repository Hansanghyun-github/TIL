# stern 명령어

쿠버네티스 로그를 실시간으로 모니터링할 수 있게 해주는 오픈 소스 CLI 도구  
여러 Pod의 로그를 한 번에 모니터링하고 필터링할 수 있는 기능을 제공한다.

> Pod: 쿠버네티스에서 가장 작은 배포 단위, 하나 이상의 컨테이너를 묶어서 실행하는 논리적인 단위

> 동일한 이름의 여러 Pod가 동시에 실행될 때 유용하다.

## stern 명령어 기능

1. 여러 Pod 로그 동시 조회
2. 실시간 로그 스트리밍
3. 컨테이너 필터링
4. 기존의 kubectl 설정 그대로 활용 가능

## stern 사용 예시

'stern buzzscreen-staging- -n buzzscreen -c buzzscreen --since 1s'

'stern <POD_NAME>'  
이름이 POD_NAME로 시작하는 Pod들의 로그를 모두 보여준다.

(위 예시는 이름이 'buzzscreen-staging-로 시작하는 Pod들의 로그를 조회한다)

> 이름은 정규표현식으로 해석된다.

'-n'  
네임스페이스를 지정한다.

'-c'  
컨테이너를 지정한다.

'--since 1s'  
최근 1초 이내의 로그부터 출력을 시작한다.

