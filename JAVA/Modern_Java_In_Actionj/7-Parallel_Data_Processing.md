이전 장까지 스트림 인터페이스를 이용해서 데이터 컬렉션을 선언형으로 제어하는 방법을 살펴봤다. 

이번 장에서는 스트림으로 데이터 컬렉션 관련 동작을 얼마나 쉽게 병렬로 실행할 수 있는지 알아본다.

---
### 병렬 스트림
컬렉션에 parallelStream을 호출하면 병렬 스트림이 생성된다. 병렬 스트림이란 각각의 스레드에서 처리할 수 있도록 스트림 요소를 여러 청크로 분할한 스트림이다. 따라서 병렬 스트림을 이용하면 모든 멀티코어 프로세서가 각각의 청크를 처리하도록 할당할 수 있다.

이제부터 그냥 반복문으로 처리했을때, 스트림을 이용했을때, 병렬 스트림을 이용했을떄의 성능들을 비교하면서 알아보겠다.

```java
public static long iterativeSum(long n) {
    long result = 0;
    for (long i = 0; i <= n; i++) {
      result += i;
    }
    return result;
  }
```
위 코드는 n을 받으면 1부터 n까지 더한 결과를 반환하는 iterativeSum 메서드이다.<br>
위 메서드는 스트림을 이용하지 않고, 반복문으로 처리하는 메서드이다.

```java
public static long sequentialSum(long n) {
    return Stream.iterate(1L, i -> i + 1).limit(n).reduce(Long::sum).get();
  }
```
위 코드도, n을 받으면 1부터 n까지 더한 결과를 반환하는 sequentialSum 메서드이다.<br>
위 메서드는 스트림을 이용해서 처리하는 메서드이다.

```java
public static long parallelSum(long n) {
    return Stream.iterate(1L, i -> i + 1).limit(n).parallel().reduce(Long::sum).get();
  }
```
위 코드도, n을 받으면 1부터 n까지 더한 결과를 반환하는 parallelSum 메서드이다.<br>
위 메서드는 parallel() 메서드를 호출해서 기존의 함수형 리듀싱 연산이 병렬로 처리된다.

---
### 성능 측정
위 3개의 메서드 중 어떤 메서드를 호출해도 결과는 똑같이 나온다.<br>
지금부터는 병렬 스트림을 이용했을때 성능이 얼마나 나오는지 비교해본다.
> 성늑 측정은 해당 메서드를 실행하기 전 시간을 측정하고, 메서드를 실행한 뒤의 시간을 측정해서, 두 시간의 차를 측정했습니다.
>
> 각각의 상황마다 다른 결과가 나올 수 있습니다

---
### 성능 측정 결과
위 3개의 메서드의 측정 결과<br>
Iterative Sum done in: 3 msecs<br>
Sequential Sum done in: 73 msecs<br>
Parallel   Sum done in: 117 msecs<br>

>여기서 n은 10_000_000L입니다

분명히 병렬 스트림을 이용하면 기존 코드에 비해 좋은 성능이 나올것으로 기대했지만, 매우 실망스러운 결과가 나왔다.<br>
(오히여 순차 스트림보다 병렬 스트림이 더 느린 결과가 나왔다)

왜 이런 결과가 나온 것일까?

---
### 현재 코드의 문제점
1. 언박싱문제 - 박싱된 객체로 숫자를 더하려면 언박싱해야함
2. 반복작업은 병렬로 나눌수없음 (ex) iterate)

**1. 언박싱문제 - 박싱된 객체로 숫자를 더하려면 언박싱해야함**
```iterate``` 메서드는 제네릭을 사용한다. 따라서 1부터 n까지의 숫자가 Long으로 선언되고, ```.reduce(Long::sum)``` 메서드를 실행할때 Long 타입 숫자들이 자동으로 언박싱된다.<br>
이때 성능이 떨어진다.
> 1번 문제때문에 그냥 반복문으로 처리했을때보다 스트림을 이용했을때 더 안 좋은 결과가 나왔다.

**2. 반복작업은 병렬로 나눌수없음 (ex) iterate)**
사실 이 문제의 핵심은 2번이다.
>```iterate()``` 메서드는 본질적으로 순차적이다

이와 같은 상황에서는 리듀싱 연산이 병렬적으로 수행되지 않는다.<br>
리듀싱 과정을 시작하는 시점에 숫자 리스트가 준비되지 않았으므로 스트림을 병렬로 처리할 수 있도록 청크로 분할할 수 없다.
> **순차스트림보다 병렬스트림의 결과가 더 안좋은 이유**
>
>순차 스트림은 리듀싱 연산을 수행할때 받은 데이터들을 그냥 순서대로 연산을 진행하면 끝난다.<br>
>하지만 병렬 스트림은 할일이 더많다.<br>
>일단 받은 데이터를 여러 청크로 나누고, 스레드에 할당하는 일을 해야한다.<br>
>이때 생기는 오버헤드 때문에 병렬스트림의 결과가 안 좋은 것이다.

---
이처럼 병렬 프로그래밍은 까다롭고 때로는 이해하기 어려운 함정이 숨어 있다.<br>
심지어 병렬 프로그래밍과 거리가 먼 반복 작업을 병렬처리를 하면, 오히려 전체 프로그램의 성능이 더 나빠질 수 있다.

따라서 마법 같은 parallel 메서드를 호출했을때 내부적으로 어떤 일이 일어나는지 이해해야 한다.

---
### 더 특화된 메서드 사용
멀티코어 프로세서를 활용해서 효과적으로 합계 연산을 병렬로 실행하려면 어떻게 해야 할까?<br>
```iterate```메서드대신 ```rangeClosed```메서드를 이용하면 더 좋은 결과가 나올 것이다.
> ```rangeClosed``` 메서드의 장점
1. ```rangeClosed``` 메서드는 기본형 long을 직접 사용하므로 박싱과 언박싱 오버헤드가 사라진다.
2. ```rangeClosed``` 메서드는 쉽게 청크로 분할할 수 있는 숫자 범위를 생산한다.

---
### ```rangeClosed``` 메서드 사용
```rangeClosed``` 메서드를 이용한 sum의 성능을 보자

Iterative Sum done in: 3 msecs<br>
Sequential Sum done in: 73 msecs<br>
Parallel   Sum done in: 119 msecs<br>
Ranged     Sum done in: 5 msecs<br>
ParallelRanged Sum done in: 1 msecs

기존 iterate 팩토리 메서드로 생성한 버전에 비해 rangeClosed 메서드로 생성한 번전이 더 좋은 성능을 보여줬다.

그리고 드디어 순차 실행보다 빠른 성능을 갖는 병렬 리듀싱을 만들었다.<br>
실질적으로 리듀싱 연산이 병렬로 수행되는 것을 알수있다.

> 올바른 자료구조를 선택해야 병렬 실행도 최적의 성능을 발휘할 수 있다.<br>
상황에 따라서는 어떤 알고리즘을 병렬화하는 것보다 적절한 자료구조를 선택하는 것이 더 중요할 수 있다.

결국 함수형 프로그래밍을 올바로 사용하면 반복적으로 코드를 실행하는 방법에 비해 최신 멀티코어 CPU가 제공하는 병렬 실행의 힘을 단순하게 직접적으로 얻을 수 있다

---
### 병렬화 유의할 점
하지만 병렬화가 완전 공짜는 아니라는 사실을 기억하자. 병렬화를 이용하려면 스트림을 재귀적으로 분할해야 하고, 각 서브스트림을 서로 다른 스레드의 리듀싱 연산으로 할당하고, 이들 결과를 하나의 값으로 합쳐야 한다.

멀티코어 간의 데이터 이동은 생각보다 비싸다. 따라서 코어간의 데이터 전송시간보다 훨씬 오래 걸리는 작업만 병렬로 다른 코어에서 수행하는 것이 바람직하다.

또한 상황에 따라 병렬화를 이용할 수 없는 때도 있다.

---
### 병렬화를 이용할때 흔히 일어나는 실수
다음 코드를 보자
```java
public static class Accumulator {

    private long total = 0;

    public void add(long value) {
      total += value;
    }

}
```
Accumulator 클래스의 add 메서드를 호출하면, 받은 인자를 total에 더해주는 일을 한다.

```java
public static long sideEffectSum(long n) {
    Accumulator accumulator = new Accumulator();
    LongStream.rangeClosed(1, n).forEach(accumulator::add);
    return accumulator.total;
}

public static long sideEffectParallelSum(long n) {
    Accumulator accumulator = new Accumulator();
    LongStream.rangeClosed(1, n).parallel().forEach(accumulator::add);
    return accumulator.total;
}
 
```
Accumulator 클래스의 add 메서드를 총 n번 수행해주는 메서드들이다.<br>
위 메서드는 순차스트림으로 실행하고, 아래 메서드는 병렬 스트림으로 수행한다.

두 메서드를 10번씩 돌렸을때의 결과를 보자
```
(sideEffectSum)
Result: 50000005000000
Result: 50000005000000
...
Result: 50000005000000
SideEffect sum done in: 5 msecs

(sideEffectParallelSum)
Result: 11505370682673
Result: 3810317718362
...
Result: 6593045014487
SideEffect parallel sum done in: 4 msecs
```
성능보다 메서드의 결과를 보자<br>
병렬 스트림을 이용했을때 원하는 결과가 나오지 않고, 실행할 때마다 다른 결과가 나왔다.

왜 이런일이 발생한 것일까?

---
### 레이스 컨디션(race condition)
Accumulator 클래스 코드를 다시 보면
```java
public static class Accumulator {

    private long total = 0;

    public void add(long value) {
      total += value;
    }

}
```
여기서 문제는 add 메서드가 total 필드에 접근한다는 것이다.

순차 스트림에서는 n개의 add 메서드가 순차적으로 실행되기 때문에, 결과는 항상 같다

하지만 병렬 스트림에서는 n개의 add 메서드가 동시에 일어날 수 있기 때문에, <br>
결국 여러 스레드에서 공유하는 객체의 상태를 바꾸는 add 메서드를 호출하면서 이같은 문제가 발생한다.<br>
> 이런 상황처럼, 두 개 이상의 프로세스가 공통 자원을 병행적으로 읽거나 쓸때, 공용 데이터에 대한 접근이 어떤 순서에 따라 이루어졌는지에 따라 그 실행 결과가 달라지는 상황을 **레이스 컨디션**이라 말한다.

위처럼 병렬 스트림과 병렬 계산에서는 공유된 가변 상태를 피해야 한다는 사실을 확인했다.

마지막으로 병렬 스트림을 효과적으로 사용하는 방법들을 알아보자

---
### 병렬 스트림 효과적으로 사용하기
1. 확신이 서지 않으면 직접 측정하라
2. 박싱을 주의하라. 자동 박싱과 언박싱은 성능을 크게 저하시킬 수 있는 요소다
> 자바 8은 박싱 동작을 피할 수 있도록 기본형 특화 스트림(IntStream, LongStream, DoubleStream)을 제공한다.
(rangeClosed 메서드도 기본형 특화 스트림에서 사용하는 메서드이다)
3. 순차 스트림보다 병렬 스트림에서 성능이 떨어지는 연산이 있다 (limit, iterate, findFirst, ...)
4. 스트림에서 수행하는 전체 파이프라인 연산 비용을 고려하라
> 처리해야 할 요소 수가 N이고 하나의 요소를 처리하는데 드는 비용을 Q라 하면 전체 파이프라인 처리 비용을 N*Q라 예상할 수 있다.
5. 소량의 데이터에서는 병렬 스트림이 도움이 되지 않는다.
6. 스트림을 구성하는 자료구조가 적절한지 확인하라
> 예를 들어 ArrayList를 LinkedList보다 효과적으로 분해할 수 있다.
LinkedList를 분할하려면 모든요소를 탐색해야하지만, ArrayList는 모든 요소를 탐색하지 않고도 분할할 수 있기 때문이다
7. 최종 연산의 병합과정 비용을 살펴보라. 병합 과정의 비용이 비싸다면 병렬 스트림의 성능이 떨어질 수 있다.


