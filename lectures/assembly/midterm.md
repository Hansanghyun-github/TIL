## 1. Processors & Languages & Numbers

Processor / CPU
메인 메모리에 있는 프로그램의 명령들을 fetch
execution of instructions for basic/logic operations and so on
control of components in the processor responding to instructions
Interface to I/O and main memory ^6f8813

registers
high-speed CPU 안에 있는 임시 저장소 ^67813b

ALU(Arithmetic Logic Unit)
Hardware for arithmetic(ADD, SUB) and logic(AND, OR) operation

CU(Control Unit)
Control of all components in the CPU responding to instrucitons

Buses
Channel for data transmission among components in the CPU

microprocessor - processor on a single IC chip

Computer Program
A collection of instructions executed by a processor to perform a specific task

high-level language - c, c++, Java, cobol
machine language - Intel, MIPS, ARM - Assembly language

machine language는 0과 1로 이루어져 있음

컴파일 과정
task -> C language -> Assembly language -> machine language

어셈블리 언어의 장점 - efficiency
space-efficiency, time-efficiency, accessibility to system hardware

high-level 언어의 장정
software development, software maintanance, software portability

|-|Assembly|High-level|
|--|--|--|
|protability|low|high|
|performance|high|low|
|ease of maintenance|low|high|
|accessibility to machine|high|low|

Assembly Instructions - two pieces
Opcode - 데이터를 가지고 뭘 할 것인가 - ADD, SUM
Operands - 어디에 데이터를 넣고 가져올지 - r1, #3 - registers, numbers
- registers - Rn
- Numbers - #(decimal), x(hex)
- Separated by comma

숫자의 표현
binary(01), Octal(0-7), Decimal(0-9), Hexadecimal(0-F)

1 hex = 4 binary
bit = b(inary dig)it

MSB(Most Significant bit) - 가장 왼쪽 숫자
LSB(Least Significant bit) - 가장 오른쪽 숫자

2진수와 10진수 변환
![[Pasted image 20231021203807.png]]

2진수로 음수 표현하는 법
1. Sign-and-magnitude - MSB가 sign bit가 된다
2. 1's complement - invert를 통해 음수 표현($-2^{n-1}-1$ ~ $2^{n-1}-1$)
	- 연산할때 편함, 대신 0이 두가지로 표현됨(이게 별로)
3. 2's complement - invert 후 1 더해 음수 표현 or $2^n$에서 양수를 빼서 음수 표현
	($-2^{n-1}$ ~ $2^{n-1}-1$)
	- 연산할때 편함, 0은 1가지로 표현됨(0000)

> 2's complement number로 표현된 음수를 확인하는 법
> - 1빼고, invert

sign extension - ex) 16비트 숫자를 32비트로 표현하기 위해, MSB를 늘려줌
- 양수는 0을 늘림(MSB가 0)
- 음수는 1을 늘림(MSB가 1)

> 2's complement numbers는 양수와 양수를 더했을때 `overflow` 발생, 음수와 음수를 더했을 떄 `underflow` 발생
> 
> (CPSR(V)의 오버플로 비트가 설정)
> (carry bit는 관련성이 없기 때문에 볼 필요가 없다)
> 
>  > 컴퓨터로 표현하는 수는 범위가 제한되어 있기 때문에 발생
> 
> 정확히는 overflow는 + + 를 더했을때 -가 나온것
> underflow는 - - 를 더했을때 +가 나온것
> 숫자 두 개 - + 는 overflow나 underflow가 발생하지 않는다.

문자의 표현 - 아스키코드, 유니코드
'0' - 48, 'A' - 65, 'a' - 97

---
## 2. ISA MU0


---
## 3. Architecture Programming Model


---
## 4. Assembly Program


---
## 5. ARM Instruction Set


---
## 6. Data Processing Instructions


---
## 7. Data Transfer Control Flow