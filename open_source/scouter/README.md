# Scouter

스카우터란 자바 에이전트를 사용하여 자바 프로그램의 동작을 모니터링하는 오픈소스 프로젝트이다.

agent.java 를 통해 자바 프로그램을 모니터링 한다.

> agent.java, agent.host 를 통해 메트릭을 수집하고,  
> 이를 collector(server)에게 전송한다.

---

이 문서는 스카우터의 agent.java 코드를 분석하고 정리한 문서이다.