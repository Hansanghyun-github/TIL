# 그리디 알고리즘

탐욕법은 가장 직관적임 알고리즘 설계 패러다임 중 하나입니다.  
탐욕법을 이용한 알고리즘은 우리가 원하는 답을 재귀 호출과 똑같이 여러 개의 조각으로 쪼개고,  
각 단계마다 답의 한 부분을 만들어 간다는 점에서 완전 탐색이나 동적 계획법 알고리즘과 다를 것이 없습니다.

그러나 모든 선택지를 고려해 보고 그중 전체 답이 가장 좋은 것을 찾는 두 방법과 달리,  
탐욕법은 각 단계마다 지금 당장 좋은 방법만을 선택합니다.

탐욕법은 `지금의 선택이 앞으로 남은 선택들에 대해 어떤 영향을 끼칠지는 고려하지 않습니다`.

---

실제로 최적해를 얻을 수 있는 접근이 직관적이지 않은 경우도 많기 때문에 실수에 더 유의해야 합니다.  
그러니 탐욕적 알고리즘을 연습 문제를 풀때는 알고리즘의 정당성을 증명하는 과정을 빼먹지 않고 연습하는 것이 좋습니다.

> 탐욕적 선택 속성(greedy choice property)  
> 동적 계획법처럼 답의 모든 부분을 고려하지 않고 탐욕적으로만 선택하더라도 최적해를 구할 수 있다는 것
> 
> 최적 부분 구조  
> 항상 최적의 선택만을 내려서 전체 문제의 최적해를 얻을 수 있음
> 
> 위 두가지를 증명해야 탐욕법을 적용할 수 있다.  
> (최적 부분 구조는 대부분 자명해서 증명할 필요가 없다고 한다)

---

## 그리디 문제 접근 방법

사실 최적해를 바로 떠올리기는 쉽지 않다.  
그리고 최적해를 떠올려도 해당 최적해가 이 문제에 적용되는지 검증하는 것도 쉽지 않다.

맨 처음에는 주어진 예시를 한번 풀어보는게 좋다.  
그리고 예시를 풀면서 내가 어떻게 접근했는지를 의식하면서 푼다면,  
최적해를 그나마 쉽게 찾을 수 있다.

---

## 그리디 알고리즘 문제들

2839  
봉지의 개수를 줄이려면, 최대한 5킬로 봉지를 많이 사용해야 한다.  
-> 5킬로 봉지 개수를 줄이면서, 가능한 경우를 탐색한다.

11399  
최솟값을 구하려면, 인출 시간이 짧은 사람은 앞에 둬야 한다.

11047  
동전 개수를 줄이려면, 최대한 가치가 높은 동전을 사용해야 한다.  

1931  
회의 개수를 최대로 하기 위해, 끝나는 시간이 빠른 회의를 먼저 담아야 한다.  

1541  
값을 최소로 하기 위해, 마이너스 부호 뒤의 수를 최대한 키워야 한다.  
-> 다음 마이너스 부호가 오기 전까지의 숫자를 모두 괄호로 묶는다.

1026  
S의 최솟값을 구하려면, 가장 큰 수에는 가장 작은 수를 곱해줘야 한다.

5585, 2217

1789  
서로 다른 N개의 자연수의 합이 S일때, N이 최대려면,  
결국 1부터 N까지 더한다고 가정해야 한다.  
(N을 제외한 모든 수는 최소가 되야 하기 때문)  
-> 1 + ... + N 이 S를 넘어설 때의 N(or N-1)이 정답이다.

1715  
최대한 적은 수를 먼저 사용해야 한다. (우선순위 큐 이용)

16953  
A를 B로 바꾸는 문제인데,  
B를 A로 그리디하게 바꾸면 간단하게 풀 수 있다.  
B의 끝이 1 -> 1 뺀다, B의 끝이 짝수 -> 2 나눈다.  
(그 외의 수는 -1 처리)

1439  
그냥 0일 때와 1일 때의 개수를 세서 최소인 값을 반환하면 끝

1946  
면접과 서류 순위에서, 다른 지원자의 성적보다 떨어지지 않는다면 뽑는다.  
-> 한쪽 순위를 정렬해놓고 비교하면 편해진다.  
1. 면접 순위 오름차순으로 정렬
2. i번째 사람은 왼쪽 사람들 보다 서류 순위가 높으면 뽑는다.  
   (오른쪽 사람들보다 면접 순위가 높기 때문에)

1339  
맨 앞자리 알파벳부터 가중치를 부여한다.  
가중치 내림차순으로 9~1 숫자를 부여해서 계산한다.

1202  
기존 배낭 문제에서, 배낭의 개수가 늘어난 케이스  
여기서 가방에 보석은 딱 1개만 넣을 수 있다는게 핵심이다.  
-> 보석과 가방을 최대한 딱 맞게 넣어야 한다.  
(무게가 5인 보석을 중량이 10인 가방 보다는 6인 가방에 넣는 것이 더 이득이다)
1. 보석을 가치 내림차순으로 정렬
2. 가방을 무게 오름차순으로 정렬
3. 가치가 높은 보석순으로 가장 딱 맞는 가방을 탐색한다. (lower_bound)



---

경우의 수가 많아 풀기 힘들다면,  
한쪽을 정렬해서 풀면 수월해질 수도 있다.

---

## 한번 더 생각해볼 문제들

1946 - 한쪽을 정렬해서 편하게 푸는 케이스