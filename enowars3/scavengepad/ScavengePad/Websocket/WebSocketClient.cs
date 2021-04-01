using Microsoft.AspNetCore.Http;
using Newtonsoft.Json;
using ScavengePad;
using ScavengePad.Models.Database;
using ScavengePad.Models.Json;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace ScavengePad.Websocket
{
    public class WebSocketClient
    {
        readonly HttpContext Context;
        readonly WebSocket WebSocket;
        readonly Channel Channel;
        public User User { get; }
        public ConcurrentQueue<WebSocketServerMessage> OutputQueue { get; } = new ConcurrentQueue<WebSocketServerMessage>();
        public CancellationTokenSource CancelSource { get; } = new CancellationTokenSource();

        public WebSocketClient(HttpContext context, WebSocket webSocket, User user, Channel channel)
        {
            Context = context;
            WebSocket = webSocket;
            User = user;
            Channel = channel;
        }

        public Task StartOutputTask(CancellationToken token)
        {
            return Task.Run(async () =>
            {
                try
                {
                    while (!token.IsCancellationRequested)
                    {
                        if (OutputQueue.TryDequeue(out var message))
                        {
                            var encoded = Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(message));
                            var buffer = new ArraySegment<byte>(encoded, 0, encoded.Length);
                            await WebSocket.SendAsync(buffer, WebSocketMessageType.Text, true, token);
                        }
                        else
                        {
                            if (CancelSource.IsCancellationRequested)
                            {
                                await WebSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "nologin", token);
                                break;
                            }
                            await Task.Delay(100);
                        }
                    }
                }
                catch (TaskCanceledException) { }
                catch (Exception e)
                {
                    Console.WriteLine($"OutputTask failed: {e.Message}\n{e.StackTrace}");
                }
                Console.WriteLine($"OutputTask finished");
            });
        }

        public Task StartInputTask(CancellationToken token)
        {
            return Task.Run(async () =>
            {
                try
                {
                    while (!token.IsCancellationRequested)
                    {
                        WebSocketReceiveResult response;
                        var message = new List<byte>();
                        var buffer = new byte[4096];

                        do
                        {
                            response = await WebSocket.ReceiveAsync(new ArraySegment<byte>(buffer), token);
                            message.AddRange(new ArraySegment<byte>(buffer, 0, response.Count));
                            if (response.MessageType == WebSocketMessageType.Close)
                            {
                                CancelSource.Cancel();
                                Console.WriteLine($"InputTask finished");
                                return;
                            }
                        } while (!response.EndOfMessage);
                        var msg = Encoding.UTF8.GetString(message.ToArray());
                        await Channel.HandleWSMessage(this, msg);
                    }
                }
                catch (TaskCanceledException) { }
                catch (WebSocketException) { }
                catch (Exception e)
                {
                    Console.WriteLine($"InputTask failed: {e.ToFancyString()}");
                    CancelSource.Cancel();
                }
            });
        }
    }
}
