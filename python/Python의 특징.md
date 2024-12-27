## 파이썬의 주요 특징

### 코드가 간결하고 가독성이 좋다

중괄호(`{}`) 대신 들여쓰기로 코드 블록을 구분하기 때문에 가독성이 좋다.

```python
for i in range(10):
    print(i)
```

### 자료형 변환이 자유롭다

```java
class Main{
    public static void main(String[] args){
        int a = 10;
        String b = Integer.toString(a);
    }
}
```

```python
a = 10
b = str(a)
```

### 문자열 처리가 편리하다

```python
a = 'hello'
print(f"안녕하세요, {a}")  # f-string
```

---