# 12 새로운 날짜와 시간 API

기존 자바 1.0 java.util.Date 클래스를 통해 날짜 구하기
```java
Date date =  new Date(117, 8, 21);
// Thu Sep 21 00:00:00 CET 2017
```

직관적이지 않다.

이외에도 Calender, DateFormat 등 여러 클래스를 제공했지만, 문제가 조금씩 있었다.

결국 자바 8에서는 Joda-Time 서드파티의 많은 기능을 java.time 패키지로 추가했다.

## 12.1 LocalDate, LocalTime, Instant, Duration, Period 클래스

### 12.1.1 LocalDate와 LocalTime 사용

LocalDate 인스턴스는 시간을 제외한 날짜를 표현하는 불변 객체다.
```java
LocalDate date = LocalDate.of(2014, 3, 18);
int year = date.getYear(); // 2014
Month month = date.getMonth(); // MARCH
int day = date.getDayOfMonth(); // 18
DayOfWeek dow = date.getDayOfWeek(); // TUESDAY
int len = date.lengthOfMonth(); // 31 (3월의 길이)
boolean leap = date.isLeapYear(); // false (윤년이 아님)
```

팩토리 메서드 now는 시스템 시계의 정보를 이용해서 현재 날짜 정보를 얻는다.<br>
```LocaleDate today = LocalDate.now();```

get 메서드에 TemporalField를 전달해서 정보를 얻는 방법도 있다.<br>
TemporalField는 시간 관련 객체에서 어떤 필드의 값에 접근할지 정의하는 인터페이스이다.<br>
TemporalField의 구현체인 ChronoField의 열거자 요소를 이용해서 원하는 정보를 쉽게 얻을 수 있다.

```java
int y = date.get(ChronoField.YEAR);
int m = date.get(ChronoField.MONTH_OF_YEAR);
int d = date.get(ChronoField.DAY_OF_MONTH);
```

다음처럼 내장메서드 getYear(), getMonthValue(), getDayOfMonth() 등을 이용해 가독성을 높일 수 있다.

```java
int y = date.getYear();
int m = date.getMonthValue();
int d = date.getDayOfMonth();
```

마찬가지로 13:45:20 같은 시간은 LocalTime 클래스로 표현할 수 있다.

```java
LocalTime time = LocalTime.of(13, 45, 20); // 13:45:20
int hour = time.getHour(); // 13
int minute = time.getMinute(); // 45
int second = time.getSecond(); // 20
System.out.println(time);
```

날짜와 시간 문자열로 LocalDate와 LocalTime의 인스턴스를 만드는 방법도 있다. 다음처럼 parse 정적 메서드를 사용할 수 있다.

```java
LocalDate date = LocalDate.parse("2017-09-21");
LocalTime time = LocalTIme.parse("13:44:24");
```

parse 메서드에 DateTimeFormatter를 전달할 수 있다.
> DateTimeFormatter의 인스턴스는 날짜, 시간 객체의 형식을 지정한다.
>
> java.util.DateFormat 클래스를 대체하는 클래스다.

문자열을 파싱할 수 없을때, DateTimeParseException을 일으킨다.

### 12.1.2 날짜와 시간 조합

LocalDateTime은 LocalDate와 LocalTime을 쌍으로 갖는 복합 클래스다.<br>
LocalDate의 atTime 메서드에 시간을 제공하거나 LocalTime의 atDate 메서드에 날짜를 제공해서 LocalDateTime을 만드는 방법도 있다.

    LocalDateTime을 LocalDate나 LocalTime으로 변환하는 방법도 있다.

### 12.1.3 Instant 클래스: 기계의 날짜와 시간

사람은 보통 주, 날짜, 시간, 분으로 날짜와 시간을 계산한다. 하지만 기계에서는 이와 같은 단위로 시간을 표현하기가 어렵다. 기계의 관점에서는 연속된 시간에서 특정 지점을 하나의 큰수로 표현하는 것이 가장 자연스러운 시간 표현 방법이다.

이를 java.time.Instant 클래스가 기계적인 관점에서 시간을 표현한다.<br>
Instant 클래스는 유닉스 에포크 시간(1970-01-01 00:00:00 UTC)을 기준으로 특정 지점까지의 시간을 초로 표현한다.

팩토리 메서드에 ofEpochSecond에 초를 넘겨줘서 Instant 클래스 인스턴스를 만들 수 있다. Instant 클래스는 나노초(10억분의 1초)의 정밀도를 제공한다.<br>
또한 오버로드된 ofEpochSecond 메서드 버전에서는 두번째 인수를 이용해서 나노초 단위로 시간을 보정할 수 있다.(0 ~ 999,999,999)

Instant 클래스도 사람이 확인할 수 있도록 시간을 표시해주는 정적 팩토리 메서드 now를 제공한다.

    Instant에서는 Duration과 Period 클래스를 함께 활용할 수 있다.

### 12.1.4 Duration과 Period 정의

지금까지 살펴본 모든 클래스는 Temporal 인터페이스를 구현하는데, Temporal 인터페이스는 특정 시간을 모델링하는 객체의 값을 어떻게 읽고 조작할지 정의한다.

Duration 클래스의 정적 팩토리 메서드 between으로 두 시간 객체 사이의 지속시간을 만들 수 있다. 다음 코드에서 보여주는 것처럼 두 개의 LocalTime, 두개의 LocalDateTime, 두개의 Instant로 Duration을 만들 수 있다.

    Duration 클래스는 나노초로 시간 단위를 표현하므로 between 메서드에 LocalDate를 전달할 수 없다.

년, 월, 일로 시간을 표현할때는 Period 클래스를 사용한다. - LocalDate 사용

마지막으로 Duration과 Period 클래스는 자신의 인스턴스를 만들 수 있도록 다양한 팩토리 메서드를 제공한다.

---

지금까지 살펴본 모든 클래스는 불변이다. 불변 클래스는 함수형 프로그래밍 그리고 스레드 안전성과 도메인 모델의 일관성을 유지하는데 좋은 특징이다.

## 12.2 날짜 조정, 파싱, 포메팅

withAttribute 메서드로 기존의 LocalDate를 바꾼 버전을 직접 간단하게 만들 수 있다.
```java
LocalDate date1 = LocalDate.of(2017, 9, 21); // 2017-09-21
LocalDate date2 = date1.withYear(2011); // 2011-09-21
LocalDate date3 = date2.withDayOfMonth(25); // 2011-09-25
LocalDate date4 = date3.with(ChronoField.MONTH_OF_YEAR, 2) // 2011-02-25
```

위 메서드들은 년, 월, 일을 주어진 값으로 세팅하는 메서드들

아래 메서드들은 지정된 시간을 추가하거나 뺄 수도 있다.
```java
LocalDate date1 = LocalDate.of(2017, 9, 21); // 2017-09-21
LocalDate date2 = date1.plusWeeks(1); // 2017-09-28
LocalDate date3 = date2.minusYears(6); // 2011-09-28
LocalDate date4 = date3.plus(6, ChronoUnit.MONTHS) // 2012-03-28
```

    LocalDate는 불변 클래스라서, 해당 값이 변하지는 않는다.
    date.withYear(2011); // 아무 일도 일어나지 않음

### 12.2.1 TemporalAdjusters 사용하기

때로는 다음주 일요일, 돌아오는 평일, 어떤 달의 마지막 날 등 좀 더 복잡한 날짜 조정기능이 필요할 것이다.<br>
이때는 오버로드된 버전의 with 메서드에 좀 더 다양한 동작을 수행할 수 있도록 기능을 제공하는 TemporalAdjuster를 전달하는 방법으로 문제를 해결할 수 있다.
```java
import static java.time.temporal.TemporalAdjusters.*;

LocalDate date = LocalDate.of(2014, 3, 18); // 2014-03-18
date = date.with(nextOrSame(DayOfWeek.SUNDAY)); // 2014-03-23
date = date.with(lastDayOfMonth()); // 2014-03-31
```

이뿐만 아니라 필요한 기능이 정의되어 있지 않을 때는 비교적 쉽게 커스텀 TemporalAdjuster 구현을 만들 수 있다.
```java
@FunctionalInterface
public interface TemporalAdjuster {
    Temporal adjustInto(Temporal temporal);
}
```

TemporalAdjuster 인터페이스 구현은 Temporal 객체를 어떻게 다른 Temproal 객체로 변할지 정의한다.

    TemporalAdjuster를 람다 표현식으로 정의하고 싶다면 UnaryOperator<LocalDate>를 인수로 받는 TemporalAdjusters 클래스의 정적 팩토리 메서드 ofDateAdjuster를 사용하는 것이 좋다.

### 12.2.2 날짜와 시간 객체 출력과 파싱

java.time.format 패키지에서 가장 중요한 클래스는 DateTimeFormatter다.

이 클래스는 정적 팩토리 메서드와 상수를 이용해서 손쉽게 포매터를 만들 수 있다.<br>
-> DateTimeFormatter를 이용해서 날짜나 시간을 특정 형식의 문자열로 만들 수 있다.

    DateTimeFormatter는 스레드에서 안전하게 사용할 수 있는 클래스다.

```java
LocalDate date = LocalDate.of(2014, 3, 18); // 2014-03-18

// DateTimeFormatter 클래스는 BASIC_ISO_DATE와 ISO_LOCAL_DATE 등의 상수를 미리 정의하고 있다.
String s1 = date.format(DateTimeFormatter.BASIC_ISO_DATE); // 20140318
String s2 = date.format(DateTimeFormatter.ISO_LOCAL_DATE); // 2014-03-18

// 특정 패턴으로 포매터를 만들 수 있는 정적 메서드도 제공한다.
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
String formattedDate = date.format(formatter); // 18/03/2014
LocalDate date1 = LocalDate.parse(formattedDate, formatter);

// 이외에도 많음
```

## 12.3 다양한 시간대와 캘린더 사용 방법

새로운 날짜와 시간 API의 큰 편리함 중 하나는 시간대를 간단하게 처리할 수 있다는 점이다.

기존의 java.util.TimeZone을 대체할 수 있는 java.time.ZoneId 클래스가 새롭게 등장했다.

### 12.3.1 시간대 사용하기

ZoneRules 클래스에는  약 40개 정도의 시간대가 있다. ZoneId의 getRules()를 이용해서 해당 시간대의 규정을 획득할 수 있다.<br>
```ZoneId romeZone = ZoneId.of("Europe/Rome");```

지역 ID는 "지역/도시" 형식으로 이루어진다.

ZoneId 객체를 얻은 다음에는 LocalDate, LocalDateTime, Instant를 이용해서 ZonedDateTime 인스턴스로 변환할 수 있다. ZonedDateTime은 지정한 시간대에 상대적인 시점을 표현한다.

```java
ZoneDateTime zdt1 = date.atStartOfDay(romeZone);
```

    LocalDate + LocalTime = LocalDateTime 인것 처럼
    LocalDateTime + ZoneID = ZonedDateTime이 된다.

ZoneID를 이용해서 LocalDateTime을 Instant로 바꾸는 방법도 있다.

```java
Instant instant = Instant.now();
LocalDateTime timeFromInstant = LocalDateTime.ofInstant(instant, romeZone);
```

## 12.4 마치며

자바 8 이전 버전에서 제공하는 기존의 java.util.Date 클래스와 관련 클래스에서는 여러 불일치점들과 가변성, 어설픈 오프셋, 기본값, 잘못된 이름 결정 등의 설계 결함이 존재했다.

새로운 날짜와 시간 API에서 날짜와 시간 객체는 모두 불변이다.

새로운 API는 각각 사람과 기계가 편리하게 날짜와 시간 정보를 관리할 수 있도록 두 가지 표현 방식을 제공한다.

날짜와 시간 객체를 절대적인 방법과 상대적인 방법으로 처리할 수 있으며, 기존 인스턴스를 변환하지 않도록 처리 결과로 새로운 인스턴스가 생성된다.

TemporalAdjuster를 이용하면 단순히 값을 바꾸는 것 이상의 복잡한 동작을 수행할 수 있으며, 자신만의 커스텀 날짜 변환 기능을 정의할 수 있다.

날짜와 시간 객체를 특정 포맷으로 출력하고 파싱하는 포매터를 정의할 수 있다. 포매터는 스레드 안전성을 제공한다.

특정 지역/장소에 상대적인 시간대를 이용해서 시간대를 정의할 수 있으며, 이 시간대를 날짜와 시간 객체에 적용해서 지역화할 수 있다.