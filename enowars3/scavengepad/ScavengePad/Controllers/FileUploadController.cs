using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using ScavengePad.Models;
using ScavengePad.Websocket;
using ScavengePad;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using ScavengePad.Storage;

namespace ScavengePad.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FileUploadController : Controller
    {
        [HttpPost]
        public async Task<IActionResult> Post([FromForm] ICollection<IFormFile> files, [FromForm] long? objectiveId, [FromForm] long operationId)
        {
            var userId = HttpContext.Session.GetInt32("userid");
            if (userId.HasValue)
            {
                await DbUtils.InsertFilesForObjective(files, userId.Value, objectiveId.Value, operationId);
                return NoContent();
            }
            return Forbid();
        }
    }
}