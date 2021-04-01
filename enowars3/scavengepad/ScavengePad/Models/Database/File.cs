using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ScavengePad.Models.Database
{
    public class File
    {
        public long Id { get; set; }
        public string Name { get; set; }
        public User Uploader { get; set; }
        public long UploaderId { get; set; }
        public string MimeType { get; set; }
        public DateTime Timestamp { get; set; }
    }
}
