# 스프링에서 사용하는 레디스

## dependency 추가

```gradle
implementation 'org.springframework.boot:spring-boot-starter-data-redis'
```

## application.properties 설정

```properties
spring.data.redis.host=localhost
spring.data.redis.port=6379
```

> 위와 같이 설정하면 굳이 레디스 관련 빈을 추가하지 않아도 된다.  
> (스프링 부트가 자동으로 레디스 관련 빈을 추가해준다)

---

## 레디스 사용

### RedisTemplate 사용

```java
@Service
@Slf4j
@RequiredArgsConstructor
public class RedisService {
    private final RedisTemplate<String, String> redisTemplate;

    public void save(String key, String value) {
        redisTemplate.opsForValue().set(key, value);
    }

    public String get(String key) {
        return redisTemplate.opsForValue().get(key);
    }

    public Set<String> getKeys(String pattern) {
        return redisTemplate.keys(pattern);
    }
}
```

위 예시는 `RedisTemplate`을 사용하여 레디스에 데이터를 저장하고 조회하는 방법이다.  
(가장 기본적인 방법이다)

> 위 예시는 레디스의 String 타입을 다루는 예시이다.  
> 다른 데이터 타입을 다루려면,  
> `redisTemplate.opsForList()`, `redisTemplate.opsForSet()` 등을 사용하면 된다.

### @Cacheable 사용

`@Cacheable` 어노테이션을 사용하면,  
메소드의 리턴값을 캐싱할 수 있다.

> Cache HIT - 메소드가 호출되지 않고 캐시된 값을 반환  
> Cache MISS - 메소드가 호출되고 캐시된 값을 반환

```java
@Service
@Slf4j
public class CachingService {
    @Cacheable(value = "caching")
    public String getName() {
        log.info("getName() called");
        return "CachingService";
    }
}
```

### @Cacheable 주의사항

이 어노테이션은 해당 메서드가 호출 됐을 때,  
캐싱됐는지 확인하기 위해 레디스를 조회하는데  
해당 값이 존재하는 지만 조회한다.

여기서 문제는 조회된 값이 유효한 값인지  
(이전에 캐싱했을 때와 같은 값인지) 확인하지 않는다.

ex) 위 `getName()` 메서드를 호출하면  
맨 처음에 "CacheService"를 반환하고 캐싱한다.

여기서 위 메서드를 다시 호출하기 전에  
다른 개발자가 레디스에서 직접 값을 변경했다면,  
이전에 캐싱했던 값과 다른 값을 반환할 수 있다.  

혹은 에러가 발생할 수 있다.  
(이전에 캐싱한 값보다 길이가 짧은 값을 반환한다면 EOF 에러가 발생한다)  
(특정 객체를 캐싱한 경우에는 UnrecognizedPropertyException 에러가 발생할 수 있다)

> 이전에 캐싱했던 값보다 길이가 긴 값이 저장되어 있다면  
> (에러가 발생하지 않고)  
> 이전에 캐싱했던 값의 길이만큼만 조회된다.

> 물론 이런 상황은 드물게 발생한다.  
> (개발자가 직접 레디스에 접근하는 경우가 드물기 때문)

---