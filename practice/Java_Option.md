### 자바 힙 옵션

자바 힙 옵션은 힙 영역의 크기를 조절하는 옵션이다.

`-Xms{size}` : 최소 힙 크기  
`-Xmx{size}` : 최대 힙 크기

> 여기서 {size}는 크기를 나타내는 단위를 포함한 숫자이다.  
> (ex. 256m, 512m, 1g)

---

### OutOfMemory Error 발생 시 힙 덤프 파일 생성

OutOfMemory Error가 발생하면 힙 덤프 파일을 생성하여 OutOfMemory Error가 발생한 시점의 힙 상태를 분석할 수 있다.

자바 프로그램 실행 시 `-XX:+HeapDumpOnOutOfMemoryError` 옵션을 추가하면 OutOfMemory Error 발생 시 힙 덤프 파일을 생성한다.

> 이때 해당 파일은 `java_pid{pid}.hprof` 형식으로 생성된다.  
> 그리고 해당 프로세스가 실행된 디렉토리에 생성된다.

---

### GC 로그 파일 생성

GC 로그 파일을 생성하여 GC가 어떻게 동작하는지 분석할 수 있다.

`-verbose:gc` 옵션을 추가하여 GC 로그를 확인 할 수 있다.

> 이때 해당 로그들은 stdout으로 출력된다.

`-XX:+PrintGCDetails` 옵션을 추가하여 GC 로그를 자세히 확인 할 수 있다.

기존 GC 로그  
```
[0.151s][info][gc] GC(0) Pause Young (Normal) (G1 Evacuation Pause) 27M->23M(248M) 11.742ms
[0.170s][info][gc] GC(1) Pause Young (Normal) (G1 Evacuation Pause) 44M->46M(248M) 9.782ms
[0.191s][info][gc] GC(2) Pause Young (Normal) (G1 Evacuation Pause) 72M->74M(248M) 11.244ms
[0.221s][info][gc] GC(3) Pause Young (Normal) (G1 Evacuation Pause) 109M->110M(248M) 15.394ms
[0.239s][info][gc] GC(4) Pause Young (Concurrent Start) (G1 Humongous Allocation) 132M->133M(252M) 9.986ms
[0.239s][info][gc] GC(5) Concurrent Mark Cycle
[0.270s][info][gc] GC(6) Pause Young (Normal) (G1 Evacuation Pause) 172M->174M(252M) 12.036ms
[0.283s][info][gc] GC(7) Pause Young (Normal) (G1 Evacuation Pause) 189M->190M(252M) 7.234ms
```

Details 옵션 추가 후 GC 로그  
```
[0.005s][warning][gc] -XX:+PrintGCDetails is deprecated. Will use -Xlog:gc* instead. // ***
[0.016s][info   ][gc] Using G1
[0.018s][info   ][gc,init] Version: 17.0.9+8-LTS (release)
[0.018s][info   ][gc,init] CPUs: 8 total, 8 available
[0.018s][info   ][gc,init] Memory: 15792M
[0.018s][info   ][gc,init] Large Page Support: Disabled
[0.018s][info   ][gc,init] NUMA Support: Disabled
[0.018s][info   ][gc,init] Compressed Oops: Enabled (Zero based)
[0.018s][info   ][gc,init] Heap Region Size: 2M
[0.018s][info   ][gc,init] Heap Min Capacity: 8M
...
[8.889s][info   ][gc,start    ] GC(16) Pause Young (Normal) (G1 Evacuation Pause)
[8.889s][info   ][gc,task     ] GC(16) Using 8 workers of 8 for evacuation
[8.893s][info   ][gc,phases   ] GC(16)   Pre Evacuate Collection Set: 0.1ms
[8.893s][info   ][gc,phases   ] GC(16)   Merge Heap Roots: 0.1ms
[8.893s][info   ][gc,phases   ] GC(16)   Evacuate Collection Set: 3.8ms
[8.893s][info   ][gc,phases   ] GC(16)   Post Evacuate Collection Set: 0.7ms
[8.893s][info   ][gc,phases   ] GC(16)   Other: 0.1ms
[8.893s][info   ][gc,heap     ] GC(16) Eden regions: 27->0(24)
[8.893s][info   ][gc,heap     ] GC(16) Survivor regions: 3->4(4)
[8.893s][info   ][gc,heap     ] GC(16) Old regions: 17->19
[8.893s][info   ][gc,heap     ] GC(16) Archive regions: 0->0
[8.893s][info   ][gc,heap     ] GC(16) Humongous regions: 0->0
[8.893s][info   ][gc,metaspace] GC(16) Metaspace: 74805K(75456K)->74805K(75456K) NonClass: 64137K(64448K)->64137K(64448K) Class: 10668K(11008K)->10668K(11008K)
[8.893s][info   ][gc          ] GC(16) Pause Young (Normal) (G1 Evacuation Pause) 92M->42M(114M) 4.893ms
[8.893s][info   ][gc,cpu      ] GC(16) User=0.00s Sys=0.00s Real=0.01s
```

로그에서 보이듯이 -XX:+PrintGCDetails 옵션은 deprecated 되었으므로 -Xlog:gc* 옵션을 사용하도록 권장된다.

---