## scouter의 agent.java를 자바 프로그램과 같이 실행했는데 xlog가 확인이 되지 않는다.

### 개요

agent.java jar 파일을 javaagent 로 하고 기존 프로젝트 jar 파일과 같이 실행했는데,

GC 나 Heap 같은 메트릭은 collector에서 수집이 됐지만, xlog, TPS 같은 사용자 요청과 관련된 메트릭이 수집이 되지 않았다.

### 원인

scouter 깃허브 문서를 보고, 구글링으로 비슷한 오류를 찾아봤지만  
도저히 찾을 수 없어서,

직접 agent.java 의 코드를 뜯어봤다.

agent.java 의 코드를 보다가 버전에 의한 문제라는 것을 확인했다.

![img_2.png](../img/agent_java_version_20.png)  
scouter 2.20 버전의 agent.java 파일에서  
HttpServiceASM 클래스는 jakarta 클래스를 지원하는데

![img_3.png](../img/agent_java_version_17.png)  
scouter 2.17 버전의 agent.java 파일에서  
HttpServiceASM 클래스는 jakarta 클래스를 지원하지 않는다.

> 자바 9 이후로 javax 패키지가 jakarta 패키지로 변경되었다.  
> 프로젝트의 스프링 부트 버전은 3.X인데, 이 버전은 jakarta 패키지를 사용한다.

스프링 부트는 jakarta 를 사용하는데, agent.java의 버전은 2.17 이라서 jakarta 클래스를 지원하지 않아서,  
Xlog, TPS 메트릭이 수집되지 않았다.

(2.20 버전의 업데이트 내용을 보면 알 수 있다)  
![img_1.png](../img/scouter_doc_1.png)

### 해결

agent.java 버전을 2.17에서 2.20으로 올려주었다.  
그랬더니 xlog TPS 메트릭이 정상적으로 수집되었다.

![img.png](../img/xlog_1.png)

> 이래서 공식 문서를 꼼꼼이 보라는 거구나...
>
> 이 문제는 에러나 로그가 아예 없어서 찾기 힘들었다.

---

## 스카우터의 xlog에서 cpu 사용 시간, KBytes 메트릭이 확인이 되지 않는다.

### 개요

스카우터를 통해 부하테스트의 요청들의 xlog를 확인하고 있는데,  
다른 필드는 잘 나오는데, cpu 사용 시간, KBytes 메트릭이 확인이 되지 않았다.

### 원인

이를 알아보기 위해 scouter.agent.java의 코드를 확인해봤다.  

> 스카우터의 agent.java는 TraceMain 클래스를 통해 xlog를 수집한다.  
> (startHttpService, endHttpService 메서드에서 메트릭을 수집한다)

위 메서드들의 코드를 확인해 보니  
cpu, 메모리 사용량과 관련된 코드가 있었다.

```java
class TraceMain {
    startHttp() {
        // ...
        ctx.bytes = SysJMX.getCurrentThreadAllocBytes(conf.profile_thread_memory_usage_enabled); // 메모리 사용량
        ctx.profile_thread_cputime = conf.profile_thread_cputime_enabled;
        if (ctx.profile_thread_cputime) {
            ctx.startCpu = SysJMX.getCurrentThreadCPU(); // cpu 사용 시간
        }
        // ...
    }
}
```

코드를 확인해 보니,  
profile_thread_memory_usage_enabled 값이 true일 때 메모리 사용량을 수집하고,  
profile_thread_cputime_enabled 값이 true일 때 cpu 사용 시간을 수집한다.

하지만 두 변수의 default 값은 false로 설정되어 있었다.

### 해결

해당 값을 true로 설정해주었더니,  
cpu 사용 시간, KBytes 메트릭이 정상적으로 수집되었다.