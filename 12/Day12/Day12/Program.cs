using System;
 
namespace Day12
{
    class Program
    {
        static void Main(string[] args)
        {
            //string initialState = "#..#.#..##......###...###";
            //var pots = new Pots(initialState, "example.txt");
            string initialState = "##.##.#.#...#......#..#.###..##...##.#####..#..###.########.##.....#...#...##....##.#...#.###...#.##";
            var pots = new Pots(initialState, "rules.txt");

            //Console.WriteLine(pots.SumOfTheNumbersOfPotsWhichContainPlant());
            //for (int i = 0; i < 2000; i++)
            //{
            //    pots.NextGeneration();
            //    pots.PrintStatus();
            //}


            pots.ForwardGenerations(50000000000);
            Console.WriteLine($"Result 2: {pots.SumOfTheNumbersOfPotsWhichContainPlant()}");

            Console.ReadKey();
        }
    }
}
