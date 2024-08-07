# 백트래킹 알고리즘

## 정의

백트래킹(Backtracking)은 해결책에 대한 후보를 구축해 나아가다  
가능성이 없다고 판단되는 시점에서 후보를 포기(Backtrack)해 정답을 찾아가는 기법이다.

## 특징

1. 완전탐색 기법 중 하나로, 모든 경우의 수를 탐색하는 방법이다.
2. 해를 찾기 위해 후보군을 점진적으로 구축하다가,  
   가능성이 없다고 판단되는 즉시 후보군을 포기하는 방법이다.
3. 최적해를 찾는 방법은 아니다.
4. 모든 경우의 수를 탐색하므로, 시간이 오래 걸릴 수 있다.
5. 재귀 함수를 이용해 구현한다.
6. DFS와 유사하다.
7. 탐색을 진행하면서 지금까지 선택한 상태를 저장하고,  
   다음 단계로 진행하기 전에 선택한 상태를 되돌린다.
   
> 그래프에서 최대한 정점을 많이 방문해야 하는 문제도,  
> 백트래킹 알고리즘을 사용해 풀 수 있다.

---

## 백트래킹 문제들

15649  
순열을 구하는 문제  
사전순으로 출력해야 하기 때문에,  
1부터 N까지 탐색하면서 M개를 고른다.  
`permutation(int m)` // m개를 골랐을 때 다음 M개까지 골라서 출력하는 메서드  
(이때 visited 배열을 이용해 중복을 방지한다) 

> 포기하는 케이스  
> M개를 고르지 못하고 끝나는 케이스  
> (출력이 안된다)

15650  
조합을 구하는 문제  
`permutation(int i, int m)` // i 위치 전까지 m개를 골랐을 때 다음 M개까지 골라서 출력하는 메서드  
(오름차순으로 출력하기 위해 i 파라미터를 추가했다)

> 포기하는 케이스  
> M개를 고르지 못하고 끝나는 케이스  
> (오름차순만 출력이라 더 많이 포기하게 된다)

15651  
중복순열 문제  

15652  
중복조합 문제

9663  
N-Queen  
처음 나는 시간복잡도가 O(n^3)이라고 생각했다.  
하지만 이 문제의 시간복잡도는 O(n!)이다.  
(이론적으로는 무식하게 생각하면 O(n^n)이지만, 백트래킹으로 접근하면 O(n!)이다)

> O(n^3)이 아니라, O(n!)인 이유  
> 
> 어떤 위치에 퀸을 놓을 때,  
> 윗 줄의 상태에 따라 해당 위치에 퀸을 놓을 수 있을 지가 갈린다.  
> 
> 이때, 윗 줄의 상태를 확인하는데 O(n)이 걸린다.  
> (메모이제이션 활용)  
> 
> 즉, 각 줄마다 O(n)이 걸리므로,  
> O(n^n)이 걸리지만, 백트래킹으로 접근하면 O(n!)이 된다.

14888  
숫자 순서는 고정이고, 연산자의 순서를 바꿔서 숫자를 최대로 하는 문제  
이때 사칙연산이 아니라 앞에서부터 계산하기 때문에, DP & 그리디 같은 알고리즘을 적용할 수 없다.  
연산량을 줄이기 위해 백트래킹을 사용한다.  
시간복잡도: O(n!)

14889  
능력치의 차이가 되기 위한 최적해는 없기 떄문에  
모든 경우의 수를 탐색하면서 백트래킹을 사용한다.  
(n개 중에 n/2개를 선택하고 계산하는 문제)  
이때 순열이 아닌 조합을 사용한다.  
시간복잡도: O(C(n, n/2))

15686  
최소가 되는 경우를 구하려면,  
모든 경우를 탐색해야 한다.  
(이때, 치킨집을 M개 선택하는 조합을 사용한다 - 백트래킹)
시간복잡도: O(C(13, m) * M * 2 * N)

1759  
알파벳들을 정렬한 다음, 조합을 사용해 문제를 풀 수 있다.  
(이때, 모음과 자음의 개수를 세어서 조건을 만족하는지 확인한다)

6603  
숫자들을 정렬한 다음, 조합을 사용해 문제를 풀 수 있다.  
(이때, 6개를 고르는 조합을 사용한다)

15654  
순열 문제

1987  
DFS + 백트래킹 문제  



---

## 문제를 풀면서 얻은 팁들

1. 백트래킹은 재귀함수가 편하다.
2. DP나 그리디처럼 최적해를 찾는 것이 아니므로,  
   모든 경우의 수를 탐색해야 한다.  
   (이때 안되는 케이스를 포기함으로써 시간을 줄인다)

NxN 보드를 탐색할 때, O(N^N)으로 탐색하는 경우와 O(N^2)으로 탐색하는 경우 비교

O(N^N) 케이스  
특정 행에서 n개 중에 하나를 고르고,  
다음 행에서 n개 중에 하나를 고른다.  
이런식으로 계속 진행하면 O(N^N)이 된다.

O(N^2) 케이스  
보드를 순차적으로 탐색하는 케이스

---

## 한번 더 해보면 좋을 문제들

15649 - 백트래킹의 대표적인 조합 문제

9663 - 백트래킹 알고리즘의 시간복잡도에 대해 오해한 문제

