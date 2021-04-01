using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.WebSockets;
using System.Threading.Tasks;
using ScavengePad.Models;
using ScavengePad.Websocket;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using SharpReverseProxy;
using ScavengePad;
using ScavengePad.Storage;
using Microsoft.AspNetCore.DataProtection;
using System.IO;

namespace ScavengePad
{
    public class Startup
    {
        public static IHostingEnvironment HostingEnvironment { get; private set; }
        public static IApplicationLifetime ApplicationLifetime { get; private set; }

        // This method gets called by the runtime. Use this method to add services to the container.
        // For more information on how to configure your application, visit https://go.microsoft.com/fwlink/?LinkID=398940
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddMvc().SetCompatibilityVersion(CompatibilityVersion.Version_2_1);
            services.AddDistributedRedisCache(options =>
            {
                options.Configuration = $"{Environment.GetEnvironmentVariable("REDIS_DOMAIN") ?? "redis"}:6379";
            });
            services.AddSession(options =>
            {
                options.Cookie.IsEssential = true;
                options.IdleTimeout = TimeSpan.FromDays(30);
                options.Cookie.HttpOnly = true;
            });
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IApplicationLifetime applicationLifetime, IHostingEnvironment env)
        {
            HostingEnvironment = env;
            ApplicationLifetime = applicationLifetime;
            DbUtils.Migrate();
            app.UseSession();
            app.UseWebSockets(new WebSocketOptions() { KeepAliveInterval = TimeSpan.FromSeconds(45) });
            app.Use(async (context, next) =>
            {
                if (context.Request.Path == "/scavengepadws/")
                {
                    if (context.WebSockets.IsWebSocketRequest)
                    {
                        WebSocket webSocket = await context.WebSockets.AcceptWebSocketAsync();
                        await ScavengePadController.HandleNewWebSocketClient(context, webSocket);
                    }
                    else
                    {
                        await next();
                    }
                }
                else
                {
                    await next();
                }
            });

            app.UseProxy(new List<ProxyRule>
            {
                new ProxyRule
                {
                    Matcher = uri => IsCodiMDRequest(uri),
                    Modifier = (req, user) =>
                    {
                        req.RequestUri = req.RequestUri
                            .SetPort(Program.CodiPort)
                            .SetHost(Program.CodiDomain);
                    }
                }
            });

            app.UseMvc();
            app.UseDeveloperExceptionPage();
            app.UseFileServer(options: new FileServerOptions()
            {
                EnableDirectoryBrowsing = true
            });
            app.UseStaticFiles(new StaticFileOptions()
            {
                ServeUnknownFileTypes = true,
                OnPrepareResponse = ctx =>
                {
                    ctx.Context.Response.Headers.Append("filename", "foo.txt");
                }
            });
        }

        private static bool IsEtherpadRequest(Uri uri)
        {
            if (uri.AbsoluteUri.Contains("/static"))
                return true;

            if (uri.AbsoluteUri.Contains("/p/"))
                return true;

            if (uri.AbsoluteUri.Contains("/locales/"))
                return true;

            if (uri.AbsoluteUri.Contains("/socket.io/"))
                return true;

            if (uri.AbsoluteUri.EndsWith("/locales.json"))
                return true;

            if (uri.AbsoluteUri.Contains("/javascripts/"))
                return true;

            if (uri.AbsoluteUri.Contains("/pluginfw/"))
                return true;

            if (uri.AbsoluteUri.EndsWith("/etherpad"))
                return true;

            return false;
        }

        public static string[] CodiPages = new string[]
        {
            "/build/",
            "/config",
            "/PAD_",
            "/socket.io/",
            "/me",
            "js/mathjax-config-extra.js"
        };
        public static bool IsCodiMDRequest(Uri uri)
        {
            foreach (var path in CodiPages)
            {
                if (uri.AbsoluteUri.Contains(path))
                    return true;
            }
            return false;
        }
    }
}
