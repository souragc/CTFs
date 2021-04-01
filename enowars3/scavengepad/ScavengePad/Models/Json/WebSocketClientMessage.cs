using ScavengePad.Models.Database;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ScavengePad.Models.Json
{
    public class WebSocketClientMessage
    {
        public OperationMessage ModifyOperationMessage { get; set; }
    }
}
