# VARCHAR vs TEXT

TEXT는 큰 문자열 저장에 쓰여 주로 게시판의 본문을 저장할때 쓴다고 한다.

TEXT type은 일반 문자열을 저장할 때 많이 쓰이는 VARCHAR type과 어떤 점이 다를까?

~~만약 저장 & 동작하는 방식이 같다면 VARCHAR을 쓰는 의미가 없을 것이다~~  
~~어차피 작은 문자열도 TEXT로 저장하면 되니까~~

---

### 저장할 수 있는 데이터의 양

VARCHAR은 최대 655,535자까지 가변 길이의 문자열을 저장할 수 있다.

TEXT는 최대 4기가바이트까지 대용량의 데이터를 저장할 수 있다.  
($2^{32} - 1$)

---

### 저장하는 방식

VARCHAR은 가변 길이의 데이터를 저장하기 때문에, 저장공간의 양은 그 길이에 따라 달라진다.

TEXT는 정적 길이 형식으로 저장되기 때문에, 저장공간의 양은 일정하다.

---

### 용도

VARCHAR은 일반적인 이름, 위치와 같은 짧은 길이에서 중간 길이의 문자열을 저장하는 데 적합하다.

TEXT는 기사, 댓글, 메시지와 같은 데이터를 저장하는데 적합하다.

---

### 성능

VARCHAR은 저장 용량이 적고 데이터에 대한 접근 속도가 빠르기 때문에,  
VARCHAR이 TEXT보다 성능이 우수하다.

// TODO

---

|Feature|TEXT|VARCHAR|
|--|--|--|
|Data Length|$2^{32}-1$|65536|
|Storage|stored static form|variable|
|Performance|Slower|Faster|
|Indexing|Not Possible|Possible|

---

### Reference

https://medium.com/daangn/varchar-vs-text-230a718a22a1

https://www.scaler.com/topics/varchar-vs-text-mysql/