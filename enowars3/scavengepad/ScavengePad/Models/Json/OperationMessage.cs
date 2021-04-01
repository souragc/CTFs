using ScavengePad.Models.Database;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ScavengePad.Models.Json
{
    public class OperationMessage
    {
        public long? Id { get; set; }
        public long TeamId { get; set; }
        public string Title { get; set; }
        public string OperationPadSuffix { get; set; }
        public List<File> Files { get; set; } = new List<File>();
        public Dictionary<string, List<Objective>> Categories { get; set; } = new Dictionary<string, List<Objective>>();

        public OperationMessage()
        {

        }

        public OperationMessage(Operation operation)
        {
            Id = operation.Id;
            Title = operation.Title;
            Categories = operation.GetObjectivesDictionary();
            TeamId = operation.TeamId;
            OperationPadSuffix = operation.OperationPadSuffix;
            Files = operation.Files;
        }

        public Operation GetOperation()
        {
            return new Operation()
            {
                Id = Id ?? 0,
                Objectives = Categories.Values.SelectMany(x => x).ToList(),
                TeamId = TeamId,
                OperationPadSuffix = OperationPadSuffix,
                Title = Title,
                Files = Files
            };
        }
    }
}
