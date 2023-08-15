# 다익스트라 알고리즘

그래프에서 한 정점에서 모든 정점으로의 최단거리를 찾는 알고리즘

DP, 우선순위 큐(힙)를 사용하는 알고리즘
> 모든 간선이 0보다 크다는걸 가정한다.

---

### 과정
1. 첫번쨰 정점에서 갈수 있는 모든 정점으로의 거리로 dp 배열을 업데이트
2. 현재 dp 배열에서 가장 값이 낮은 정점을 기준으로 탐색
3. 현재 위치 x에서 갈수있는 다른 정점 y로의 거리 + dp[x] < dp[y] 라면 dp[y]를 업데이트
4. 2,3 과정을 계속 반복하여 dp배열을 업데이트

---

시간복잡도: $O(ElgE)$

---

실제코드

```cpp
vector<int> dp; // 한 정점에서 다른 정점으로의 최단거리
vector<vector<pair<int, int>>> node; // {가중치, 목표노드}
priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
// {가중치, 목표노드}

pq.push({ 0,c }); // c가 시작노드
dp[c] = 0;

int len;
pair<int, int> cur;
int distance, next;
while (!pq.empty()) {
    cur = pq.top();
    pq.pop();

    if (cur.first > dp[cur.second]) continue;
    len = node[cur.second].size();
    for (int i = 0; i < len; i++) {
        next = node[cur.second][i].second;
        distance = node[cur.second][i].first + cur.first;
        if (dp[next] > distance) { // 기존 거리 > 새로운노드를 이용한 거리
            dp[next] = distance;
            pq.push({ distance,next });
        }
    }
}
```