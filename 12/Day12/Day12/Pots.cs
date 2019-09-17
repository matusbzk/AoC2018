using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Day12.Helpers;

namespace Day12
{
    /// <summary>
    /// Represents the row of pots
    /// </summary>
    public class Pots
    {
        #region Properties and constructor
        /// <summary>
        /// Contains numbers of all pots that contain plant
        /// </summary>
        public HashSet<long> Plants { get; set; } = new HashSet<long>();

        public Rules Rules { get; set; } = new Rules();

        /// <summary>
        /// After a while, the formation of the plants is always the same, it just moves in some direction.
        /// When this is achieved, getting next generation(s) is much easier.
        /// </summary>
        public bool HasAchievedFinalFormation { get; set; }

        /// <summary>
        /// After final position is achieved, this is its movement - the difference between the number of
        /// the first plant between the generations.
        /// </summary>
        public long? FinalFormationMovement { get; set; }

        /// <summary>
        /// Creates instance of Pots
        /// </summary>
        /// <param name="initialState">Initial state as string of # and .</param>
        /// <param name="rulesFileName">Name of the file containing rules</param>
        public Pots(string initialState, string rulesFileName)
        {
            var regex = RegexHelper.ValidStateRegex;
            if (!regex.IsMatch(initialState))
            {
                throw new ArgumentException($"Invalid initial state: {initialState}");
            }

            ParseInitialState(initialState);
            Rules.LoadRules(rulesFileName);
        }


        #endregion

        #region Getting next generations
        /// <summary>
        /// Forwards the pots by X generations
        /// </summary>
        /// <param name="generations">Number of generations</param>
        public void ForwardGenerations(long generations)
        {
            if (HasAchievedFinalFormation)
            {
                ForwardGenerationsWithFinalFormation(generations);
            }
            else
            {
                for (var i = generations; i > 0; i--)
                {
                    if (NextGeneration())
                    {
                        ForwardGenerations(i - 1);
                        return;
                    }
                }
            }
        }

        /// <summary>
        /// Forwards the pots by 1 generation
        /// </summary>
        /// <returns>True if it has reached the final formation</returns>
        public bool NextGeneration()
        {
            HashSet<long> newPlants = new HashSet<long>();
            if (Plants.Count == 0)
            {
                return false;
            }
            for (var i = Plants.Min() - 2; i <= Plants.Max() + 2; i++)
            {
                if (WillContainPlantNextGeneration(i))
                {
                    newPlants.Add(i);
                }
            }

            var oldStatus = GetCurrentStatus();
            var oldFirstPosition = Plants.Min();
            Plants = newPlants;
            var newStatus = GetCurrentStatus();
            if (oldStatus == newStatus)
            {
                Logger.Info("Achieved final position");
                var newFirstPosition = Plants.Min();
                HasAchievedFinalFormation = true;
                FinalFormationMovement = newFirstPosition - oldFirstPosition;
                Logger.Info($"Final formation movement is {FinalFormationMovement}");
            }

            return HasAchievedFinalFormation;
        }

        /// <summary>
        /// Checks whether pot with given number will contain plant in the next generation
        /// </summary>
        /// <param name="index">Number of pot</param>
        /// <returns>True if the pot will contain plant</returns>
        private bool WillContainPlantNextGeneration(long index)
        {
            bool[] neighborhood = new[]
            {
                Plants.Contains(index - 2),
                Plants.Contains(index - 1),
                Plants.Contains(index),
                Plants.Contains(index + 1),
                Plants.Contains(index + 2)
            };
            return Rules.ApplyRule(neighborhood);
        }

        private void ForwardGenerationsWithFinalFormation(long generations)
        {
            if (!HasAchievedFinalFormation || !FinalFormationMovement.HasValue)
            {
                Logger.Error("Calling ForwardGenerationsWithFinalFormation before achieving final formation");
                throw new InvalidOperationException(
                    "Calling ForwardGenerationsWithFinalFormation before achieving final formation");
            }

            Logger.Info($"Starting final movement with first position {Plants.Min()}");
            HashSet<long> newPlants = new HashSet<long>();
            foreach (long plant in Plants)
            {
                newPlants.Add(plant + FinalFormationMovement.Value * generations);
            }

            Plants = newPlants;
            Logger.Info($"Ended final movement with first position {Plants.Min()}");
        }
        #endregion

        #region Results
        /// <summary>
        /// After 20 generations this is the result 1
        /// After 50000000000 generations  this is the result 2
        /// </summary>
        /// <returns>Sum of the numbers of all pots which contain a plant</returns>
        public long SumOfTheNumbersOfPotsWhichContainPlant() => Plants.Sum();
        #endregion

        #region Printing and status strings
        public void PrintStatus()
        {
            PrintStatus(Plants.Min() - 2, Plants.Max() + 2);
        }

        public void PrintStatus(long firstIndex, long lastIndex)
        {
            Console.WriteLine(GetCurrentStatus(firstIndex, lastIndex));
        }

        public string GetCurrentStatus()
        {
            return GetCurrentStatus(Plants.Min() - 2, Plants.Max() + 2);
        }

        public string GetCurrentStatus(long firstIndex, long lastIndex)
        {
            var stringBuilder = new StringBuilder();
            for (var i = firstIndex; i <= lastIndex; i++)
            {
                stringBuilder.Append(Plants.Contains(i) ? "#" : ".");
            }

            return stringBuilder.ToString();
        }

        /// <summary>
        /// Parses initial state
        /// </summary>
        /// <param name="initialState">Initial state as string of # and .</param>
        private void ParseInitialState(string initialState)
        {
            for (int i = 0; i < initialState.Length; i++)
            {
                if (initialState[i] == '#')
                {
                    Plants.Add(i);
                }
            }
        }
        #endregion
    }
}
