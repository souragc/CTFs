using ScavengePad.Websocket;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Net.WebSockets;
using Microsoft.AspNetCore.Http;
using ScavengePad.Models;
using Nito.AsyncEx;
using ScavengePad;
using ScavengePad.Storage;

namespace ScavengePad
{
    public class ScavengePadController
    {
        private static readonly Dictionary<long, Channel> WebsocketChannels = new Dictionary<long, Channel>();
        private static readonly AsyncLock Lock = new AsyncLock();

        public static async Task HandleNewWebSocketClient(HttpContext context, WebSocket webSocket)
        {
            if (!context.Session.GetInt32("userid").HasValue)
            {
                return;
            }
            var userId = context.Session.GetInt32("userid").Value;
            var user = await DbUtils.GetUser(userId);
            var channel = await GetOrCreateChannel(user.TeamId);
            var client = new WebSocketClient(context, webSocket, user, channel);
            
            var outputTask = client.StartOutputTask(Startup.ApplicationLifetime.ApplicationStopping);
            var inputTask = client.StartInputTask(Startup.ApplicationLifetime.ApplicationStopping);
            await channel.Add(client);
            await outputTask;
            await inputTask;
        }

        public static async Task DispatchOperationUpdate(long teamId, long operationId)
        {
            var channel = await GetOrCreateChannel(teamId);
            await channel.DispatchOperationUpdate(operationId);
        }

        private static async Task<Channel> GetOrCreateChannel(long teamId)
        {
            using(await Lock.LockAsync())
            {
                if (WebsocketChannels.ContainsKey(teamId))
                {
                    return WebsocketChannels[teamId];
                }
                else
                {
                    var channel = new Channel();
                    WebsocketChannels.Add(teamId, channel);
                    return channel;
                }
            }
        }
    }
}
