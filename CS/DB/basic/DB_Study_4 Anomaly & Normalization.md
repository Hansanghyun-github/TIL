## 이상 현상(Anomaly)

이상 현상은 **테이블을 설계할 때 잘못 설계하여 데이터를 삽입, 삭제, 수정할 때 논리적으로 생기는 오류**를 말한다.

> 좋은 관계형데이터베이스를 설계하는 목적 중 하나가 정보의 이상 현상(Anomaly)이 생기지 않도록 고려해 설계하는 것

삽입 이상, 갱신 이상, 삭제 이상이 있다.

### 삽입 이상(Insertion Anomaly)

새로운 데이터를 삽입할 때, 의도와는 상관없이 데이터 무결성이 깨지는 현상을 나타냅니다.

예시  
데이터 중복(동일한 데이터가 여러 행에 중복되어 저장되는 경우)  
-> 의미없는 데이터가 삽입될 수 있다.

### 갱신 이상(Update Anomaly)

데이터를 갱신할 때 발생하는 문제

예시  
중복에 의한 갱신 이상(중복된 데이터 중 일부만 갱신되어, 데이터 일관성이 깨지는 경우)

### 삭제 이상(Deletion Anomaly)

데이터를 삭제할 때 발생하는 문제

예시  
의도하지 않은 데이터 손실(특정 데이터를 삭제하려고 할 때, 그 데이터와 연결된 다른 데이터도 함께 손실되는 경우)

> 이상 현상은 대부분 정규화를 제대로 하지 않아서 생기는 것들이다.

---

## Functional Dependency

한 테이블에 있는 두 개의 속성 집합 사이의 제약

### X -> Y

(X, Y는 속성 집합)

속성 집합 X의 값 각각에 대해 항상 속성 집합 Y의 값이 오직 하나만 연관되어 있을 때 Y는 X에 함수 종속이라 하고, X → Y라고 표기한다.

> X 값에 따라 Y 값이 유일하게 결정된다.  
> x가 Y를 함수적으로 결정한다.  
> Y가 X에 함수적으로 의존한다.

member 테이블에서  
member_id 값에 따라 {name, age}이 유일하게 결정된다.  
따라서 {member_id} -> {name, age}  

### FD 파악하기

`테이블의 스키마`를 보고 의미적으로 파악해야 한다.  
(테이블의 state를 보고 FD를 파악해서는 안된다)

> 주의 X -> Y, not Y -> X

> {} -> Y  
> (Y는 언제나 하나의 값만을 가진다는 의미)

### trivial FD

when X -> Y holds, if Y is subset of X, then X -> Y is trivial FD

Y가 X의 부분집합일 때의 X -> Y를 trivial FD라고 한다.

### non-trivial FD

when X -> Y holds, if Y is `not` subset of X, then X -> Y is non-trivial FD

Y가 X의 부분집합이 아닐 때의 X -> Y를 trivial FD라고 한다.

> 만약 Y의 속성들과 X의 속성들 중, 겹치는 속성이 하나도 없을 때,  
> X -> Y를 completely non-trivial FD라고 한다. 

### Partial FD

when X -> Y holds, if any proper subset of X can determine Y, then X -> Y is partial FD

X -> Y를 만족할 때, X의 진부분집합 중 하나가 Y를 결정할 경우,  
X -> Y를 부분 함수적 종속이라고 한다.

> 특정 테이블에서, 후보키 + α (슈퍼키)가 X이고 해당 테이블의 속성들이 Y에 왔을 때의 X -> Y는 부분 FD를 일 듯

### Full FD

when X -> Y holds, if `every` proper subset of X can `not` determine Y, then X -> Y is full FD

X -> Y를 만족할 때, X의 어떤 진부분집합도 Y를 구별할 수 없을 때,  
X -> Y를 완전 함수적 종속이라고 한다.

> 특정 테이블에서, 후보키가 X이고 해당 테이블의 속성들이 Y에 왔을 때의 X -> Y는 완전 FD를 일 듯

### 이행적 함수적 종속

X -> Y, Y -> Z를 만족하는 속성 집합 X, Y, Z가 있을 때,  
X -> Z를 이행적 함수적 종속이라고 한다.

---

## 정규화(Normalization)

이상 현상(anomaly)를 최소화하기 위해  
일련의 normal forms(NF)에 따라 relational DB를 구성하는 과정

> normal forms  
> 정규화 되기 위해 준수해야 하는 몇가지 규칙들

> DB의 정규화 규칙
> 
> 이전 normal form을 만족해야, 다음 단계로 진행할 수 있다  
> (어떤 테이블이 3NF를 만족한다 - 1NF, 2NF도 만족한다)

### 1NF

모든 attribute의 value는 atomic해야 한다.  
(쪼개질 수 없는 단일 값이어야 한다)

### 2NF

모든 non-prime attribute는 모든 key에 대해 full FD를 만족해야 한다.

> non-prime attribute
> 
> 후보키를 제외한 attribute들

> (다른 표현)  
> 후보키가 X이고, 다른 attribute가 Y일때,  
> X -> Y가 Partial FD를 만족하지 않아야 한다.

### 3NF

non-prime attribute와 non-prime attribute 사이에는 FD가 있으면 안된다.

### BCNF

모든 유효한 FD X -> Y에서, X가 슈퍼키여야 한다.  
(여기서 Y는 X의 부분집합이 아니여야 함)

> 다른 표현  
> non-prime attribute가 key의 어떤 attribute도 FD하면 안된다.  
> (non-prime attribute -> key's attribute - 이렇게 되면 안됨)

---

> 정규화 과정을 거쳐, 테이블을 많이 쪼개다 보면  
> 쿼리를 보낼 때 여러 테이블을 조인 해야 하므로,성능이 느려지는 이슈가 생길 수 있다.

### 반정규화(Denormalization)

데이터베이스 설계에서 정규화된 데이터 모델을  
일부러 테이블/속성 중복을 통해 성능을 향상시키는 과정

테이블 단위 반정규화로, 테이블 병합/분할/추가 가 있다.

컬럼 단위 반정규화로, 중복/파생/이력테이블 컬럼 추가 등이 있다.