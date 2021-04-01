using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using ScavengePad.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using ScavengePad.Storage;

namespace ScavengePad.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class LoginController : Controller
    {
        [HttpPost]
        public async Task<IActionResult> Post([FromForm] string username, [FromForm] string password)
        {
            if (await DbUtils.TestLogin(username, password))
            {
                var user = await DbUtils.GetUser(username);
                HttpContext.Session.SetInt32("userid", (int) user.Id);
                return Json(new {
                    username = user.Username,
                    teamId = user.TeamId
                });
            }
            throw new Exception();
        }
    }
}