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