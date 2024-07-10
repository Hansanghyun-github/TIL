스프링 프로젝트를 빌드할 때 자주 사용하는 명령어

`./gradlew build`

위 명령어를 사용하면 어떻게 프로젝트가 빌드되는지 궁금해졌다.

> maven을 이용한 빌드도 있지만,  
> gradle을 더 많이 사용하여 gradle을 이용한 빌드를 살펴보기로 했다.

---

## gradlew 파일

해당 파일은 스크립트 파일이다.

> 맨 첫 줄에 `#!/bin/sh`가 있다.

전체적으로 하는 일은,

현재 디렉토리 경로를 app_path에 저장하고,
절대경로는 APP_HOME에 저장한다.

JAVA_HOME의 java or path 환경변수의 java 경로를 JAVACMD에 저장한다.

그리고 java 명령어를 실행하기 위해, 세팅할 옵션들을 설정한다.

마지막으로 java 명령어를 실행한다.  

gradle/wrapper/gradle-wrapper.jar 파일을 실행한다.  
이때 실행하는 메서드 이름은 `org.gradle.wrapper.GradleWrapperMain`이다.

---

### set --

gradlew 파일 코드 중에 재밌는 점은,  
set 명령어를 이용해 java 명령어의 옵션들을 설정한다.

`set --` 명령어를 통해 위치 매개변수를 설정한다.

> `set` 명령어는 환경변수를 설정하는 명령어이다.  
> `--` 옵션을 통해 위치 매개변수를 설정할 수 있다.

```bash
set -- \
        "-Dorg.gradle.appname=$APP_BASE_NAME" \
        -classpath "$CLASSPATH" \
        org.gradle.wrapper.GradleWrapperMain \
        "$@"
```

위 코드를 통해  
`$1`로 `-Dorg.gradle.appname=$APP_BASE_NAME`를 설정하고,  
`$2`로 `-classpath "$CLASSPATH"`를 설정하고,  
`$3`로 `org.gradle.wrapper.GradleWrapperMain`를 설정한다.

`$@`는 모든 매개변수를 의미한다.  
-> `$4`, `$5`, ... 로 설정된다.

그리고 마지막 코드에서 java 명령어를 실행한다.

`exec "$JAVACMD" "$@"`

`"$@"` 를 통해 지금까지 설정한 모든 위치 매개변수가 java 명령어의 옵션으로 설정된다.

---

### gradlew 파일 정리

OS 별로 설정한 다음  
java 명령어를 실행하는 스크립트 파일이다.

`./gradlew build` 명령어를 실행했을 때 마지막으로 실행되는 java 명령어 실행 예시
`java -Xmx64m -Xms64m -Dorg.gradle.appname=gradlew -classpath /{path}/gradle/wrapper/gradle-wrapper.jar org.gradle.wrapper.GradleWrapperMain build`

---