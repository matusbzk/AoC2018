using System.Text.RegularExpressions;

namespace Day12.Helpers
{
    public static class RegexHelper
    {
        public static Regex RuleRegex => new Regex(@"^(#|\.)(#|\.)(#|\.)(#|\.)(#|\.) => (#|\.)$");

        public static Regex ValidStateRegex => new Regex(@"^(#|\.)*$");
    }
}
