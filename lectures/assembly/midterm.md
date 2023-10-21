1. Processors & Languages & Numbers

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
2. ISA MU0
ISA(Instruction Set Architecture)

Opcode
reserved mnemonic symbols for instructions

Operands  - registers, memory, I/O device, numbers
- Source operand reference
- Destination operand reference

> add r1, r2, r3 (assembly language)
> r1 = r2 + r3 (high-level language)
> r1이 destination operand
> r2, r3이 source operand

assembly program
- list of instrucitons to be executed in the CPU

Instruction set
- the complete collection of instructions that are understood by a CPU
- the instruction set is ultimately represented in binary machine code also referred to as mnemonic assembly instruction

the computer architecture visible to assembly language programmers or compiler deisners

ISA includes
- instruction set
- programming registers
- operand access
- type and size of operands
- addressing modes
- instruction encoding (format)

ISA design issues
1. what operations are supported? - ADD, SUB, MUL
2. where are operands stored? - registers, memory
3. what types & sizes of operands are supported? - byte, half-word, word, float
4. how many operands are used? - 0, 1, 2, 3(4도 있는데 - two cycle)

ARM instruction
- size - 32 bits(고정)
- number of operands - 최대 3개
- operand의 size - 최대 32 bits(몇몇 operand는 김)
> word - 32 bits, halfword - 16 bits, byte - 8 bits

CISC vs RISC(ARM)
CISC(Complex Instruction Set Computers)
RISC(Reduced Instruction Set Computers) - instruction size 고정, load-store 아키텍쳐

RISC의 장점 - die size 작음, 높은 성능(higher clock speed, pipelining)
RISC의 단점 - poor code density
> Thumb instruction set: 기존 명령을 압축한 16-bit 명령

Registers vs Memory
- register는 CPU 내에 있음 - 피연산자 또는 명령어 저장, 32-64 소량 데이터 저장
- Memory는 CPU 밖에 있음 - 명령어와 데이터를 저장, 대량 데이터 저장
- register보다 memory의 capacity가 매우 높다
- memory보다 register의 access time이 짧다
> 메모리는 8 bits 단위로 데이터를 관리한다
> ARM processor의 레지스터는 32-bit 단위로 데이터를 관리한다
> -> 4만큼 차이남

memory addressing
1. alignment - 32-bit word를 딱 맞게 놔야 한다.
2. byte ordering
	1. big endian - LSB가 높은 주소에 있음
	2. little endian - LSB가 낮은 주소에 있음(default)

MU0: Design of a Simple Processor
- 16bits에서 4bits가 opcode, 12bits가 S
	1. LDA S 0000 - S위치 메모리의 값을 ACC에 로드
	2. STO S 0001 - ACC의 값을 S위치 메모리에 저장
	3. ADD S 0010 - ACC에 S위치 메모리의 값을 더함
	4. SUB S 0011 - 빼는거
	5. JMP S 0100 - S로 점프
	6. JGE S 0101 - ACC값이 0보다 크거나 같다면 S로 점프
	7. JNE S 0110 - ACC값이 0이 아니라면 S로 점프
	8. STP   0111 - stop

Each instruction takes exactly the number of clock cycles defined by the number of memory accesses
◎ The first four instructions each require two memory accesses.
◎ The last four only require one cycle.

MU0 Datapath - execute, fetch의  two states
PC: program counter: 다음으로 실행할 instruction의 address를 가지고 있음
ACC: accumulator라고 불리는 signle register: 현재 data 값을 가지고 있음
ALU: Arithmetic-Logic Unit: 연산 수행
IR: Instruction Register: 현재 실행될 instruction code를 가지고 있음
Instruction decode and control logic
- 그리고 CPU 밖의 Main Memory

// MU0 명령어 돌아가는거 강의자료에서 확인




---
3. Architecture Programming Model


---
4. Assembly Program


---
5. ARM Instruction Set


---
6. Data Processing Instructions


---
7. Data Transfer Control Flow