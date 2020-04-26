(LOOP)

//draw current state
@SCREEN
D=A
@row
M=D
@100
D=A
@BLOCK
M=D
(DRAWROW) // draw current row
	@24576 //reaching this address means all rows were drawn
	D=A
	@row
	D=M-D
	@START ///finished drawing
	D;JGE
	@cnt
	M=0
		(DRAWCELLS) // draw next 32 cells
		@32
		D=A
		@cnt
		D=M-D
		@ROWCONT 
		D;JGE //if all 32 cells have been drawn
		@SCREENBLOCKCNT
		M=0
			(DRAWBLOCKS) // draw 16 blocks
			@512
			D=A
			@SCREENBLOCKCNT
			D=D-M
			@CELLCONT //if all 16 block have been drawn
			D;JLE

			//actually placing the block
			@SCREENBLOCKCNT
			D=M
			@cnt
			D=M+D
			@row
			D=M+D //D contains index of block
			@ADDRBLOCK
			M=D
			@BLOCK
			A=M
			D=M //EITHER 0 or 1
			@WHITE
			D;JEQ
			(BLACK)
				@ADDRBLOCK
				A=M
				M=-1
				@CONTINUEDRAWING
				0;JMP
			(WHITE)
				@ADDRBLOCK
				A=M
				M=0
			(CONTINUEDRAWING)
			
			@32
			D=A
			@SCREENBLOCKCNT
			M=M+D
			@DRAWBLOCKS
			0;JMP
		(CELLCONT)	
		@BLOCK
		M=M+1
		@1
		D=A
		@cnt
		M=M+D
		@DRAWCELLS
		0;JMP
	(ROWCONT)	
	@512 // continue to drawing next row of cells (16x32 screen blocks are already used for last row)
	D=A
	@row
	M=M+D 
@DRAWROW
0;JMP



(START)
@99
D=M
@END
D;JEQ
@99
M=M-1


//need to back up current world:
@100
D=A
@BLOCK //address of current cell value
M=D
@1100
D=A
@COPY //address of backup of current cell value
M=D

(BACKUP)
@BLOCK
D=M
@611 
D=A-D
@NEW //if all cells have been copied, move on
D;JLT
@BLOCK
A=M
D=M
@COPY
A=M
M=D //copy
@BLOCK//move on to next cell
M=M+1
@COPY
M=M+1
@BACKUP
0;JMP

(NEW) //new generation
@100
D=A
@BLOCK //address of current cell value
M=D
@1100
D=A
@COPY //address of backup of current cell value
M=D
@2100
D=A
@COUNTS //address of counts of each cell
M=D
	//clean previous iteration counts
	@2100
	D=A
	@CLEARER
	M=D
	(CLEANCNT)
		@2611
		D=A
		@CLEARER
		D=D-M
		@NEXTCELL
		D;JLT
		@CLEARER
		A=M
		M=0 //remove any previous value from counter
		@CLEARER
		M=M+1
		@CLEANCNT
		0;JMP

(NEXTCELL) //need to calculate neighbor count of each cell:
	@BLOCK
	D=M
	@611
	D=A-D
	@LOOP //if all cells have been recalculated, goto next iteration
	D;JLT
	@5543
	@UPEXIST
	M=0
	@DOWNEXIST
	M=0

	//UPPER
	@5544
	@131
	D=A
	@BLOCK
	D=M-D
	@NEXT1 
	D;JLE	//jumping means no upper row
	@UPEXIST
	M=1
	@32
	D=A
	@COPY
	D=M-D // D contains address of upper cell (backup)
	A=D
	D=M //D contains value of upper cell (backup)
	@NEXT1
	D;JEQ
	@COUNTS
	A=M
	M=M+1

	//LOWER
	@5545
	(NEXT1)
	@580 //last row
	D=A
	@BLOCK
	D=M-D
	@NEXT2
	D;JGE //jumping means no lower row
	@DOWNEXIST
	M=1
	@32
	D=A
	@COPY
	D=M+D // D contains address of lower cell (backup)
	A=D
	D=M //D contains value of lower cell (backup)
	@NEXT2
	D;JEQ
	@COUNTS
	A=M
	M=M+1 

	//LEFT
	@5546
	(NEXT2)
	@100
	D=A
	@LEFTCOUNTER
	M=D
		(LEFTLOOP) //check if left exists
		@611
		D=A
		@LEFTCOUNTER
		D=M-D 
		@CONTLEFT //jumping here means left exists
		D;JGE
		@BLOCK
		D=M
		@LEFTCOUNTER
		D=M-D
		@NEXT3
		D;JEQ
		@32
		D=A
		@LEFTCOUNTER
		M=M+D
		@LEFTLOOP
		0;JMP
	(CONTLEFT)
	@5547
	@COPY
	D=M-1 //D contains address of left cell
	A=D
	D=M //D contains value of left cell
	@DIAGUPLEFT
	D;JEQ
	@COUNTS
	A=M
	M=M+1
	//check up and down left diagonally:
		@5548
		(DIAGUPLEFT)
		@UPEXIST
		D=M
		@DIAGDOWNLEFT
		D;JEQ
		@33 
		D=A
		@COPY
		D=M-D //D contains address of backup of upper left cell
		A=D
		D=M //D contains value of backup of upper left cell
		@DIAGDOWNLEFT
		D;JEQ
		@COUNTS
		A=M
		M=M+1
			@5549
			(DIAGDOWNLEFT)
			@DOWNEXIST
			D=M
			@NEXT3
			D;JEQ
			@31
			D=A
			@COPY
			D=M+D //D contains address of down left cell
			A=D
			D=M //D contains value of down left cell
			@NEXT3
			D;JEQ
			@COUNTS
			A=M
			M=M+1

	//RIGHT
	@5550
	(NEXT3)
	@131
	D=A
	@RIGHTCOUNTER
	M=D
		@5551
		(RIGHTLOOP) //check if right exists
		@611
		D=A
		@RIGHTCOUNTER
		D=M-D
		@CONTRIGHT //jumping here means right exists
		D;JGT
		@BLOCK
		D=M
		@RIGHTCOUNTER
		D=M-D
		@UPDATECELL
		D;JEQ
		@32
		D=A
		@RIGHTCOUNTER
		M=M+D
		@RIGHTLOOP
		0;JMP
	(CONTRIGHT)
	@5552
	@COPY
	D=M+1 //D contains address of right cell
	A=D
	D=M //D contains value of right cell
	@DIAGUPRIGHT
	D;JEQ
	@COUNTS
	A=M
	M=M+1
	//check up and down right diagonally:
		@5553
		(DIAGUPRIGHT)
		@UPEXIST
		D=M
		@DIAGDOWNRIGHT
		D;JEQ
		@31 
		D=A
		@COPY
		D=M-D //D contains address of backup of upper right cell
		A=D
		D=M //D contains value of backup of upper right cell
		@DIAGDOWNRIGHT
		D;JEQ
		@COUNTS
		A=M
		M=M+1
			@5554
			(DIAGDOWNRIGHT)
			@DOWNEXIST
			D=M
			@UPDATECELL
			D;JEQ
			@33
			D=A
			@COPY
			D=M+D //D contains address of down right cell
			A=D
			D=M //D contains value of down right cell
			@UPDATECELL
			D;JEQ
			@COUNTS
			A=M
			M=M+1

//update cell
@5555
(UPDATECELL)
@BLOCK
A=M
D=M // value of current cell
@UNPOPULATED
D;JEQ
	//if this part is reached, cell is populated
	@1
	D=A
	@COUNTS
	A=M
	D=M-D
	@MORENEIGHBORS
	D;JGT // has more than 1 neighbor
	@BLOCK
	A=M
	M=0 //cell is dead :(
	@CONTINUE
	0;JMP
		@5556
		(MORENEIGHBORS)
		@4
		D=A
		@COUNTS
		A=M
		D=M-D
		@CONTINUE
		D;JLT // has less than 4 neighbors
		@BLOCK
		A=M
		M=0 //cell is dead :(
		@CONTINUE
		0;JMP

(UNPOPULATED)
@5557
	@3
	D=A
	@COUNTS
	A=M
	D=M-D
	@CONTINUE
	D;JNE //if not three neighbors, cant become populated
	@BLOCK //if this part is reached, new cell is born
	A=M
	M=1

(CONTINUE)
@5558
@BLOCK //move onto next cell
M=M+1
@COPY
M=M+1
@COUNTS
M=M+1
@NEXTCELL
0;JMP

(END)
@END
0;JMP