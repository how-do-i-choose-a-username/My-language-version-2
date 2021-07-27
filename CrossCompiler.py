import custom_exceptions as errors
import sys

# Get the file and read it
#filename = input("Please enter the name of the file to run: ")
filename = "HelloWorld"
if not filename.endswith(".mlv2"):
  filename += ".mlv2"
code = open(filename.replace("*doff", ""), "r").read()
lines = code.split("\n")


# Remove comments and clean the code up
cleanedCode = ""
for line in lines:
  line = line.split(r"//", 1)[0]  # Remove comments
  line = line.strip()
  if line != "":
    cleanedCode += line
cleanedCode = cleanedCode.replace(";", ";\n").replace("}", "\n}\n").replace("{", "\n{\n")


# Prep the code for compilation, making sure variables are valid etc.
cleanedCode = cleanedCode.replace("~$list", "~$int[]")  # Convert 'list' to 'int[]'
cleanedCode = cleanedCode.replace("~$", "~").replace("<$", "<<<")
cleanedCode = cleanedCode.replace("$", "$m_")
cleanedCode = cleanedCode.replace("~", "~$").replace("<<<", "<$")
lines = cleanedCode.split("\n")


# Get all custom variable and function names so we can check them later
functionNames = ["Out", "InList", "InNumber", "InKey", "GetDateTime", "if", "GetRandom"]
variableNames = ["int", "int[]"]
for line in lines:
  if line.startswith("<#"):
    line = line.replace("<#", "").replace(">","")
    line = line.split("(", 1)[0]
    functionNames.append(line)
  if line.startswith("<$"):
    variableNames.append(line.replace("<$", "").replace(">", ""))


# Check the code to make sure all functions and variables are valid
if "*doff" not in filename:
  try:
    # Checks brackets, ie, ensures none are missing
    openBrackets = cleanedCode.count("(")
    closedBrackets = cleanedCode.count(")")
    if openBrackets != closedBrackets:
      raise errors.unmatchedBrackets(openBrackets, closedBrackets)

    for line in lines:
      # Checks if variables are valid types
      if "~$" in line:
        for phrase in line.split("~$"):
          if not phrase or "=:" in phrase:
            continue
          phrase = phrase.split("$", 1)[0].strip()
          if phrase not in variableNames:
            raise errors.unknownVariable(phrase)

      # Checks if methods are valid
      if "#" in line and "<#" not in line:
        for phrase in line.split("#"):
          if not phrase or "=:" in phrase or "~$" in phrase:
            continue
          phrase = phrase.split("(", 1)[0].strip()
          if phrase not in functionNames:
            raise errors.unknownMethod(phrase)

  except errors.unmatchedBrackets as e:
    print(e)
    sys.exit(0)

  except errors.unknownVariable as e:
    print(e)
    sys.exit(0)

  except errors.unknownMethod as e:
    print(e)
    sys.exit(0)


# Convert .mlv2 to C#
generatedCode = open("StartOfCs.mlsupport", "r").read()
returningVariable = ""
bracketDepth = 0
for line in lines: # Need to add syntax checking
  line = line.strip()
  if line.startswith("<#"): # Need to add support for receiving variables, and proper sending suport
    if "=:" in line:
      variableName = line.split("=:", 1)[1].strip().replace(">","")
      returningVariable = variableName
      newLine = "public static " + variableName.split("~$")[1].split("$")[0].strip()
      newLine +=  " " + line.replace("<#", "").replace(">","").split("=:")[0].strip()
      line = newLine
    else:  
      line = "public static void " + line.replace("<#", "").replace(">","")
  elif line.startswith("<$"):
    line = "struct " + line.replace("<$", "").replace(">", "")
  elif line.startswith("~$"): # Will need to check if its in a struct and add public
    newLine = line.split(" ", 1)[0].replace("~$","")
    newLine += " " + line.split("$")[2]
    line = newLine.replace("#", "")
  elif line.startswith("$"):
    line = line.replace("$", "").replace("#", "")
  elif line.startswith("#"):
    line = line.replace("#", "").replace("$","")
  elif line.startswith("repeat"):
    line = "while(true)"
  elif line.startswith("if"):
    line = line.replace("$", "").replace("#", "")
  elif line.startswith("exit;"):
    line = "break;"
  elif line.startswith("{") and returningVariable != "":
    line = "{" + returningVariable.split(" ", 1)[0].replace("~$","") + " " + returningVariable.split("$")[2] + ";\n"
  elif line.startswith("}") and bracketDepth == 0 and returningVariable != "":
    line = "return " + returningVariable.split("$")[2].strip() + "; }"
    returningVariable = ""
  elif line.startswith("{"):
    bracketDepth += 1
  elif line.startswith("}"):
    bracketDepth -= 1
  generatedCode += line
generatedCode += "}"


# Add new lines where they should be
generatedCode = generatedCode.replace(";", ";\n").replace("}", "\n}\n").replace("{", "\n{\n")


# Remove blank lines from the generated code
lines = generatedCode.split("\n")
generatedCode = ""
bracketDepth = 0
for i in range(len(lines)):
  line = lines[i]
  if "}" in line:
    bracketDepth -= 1
  if line.strip() != "":
    generatedCode += " " * 2 * bracketDepth + line.strip() + "\n"
  if "{" in line:
    bracketDepth += 1


# Write the generated code to file, and print it for debug
#print(generatedCode)
newFile = open("main.cs", "w")
newFile.write(generatedCode)
newFile.close()

sys.exit(1)