using ScavengePad.Models.Database;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ScavengePad.Models.Json
{
    public class WebSocketServerMessage
    {
        public OperationListMessage OperationListMessage { get; set; }
        public bool NotLoggedInMessage { get; set; }
        public OperationMessage ModifyOperationMessage { get; set; }
    }
}
