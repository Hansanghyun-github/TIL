# Redis

> 데이터베이스보다 더 빠른 메모리에 더 자주 접근하고 덜 자주 바뀌는 데이터를 저장하자

## Redis 란?

> Remote Dictionary Server  
> 외부에 있는 딕셔너리(자바의 HashMap과 비슷한 구조) 구조의 서버

Redis(Remote Dictionary Server)는 메모리 기반의 Key-Value 구조 데이터 관리 시스템으로,  
모든 데이터를 메모리에 저장하고 빠른 속도로 데이터를 처리하는 비관계형 데이터베이스이다.  
(인메모리 데이터베이스)

---

## Redis 특징

1. 영속성을 지원하는 인메모리 데이터 저장소
2. 다양한 데이터 구조 지원(List, Set, Sorted Set, Hash, String)
3. Single Threaded  
   (따라서 시간복잡도에 주의해야 한다)

---