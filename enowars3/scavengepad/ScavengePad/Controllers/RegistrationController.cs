using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using ScavengePad.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using ScavengePad.Storage;

namespace ScavengePad.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class RegistrationController : Controller
    {
        [HttpPost]
        public async Task<IActionResult> Post([FromForm] string username, [FromForm] string password1, [FromForm] string password2, [FromForm] string authkey)
        {
            var user = await DbUtils.InsertNewUser(username, password1, authkey);
            HttpContext.Session.SetInt32("userid", (int)user.Id);
            return Json(new {
                username = user.Username,
                teamId = user.TeamId
            });
        }
    }
}