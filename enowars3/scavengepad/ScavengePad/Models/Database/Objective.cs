using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

namespace ScavengePad.Models.Database
{
    public class Objective
    {
        public long Id { get; set; }
        [Required]
        public string Title { get; set; }
        [Required]
        public string Category { get; set; }
        public long Points { get; set; }
        public bool Solved { get; set; }
        [JsonIgnore]
        [Required]
        public Operation Operation { get; set; }
        public long OperationId { get; set; }
        public string ObjectivePadSuffix { get; set; }
        public Team Team { get; set; }
        public long TeamId { get; set; }
        public List<File> Files { get; set; } = new List<File>();
    }
}
