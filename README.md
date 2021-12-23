liFuck
======

**What is this?**

An interpreter for something like brainfuck.

**Why 'something like'?**

For various reasons:
 - It's probably inefficient AF. It's not built to be very useful.
 - It has configurable limits on the max and min values for cells.
 - It implements procedures. Probably one of the worst ways to do so but still.

**So why make it?**

For fun. The idea to build 'brainfuck but with functions' seemed pretty funny.

**Does it work?**

I think so. I'm not the greatest brainfuck programmer so there's only so much
I am able to test and understand.


Syntax
------

`+`     Adds 1 to the current cell.  
`-`     Substracts 1 from the current cell.  
`>`     Moves right 1 cell.  
`<`     Moves left 1 cell.  
`[`     Begins loop.  
`]`     Checks current cell for 0 if not found, restarts loop.  
`.`     Prints the current number or printable char.  
`,`     Reads input and overwrites current cell.  
`(`     Begins procedure declaration. The following code doesn't execute inmediately.  
`)`     Ends fucntion declaration and appends the procedure to the procedure list.  
`*`     Reads the current cell and calls the procedure read index in the procedure list.