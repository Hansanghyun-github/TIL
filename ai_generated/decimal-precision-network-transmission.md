# 네트워크 전송 시 소수점 정밀도 보존 방법

## 문제: 부동소수점 오차

gRPC의 `double`, HTTP/JSON의 숫자 타입 모두 IEEE 754 64비트 부동소수점을 사용한다.

```python
0.1 + 0.2  # 예상: 0.3, 실제: 0.30000000000000004
```

금융/정산 데이터에서는 이 오차가 치명적일 수 있다.

## gRPC/HTTP 모두 Decimal 미지원

| 프로토콜 | Decimal 지원 | 숫자 처리 방식 |
|----------|-------------|---------------|
| gRPC (Protobuf) | X | float, double, int 등 |
| HTTP (JSON) | X | 파서가 보통 double로 처리 |

## 주요 기업들의 해결 방식

### 1. Stripe - 정수 (최소 통화 단위)

```json
{
  "amount": 1050,
  "currency": "usd"
}
```

- $10.50 → `1050` cents
- 단순하고 오차 없음

### 2. PayPal - 문자열

```json
{
  "currency_code": "USD",
  "value": "10.50"
}
```

- 소수점 2자리 문자열
- 정밀도 완벽 보장

### 3. Google Cloud - units + nanos (Protobuf)

```protobuf
message Money {
  string currency_code = 1;
  int64 units = 2;           // 정수 부분
  int32 nanos = 3;           // 10^-9 단위
}
```

- $10.50 = `{units: 10, nanos: 500000000}`
- 최대 9자리 소수점 정밀도

### 4. Shopify - GraphQL에서 문자열

```json
{
  "amount": "29.99",
  "currencyCode": "USD"
}
```

## 방식 비교

| 방식 | 예시 ($10.50) | 장점 | 단점 |
|------|--------------|------|------|
| 정수 (cents/micros) | `1050` | 단순, 오차 없음 | 스케일 고정 필요 |
| 문자열 | `"10.50"` | 정밀도 보장, 가독성 | 파싱 필요 |
| units + nanos | `{10, 500000000}` | 고정밀, 표준화 | 복잡함 |

## AWS Athena의 Decimal 처리

Athena는 `DECIMAL(precision, scale)` 타입을 지원한다.

```sql
CREATE TABLE financial_data (
  revenue DECIMAL(18, 6)
);
```

### API 응답: 모든 값이 문자열로 반환

```json
{
  "ResultSet": {
    "Rows": [
      {
        "Data": [
          { "VarCharValue": "10.214325" }
        ]
      }
    ]
  }
}
```

### 처리 흐름

```mermaid
flowchart LR
    A[Athena DECIMAL] -->|문자열| B[API Response]
    B -->|"10.214325"| C[Client]
    C -->|Decimal 파싱| D[정확한 값]
```

### Python 예시

```python
from decimal import Decimal

# Athena 응답에서 문자열로 받음
revenue_str = row['Data'][0]['VarCharValue']  # "10.214325"

# Decimal로 변환 (정밀도 유지)
revenue = Decimal(revenue_str)
```

## 결론

| 상황 | 권장 방식 |
|------|----------|
| 금융/결제 API | 정수 (micros/cents) 또는 문자열 |
| gRPC 금융 데이터 | `int64` micros 또는 `google.type.Money` |
| REST API | 문자열 |
| DB → API | 문자열로 전송 후 Decimal 파싱 |

핵심: 전송 구간에서는 문자열 또는 정수를 사용하고, 애플리케이션에서 Decimal로 처리한다.
