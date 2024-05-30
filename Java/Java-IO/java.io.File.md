# File 클래스란

파일 및 디렉토리의 정보를 제공해주는 역할을 하는 클래스

문자열을 파라미터로 받아서 생성한다.

```File file = new File("C:\\Temp\\file.txt")"```

> File 클래스가 절대경로와 상대경로를 구분하는 기준
> 
> / 가 있냐 없냐에 따라 구분한다. ( or \\)
> 
> 절대경로: ```file = new File("C:/Users/User/Desktop/test.txt")```  
> 상대경로: ```file = new File("test.txt") // 현재 ```  
> (상대경로의 기준은 현재 작업 디렉토리가 기준이 된다)

---

## File 클래스의 기능

### File 클래스의 기능 1 - 파일/디렉토리의 생성 및 삭제

createNewFile(), mkdir(), mkdirs(), delete() 메서드들을 통해, File 객체에 해당하는 경로에 파일/디렉토리를 생성할 수 있다.

### File 클래스의 기능 2 - 파일/디렉도리의 정보 확인

exists(), isFile(), isDirectory(), getName(), getPath(), getParent(), length()  
메서드들을 통해 해당 파일/디렉토리의 정보를 확인할 수 있다.

### File 클래스의 기능 3 - 디렉토리 내 하위 폴더/디렉토리 확인

list(), listFiles() 메서드들을 통해,  
디렉토리 내의 파일과 하위 디렉토리를 알 수 있다.

> 이 외에도 다양한 기능이 있다고 한다.

---

## File 클래스의 한계점

1. Blocking I/O의 한계  
   java.io.File은 기본적으로 Blocking I/O만을 지원한다.  
   이는 파일 작업이 끝날 때까지 스레드가 blocking 되어 다른 작업을 수행할 수 없다는 의미이다.
2. 디렉터리 및 파일 조작의 제한  
   java.io.File은 디렉터리를 다루는 데에 제약이 있다. 디렉터리를 조작하거나 디렉터리 내의 파일 목록을 검색하는 작업이 다소 불편하다.
   
> 위 한계점들을 개선한 java.nio.file 패키지가 이후에 나와, 현재는 이것들을 권장한다고 한다.  
> (java.io.File 클래스가 제공하는 기능 외에 다양한 기능이 추가됐다고 한다)