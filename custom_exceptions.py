class unmatchedBrackets(Exception):
  """Called when an inequal number of brackets is found in the code
  
  Attributes:
    open - Number of open brackets
    closed - Number of closed brackets
  """
  def __init__(self, open, closed):
    self.message = "Inequal Number of Brackets"
    self.open = open
    self.closed = closed
  
  def inequality(self):
    if self.closed > self.open:
      return "("
    else:
      return ")"

  def __str__(self):
    self.missing = self.inequality()
    return f"CrossCompiler - {self.message}, expected '{self.missing}'"


class unknownVariable(Exception):
  """Called when an unknown variable type is referenced in the code

  Attributes:
    variable - Unknown variable that raised the error
  """
  def __init__(self, variable):
    self.variable = variable
    self.message = "Unknown variable type"

  def __str__(self):
    return f"CrossCompiler - {self.message}: {self.variable}"


class unknownMethod(Exception):
  """Called when an unknown method is referenced in the code

  Attributes:
    method - Unknown method that raised the error
  """
  def __init__(self, method):
    self.method = method
    self.message = "Unknown method referenced"

  def __str__(self):
    return f"CrossCompiler - {self.message}: {self.method}"
