using ScavengePad;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Nito.AsyncEx;
using Newtonsoft.Json;
using ScavengePad.Models.Json;
using ScavengePad.Storage;

namespace ScavengePad.Websocket
{
    public class Channel
    {
        private readonly List<WebSocketClient> Clients = new List<WebSocketClient>();
        private readonly AsyncLock Lock = new AsyncLock();

        public async Task HandleWSMessage(WebSocketClient client, string message)
        {
            var wsMessage = JsonConvert.DeserializeObject<WebSocketClientMessage>(message);
            if (wsMessage.ModifyOperationMessage != null)
            {
                await HandleModifyOperationMessage(client, wsMessage.ModifyOperationMessage);
            }
        }

        private async Task BroadcastLocked(long channelId, WebSocketServerMessage message)
        {
            using (await Lock.LockAsync())
            {
                Broadcast(channelId, message);
            }
        }

        private void Broadcast(long channelId, WebSocketServerMessage message)
        {
            foreach (var client in Clients)
            {
                client.OutputQueue.Enqueue(message);
            }
        }

        private async Task HandleModifyOperationMessage(WebSocketClient client, OperationMessage modifyOperationMessage)
        {
            using (await Lock.LockAsync())
            {
                var modifiedOperation = await DbUtils.ModifyOperation(client, modifyOperationMessage.GetOperation());
                Broadcast(client.User.TeamId, new WebSocketServerMessage()
                {
                    ModifyOperationMessage = new OperationMessage(modifiedOperation)
                });
            }
        }

        internal async Task Add(WebSocketClient client)
        {
            Clients.Add(client);
            client.OutputQueue.Enqueue(new WebSocketServerMessage()
            {
                OperationListMessage = new OperationListMessage()
                {
                    OperationMessages = (await DbUtils.GetOperations(client.User.Id)).Select(x => new OperationMessage(x)).ToList(),
                    TeamId = client.User.TeamId
                }
            });
        }

        public async Task DispatchOperationUpdate(long operationId)
        {
            using (await Lock.LockAsync())
            {
                var operation = await DbUtils.GetOperation(operationId);
                Broadcast(operation.TeamId, new WebSocketServerMessage()
                {
                    ModifyOperationMessage = new OperationMessage(operation)
                });
            }
        }
    }
}
