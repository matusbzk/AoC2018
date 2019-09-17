using System;
using Day12.Helpers;

namespace Day12
{
    /// <summary>
    /// Represents the rule for next generation
    /// </summary>
    public class Rule
    {
        public bool[] Input { get; set; }
        public bool Result { get; set; }

        public Rule(string ruleStr)
        {
            var regex = RegexHelper.RuleRegex;
            var match = regex.Match(ruleStr);
            if (!match.Success)
            {
                throw new ArgumentException($"String {ruleStr} does not contain valid rule");
            }

            var groups = match.Groups;
            Input = new[]
            {
                DoesContainPlant(groups[1].Value),
                DoesContainPlant(groups[2].Value),
                DoesContainPlant(groups[3].Value),
                DoesContainPlant(groups[4].Value),
                DoesContainPlant(groups[5].Value)
            };
            Result = DoesContainPlant(groups[6].Value);
        }

        /// <summary>
        /// Checks whether pot contains plant
        /// </summary>
        /// <param name="pot"># if given pot contains plant, . otherwise</param>
        /// <returns></returns>
        private bool DoesContainPlant(string pot)
        {
            switch (pot)
            {
                case "#":
                    return true;
                case ".":
                    return false;
                default:
                    throw new ArgumentException(nameof(pot));
            }
        }
    }
}
