using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ScavengePad.Models.Database
{
    public class User
    {
        public long Id { get; set; }
        public byte[] Username { get; set; }
        public byte[] Password { get; set; }
        public Team Team { get; set; }
        public long TeamId { get; set; }
    }
}
