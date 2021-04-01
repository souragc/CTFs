using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace ScavengePad.Pages
{
    public class IndexModel : PageModel
    {
        public IActionResult OnGet()
        {
            var userId = HttpContext.Session.GetInt32("userid");
            if (userId.HasValue)
            {
                ViewData["Userid"] = (long) userId.Value;
            }
            return Page();
        }
    }
}