using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ScavengePad.Models.Database
{
    public class Team
    {
        public long Id { get; set; }
        public string Teamname { get; set; }
        public string Authkey { get; set; }
    }
}
