using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace Day12
{
    /// <summary>
    /// Represents the set of rules
    /// </summary>
    public class Rules
    {
        public List<Rule> RuleList { get; set; } = new List<Rule>();

        /// <summary>
        /// Load rules from file
        /// </summary>
        /// <param name="fileName">Name of the file containing rules</param>
        public void LoadRules(string fileName)
        {
            RuleList.RemoveAll(r => true);
            var lines = File.ReadLines(fileName);
            foreach (var line in lines)
            {
                RuleList.Add(new Rule(line));
            }
        }

        /// <summary>
        /// Given neighborhood, will the middle pot be occupied?
        /// </summary>
        /// <param name="neighborhood">Neighborhood of some pot</param>
        /// <returns>True if it will be occupied by plant next generation</returns>
        public bool ApplyRule(bool[] neighborhood)
        {
            return FindRuleByNeighborhood(neighborhood)?.Result ?? false;
        }

        private Rule FindRuleByNeighborhood(bool[] neighborhood)
        {
            return RuleList.FirstOrDefault(r => neighborhood.SequenceEqual(r.Input));
        }
    }
}
