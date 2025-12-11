# Protobuf Reserved 필드 가이드

## reserved란?

protobuf에서 더 이상 사용하지 않는 필드 번호나 이름을 예약해서 미래에 실수로 재사용하지 못하게 막는 기능이다.

## 문법

```protobuf
message Example {
  reserved 2, 15, 9 to 11;       // 번호 예약
  reserved "foo", "bar";          // 이름 예약 (별도 문장으로)
}
```

번호와 이름을 같은 문장에 섞을 수 없다.

## 왜 필요한가?

protobuf는 필드 번호로 데이터를 직렬화/역직렬화한다.

1. `old_field = 5`로 데이터를 저장한 클라이언트가 있고
2. 나중에 다른 의미의 필드로 5번을 재사용하면
3. 타입이 같을 경우 에러 없이 잘못된 값이 들어감

## reserved의 역할

| 시점 | 동작 |
|------|------|
| 컴파일 타임 | 해당 번호/이름 재사용 시 컴파일 에러 발생 |
| 런타임 | 영향 없음 (데이터 전송과 무관) |

reserved는 순수하게 컴파일러 힌트이며, 런타임 데이터 전송에는 영향을 주지 않는다.

## 장단점

### 장점

- 필드 번호 재사용 실수 방지
- 구버전/신버전 호환성 문제 예방
- 스키마 히스토리 추적 가능 (왜 특정 번호가 비었는지 알 수 있음)

### 단점

사실상 없다.

| "단점"이라고 할 수 있는 것 | 실제로는 |
|---------------------------|----------|
| 코드 한 줄 추가 | 부담 아님 |
| 필드 번호가 sparse해짐 | 성능/용량 영향 없음 |
| reserved 목록 관리 | 어차피 건드릴 일 없음 |

## 필드 번호와 데이터 용량

protobuf는 값이 있는 필드만 직렬화한다.

```protobuf
message Example {
  double field_a = 1;   // 값: 100.0
  double field_b = 2;   // 값: 0 (기본값)
  double field_c = 3;   // 값: 200.0
}
```

전송되는 데이터: `[1: 100.0][3: 200.0]`

- 기본값인 field_b는 전송 안 됨
- 중간 번호가 비어있어도 용량 손해 없음
- 필드 번호가 43이든 4300이든 용량 차이 거의 없음 (varint 인코딩)

## 사용 예시

기존 필드를 삭제하고 새 필드를 추가할 때:

```protobuf
// Before
message User {
  string email = 5;
}

// After
message User {
  reserved 5;
  reserved "email";
  string primary_email = 6;
  string secondary_email = 7;
}
```

## 이름 예약이 필요한 이유

번호만 예약하면 같은 이름으로 다른 번호에 필드를 만들 수 있다.

```protobuf
reserved 5;
string email = 10;  // 컴파일 됨
```

이름도 예약하면 방지된다.

```protobuf
reserved 5;
reserved "email";
string email = 10;  // 컴파일 에러
```

JSON 직렬화, TextFormat에서 필드 이름을 사용하므로 이름 예약도 권장된다.

## 공식 문서

- [Proto3 Language Guide](https://protobuf.dev/programming-guides/proto3/) - reserved 섹션 포함
- [Proto Best Practices](https://protobuf.dev/best-practices/dos-donts/) - Do/Don't 가이드

## 안전한 마이그레이션 순서

클라이언트가 기존 필드를 사용 중일 수 있는 경우, 단계적으로 마이그레이션해야 한다.

### Step 1: 새 필드 추가 (기존 필드 유지)

```protobuf
message User {
  string email = 5;           // deprecated, 유지
  string primary_email = 6;   // 신규
  string secondary_email = 7; // 신규
}
```

### Step 2: 클라이언트 마이그레이션

- 모든 서비스가 새 필드(6, 7) 사용하도록 코드 변경
- 구 필드(5) 읽거나 쓰는 코드 제거

클라이언트 코드에서 구 필드를 제거해야 하는 이유:
- Step 3에서 reserved 처리 후 proto 업데이트 시 컴파일 에러 발생 (필드가 없으니까)
- 또는 구버전 proto 사용 시 항상 빈 값

### Step 3: reserved 처리

```protobuf
message User {
  reserved 5;
  reserved "email";
  string primary_email = 6;
  string secondary_email = 7;
}
```

```mermaid
flowchart LR
    A[기존 필드 사용 중] --> B[새 필드 추가]
    B --> C[클라이언트 마이그레이션]
    C --> D[기존 필드 reserved 처리]
```

### 바로 reserved 처리해도 되는 경우

- 해당 필드를 아무도 사용하지 않음이 확실할 때
- 프로덕션에 배포된 적 없거나 데이터가 없을 때

## 결론

reserved는 비용 0, 이득만 있는 기능이다. 필드를 삭제할 때는 항상 사용하자.
