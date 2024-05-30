# 'ArrayList vs LinkedList'

## ArrayList

ArrayList는 중복을 허용하고 순서를 유지하며 원소들을 관리하는 ```List<E>```의 구현체이다.

null을 포함한 모든 원소를 허용한다.

그리고 인덱스로 원소에 접근 가능하고, 시간복잡도가 O(1)이다.

이는 배열과 매우 비슷하다.

    하지만 배열은 크기가 지정되면 고정된다.

    ArrayList는 클래스이기 때문에 배열을 추가, 삭제할 수 있다.

`여기서 ArrayList는 계속 원소를 추가할 수 있다고 마냥 좋은 것은 아닙니다.`

ArrayList의 코드를 살펴보면

```java
public class ArrayList<E> extends AbstractList<E>
        implements List<E>, RandomAccess, Cloneable, java.io.Serializable
{
    ...
    transient Object[] elementData;
    ...

    private void add(E e, Object[] elementData, int s) {
        if (s == elementData.length)
            elementData = grow(); // grow?
        elementData[s] = e;
        size = s + 1;
    }

    public boolean add(E e) {
        modCount++;
        add(e, elementData, size);
        return true;
    }
    ...
}
```

ArrayList도 결국은 ( Object[] )배열을 사용한다.

그리고 원소를 추가하는 add 메서드를 살펴보면<br>
해당 배열의 길이가 현재 사이즈가 같을때, 즉 현재 배열이 꽉찼을때 grow라는 메서드를 호출한다.

```java
    ...
    private Object[] grow(int minCapacity) {
        return elementData = Arrays.copyOf(elementData,
                                           newCapacity(minCapacity));
    }

    private Object[] grow() {
        return grow(size + 1);
    }
    ...
```

( newCapacity 메서드는 현재 사이즈 기준으로 새 용량을 구하는 메서드 )<br>
grow 메서드는 현재 배열 뒤에 새로 용량을 늘리는 역할을 하는데,

여기서 Arrays.copyOf의 시간복잡도는 O(n)이다. // n = 전체 용량

따라서 ArrayList 객체를 만들때 초기 용량을 설정하는 것이 좋다.
    
    DEFAULT 용량은 `DEFAULT_CAPACITY = 10`이다. (초기 용량을 설정하지 않았을 때)

### `ArrayList의 API`

인덱스로 접근 가능해서, 특정 원소를 탐색하는 `get` 메서드의 시간복잡도는 O(1)

원소를 추가 `add` 메서드의 시간복잡도는 웬만한 경우에선 O(1), 특정 경우(용량이 꽉찼을때)는 O(n)

원소를 삭제하는 `remove` 메서드의 시간복잡도는 최대 O(n)
    
    배열을 사용하기 때문에 삭제할 때 최대 O(n)이 걸린다.

## LinkedList

LinkedList는 내부적으로 양방향 연결 리스트로 구성되어 있다.

첫 노드에서 순방향으로 또는 마지막 노드에서 역순으로 조회 가능하다.

LinkedList는 배열이 아니라 각 노드들이 다음 노드를 가리키면서 이어져 있습니다.

### `LinkedList의 API`

add(E element): 원소를 마지막에 추가하기

    LinkedList는 첫번쨰 노드와 마지막 노드를 가지고 있습니다.
    따라서 마지막 노드 다음에 바로 추가하면 되기 때문에,
    시간복잡도는 O(1)입니다.


add(int index, E element): 원소를 지정된 위치에 추가하기

    원소를 지정된 위치에 추가하려면,
    시작 노드 또는 마지막 노드에서 출발해서 원하는 위치까지 도달한 후에, 원소를 추가해야 합니다.

    따라서 시간복잡도는 O(n)입니다.
    
    하지만 ArrayList은 원소를 추가한뒤 뒤쪽 원소들을 한칸씩 옮겨줘야 하는 반면,
    LinkedList는 가리키기만 하면 되기 떄문에 추가적으로 시간이 발생하지 않습니다.

remove(int index): 원소를 삭제하기

    중간에 원소를 삭제하는 경우는, 중간에 원소를 추가하는 경우와 비슷합니다.

    시간복잡도는 O(n)입니다.

    이 역시 ArrayList보다는 더 빠릅니다.

get(int index): 인덱스에 해당하는 원소 찾아오기

    LinkedList는 ArrayList와 달리 바로 접근하지 못하기 때문에, 시작 노드 혹은 마지막 노드에서 탐색해야 합니다

    시간복잡도는 O(n)입니다.

## ArrayList와 LinkedList의 차이

각 클래스의 API에 대한 시간복잡도 비교

`add(value)` - ArrayList, LinkedList 모두 O(1)

    ArrayList가 O(n)이 걸리는 경우는 아주 가끔이기 때문에 제외하고 생각하겠습니다.

`add(index, value)` - ArrayList > LinkedList (둘다 O(n)이지만 ArrayList는 추가 비용 발생)

`remove(index)` - ArrayList > LinkedList (둘다 O(n)이지만 ArrayList는 추가 비용 발생)

`remove(value)` - ArrayList > LinkedList (둘다 O(n)이지만 ArrayList는 추가 비용 발생)

`get(index)` - ArrayList O(1) < LinkedList O(n)

위 API들을 비교해보면 시간복잡도가 제일 갈리는 부분은,

마지막 위치가 아닌, 특정 위치에 원소를 삽입/삭제 할때 LinkedList가 ArrayList보다 우세합니다.

그리고

인덱스를 이용해 특정 원소를 조회할때는 ArrayList가 LinkedList보다 우세합니다.

## 정리

대부분의 경우(인덱스를 이용한 접근이 잦을 때)는 ArrayList를 사용하지만,

특정 위치에 데이터의 삽입/삭제가 잦을 때는 LinkedList를 쓰는 것이 현명하다고 판단됩니다.