Profiling the engine is actually not as hard as it looks, and one only needs the default built engine version and no other special tools.

**Requirements:**

Very Sleepy CS profiler (free, just google it) (included in repo)

sleepy_translator.py (included in repo)

zip.exe and addr2line.exe (included in repo)

A copy of the engine source (get the correct tag from github, just webdownload is sufficient) which reflects the version being debugged

Download and unzip next to script the debug symbols from http://springrts.com/dl/buildbot/default/develop/101.0.1-63-g5ebf047/win32/ (chose the right version!) 

Python 2.x 


**Process:**

Launch spring, get to the part you want to profile, then launch Very Sleepy, and select the threads you wish to profile (main thread of spring is sufficient)

When you are finished with collecting the samples, just save the myprofile.sleepy file from Very Sleepy->Save As next to your sleepy_translator.py

Launch the translator with:

python sleepy_translator.py -i myprofile.sleepy -s c:\temp\springsources\spring-master\ dont forget the trailing slash at the -s path to source option.

Open the myprofile_translated.sleepy file, and bask in the translated glory!

**Creating a spring.dbg**

As the debug symbols are no longer on buildbot, you gotta make them yourself:

set tostripfile=G:\_programming\zero-k\spring-m\build-mingw-m64\spring.exe

set debugfile=E:\Games\Spring\_support\spring.dbg

objcopy --only-keep-debug "%tostripfile%" "%debugfile%"
