### gradle.properties에서 설정할 수 있는 속성들

org.gradle.console=(auto,plain,rich,verbose)<br>
: Gradle 속성을 통해 콘솔 모드를 지정

plain: 일반 텍스트 생성, 콘솔 출력에서 모든 색상 및 기타 풍부한 출력을 비활성화함

rich: 콘솔 출력에서 색상 및 기타 풍부한 출력을 활성화

auto(default): 콘솔에 연결될 때 콘솔 출력에서 색상 및 기타 풍부한 출력을 활성화하거나 콘솔에 연결되지 않은 경우에만 일반 텍스트를 생성

org.gradle.jvmargs: Set JVM arguments.

org.gradle.jvmargs=-Dfile.encoding=UTF-8<br>
: 인코딩 방식을 UTF-8로 설정
