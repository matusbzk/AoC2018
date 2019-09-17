using System;

namespace Day12.Helpers
{
    /// <summary>
    /// Simple logging class that logs to console
    /// </summary>
    public static class Logger
    {
        public static void Info(string message)
        {
            Console.WriteLine(message);
        }

        public static void Warn(string message)
        {
            Console.WriteLine(message);
        }

        public static void Error(string message)
        {
            Console.WriteLine($"ERROR:{message}");
        }
    }
}
