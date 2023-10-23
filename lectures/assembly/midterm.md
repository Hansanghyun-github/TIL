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

ARM Processor - Advanced RISC Machines(높은 스피드, 작은 사이즈, 낮은 파워 소비)

특징
1. Load/Store architecture
2. Fixed-length instructions(32 bits)
3. Pipeline
4. Enhanced power-saving design
=> Simplicity - operating at higher clock frequencies

ARMv1: `26-bit addressing`
ARMv2: 26-bit addressing, 32-bit MUL, MLA, `three privileged processing modes`(Supervisor, IRQ and FIQ)

> Architecture of a processor mostly refers to the `instruction sets` that the processors execute.

ARMv3: 32-bit addressing, `two new privileged processing modes`(undefined and abort), `SPSR`(saved program status registers), MUL - 64 bit result
ARMv4: Add signed, unsigned half-word and signed byte `load/store` instructions
** ARMv4T: `16-bit Thumb compressed form`
ARMv5T: BLX(Branch with Link and eXchange), CLZ(Count Leading Zeros), BRK(software BReaKpoint)
ARMv5TE: add the signal processing instruction set extension
ARMv5TEJ: jazelle tech ~ JVM
ARMv6: SIMD(Single Instruction Multiple Data) extensions
ARMv7~: ARM Cortex series

ARM: 32-bit architecture

> Byte - 8 bits
> Halfword - 16 bits
> Word - 32 bits

32-bit ARM instruction Set
16-bit Thumb instruction Set

ARM has 7 basic operating modes:
- User: (unprivileged mode) most tasks run
- Privileged
	- FIQ: entered when a `high priority interrupt` is raised
	- IRQ: entered when a `low priority interrupt` is raised
	- Supervisor: entered on `reset` and when a `Software interrupt` instruction is executed
	- Abort: used to handle `memory access violations`
	- Undef: used to handle `undefined instructions`
	- System: privileged mode using the same registers as user mode
> system을 제외한 다른 privileged mode는 exception mode

r0-r15가 사용 가능한 레지스터(current visible registers - User(System) mode)

banked out registers

|-|-|
|--|--|
|Abort| r13, r14, spsr|
|FIQ| r8-r14, spsr|
|IRQ| r13,r14, spsr|
|SVC| r13, r14, spsr|
|Undef| r13, r14, spsr|

> 그냥 FIQ만 r8-r14, spsr
> 나머지는 r13, r14, spsr
> 
> r15(pc)와 cpsr은 무조건 visible?

ARM은 32-bits의 37개의 register를 가지고 있다
1 - PC(r15)
1 - CPSR
5 - SPSR
30 - general purpose registers

r0-r12 그냥 사용 가능
r13 - SP(Stack Pointer)
r14 - LR(Link Register)
r15 - PC(Program Counter)

System을 제외한 privileged modes는 SPSR 레지스터에 접근 가능
SPSR(Saved Program Status Register)

Program Status Register
![[Pasted image 20231022023837.png]]
![[Pasted image 20231022024131.png]]

13(sp),14(lr),15(pc)번 레지스터는 안쓰는게좋음

r13 - Stack Pointer register
각 함수가 시작하는 위치를 저장함, 이 위치를 저장하는 레지스터
- 함수는 스택방식으로 call됨
- 가장 마지막으로 호출한것이, 가장 먼저 마무리됨
- 그래서 queue가 아닌 stack

r14 - Link register
돌아올곳의 주소를 저장하는 레지스터
- BL(Branch and Link) 명령어를 통해 저장됨

> 13번은 주소의 모음이 있는 주소를 저장
> 14번은 주소를 저장
> 13번에 있는 스택은 여러데이터가 있지만
> 14번은 딱 한개만 저장(돌아올곳)  

13,14 레지스터를 특정레지스터로 지정했지만 사용 가능
(그런데 다른 명령어에 의해 값이 바뀔수있음)

r15 - Program Counter
다음에 수행할 명령어가 있는 위치(0,4,8,C, ...)
뒤의 최하위 두비트[1:0]는 00이다(instruction이 32 bits 라서)
> ARM 프로세서의 모든 명령어는 32 bits wide
> 메모리는 바이트 단위로 저장되어있음
> PC는 4개씩 읽는다
> 
> 15번레지스터는 일반 레지스터로 사용 불가능

> ARM state - 32 bits, [1:0] 00
> Thumb state - 16 bits, [0] 0
> Jazelle state - 8 bits, 프로세서가 4개를 한번에 읽음

Exceptions
모든예외처리루틴은 어딘가에 있음
그위치를 첫 부분에 포인터들로 저장해놓음(vector table)
- reset
- undefined instruction
- software interrupt(SWI)
- prefetch abort
- data abort
- IRQ
- FIQ

ARM Instruction Set 특징
- Load/Store architecture
- 3-address data processing instructions
- Conditional execution
- Load/Store multiple registers
- Shift & ALU operation in single clock cycle
- Open instruction set extension
- very dense 16-bit compressed representation of instruction (Thumb)

// 자료 뒷부분 7TDMI 제외

---
4. Assembly Program

코드의 general form
```
label □ instruction|directive|pseudo-instruction □ ;comment
```

|-|-|
|--|--|
|instructions|opcode □ operands|
|pseudo-instruction|Instructions that is translated into the appropriate combination of instructions at assembly time by the assembler|
|directives|direct the assembler to perform various tasks|
|Labels|Names to represent an address in memory with numeric values for the programmer|
|Comments|주석|

ARM instruction set - 32 bits
Thumb instruction set - 16 bits(ARMv4T and later)
Thumb2 instruction set - 16 and 32 bits(ARMv6T2 and later)

Data Processing Instructions
- arithmetic operations(ADD, SUB, ...)
- Comparisons(CMP, TEQ, ...)
- Logical operations(AND, ORR, BIC, ...)
- Data movement between registers(MOV, MVN)
Data Transfer Instructions
- Single register data transfer(LDR, STR)
- Block data transfer(LDM, STM)
- Data swap(SWP)
Control Flow Instructions
- Branch and Branch with Link(B, BL)

numbers - \#로 시작, 0x(Hex), 그냥(dec)
characters - #'A'
String - str1 DCB "Hello World", 0

Labels - Symbolic address of the line

Directive  - 어떤 동작하라고 가리키는 것

|Directive 이름|설명|예시|
|--|--|--|
|AREA|Defines a code or data section|코드 맨 첫줄|
|RN|Defines a register name for a specified register|name RN 번호(0-15)|
|EQU|gives a symbolic name to a value|name EQU 숫자|
|ENTRY|declares an entry point to a program|코드 두번째 줄|
|ARM or CODE32|ARM state 가리킴||
|THUMB or CODE16|THUMB state 가리킴||
|DCB/DCW/DCD|Allocate memory and specifies initial values|name DCB values|
|ALIGN|aligns the current location to a specified boundary by padding with zeros|?|
|SPACE|reserves a zeroed block of memory|name SPACE values|
|END|end에 도달 했음을 알림||

```assembly
AREA example, CODE, READONLY
ENTRY

...

END

```

> 여기서 example(label) 제외하고 전부 다 directive

// 강의 자료에 코드 예시 있음

---
5. ARM Instruction Set

모든 ARM 명령어들은 32-bit
& execute conditionally depending on flags in CPSR
& Load/Store architecture

Instruction types 
1. Data Processing instruction
2. Data Transfer instruction
3. Control Flow instruciton

Conditional Field {cond}
All operations can be performed conditionally, testing condition flags in CPSR.
![[Pasted image 20231023103956.png]]

Condition flags
1. N: set when the result was Negative(MSB of the result is 1)
2. Z: set when the result was Zero
3. C: set when a Carry occurs
4. V: set when oVerflow occurs

15 different conditions
![[Pasted image 20231023104536.png]]

Status Update Field {S}
일반 명령어에 S를 붙이면, CPSR의 flags가 업데이트 됨
ADD - 그냥 더함
ADDS - 더하고, CPSR(flags) 업데이트
> CMP, CMN은 flags만 업데이트하는 명령어 (S 안씀)
> (CMP는 앞 숫자에서 뒤 숫자를 빼서 결과를 통해 flags를 업데이트)

Special Purpose Registers
1. Stack Pointer(r13)
2. Link Register(r14)
3. Program Counter(r15)
4. CPSR
5. SPSR - To store the current value of the CPSR when an exception is taken
---
6. Data Processing Instructions



---
7. Data Transfer & Control Flow


