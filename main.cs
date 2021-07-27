using System;
class MainClass
{
  public static void Out(int number)
  {
    Console.WriteLine(number.ToString());
  }
  public static void Out(int[] numbers)
  {
    string output = "";
    for(int i = 0;
    i < numbers.Length;
    i++)
    {
      output += Convert.ToChar(numbers[i] % 65536);
    }
    Console.WriteLine(output);
  }
  public static int[] InList()
  {
    string input = Console.ReadLine();
    int[] numbers = new int[input.Length];
    for(int i = 0;
    i < numbers.Length;
    i++)
    {
      numbers[i] = Char.ConvertToUtf32(input, i);
    }
    return numbers;
  }
  public static int InNumber()
  {
    string input = Console.ReadLine();
    Int32.TryParse(input, out int j);
    return j;
  }
  public static int InKey()
  {
    ConsoleKeyInfo key = Console.ReadKey(true);
    return (int)Char.ConvertToUtf32(key.KeyChar.ToString(), 0);
  }
  public static int[] GetDateTime()
  {
    DateTime now = DateTime.Now;
    int[] dateTime = new int[6];
    dateTime[0] = now.Second;
    dateTime[1] = now.Minute;
    dateTime[2] = now.Hour;
    dateTime[3] = now.Day;
    dateTime[4] = now.Month;
    dateTime[5] = now.Year;
    return dateTime;
  }
  public static Random rand = new Random();
  public static int GetRandom()
  {
    return rand.Next();
  }
  public static void Main()
  {
    int m_lastTime = 0;
    while(true)
    {
      int[] m_date = GetDateTime();
      if (m_lastTime != m_date[0])
      {
        Out(m_date[0]);
      }
      m_lastTime = m_date[0];
    }
    TestFunction();
  }
  public static void TestFunction()
  {
    while(true)
    {
      Out(InKey());
    }
  }
  struct Vector
  {
    int m_xValue;
    int m_yValue;
  }
  public static int Fifteen()
  {
    int m_number;
    m_number = 15;
    return m_number;
  }
}
