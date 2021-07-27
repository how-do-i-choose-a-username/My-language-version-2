# Runs the python code to cross compile my language to C#
# It then compiles and runs the generated C# code

echo "Now running"
python CrossCompiler.py
echo "Compiling C# code"
mcs -out:main.exe main.cs
echo "Running code"
mono main.exe
echo "Complete"