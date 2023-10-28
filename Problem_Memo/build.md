### java.io.IOExcetion: 파이프가 닫히는 중입니다.
오류 : 기본 클래스 worker.org.gradle.process.internal.worket.GradleWorkerMain을(를) 찾거나 로드할 수 없습니다.

./gradlew.bat clean test 명령어를 실행 중에 일어난 문제

(직접 IDE에서 테스트했을 때는 문제가 없었다)

이 문제를 해결하는 방법은 두가지가 있다.

1. Build and run using과 Run tests using 환경을 Gradle -> IntelliJ IDEA로 설정 후 실행
2. 경로에 한글이 있는지 검사 -> 영어로 바꿔야 한다.

> 이때 윈도우 사용자명이 한글이라면, 포맷을 해서 영어 이름으로 바꿔야 한다...

---