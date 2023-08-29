### DFS(Depth-First Search)

최대한 깊이 이동한 뒤, 더이상 갈곳이 없을경우 이전 노드로 이동하고 다시 탐색하는 알고리즘
재귀함수 or 스택을 이용해서 구현

![](https://velog.velcdn.com/images/tkdgus5828/post/64998513-25f8-4aad-8308-ef08a8efdf2a/image.png)

노드를 방문하는 순서 (1번시작)<br>
1->2->6->7 (다시1)->3->4->5

```java

void dfs(해당 노드 정보){
	
	for(int i=0;i<cur의 엣지 개수;i++){
		if(visited[cur이 가리키는 다음노드] == true) { // 이미 방문했음
			continue;
		}

		visited[다음노드] = true;
		dfs(다음노드정보); // 바로 다음 노드로 이동(깊게탐색함)
	}
}
```

### BFS(Breadth-First Search)

최대한 넓게 이동한 다음(주위), 더 이상 갈곳이 없을경우 다음 노드로 이동해서 다시 탐색하는 알고리즘

큐를 이용해서 구현

![](https://velog.velcdn.com/images/tkdgus5828/post/64998513-25f8-4aad-8308-ef08a8efdf2a/image.png)

노드를 방문하는 순서(1번시작)<br>
1->2->3->6->4->7->5<br>
인접한 노드를 먼저 방문하는 알고리즘

```java
q.push(root노드정보)
while(!q.empty()){
	cur = q.front();
	q.pop();
	
	for(int i=0;i<cur의 엣지 개수;i++){
		if(visited[cur이 가리키는 다음노드] == true) { // 이미 방문했음
			continue;
		}

		visited[다음노드] = true;
		q.push(다음노드정보); // 큐에 넣어놓고 나중에 방문(현재는 주위노드먼저 방문한다)
	}
}
```

---

### DFS vs BFS

언제 DFS를 쓰고 또 언제 BFS를 쓸까

**CASE 1 - 모든 노드(정점)를 탐색할때**

어떤 알고리즘을 쓰던 상관없다

> 문제 예시
[10026번: 적록색약](https://www.acmicpc.net/problem/10026) / [2573번: 빙산](https://www.acmicpc.net/problem/2573)
위 문제들은 연결된 노드들을 찾기만 하면 되기 때문에 어떤 알고리즘을 쓰던 상관없다

**CASE 2 - 최단거리를 찾을때 (최대한 노드를 적게 방문하는 경우의 수를 구할때) or 주위를 우선적으로 탐색해야 할때**

인접노드를 우선적으로 탐색하는 BFS가 유리하다.

> 문제 예시
[7576번: 토마토](https://www.acmicpc.net/problem/7576) / [2206번: 벽 부수고 이동하기](https://www.acmicpc.net/problem/2206)
위 문제들은 모든 노드를 탐색하는데, 최단거리를 찾는 문제이다.
이는 DFS로 구할 수는 있지만 BFS에 비해 비효율적이다. (언제가 최소인지 바로바로 알 수 없다)
가장 가까운 노드부터 탐색하는 BFS를 이용해야 한다.

**CASE 3 - 경로의 특징을 저장하고 탐색하는 문제**

> 현재 그래프의 사이클을 구하는 문제, 지금까지 왔던 노드들의 정보들을 저장해놔야 하는 문제, ...

이때는 DFS를 사용하는 것이 더 좋다.
물론 현재 상태를 저장해서 다음 노드로 전달하는 간단한 문제는 BFS로도 구현이 가능하지만, 상태를 저장하는 문제 대부분은 DFS를 썼을때 좀더 쉽게 풀린다.

---
### DFS vs BFS 정리

최단거리는 BFS 알고리즘이 매우 효율적이기 때문에, BFS를 사용하면 되지만,
DFS를 적용하는 문제는 (최단거리 문제에 비해) 바로바로 캐치가 안된다.
따라서 최단거리 이외에 다른 경우는 웬만하면 DFS로 시도를 해보자.

---

### 특이한 DFS (약간 다른 알고리즘)

>사실 이번글은 이 알고리즘을 다루고 싶어서 작성했습니다

위의 알고리즘은 visited를 이용해서 이전에 방문한 노드는 방문하지 않는 간단한 알고리즘이다.

지금부터 알아볼 알고리즘은 현재 노드를 방문했을때 visited=true 체크 후 주변 노드를 전부 탐색후 자기자신 노드의 visited를 false로 돌리는 기존과는 살짝? 다른 알고리즘이다.

```java
void dfs(해당 노드 정보){
	
	for(int i=0;i<cur의 엣지 개수;i++){
		if(visited[cur이 가리키는 다음노드] == true) { // 이미 방문했음
			continue;
		}

		visited[다음노드] = true;
		dfs(다음노드정보); // 바로 다음 노드로 이동(깊게탐색함)
		visited[다음노드] = false; // ************** false로 다시 되돌림 ***************
	}
}
```

이런 알고리즘이 필요한 경우는 언제일까?

기존의 dfs, bfs 알고리즘으로는 못푸는 경우에 이 알고리즘이 필요한 경우가 있다.

다음 경우를 보자.

![](https://velog.velcdn.com/images/tkdgus5828/post/64998513-25f8-4aad-8308-ef08a8efdf2a/image.png)

이러한 형태의 그래프가 있는데 1번에서 출발했을때 최대 이동거리를 구해보자(가중치는 모두 1)
일반적인 dfs로 푼다면 방문 순서는
1 → 2 → 6 → 7
(다시1) → 3 → 4 → 5

여기서 끝나게 된다. (visited때문에 전에 방문한 노드는 방문하지 않음)
이렇게 되면 답은 4로 나오는데, 사실 이문제의 답은 (1→3→4→5→6→7) 6이 된다.

>왜 이런 문제가 발생했을까?

visited때문에 이전에 방문한 노드는 방문하지 못했기 때문에 최댓값을 구하지 못했다.
(3을 먼저 방문했다면 답을 구했겠지만, 이런 조건부 답은 생각하지 않는다)

이처럼 그래프를 이용했을때 특정 노드를 한번만 방문하면 안되는 경우에 이 알고리즘을 사용할 수 있다.

ex) 노드를 최대한 많이 방문하는 문제

---
### 특이한 DFS 알고리즘 사용 예시
실제 문제 예시를 보자
[1987번: 알파벳](https://www.acmicpc.net/problem/1987)

>2차원 배열이 주어진 상황에서, 첫번째 위치([0][0])에서 상하좌우로 이동을 시작하는데, 새로 이동한 칸에 적혀 있는 알파벳은 지금까지 지나온 모든 칸에 적혀 있는 알파벳과는 달라야 한다. 즉, 같은 알파벳이 적힌 칸을 두 번 지날 수 없다. 이때 최대 이동거리를 구해야 한다.

이문제는 기존의 dfs, bfs로는 풀수없다.
최대 이동거리기 때문에, 기존의 방문한 노드를 다시 방문해야만 한다.

---
또 다른 문제를 보자
[1103번: 게임](https://www.acmicpc.net/problem/1103)

위 문제와 조건은 조금 다르지만, 이문제 역시 최대한 노드를 많이 방문했을때의 값을 구하는 문제이다.

이렇게 최대 노드 방문 개수와 관련있는 문제는 이 알고리즘을 이용하자


> 다음 노드에 방문하기 전에 visited에 true를 입력했기때문에, 현재 위치에서 이전까지 방문한 노드는 다시 방문하지 않습니다.
visited없이 dfs를 돌리면 무한루프에 빠질 위험이 있습니다.

---
### 특이한 DFS의 시간복잡도

그렇다면 이 알고리즘의 시간복잡도는 어느정도일까?

행과 열이 n인 상하좌우로 이동가능한 2차원 배열을 기준으로 이 알고리즘의 코드를 n=2부터 n=6까지 돌려봤는데,

|n|노드를 방문한 횟수|
|-|-|
|2|5|
|3|51|
|4|1271|
|5|90111|
|6|18470411|

끝도 없이 증가한다.
굉장히 비효율적인 알고리즘이다.

이 알고리즘을 쓰는 문제들은 인풋이 굉장히 작고, visited 외에 다른 제한조건이 많이 달려있다.

> 사실 이 알고리즘은 한 노드를 굉장히 많이 방문한다 -> 상태가 중복된다
이 알고리즘을 쓸때는 최적화를 위해 dp를 쓰는 경우도 있다.

---
### 정리
그냥 최대한 노드를 적게 방문하는 경우의수를 구한다면 BFS,
특정 노드를 한번만 방문하면 안되는 문제(ex - 노드를 최대한 많이 방문하는 문제)는 특이한 DFS, 
> (인풋이 굉장히 작을때 & 다른 제한조건이 있을때 가능)

나머지는 DFS를 쓰자

---
### (Appendix) 그래프 탐색을 할때 visited
그래프 탐색을 할때 중복 방지를 위해 visited 배열을 이용한다.
이때 문제에 따라 다양한 visited가 있다.

(행과 열이 n인 2차원 배열 기준)

1. 일반적인 visited
https://www.acmicpc.net/problem/1012 유기농 배추 문제
일반적인 그래프 탐색 문제이다.
$n^2$만큼 visited 배열을 선언해주면 된다.

2. 일반적이지 않은 visited
(2-1) https://www.acmicpc.net/problem/13459 구슬탈출 문제
빨간 구슬과 파란 구슬, 각각 구슬의 위치 별로 visited를 체크해줘야 한다.
$n^2 * n^2$로 visited 배열을 선언해줘야 한다.
(2-2) https://school.programmers.co.kr/learn/courses/30/lessons/67259# 
경주로 건설 문제
같은 위치라도 위에서 왔는지, 오른쪽에서, 왼쪽에서, 아래에서 왔는지 4가지를 따로 체크해줘야 한다.
$n^2 * 4$로 visited 배열을 선언해줘야 한다.
> 이문제를 특이한 DFS와 DP를 이용해서 풀었습니다.

---

> 제 생각을 그대로 썼기 때문에 틀린 부분이 있을 수 있습니다.
지적, 피드백 환영합니다.