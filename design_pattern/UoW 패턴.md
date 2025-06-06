# Unit of Work 패턴

## 개요

WAS에 여러 서비스가 있고 여러 레포지토리가 있다.  
이때 어떤 서비스가 여러 레포지토리를 사용할 때,  
각 레포지토리에서 트랜잭션을 처리하면 트랜잭션 관리가 어려워진다.  
그리고 데이터간 정합성 문제가 발생할 수 있다.

이를 해결하기 위해  
하나의 작업 단위(트랜잭션) 내에서 여러 개의 데이터 변경 작업을 모아  
관리하는 디자인 패턴을 `Unit of Work(UoW)` 패턴이라고 한다.

---

## UoW 패턴 주요 개념

### 작업 단위(트랜잭션) 내에서 여러 변경 사항을 관리

여러 개의 데이터 조작 작업(Insert, Update, Delete)을 하나의 작업 단위로 묶어서 관리한다.

변경된 객체들을 추적하여 필요한 경우 한꺼번에 반영(Commit)한다.

> 핵심은 하나의 트랜잭션 내에서 여러 객체들의 변경을 한 번에 처리하는 것이다.

---

## UoW 패턴의 장점

- 트랜잭션 관리가 용이하다.
- 데이터간의 정합성을 유지할 수 있다.
- 하나의 트랜잭션 내에서 처리하기 때문에 성능 향상이 가능하다.

---

## UoW 패턴의 구현

### UoW 인터페이스

```python
class UnitOfWork:
    def __enter__(self):
        pass

    def __exit__(self):
        pass

class ConcreteUnitOfWork(UnitOfWork):
    def __enter__(self):
        # 트랜잭션 시작
        pass

    def __exit__(self):
        # rollback
        pass

    def commit(self):
        # 변경 사항 반영
        pass
```

### UoW 패턴 적용

```python
with ConcreteUnitOfWork() as uow:
    # 변경 사항 추적
    uow.register_new(obj1)
    uow.register_dirty(obj2)
    uow.register_deleted(obj3)

    # 변경 사항 반영
    uow.commit()
```

핵심은 여러 테이블에 대한 쓰기 작업을  
하나의 트랜잭션으로 묶어서 처리하는 것이다.