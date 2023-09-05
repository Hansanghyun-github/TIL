### 징검다리 건너기

https://school.programmers.co.kr/learn/courses/30/lessons/64062

> 징검다리를 표현하는 배열이 주어지는데, 징검다리를 밟을때마다 수가 1씩 감소함, 수가 0이 되면 그 돌은 밟지 못함, 징검다리 배열과 한번에 건널 수 있는 최대 칸수 k가 주어졌을때 최대 몇명이 징검다리를 건널수 있는지 구하는 문제

사용한 알고리즘: 슬라이딩 윈도우
> 이분탐색도 있다고 하지만, 생각나지는 않음

시간복잡도: $O(n)$

`처음에 접근한 방법`<br>
k의 범위 내에서 제일 높은 값 -> 그 칸에서 최대로 건널수 있는 사람의 수
0부터 n-1까지 k 범위씩 해당 범위 에서 제일 높은 값을 찾고, 모든 결과중에서 가장 작은 값이 답이 되도록 풀었다.

여기서 최적화를 위해,<br>
다음 돌을 볼때 현재 버려야 하는 돌의 값이 max가 아니라면 -> 다음 범위로 가도 max값은 변하지 않음<br>
바로 다음 인덱스로 이동했고, <br>
새로 추가하는 돌의 값이 max보다 크지 않다면 -> 똑같이 max값 안변함<br>
바로 다음 인덱스로 이동했다.<br>
위에 해당하지 않는다면 다시 해당 인덱스에서 k번 검사하여 최댓값을 찾았다.

답은 맞지만, 시간복잡도가 $O((n-k)k)$라서 효율성 검사 13번에서 시간초과가 났다.

> 이 접근은 대부분의 케이스는 다른 알고리즘보다 시간이 덜 걸렸다.
> 
> 그런데 k=3일때, [20, 19, 18, 17, 16, 15, ...] 이런 배열이 주어지면 최적화의 의미가 없다.
>> 버리는 돌의 값이 max에 해당하고, 추가하는 돌의 값이 max보다 작기 때문에, 항상 k번 연산 진행됨
>
> 이런 케이스에 해당하면 시간초과가 났다. -> 그래서 통과못함

`다음으로 접근한 방법`<br>
이 접근은 다른 사람의 풀이를 보고 이해했다.

```deque<pair<int,int>>``` {돌의 값, 인덱스}를 저장

항상 deque에 k개의 돌을 추가하는데, 여기서 규칙이 있다.
> 항상 내림차순으로 정렬되어있음

인덱스가 k 범위를 벗어 났다면, 첫번째돌을 제거<br>
그리고 새로운 돌을 추가하는데, 마지막돌들이 새로운 돌보다 값이 작다면 마지막 돌들을 제거한다.
> 이렇게 되면 deque가 항상 내림차순으로 저장된다.

원래였다면 deque에 인덱스를 저장할 필요는 없지만, 중간중간 빠진 돌이 있기 때문에, 나중에 버릴수있는 돌이진 체크하기 위해 인덱스가 추가됨

항상 내림차순으로 정렬되어 있기 때문에, 맨 앞의 돌이 최댓값이다.

이 접근 방법은 모든 케이스에 대해 비슷한 시간복잡도가 나온다. - 문제 통과함

> 첫번째 접근은 조건부 케이스를 제외하고는 좋은 결과가 나왔지만, 특정 케이스에 대해 시간초과가 나옴<br>
> 두번째 접근은 항상 시간복잡도가 비슷하게 나왔다.

---

### 다단계 칫솔 판매

https://school.programmers.co.kr/learn/courses/30/lessons/77486

> 다단계 직원들의 구조가 주어졌을떄, 어떤 직원이 물건을 판매하면 해당 직원은 물건 값의 90%의 이익을 얻고, 부모노드는 10%의 이익을 얻는다. 이때 부모노드가 없을때까지 반복된다. 이런 관계에서 직원들의 구조와 판매자의 정보가 주어졌을떄, 전체 직원들의 수익은 얼마인지 구하는 문제

사용한 알고리즘: 트리, 해시

시간복잡도: $O(n * log m)$ - n은 판매자 배열의 길이, m은 직원수

그냥 직원에 해당하는 문자열과 배열에서의 위치 정보를 map(해시테이블)에 넣고<br>
판매자 배열을 for문으로 탐색하면 된다.

처음에는 수익이 최대 루트 노드까지 전달되기 때문에,<br>
시간복잡도가 $O(n*m)$ 이라고 생각했는데,

문제를 다시보니 판매량의 범위가 최대 10000원이라 아무리 부모노드를 많이 거쳐도 최대 5번밖에 탐색하지 않는걸 확인했다.

그냥 트리와 해시의 구현 문제였다.

---

### 파괴되지 않은 건물

https://school.programmers.co.kr/learn/courses/30/lessons/92344

> 2차원 배열 board의 값들이 주어지고, (r1,c1)부터 (r2,c2)까지 d만큼 값을 + or - 하라는 skill 배열이 주어졌을때, skill배열을 board에 모두 적용한후 board에 있는 값들중에 0보다 큰값은 몇개인지 구하는 문제

사용한 알고리즘: 누적합

시간복잡도: $O(n*m + k)$ // n=행, m=열, k = skill 배열 size

이 문제를 구현하는건 어렵지 않지만, 시간복잡도가 문제였다.

그냥 구현하면 시간복잡도는 $O(n*m*k)$가 나와 무조건 시간초과여서 손을 못대고 있어서,<br>
풀이를 봤는데,

누적합을 이용하는 문제였다.

ex) 1차원 배열에서 r1부터 r2까지 5를 더하라는 명령이 주어졌을때,

그냥 하나씩 더해줄수 있지만, 명령이 여러개라면 시간복잡도가 최대 $O(배열의 길이 * 명령의 개수)$가 된다.

여기서 누적합을 이용하면 $O(배열의 길이 + 명령의 개수)$로 줄일 수 있다.

> 예를 들어서 (1,3,4), (1,4,5), (2,5,-1) 배열이 주어지면 (r1,c2,d)<br>
> 처음 배열에 |0|4|0|0|-4|0|0| 이렇게 저장하고 그다음으로<br>
> |0|9|0|0|-4|-5|0| 이렇게 저장함<br>
>> r1에 d를 더해주고, r2+1에 d를 빼준다.
>
> 전체 계산을 다 끝내면, |0|9|-1|0|-4|-5|1| 이렇게 됨
>
> 그리고 왼쪽에서 오른쪽으로 누적합 진행
>
> 결과: |0|9|8|8|4|-1|0|
>
> 이는
>
> |0|4|4|4|0|0|, |0|5|5|5|5|0|, |0|0|-1|-1|-1|-1| 3개의 배열 전체를 더해준 것
>
> 즉 시간복잡도 $O(n*m)$을 누적합을 이용해 $O(n+m)$으로 줄일 수 있다.

위 과정을 2차원 배열에도 적용시킬 수 있다.

> 예를 들어서 (1,1)부터 (3,3)까지 5만큼 더해준다 했을때,
>
> 위 누적합을 이용하려면
>
>|0|0|0|0| -> |0|0|0|0|0|<br>
>|0|5|5|5| -> |0|5|0|0|-5|<br>
>|0|5|5|5| -> |0|5|0|0|-5|<br>
>|0|5|5|5| -> |0|5|0|0|-5|<br>
>
> 이렇게 저장한 뒤에, 왼쪽에서 오른쪽으로 누적합을 해줘야 하는데, <br>
> 여기서 행의 개수만큼 d와 -d를 저장해줘야 하기 때문에
>
> 시간복잡도는 $O((r2-r1) * 명령의 개수 + 열) => O(행 * 명령의 개수 + 행*열)$ (최대) 이렇게 된다.
>
> 이를 간단한 아이디어를 적용하여 $O(명령의 개수 + 행*열)$로 줄일 수 있다.
>>|0|0|0|0|0|<br>
>>|0|5|0|0|-5|<br>
>>|0|0|0|0|0|<br>
>>|0|0|0|0|0|<br> 
>>|0|-5|0|0|5|<br> 
>>
>> 처럼 저장 { (r1,c2)=d, (r1,c2+1)=-d, (r2+1,c1)=-d, (r2+1,c2+1)=d }
>>
>> 그다음으로 위에서 아래로 누적합 해준후, 왼쪽에서 오른쪽으로 누적합 진행하면 원래버전과 값이 같아진다.
>>
>> 위에서 아래로 누적합 진행<br>
>>|0|0|0|0|0|<br>
>>|0|5|0|0|-5|<br>
>>|0|5|0|0|-5|<br>
>>|0|5|0|0|-5|<br> 
>>|0|0|0|0|0|<br> 
>>
>> 왼쪽에서 오른쪽으로 누적합 진행<br>
>>|0|0|0|0|0|<br>
>>|0|5|5|5|0|<br>
>>|0|5|5|5|0|<br>
>>|0|5|5|5|0|<br> 
>>|0|0|0|0|0|<br>
>>
>> 시간복잡도: $O(k + n*m)$ 완벽

위의 누적합 아이디어를 적용시키면 2차원 배열에서의 누적합도

시간복잡도를 많이 줄일 수 있다. $O(k + n*m)$ { k:명령의 개수, n:행의 개수, m:열의 개수 }

---

### 보석 쇼핑

https://school.programmers.co.kr/learn/courses/30/lessons/67258

> 보석들의 이름이 담긴 배열이 주어졌을때, 모든 보석을 포함하는데, 길이가 가장 짧은 두 위치를 찾는 문제

사용한 알고리즘: 투포인터, 해시

시간복잡도: $O(n)$

첫 접근: 그리디 - 시간복잡도가 $O((보석의 개수)^n)$ 너무 높아서 포기

두번째 접근: dp - 시간복잡도가 $O(n^2)$ n이 최대 100000이라 포기

마지막 접근: 투포인터 - 좋은 접근이였지만 두 포인터 사이의 보석의 개수를 세는 부분을 제대로 체크 못해서 풀지 못했다.

나는 각 위치마다 몇개의 보석을 포함하고 있는지를 체크해주는 배열을 만들려고 했다.

필요한 배열 크기: n * 보석의 개수

시간복잡도: $O(n * 보석의개수)$ 너무 높아서 안될것같아서 못했다.

결국 찾은 답은,

처음부터 모든 보석을 세려고 하지 말고, 

해당 위치에 있는 보석만 추가해주면된다.

> 이렇게 할 수 있는 이유는, 배열의 특정 위치에는 `보석 한개`만 있기 때문이다.
>
> 만약 특정 위치에 보석 여러개가 있었다면 내가 생각한 알고리즘을 쓰는게 맞을수도 있다.

이 알고리즘의 시간복잡도: $O(n)$

---

### 불량 사용자

https://school.programmers.co.kr/learn/courses/30/lessons/64064?language=cpp

> string인 유저 아이디들과 제제 아이디가 주어졌을때, 제제 아이디로 가능한 경우의 수를 세는 문제

시간복잡도: 

사용한 알고리즘: dfs, 비트마스킹

1. 제제 아이디마다 제제가 가능한 아이디가 있을꺼임
그 아이들을 세준다.
    > st*가 제제 가능한 아이디들: sta, stb, stc, ...
    > 
    > 여기서 해당하는 유저 아이디들을 세준다.

    여기서 문자열 그대로 저장하지 않고 숫자로 저장한다. - 비트마스킹

2. dfs를 통해 가능한 경우의 수를 세준다.
    > set을 사용 - 중복 제거 위해

    > ex - 제제 가능한 유저아이디가 0,1,2,4 라면
    > 
    > 4210을 set에 저장한다. - 0이 앞에오면 생략됨 - 체크 불가능

3. set에 저장된 자료의 개수가 정답

---

### 블록 이동하기

https://school.programmers.co.kr/learn/courses/30/lessons/60063

> n x m 보드판에서 1,1 에 위치한 2x1 크기의 로봇이 n,m  위치까지 가는데 걸리는 최소시간을 구하는 문제

사용한 알고리즘: bfs

시간복잡도: $O(n * m)$

이 문제는 백준의 통나무 문제랑 비슷한 문제<br>
https://www.acmicpc.net/problem/1938


bfs의 응용 문제였음,

단순히 n*m visited를 체크하는게 아니라 로봇의 방향까지 체크해야했음

그리고 로봇이 움직일때, 회전할때마다 if문을 제대로 구현해야함

미리미리 설계해놓고, 구현은 거의 마지막에 하는게 좋다

그래야 실수를 덜한다.

---