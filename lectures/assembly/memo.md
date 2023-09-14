# 어셈블리프로그래밍설계및실습

이 강의에서 배우는 것

Basic assembly programming skills

    assembly language의 구조
    ARM instructions and assembly programming

Microprocessor architectures and operations

    Instruction set structure
    ARM operations
    ARM programming model

---

`Processor / CPU(Central Processing Unit)`

메인 메모리에 있는 프로그램의 instructions를 Fetch함

Execution of instructions for basic arithmetic/logic operations and so on

Control of components in the processor responding to instructions

Interface to input/output and main memory

`Registers`

CPU에 있는 high-speed temporary storage

`ALU(Arithmetic Logic Unit)`

계산을 하기위한 하드웨어

`CU(Control Unit)`

`Buses`

---

요즘은 processor나 microprocessor나 같은 의미로 쓰임

---

c++, JAVA, Python은 high-level language

Assembly language는 low-level language

---

c언어를 컴파일하는 과정

c언어 -> assembly language -> machine language(0,1)

---

assembly language의 장점

space-efficiency, time-efficiency, Accessibility to system hardware

high-level language의 장점

소프트웨어 이식성, development, maintenance

---

Assembly Instructions

`ADD r1, r3, #5`

여기서 ADD는 Opcode(데이터로 뭘할지)

그 뒤는 Operands(어떤 데이터 - 레지스터, 숫자)

---

## Numbers

1 hexadecimal digit = 4 binary digits

bit = b(inary dig)it

MSB = Most Significant Bit(가장 높은 숫자)

LSB = Least Significant Bit(가장 낮은 숫자)

---

Sign and magnitude - 맨 앞숫자는 sign bit, 나머진 양수나 음수나 같음

이 표현은 연산할때 별로임

1's complement number - 양수를 뒤집은 수가 음수의 표현, 연산할때 편함, 대신 0이 두가지로 표현됨(이게 별로)

2's complement number - 숫자를 뒤집고 1을 더한게(1's complement number에서 1더한것) 음수의 표현, 연산할때 편함, 0은 1가지로 표현됨(0000)

---

2's complement numbers는 양수와 양수를 더했을때 `overflow` 발생, 음수와 음수를 더했을 떄 `underflow` 발생

    컴퓨터로 표현하는 수는 범위가 제한되어 있기 때문에 발생

정확히는 overflow는 + + 를 더했을때 -가 나온것

underflow는 - - 를 더했을때 +가 나온것

    - + 는 overflow나 underflow가 발생하지 않는다.

---

Sign Extension

맨 앞 숫자(sign bit)를 같은 숫자로 늘리는 과정

---

## Instruction Set Architecture(ISA)

Opcode: What to do with the data(ADD, SUB, ...)

Operands(Sources/Destination): Where to det data and put the result(registers, memory, I/O device, Numbers)

ISA: the computer architecture visible to assembly language programmers or complier designers ISA includes

---

CISC(Complex Instruction Set Computers) vs RISC(Redueced Instruction Set Computers)

그냥 CISC는 복잡함

RISC는 간단함(instruction size가 고정, load-store architecture)

RISC의 장점: die size가 작음, development time 짧다, 성능 좋음(higher clock speed, pipelining)

RISC의 결점: poor code density(단위가 짧기 때문에 표현할 수 있는 명령어가 적다)

---

### Registers vs Memory

register는 CPU 내에 있음

Memory는 CPU 밖에 있음

register보다 memory의 capacity가 매우 높다

memory보다 register의 access time이 짧다

---

### Endian

Big Endian - LSB has highest address

Little Endian - LSB has lowest address(요즘은 이걸로 통일됨)

---

Alignment

맨앞 두 bits가 00으로 맞춰야함

---

### Mu0: Design of a Simple Processor

16bits에서 4bits가 opcode, 12bits가 S

LDA S 0000 - S위치 메모리의 값을 ACC에 로드

STO S 0001 - ACC의 값을 S위치 메모리에 저장

ADD S 0010 - ACC에 S위치 메모리의 값을 더함

SUB S 0011 - 빼는거

JMP S 0100 - S로 점프

JGE S 0101 - ACC값이 0보다 크거나 같다면 S로 점프

JNE S 0110 - ACC값이 0이 아니라면 S로 점프

STP   0111 - stop

---

### MU0 Datapath

PC: program counter: 다음으로 실행할 instruction의 address를 가지고 있음

ACC: accumulator라고 불리는 signle register: 현재 data 값을 가지고 있음

ALU: Arithmetic-Logic Unit: 연산 수행

IR: Instruction Register: 현재 실행될 instruction code를 가지고 있음

Instruction decode and control logic

    그리고 CPU 밖의 Main Memory

---

EX, fetch는 누구나 함, 근데 몇몇 instruction은 메모리에 접근해야하는 stage가 필요

---

13(sp),14(lr),15(pc)번 레지스터는 안쓰는게좋음

13번레지스터- Stack Pointer register

각 함수가 시작하는 위치를 저장함, 이 위치를 저장하는 레지스터

    함수는 스택방식으로 call됨
    가장 마지막으로 호출한것이, 가장 먼저 마무리됨

    그래서 queue가 아닌 stack

14번레지스터 - Link register

돌아올곳의 주소를 저장하는 레지스터

    BL(Branch and Link) 명령어를 통해 저장됨

>

    13번은 주소의 모음이 있는 주소를 저장
    14번은 주소를 저장

    13번에 있는 스택은 여러데이터가 있지만
    14번은 딱 한개만 저장(돌아올곳)

---

13,14 레지스터를 특정레지스터로 지정했지만

사용 가능

그런데 다른 명령어에 의해 값이 바뀔수있음

---

15번 레지스터

다음에 수행할 명령어가 있는 위치(0,4,8,C, ...)

뒤의 최하위 두비트는 00이다.

    ARM 프로세서의 모든 명령어는 32 bits wide
    메모리는 바이트 단위로 저장되어있음
    PC는 4개씩 읽는다

15번레지스터는 일반 레지스터로 사용 불가능

---

`Exceptions`

모든예외처리루틴은 어딘가에 있음

그위치를 첫 부분에 포인터들로 저장해놓음(vector table)

(reset, undefined instruction, ...)

---

강의뒷부분 7TDMI는 안함

---

directive 어셈블러한테 어떤ㄷㅇ작하라고 가리키는것

---

label은 대소문자 구분해야함










