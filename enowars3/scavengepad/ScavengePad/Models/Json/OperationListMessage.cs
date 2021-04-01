using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ScavengePad.Models.Json
{
    public class OperationListMessage
    {
        public List<OperationMessage> OperationMessages { get; set; } = new List<OperationMessage>();
        public long TeamId { get; set; }
    }
}
