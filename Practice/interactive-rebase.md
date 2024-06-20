### interactive rebase 연습

![img.png](../img/interactive_rebase_1.png)

5개의 커밋

![img_1.png](../img/interactive_rebase_2.png)

각 커밋이 한줄씩 추가했다.

![img_2.png](../img/interactive_rebase_10.png)

첫번째 커밋 이전의 커밋 해시값을 이용해 interactive rebase 실행

> 내가 수정하고 싶은 커밋이 있다면,  
> 해당 커밋 이전의 커밋 해시값을 이용해야 한다.

`git rebase -i 5953de2`

![img_4.png](../img/interactive_rebase_7.png)

첫번째 커밋부터 현재 커밋까지  
모든 커밋의 리스트가 vim 에디터로 표시됐다.

> {명령어} {커밋 해시값} {커밋 메시지} 로 구성되어 있다.

여기서 vim 에디터를 이용해 수정해야 한다.

---

### interactive rebase 명령어

커밋 유지 - `pick`  
(default로 설정되어 있는 명령어)

커밋 삭제 - `drop`  
(또는 삭제할 커밋 라인을 지우는 것으로도 가능하다)

커밋 순서 바꾸기 - 에디터에서 순서를 바꾸면 된다.

커밋 메시지 수정 - `reword`  
pick을 해당 명령어로 수정하고, 저장 & 종료하면,  
해당 커밋 메시지를 수정하기 위한 에디터가 열린다.

> 커밋 메시지와 작업까지 동시에 수정하는 명령어는 `edit`

커밋 합치기 - `squash`, `fixup`  
둘 다 이전의 커밋과 합치는 명령어이다.

> 

---

### interactive rebase 결과

![img_6.png](../img/interactive_rebase_5.png)

첫번째 커밋은 reword를 이용해 메시지를 수정했다.  
네번째 커밋과 다섯번째 커밋은 합쳤다.

![img_7.png](../img/interactive_rebase_3.png)  
(첫번째 커밋 메시지를 수정하는 캡처 사진)

`결과`

![img_8.png](../img/interactive_rebase_6.png)
![img_9.png](../img/interactive_rebase_4.png)

첫번째 커밋 메시지가 수정됐고,  
4번째 커밋과 5번째 커밋이 합쳐졌다.

---

### interactive rebase 주의사항

이 명령어는 기존의 커밋을 수정하는 작업이기 때문에,  
원격 리포지토리에 푸시된 커밋들을 로컬에서 rebase 하여  
푸시하는 일은 지양해야 한다.

> 이 명령어는 내가 한 작업을 PR 올리기 전에  
> 커밋을 깔끔하게 하는 작업을 할때 유용한 명령어인 것 같다.