using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace ScavengePad.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TestController : Controller
    {
        [HttpGet]
        public IActionResult Get(int tasks)
        {
            for (int i = 0; i < tasks; i++)
            {
                Task.Run(() =>
                {
                    var rng = ScavengePadUtils.GetRandomInt();
                });
            }
            return Json(new
            {
                rng = ScavengePadUtils.GetRandomInt()
            });
        }
    }
}