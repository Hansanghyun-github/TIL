## io.lettuce.core.RedisCommandExecutionException: ERR hash value is not an integer

### 개요

스프링에 레디스를 연결하여 사용하던 중 발생한 에러이다. 

레디스에 저장된 데이터를 가져올 때 발생했다.

### 원인

레디스에 저장된 데이터가 숫자 형태가 아니라서 발생한 에러이다.

### 분명 나는 숫자를 저장했는데?

스프링에서 설정한 직렬화 방식 때문에 발생한 문제였다.

```java
@Configuration
class RedisConfig{
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory redisConnectionFactory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(redisConnectionFactory);
        template.setKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(new GenericJackson2JsonRedisSerializer());
        return template;
    }
}
```

위 설정은 `RedisTemplate`을 통해 레디스에 데이터를 가져오거나 저장할 때,  
직렬화/역직렬화 방식을 설정하는 부분이다.

### 레디스 설정 두가지 문제

1. 나는 레디스의 해시를 이용하여 데이터를 저장하고 있었다.  
   위 설정은 해시 데이터 설정이 아닌,  
   일반 데이터 설정이었다.
2. `GenericJackson2JsonRedisSerializer`는 모든 데이터를 JSON 형태로 저장한다.  
   숫자 데이터도 JSON 형태로 저장하기 때문에,  
   숫자 데이터를 가져올 때 문제가 발생했다.

> 직렬화/역직렬화 방식을 설정하지 않으면  
> 기본 JDK 직렬화 방식을 사용한다.  
> JDK 직렬화 방식은 레디스에 데이터를 저장할 때,  
> 데이터가 가독성이 떨어지는 이진 데이터로 저장된다.
> 
> (예시)  
> ```shell
> redis-test-server.tbgokv.ng.0001.apn2.cache.amazonaws.com:6379> hgetall hashtemp
> 1) "\xac\xed\x00\x05t\x00\x04key1"
> 2) "\xac\xed\x00\x05t\x00\x011"
> ```

이렇게 저장하는 것이 문제가 되지는 않는다.  
문제는 이렇게 저장해놓고,  
`incr`, `decr` 등의 명령어를 사용할 때 발생한다.

> `incr`, `decr` 명령어는  
> 저장된 데이터가 숫자 형태일 때만 사용할 수 있다.  
> (키에 해당하는 데이터를 증가/감소시키는 명령어)

### 해결 방법

`StringRedisSerializer`를 사용하여 해시 데이터를 저장한다.

```java
@Configuration
class RedisConfig{
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory redisConnectionFactory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(redisConnectionFactory);
        template.setKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(new StringRedisSerializer());
        template.setHashKeySerializer(new StringRedisSerializer());
        template.setHashValueSerializer(new StringRedisSerializer());
        return template;
    }
}
```

