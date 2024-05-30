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
> 똑같이 invert 후 +1

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
- MU0는 ACC 한개만 가지고 있음
- 16bits에서 4bits가 opcode, 12bits가 S
	1. LDA S 0000 - S위치 메모리의 값을 ACC에 로드
	2. STO S 0001 - ACC의 값을 S위치 메모리에 저장
	3. ADD S 0010 - ACC에 S위치 메모리의 값을 더함
	4. SUB S 0011 - 빼는거
	5. JMP S 0100 - S로 점프
	6. JGE S 0101 - ACC값이 0보다 크거나 같다면 S로 점프
	7. JNE S 0110 - ACC값이 0이 아니라면 S로 점프
	8. STP   0111 - stop
	여기서 1-4는 메모리 두 번 access, 5-8은 one cycle

MU0 Datapath - execute, fetch의  two states
PC: program counter: 다음으로 실행할 instruction의 address를 가지고 있음
ACC: accumulator라고 불리는 signle register: 현재 data 값을 가지고 있음
ALU: Arithmetic-Logic Unit: 연산 수행
IR: Instruction Register: 현재 실행될 instruction code를 가지고 있음
Instruction decode and control logic
- 그리고 CPU 밖의 Main Memory

// MU0 명령어 돌아가는거 강의자료에서 확인




---
## 3. Architecture Programming Model

ARM Processor - Advanced RISC Machines(높은 스피드, 작은 사이즈, 낮은 파워 소비)

특징
1. Load/Store architecture
2. Fixed-length instructions
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

|name|description|privileged?|
|--|--|--|
|User|most tasks run|unprivileged|
|FIQ|entered when a `high priority interrupt` is raised|privileged|
|IRQ|entered when a `low priority interrupt` is raised|privileged|
|Supervisor|entered on `reset` and when a `Software interrupt` instruction is executed|privileged|
|Abort|used to handle `memory access violations`|privileged|
|Undef|used to handle `undefined instructions`|privileged|
|System|privileged mode using the same registers as user mode|privileged|

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
각 모드에 대한 개인 스택 포인터를 제공(시스템 모드는 제외(유저 모드랑 공유함))

>각 함수가 시작하는 위치를 저장함, 이 위치를 저장하는 레지스터
	- 함수는 스택방식으로 call됨
	- 가장 마지막으로 호출한것이, 가장 먼저 마무리됨
	- 그래서 queue가 아닌 stack

> sp를 사용할 때는 SUB sp, sp, \#n으로 미리 할당해야 한다.
> 안 그러면 예상치 못한 값이 load 될 것이다.
> (여기서 n은 4의 배수)

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
모든 예외 처리 루틴은 어딘가에 있음
그 위치를 첫 부분에 포인터들로 저장해 놓음(vector table)
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
## 4. Assembly Program

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

> 실제로 LSL이라는 명령어는 없다
> ARM Processor에서 사용하는 명령어가 아님
> 사용자가 편하게 하도록 사용됨
> 
> lsl r0, r0, #1 하면
> mov r0, r0, lsl #1 됨
> LSR도 마찬가지

---
## 5. ARM Instruction Set

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
## 6. Data Processing Instructions
- Arithmetic operation(MUL 제외)
- Comparizons(no result - just set condition codes)
- Logical (boolean) operations
- Data movement between registers

> 위 명령들은 register만 사용한다, NOT memory

![[Pasted image 20231023110709.png]]

Arithmetic operation(MUL 제외)
ADD - Rd <- Rn + operand2
ADC - Rd <- Rn + operand2 + carry flag
SUB - Rd <- Rn - operand2
SBC - Rd <- Rn - operand2 + carry flag - 1(borrow)
RSB - Rd <- operand2 - Rn
RSC - Rd <- operand2 - Rn + carry flag - 1(borrow)

ADC, SBC, RBC는 multiword arithmetic을 위한 명령어

multiword arithmetic을 할 때, 
상위 명령을 제외한 명령어에 S(set flags(carry))
하위 명령을 제외한 명령에 C(carry 더해줘야 함)

Logical (boolean) operations
AND - Rd <- Rn n operand2
EOR - Rd <- Rn (XOR) operand2
ORR - Rd <- Rn u operand2
BIC - Rd <- Rn n (~operand2) // bit clear

Comparizons(no result - just set condition codes)
CMP - Rn - operand2, set flag no result written
CMN - Rn + operand2, set flags no result written
TST - Rn n operand2, set flags no result written
TEQ - Rn (XOR) operand2, set flags no result written
(S를 안쓰고 contdition flags를 업데이트)

Data movement between registers
MOV - Rd <- operand2
MVN - Rd <- ~operand2
(operand1(Rn)를 사용하지 않는다)

barrel shifter
operand2를 shift할 때 사용함
operand2가 
register - 5-bit로 shift or 다른 레지스터의 값만큼 shift
8-bit immediate value - 4-bit 값만큼(\*2해서) rotated right 

LSL: logical shift left & MSB는 carry bit
LSR: logical shift right & LSB는 carry bit
ASR: arithmetic shift right & LSB는 carry bit
ROR: rotate right & LSB는 carry bit
RRX: rotate right extended by carry - carry bit가 LSB가 됨
![[Pasted image 20231023114031.png]]

operand2(register 가정)를 shift 시킬때,
immediate value - 5-bit
register - extra cycle to execute
(ARM은 명령 한번에 최대 3개 레지스터만 사용 가능)

LSL #0 - 아무 일도 없었다

shift를 통해 MUL연산을 ADD로 최적화할 수 있다.

operand2가 immediate value - 4-bit 수\*2로 ROR 가능
=> (0~255) x $2^{2n} (0 <= n <= 15)$

MOV r0, \#0xFFFFFFFF (불가능)
MVN r0, \#0으로 가능
(불가능한 상수가 입력되면, 오류 발생)

immediate value로 한번에 32-bit 수를 load하는 것은 불가능
(정밀하게는 불가능, 대신 큰 숫자를 load하는 것은 가능(ROR으로))
대신 어셈블러는 32-bit 상수를 제공하기 위한 method를 제공한다.
LDR r0, =0x{임의의 상수}
> 여기서 MOV, MVN으로 된다면 이 명령어를 사용한다.
> 안된다면 literal pool로부터의 상수와 LDR을 사용한다.

Multiply
![[Pasted image 20231023115506.png]]
![[Pasted image 20231023115539.png]]

MUL{cond}{S} Rd, Rm, Rs ; Rd = Rm x Rs
MLA{cond}{S} Rd, Rm, Rs, Rn ; Rd = Rm x Rs + Rn

Rd와 Rm은 같은 레지스터로 사용하지 못함
PC 사용 못함

ARM의 multiplication hardware는 세가지 기능을 제공한다.
1. 8-bit Booth's Algorithm
2. Early termination method improved
3. 64-bit results

---
## 7. Data Transfer & Control Flow

>8-bit B(Byte), 16-bit H(Half-word), 32-bit (word, default)
### Data Transfer Instructions

8,16,32-bit의 데이터를 메모리에서 레지스터로 or 레지스터에서 메모리로 옮기는 Load/Store명령어

32-bit(word)의 여러 데이터를 옮기는 LDM/STM

SWP - 메모리와 레지스터 데이터 바꿈

> architecture v4에서 LDRH, STRH, LDRSH(Signed Half-word), STRSH, LDRSB(Signed Half-word), STRSB 추가됨
> 
> sign이 붙은 이유 - 16-bit와 8-bit는 계산할 때 32-bit로 확장됨
> 
> (메모리는 바이트 단위로 저장, ARM은 32-bit 단위로 저장)
> -> sign extention이 필요할 수도 있다.

STR r0, \[r1]  ; 메모리에서 (r1의 값)해당 자리를 r0로 store한다.
LDR r2, \[r1] ; 메모리에서 (r1의 값)해당 자리의 값을 r2로 load
(여기서 r1이 base register)

`data transfer instruction에서 offset` - offset은 base register에서 얼마나 떨어져 있는 가를 표현함(unsigned 12-bit immediate value)
> offset 대신 레지스터(shift될 수 있음)가 쓰일 수 있다.

offset이 적용되는 기준
1. Pre-indexed addressing(미리 인덱스가 더해지고 주소를 찾는다)
	- STR r0, \[r1, #12] ; r1에 12만큼 더한 자리가 메모리의 위치
	- STR r0, \[r1, #12]! ; auto-increment(명령 수행 후 r1에 12를 더함)
2. Post-indexed addressing(주소를 찾고 인덱스가 더해진다)
	- STR r0, \[r1], #12 ; auto-increment

> 여기서 STR r0, \[r1, #12] 명령만 r1에 변화가 없다(non-auto increment)

> 특정 element 접근할 때는, pre-indexed addressing이 편하다
> 배열의 인덱스들을 접근할 때는, post-indexed addressing이 편하다
> 여기서 byte 단위로 접근하려면, #1
> halfword 단위로 접근하려면, #2
> word 단위로 접근하려면, #4

> shift하는 값을 register로 표현하려면
> (r4가 몇번째 element인지 가리킴)
> r4, lsl #2 해줘야 함 - r4에 곱하기 4해야 제대로 가리킬 수 있다
> (메모리는 바이트 단위로 element를 저장하기 때문 & ARM은 32-bit 단위로 한번에 저장함)

> more constraint offset - half-word 명령어는(LDRH, ...) offset이 8-bit로 줄어든다. 
> & 레지스터로 쓰면 shift 불가능

> data transfer instrucntion은 offset을 unsigned로 사용하고, sign bit를 따로 사용한다.

### multiple register data transfer(LDM, STM)

- 16-bit가 register list(r0-r15 레지스터를 어떤걸 사용할지 결정)

LDM|STM\<address mode>

> address mode
> IA - after increment(default) - post-index
> IB - before increment - pre-index
> DA - after decrement - post-index
> DB - before decrement - pre-index
> (모두 auto-increment(decrement))

LDM/STM에서 base register는 메모리가 어디서 시작하는지 지정

base register에 !를 붙히면 base register가 업데이트된다.
-> stack에 유용함

LDM | STM의 장점
- saving and restoring context
- moving large blocks of data around memory

> little endian(default) - 가장 낮은 자리의 바이트가 0-7(큰 자리가 큰 자리에 저장됨)
> big endian - 가장 낮은 자리의 바이트가 24-31(큰 자리가 낮은 자리에 저장됨)

### Control Flow Instructions
(Branch Exchange 명령어는 안다룸)

Branch or Branch with Link

어셈블러가 현재 위치와 점프할 위치의 차를 구한다음 offset으로 저장하는데 이때 `8을 더 빼주고` 저장함

(ARM 프로세서는 파이프라인을 사용하기 때문에, 명령어를 읽어오는 곳의 위치가 살짝다름(명령어 두개), 두개의 명령어를 먼저 읽고 오기 때문에 그만큼(8) 빼줌)
-> 26-bit offset값을 뒤에 2-bit를 빼줘서 24-bit로 저장한다.(하나의 명령어가 32-bit이고, 4byte씩 위치가 바뀐다. -> 맨뒤의 2-bit의 주소는 무조건 00이라 저장할 필요 없음)
(& 실제 위치를 찾을때는 뒤에 00을 붙히고 & sign extension하고 찾음(32-bit로))

branch with link는 브랜치 수행 전 다음 명령의 위치를 link 레지스터(r14)에 저장함(PC-4를 저장 - 두개의 명령을 미리 가져왔기 때문에 빼줌)
다시 돌아오기 위해서는 MOV pc, lr

> 프로그램 성능을 높이기 위해서는 브랜치 명령을 적게 써야한다.  
---

data processing 명령어에서 second operand를 어떻게 사용하는가를 구분해줘야 한다
1. 상수값
2. 레지스터(shift하는 방식에서 나뉨)
3. 레지스터 - 또다른레지스터로 shift - 느리다(레지스터 4개라서(max 3개))

second operand(12비트)로 상수값을 사용해도 8비트만 사용, 4비트로 rotation시킴(뒤에 0을붙혀서 5비트로 rotation시킴)
  
> 그냥 12비트보다 좀더 넓은 범위 가능
> 일반적으로 increment(decrement)할 때 상수값들은 작은값들로 이루어져있음(8비트도 충분)
---

  

뺄셈에서 빼는수가 작으면 carry 발생 = 그래서 SBC는 carry 더하고 '1 빼줌'

  

`LDR r0, =0x42` - MOV r0, 0x42

  

`LDR r0, 0x55555555` - LDR r0, [pc, offset to lit pool]

  

브랜치는 24비트에서 뒤에두개 00붙힘

-> 이유: ARM 프로세서 명령어는 32비트단위(맨뒤2개 00)

  

브랜치쓰면 성능 떨어지는 이유

-> 다음 명령어가 뭐가 올지 모른다. -> 점프하면 기존 명령어 버려야함(state 낭비)
