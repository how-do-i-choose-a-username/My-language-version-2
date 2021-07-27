# Runs the python code to cross compile my language to C#
# It then compiles and runs the generated C# code

echo "Now running"
python CrossCompiler.py
if [ $? -eq 1 ] 
then
  echo "Compiling C# code"
  mcs -out:main.exe main.cs
  echo "Running code"
  mono main.exe
  echo "Complete"
else
then
  echo "Main - An Error Occured In The Cross Compiler"
fi