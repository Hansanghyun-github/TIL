## Gradle의 활용

```
plugins {

}

repositories {
    mavenCentral()
}

dependencies{
    implementation ...
    compileOnly ...

    testImplementation ...

    runtimeOnly ...

}
```

### 1. plugins
특정 작업을 위해 모아놓은 task들의 묶음

(dependency에서 자주 쓰는 애들을 task들의 묶음으로 만든다)



### 2. dependencies
프로젝트에서 사용하는 라이브러리나 패키지를 `의존성`이라고 한다.

프로젝트별로 어떤 의존성을 갖는지 명시해주어야 한다.

이떄 특정 시점에만 라이브러리를 추가할 수 있다.

(특정 시점외에 라이브러리가 있으면, 이는 리소스 낭비이기 때문)

```api``` - 내부 의존성을 컴파일과 런타임 모두에 보이는 API 의존성

```implementation``` - 내부 의존성을 런타임에서만 보이는 구현 의존성

```compileOnly``` - 컴파일에만 사용되는 의존성 정의

```runtimeOnly``` - 런타임에만 사용되는 의존성 정의

test + Implementation, CompileOnly, RuntimeOnly - 해당 의존성을 테스트 시에만 사용하도록 정의

### 3. repositories

dependency에서 사용한다고 추가했던 라이브러리가 저장된 위치를 정의한다.

대표적으로 mavenCentral()이 있다

라이브러리의 저장소를 명시해주면 Gradle이 해당 저장소에서 필요한 라이브러리를 가져온다.

### 4. gradle의 전역변수

```
buildscript{
    ext{
        queryDslVersion = "5.0.0"
    }
}
```

메소드 내에서 전역 변수를 사용할 때는 `${variableName}` 을 쓰면 된다.

---

## regular project -> gradle project 로 convert 하는 방법

1. 프로젝트의 루트 폴더에 build.gradle 파일 생성
2. build.gradle 파일 작성 후, 해당 프로젝트를 re-open