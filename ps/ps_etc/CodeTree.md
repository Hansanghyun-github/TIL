### 메이즈 러너 (삼성 기출)

https://www.codetree.ai/training-field/frequent-problems/problems/maze-runner/

> m명의 미로 참가자가 있다.<br>
> nxn 미로에는 빈칸, 벽(내구도 1~9), 출구가 있다.<br>
>
> 1초마다 다음을 수행한다.
> 1. 모든 참가자가 한칸씩 움직인다.(상하 우선, 출구와의 거리가 가까워지는 곳으로, 안 움직일수도 있음)
> 2. 미로가 회전한다.<br>
> 2-a 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형을 찾는다.(작은행, 작은열 우선)<br>
> 2-b 선택된 정사각형은 시계방향으로 90도 회전한다 & 벽은 내구도가 1 깎인다.
> 
> k초 동안 위 과정을 반복한다. 모든 사람이 탈출했다면 바로 종료<br>
> 모든 참가자들의 이동 거리 합과 출구 좌표를 출력한다.
>
> (사람은 같은 위치에 있을 수 있다)

사용한 알고리즘: 쌩 구현

시간복잡도: $O(k*n^3)$

이 문제를 풀려면 행렬(배열)의 회전 알고리즘에 대해 알고 있어야 했다.<br>
이런 알고리즘 문제를 한번도 해본적이 없어서 오래 걸렸다.

그냥 문제를 그대로 이해해서 구현하면 된다.

여기서 놓친 부분이 꽤 있었다.
1. 정사각형을 선택할때, 나는 그림만 보고 탈출구가 꼭짓점에 있다고 생각해 이상하게 구현을 했다.<br>
-> 그냥 3중 포문으로 일일이 보면서 탈출구와 사람을 포함하는 정사각형을 찾았다.
2. 사람이 같은 위치에 있을 수 있다는 것을 놓쳤다.

    처음에는 사람의 정보를 벡터로 따로 구현했지만, 정사각형이 회전할때 사람의 위치도 같이 변해야 하기 때문에, 이를 표현하기 위한 2차원 배열이 따로 필요했다.
    그리고 사람이 같은 위치에 있다면, 굳이 분리해서 관리할 필요 없이 그냥 사람수만 세줘도 충분히 풀수 있는 문제였다. -> 사람의 정보를 굳이 벡터로 따로 관리할 필요 없이, 2차원 배열에 사람수만 저장해놔도 충분히 가능한 문제
3. 각각의 메서드에서 사용하는 temp 배열을 공유하지 말자.<br>
미리미리 독립적인지 체크하고, 일단 처음에는 하나하나 다 따로 구현해놓자

    각각의 객체가 같은 위치에 있을 수 있다면, 이를 같이 관리할 수 있는지 체크해보자.
    각각의 코드가 독립적인지 체크하자 & 꼼꼼히 초기화 해놓자(삼성에 한해서 초기화는 꼼꼼히)

---

### 루돌프의 반란(삼성 기출)

https://www.codetree.ai/training-field/frequent-problems/problems/rudolph-rebellion/description

`사용한 자료구조 & 알고리즘:` 구현, 시뮬레이션

`시간복잡도:` $O()$

`어떻게 접근했는지, 풀었는지 설명:`

문제에서 나온대로 구현하는 문제  
(빡 구현 문제)

나는 산타의 정보를  
위치를 나타내는 2차원 배열 board와  
산타들의 상태를 나타내는 List를 이용해 구현했다.

여기서 놓친 부분
1. 산타가 이동했을 때 board 뿐만 아니라 list도 업데이트 해줘야 한다.  
   (이 부분은 디버깅으로 찾았다)
2. 산타가 밖으로 벗어나면 현재 산타의 수를 나타내는 CNT에 1을 빼줘야 하는데  
   이를 놓쳤다.  
   (런타임 에러가 발생했다)

> 2번을 놓친 이유는 모든 산타가 board를 벗어났을 때에 대한  
> 케이스를 테스트하지 않고 넘어갔기 때문이다.

---

### 고대 문명 유적 탐사(삼성 기출)

https://www.codetree.ai/training-field/frequent-problems/problems/ancient-ruin-exploration/description?page=1&pageSize=20

`사용한 자료구조 & 알고리즘:` 구현, 시뮬레이션

`시간복잡도:` $O()$

`어떻게 접근했는지, 풀었는지 설명:`

문제에서 나온대로 구현하는 문제  
(빡 구현 문제)

1. 각 위치에서 90,180,270 회전하는 경우에서 어떤 경우가 가장 높은 점수를 가지는지 확인
2. 점수가 0이라면 종료
3. 1번을 통해 얻은 위치,회전 정보를 가지고 회전시킨다.
4. 점수를 얻고, 각 위치의 조각들을 0으로 만든다.
5. 0인 위치들에 대해 인풋으로 받은 조각 후보들을 채워넣는다.
6. 다시한번 점수를 얻을 수 있는지 확인하고, 0으로 만들고, 5번을 반복한다.  
   (점수를 획들하지 못할 때까지 반복)

> 여기서  
> 1번에서 점수를 찾는 부분,  
> 4번에서 점수를 얻는 부분,  
> 6번에서 점수를 얻는 부분  
> 위 3가지를 한 메서드로 만들어서 사용했다.  
> 
> `int find(boolean erase)` - 현재 보드에서 얻을 수 있는 점수를 반환한다.  
> (erase가 true이면, 점수를 얻은 위치들을 0으로 만든다)  
> 
> 1번에서만 erase가 false로, 나머지에서는 true로 사용했다.



       이 문제를 풀면서
       여러 메서드를 생성하다 보니,
       나중엔 어떤 메서드가 어떤 역할을 하는지 헷갈렸다.
       이런 경우에는 메모장에 간단하게 메서드의 역할을 적어놓자.
       (수시로 확인하도록)

       2차원 배열에 여러 원소가 있는 상태에서,
       각 원소가 움직이려고 할 때,
       각 원소가 순서대로 바로 움직이는지 또는 모두 한 번에 같이 움직이는지 확인하자.
       전자는 그대로 구현하면 되지만,
       후자는 원소들의 움직임을 컨테이너에 넣고, 한 번에 움직이도록 구현해야 한다.

---

### 마법의 숲 탐색(삼성 기출)

https://www.codetree.ai/training-field/frequent-problems/problems/magical-forest-exploration/description?page=1&pageSize=5

`사용한 자료구조 & 알고리즘:` 

`시간복잡도:` $O()$

`어떻게 접근했는지, 풀었는지 설명:` 구현, 시뮬레이션

1. 골렘을 위에서 시작해서 못움직일 때까지 내려보낸다.
2. 골렘의 중심에 있던 정령이 최대한 갈 수 있는 행의 위치를 찾는다.
3. 찾은 위치를 결과에 더한다.
4. 위 과정을 반복한다.

> 1번에서 골렘이 보드 안에 들어오지 못하는 경우도 있다.  
> 골렘이 못들어오는 경우도 포함시키기 위해  
> 보드의 행의 길이를 R+3으로 설정했다.  
> (0,1,2 행에 골렘이 있다 -> 골렘이 못들어오는 경우)

        골렘이 못 들어오는 경우를 포함하기 위해  
        보드의 크기를 늘림으로써
        행 관련 범위 조건 검사를 할 때 
        항상 +3 을 해줘야 하는 것 때문에 번거로움이 있었다.
        -> 일단 +3 없이 써놓고 나중에 +3을 해주는 방법을 사용하자.

---