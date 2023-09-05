### 1309 동물원


💡 2*n 우리가 있을때 넣을수있는 사자의 경우의수를 구하는 문제



dp[0][n] = dp[0][n-1]+dp[1][n-1]+dp[2][n-1]

dp[1][n] = dp[0][n-1]+dp[2][n-1]

dp[2][n] = dp[0][n-1]+dp[1][n-1]

답: dp[0][n]+dp[1][n]+dp[2][n]

풀이

n번째 우리에서의 경우의 수는

n-1 우리에서 바로전 우리(n-1번째 울타리)에 사자가 있을때, 왼쪽에 있을떄, 오른쪽에 있을때

가 0,1,2 면

0에서 n번째 울타리에 사자를 안 넣거나, 왼쪽에 넣거나, 오른쪽에 넣거나

1에서 n번째 울타리에 사자를 안 넣거나, 오른쪽에 넣거나

2에서 n번째 울타리에 사자를 안 넣거나, 왼쪽에 넣거나

즉 n번째 울타리에 사자를 안넣은 경우의 수 - 0+1+2 (n-1 기준)

즉 n번째 울타리에 사자를 왼쪽에 넣은 경우의 수 - 0+2 (n-1 기준)

즉 n번째 울타리에 사자를 오른쪽에 넣은 경우의 수 - 0+1 (n-1 기준)

식을 정리하면

dp[0][n]+dp[1][n]+dp[2][n] = (dp[0][n-1]+dp[1][n-1]+dp[2][n-1])*2 + dp[0][n-1]

= dp[n-1]*2+dp[n-2] (깔끔)

[](https://www.notion.so/c6a513154d0b4066bdee4bf721bb2a80?pvs=21)

---

### 1520 내리막길 & 1937 욕심쟁이 판다


💡 그래프와 dp가 섞인 문제

1520은 경우의수, 1937은 경우의수중 최댓값 구하는 문제



2차원 배열이 주어지는데, 각 위치마다 값이 있고

상하좌우의 값을 비교해서 값보다 작다면(크다면) 이동할수 있음

그상황에서 가장 많은 경우의 수 or 최대 이동값을 찾는 문제

⇒ 우선순위 큐를 이용, 내림차순(오름차순)으로 정렬후 한개씩 받아서 현재위치 dp값+1이

다음위치 dp값보다 크다면 저장함.

이게 성립하는 이유는 (내림차순 기준), 무조건 값이 작을때만 이동할수 있기때문에, 가장 큰값을 쓰면 그 위치는 다시 갈수없다. 따라서 dp가 적용됨

[](https://www.notion.so/c6a513154d0b4066bdee4bf721bb2a80?pvs=21)

---

### 1725 히스토그램

https://www.acmicpc.net/problem/1725

> 막대그래프가 주어졌을때 막대그래프에 대해, 가장 큰 직사각형의 넓이를 구하는 문제

사용한 알고리즘: 분할 정복

시간복잡도: $O(nlgn)$

종만북을 보면서 이 문제를 풀 수 있었다.

브루트포스는 $O(n^2)$이 걸리지만, 분할정복을 사용해서 시간복잡도를 더 줄일 수 있었다.

    가운데 좌표를 기준으로
    1. 왼쪽 블럭만으로 구하는 최대 넓이
    2. 오른쪽 블럭만으로 구하는 최대 넓이
    3. 가운데 좌표를 포함했을때 구하는 최대 넓이

    위 세가지중 최대 넓이가 정답이다.

가운데 좌표를 포함하는 직사각형의 최대넓이를 구하는 방법은,<br>
가운데에서 시작해서, 왼쪽 높이와 오른쪽 높이를 비교해서 더 높은쪽으로 좌표를 옮긴다.(투포인터)

위 방법을 계속하면 최대 넓이를 구할 수 있다.

    왼쪽 오른쪽 좌표를 옮길때 좌표가 범위를 벗어나는 걸 생각해야하는데
    처음부터 이를 포함해서 if문을 짜지 말고,
    한개씩 전부다 if문으로 일일이 짜주자
    그래야 빠르다

---

### 1806 부분합
> n개의 자연수로 이루어진 수열이 주어졌을때, 
> 이 수열에서 연속된 수들의 부분합 중에 그 합이 s 이상 되는 것중 가장 짧은 것의 길이를 구하는 문제

시간복잡도 $O(n)$
두개의 포인터 l,r (l=0, r=1), result = MAX (MAX > n)

l번째 위치부터 r-1번째 위치까지의 합을 cur이라 하면

cur < s 일때 l++

cur >=s 일때 r++,
현재 r - l 이 result보다 작다면 result = r - l

답은 result

---

### 1915 가장 큰 정사각형


💡 2차원 배열이 주어졌을때, 해당 배열중 가장 큰 정사각형의 넓이를 찾는 문제



나는 누적합을 이용해서 겨우 풀었지만

dp를 이용한 방법은 몰랐다.

if (board[i][j] == '1') dp[i][j] = min(dp[i - 1][j - 1], min(dp[i - 1][j], dp[i][j - 1])) + 1;

dp는 해당 위치에서의 정사각형의 최대 길이

풀이

1 1

1 1

이 정사각형이 있다면, min(1,min(1,1))+1 = 2

1 1

0 1

이라면, min(1, min(0,1)) + 1 = 1

결국 모두 1로 채워져야 최대값이 갱신된다.

dp는 많이 풀어봐야 한다.

---

### 2293 동전 1


💡 n가지 종류의 동전이 주어졌을때, 이 동전을 이용해서 합이 k원이 되는 경우의 수를 구하는 문제

(동전은 무제한 이용 가능)



시간복잡도: $O(n)$

dp[0]=1 (0원일때의 경우의 수)

i - 0 ~ n-1 (모든 동전들 탐색)

j - 0 ~ k (0원부터 k원까지 탐색)

if(j ≥ coin[i])

dp[j] += dp[j - coin[i]];

dp[k]가 정답

풀이

1,2,5원을 이용해서 k원까지의 경우의수를 구하는 과정

1 - 1

2 - 11, 2

3 - 111, 12

4 - 1111, 112, 22

5 - 11111, 11122, 122, 5

…

여기서 4원을 보면 1원만 쓴 경우의 수와(1111),

2원에서 2를 더한 경우의 수(112, 22)

5원은 1원만 쓴 경우의 수(11111),

3원에서 2를 더한 경우의 수(11122, 122)에 5를 새로 추가

이를 점화식으로 표현하면

dp[i] = dp[i - coin[1]] + dp[i - coin[2]] + … + dp[i - coin[n]]

결국 dp[0]부터 … dp[k]까지 구하면 정답나옴

[](https://www.notion.so/c6a513154d0b4066bdee4bf721bb2a80?pvs=21)

---

### 2294 동전 2


💡 n가지 종류의 동전이 주어졌을때, 이 동전을 이용해서 합이 k원이 될때 사용한 동전의 개수가 최소일때의 동전의 개수를 구하는 문제

(동전은 무제한 이용 가능)



시간복잡도: $O(n^2)$

dp[0]=MAX (못구함)

i - 0 ~ k (0원부터 k원까지 탐색)

j - 0 ~ n-1 (모든 동전들 탐색)

if (coin[j] ≤ i)

dp[i] = min(dp[j], dp[i - coin[j]] + 1);

풀이

1,2,5원이 있을때

3원은 1원3개 or 1원,2원으로 구할수있음

5원은 1원5개,1원1개,2원2개, 1원3개,2원1개, 5원1개로 구할수있음

여기서 5원은 3원+2원 or 4원+1원임

따라서 점화식은

dp[i] = min(dp[i-coin[1]], dp[i-coin[2]], … , dp[i-coin[n]]) + 1이다.

[](https://www.notion.so/c6a513154d0b4066bdee4bf721bb2a80?pvs=21)

---

### 2565 전깃줄


💡 남아있는 모든 전깃줄이 서로 교차하지 않게 하기 위해 없애야 하는 전깃줄의 최소 개수를 구하는 문제



시간복잡도: $O(n^2)$

v[i] - {i번째 전깃줄 번호, 가리키는 전깃줄 번호}

sort(v, v.first순으로)

v.second로 LIS구하면 끝

풀이

v를 정렬후에 각각의 전깃줄이 가리키는 번호가

{8,2,9,1,4,6,7,10}일때 없애야 하는 전깃줄은

1,3,4이다.(1,2,3도 가능) 1,3,4를 없애면

{8,**2**,9,1,**4**,**6**,**7**,**10**} - 2,4,6,7,10이다.

이는 LIS를 구하는 문제랑 같음

그냥 LIS 실생활 응용문제였음

[](https://www.notion.so/c6a513154d0b4066bdee4bf721bb2a80?pvs=21)

---

### 2579 계단 오르기


💡 계단에 해당하는 점수가 주어졌을때 3번연속 밟지않고, 마지막 계단을 밟았을때의 최댓값 구하는 문제



시간복잡도: O(n)

방법1

1번 연속으로 밟았을때의

dp[i] = max(dp[1][i-2],dp[2][i-2])+x[i];

2번 연속으로 밟았을때의

dp[i] = dp[i-1]+x[i];

답: max(dp[1][n],dp[2][n])

방법2

dp - 현재 위치에서 계단 밟았을때의 최댓값

dp[i] = max(dp[i-2]+x[i], dp[i-3]+x[i-1]+x[i]);

답: dp[n]


💡 dp[i-1]을 사용하지 않고 x[i-1]을 사용하니까 3번연속금지에 위배되지않음



[](https://www.notion.so/c6a513154d0b4066bdee4bf721bb2a80?pvs=21)

---
### 2636 치즈

https://www.acmicpc.net/problem/2636

> 문제 설명

사용한 알고리즘: bfs

시간복잡도: $O(n^3)$

이전에 이런 문제를 푼적이 있었다.<br>
https://www.acmicpc.net/problem/2638<br>
똑같은 문제였네

그냥 bfs를 이용하는 구현 문제,

여기서 치즈 안에 있는 구멍이랑, 치즈 밖에 있는 구멍을 구분해야 함

여기서 치즈를 보지말고, 가장자리에 붙어 있는 구멍을 보면됨

가장자리에 붙어 있는 치즈는 녹을 치즈

0,0에서 bfs돌리면 끝

그리고 치즈가 남았는지 체크할때 일일이 탐색하지 말고, 이전 bfs 과정중에 치즈 개수를 세주면됨

이전 치즈 개수 - 현재 제거되는 치즈 개수 => 이 값이 0이되면 break