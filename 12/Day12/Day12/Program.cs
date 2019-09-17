using System;
 
namespace Day12
{
    class Program
    {
        static void Main(string[] args)
        {
            string initialState = "##.##.#.#...#......#..#.###..##...##.#####..#..###.########.##.....#...#...##....##.#...#.###...#.##";
            var pots = new Pots(initialState, "rules.txt");

            pots.ForwardGenerations(20);
            Console.WriteLine($"Result 1: {pots.SumOfTheNumbersOfPotsWhichContainPlant()}");

            pots.ForwardGenerations(50000000000 - 20);
            Console.WriteLine($"Result 2: {pots.SumOfTheNumbersOfPotsWhichContainPlant()}");

            Console.ReadKey();
        }
    }
}
