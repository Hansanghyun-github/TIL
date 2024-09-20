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

