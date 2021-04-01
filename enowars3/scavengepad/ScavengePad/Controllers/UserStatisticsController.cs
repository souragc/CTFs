using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using ScavengePad.Storage;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace ScavengePad.Controllers
{
    [Route("api/[controller]")]
    public class UserStatisticsController : Controller
    {
        [HttpGet]
        public async Task<IActionResult> Get(int take, int drop)
        {
            if (take > 100)
            {
                take = 100;
            }
            var users = await DbUtils.GetUsers(take, drop);
            return Json(users.Select(u => u.Username));
        }
    }
}
