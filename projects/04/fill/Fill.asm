// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

	(LOOP)
@KBD 
D=M
@cnt
M=0
@WHITE
D;JEQ

		(BLACK)
@cnt
D=M
@8192
D=A-D
@LOOP
D;JLE
@cnt
D=M
@SCREEN
D=A
@cnt
A=D+M
M=-1
@cnt
M=M+1
@BLACK
0;JMP

		(WHITE)
@cnt
D=M
@8192
D=A-D
@LOOP
D;JLE
@cnt
D=M
@SCREEN
D=A
@cnt
A=D+M
M=0
@cnt
M=M+1
@WHITE
0;JMP

@LOOP
0;JMP