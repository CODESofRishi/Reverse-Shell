Content-Type: text/x-zim-wiki
Wiki-Format: zim 0.4
Creation-Date: 2019-10-07T08:27:53-04:00

====== Python Network Programming ======
Created Monday 07 October 2019

**1. WHAT IS MEANT BY FILE HANDLING ?**
* You could mean the process by which a software handles its Input/Output operations with binary/text files.
* For example, in any program that handles permanent data, you need to write and read information whether that is via a Database Handler or by using explicit Files.

**2. WHAT IS STDIN, STDOUT, STDERR ?** 
* **Standard input** - this is the file handle that your process reads to get information from you.
* **Standard output** - your process writes normal information to this file handle.
* **Standard error** - your process writes error information to this file handle.

	That's about as dumbed-down as I can make it :-)

	Of course, that's mostly by convention. There's nothing stopping you from writing your error information to standard output if you wish. You can even close the three file handles totally and open your own files for I/O.

	When your process starts, it should already have these handles open and it can just read from and/or write to them.	

**3. Pipes in Python:**
	A pipe is basically a block of memory in the kernel, a buffer that is read/written by some processes. The advantage of using pipes is that it has 2 file descriptors associated 	with it, and thus sharing data between 2 processes is as simple as reading/writing to a file. 

	Thus when you run a command like (in Python):

		'''
		import os
		rfd, wfd = os.pipe()
		'''

	
	What is essentially done is a block of memory is kept aside for the pipe and 2 file descriptors are returned that can be used to write data and read data from that memory block. 

4. **subprocess.PIPE**: Special value that can be used as the stdin, stdout or stderr argument to Popen and indicates that a pipe to the standard stream should be opened.

5. For **popen()** see https://stackabuse.com/pythons-os-and-subprocess-popen-commands/

