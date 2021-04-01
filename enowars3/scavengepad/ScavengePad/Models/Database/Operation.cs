using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

namespace ScavengePad.Models.Database
{
    public class Operation
    {
        public long Id { get; set; }
        [Required]
        public string Title { get; set; }
        [Required]
        public Team Team { get; set; }
        public long TeamId { get; set; }
        public string OperationPadSuffix { get; set; }
        public List<Objective> Objectives { get; set; } = new List<Objective>();
        public List<File> Files { get; set; } = new List<File>();

        public Dictionary<string, List<Objective>> GetObjectivesDictionary()
        {
            var d = new Dictionary<string, List<Objective>>();
            foreach (var objective in Objectives)
            {
                if (d.ContainsKey(objective.Category))
                {
                    d[objective.Category].Add(objective);
                }
                else
                {
                    d.Add(objective.Category, new List<Objective>() { objective });
                }
            }
            return d;
        }
    }
}
