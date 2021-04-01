using ScavengePad.Models.Database;
using ScavengePad.Websocket;
using Microsoft.AspNetCore.Http;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using ScavengePad;
using System.Net.Sockets;
using Npgsql;
using System.Net;
using System.Text;

namespace ScavengePad.Storage
{
    public class DbUtils
    {
        const int MIGRATION_ATTEMPTS = 100;
        internal static void Migrate()
        {
            for (int i = 0;i < MIGRATION_ATTEMPTS;i++)
            {
                try
                {
                    using (var ctx = new ScavengePadDbContext())
                    {
                        var migrationsCount = ctx.Database.GetPendingMigrations().Count();
                        if (migrationsCount > 0)
                        {
                            Console.WriteLine($"Applying {migrationsCount} migrations");
                            ctx.Database.Migrate();
                            Console.WriteLine($"Database migration complete");
                        }
                        return;
                    }
                }
                catch (PostgresException e)
                {
                    Console.WriteLine($"ScavengePad DB migration failed: {e.ToFancyString()}");
                }
                catch (SocketException)
                {
                    Console.WriteLine("ScavengePad DB connection failed");
                }
                Task.Delay(1000).Wait();
            }
            throw new Exception("Database unavailable!");
        }

        internal static async Task<bool> TestLogin(string name, string password)
        {
            using (var ctx = new ScavengePadDbContext())
            {
                return await ctx.Users
                    .Where(u => u.Username == name.ToByteArray() && u.Password == password.ToByteArray())
                    .CountAsync() == 1;
            }
        }

        internal static async Task<User[]> GetUsers(int take, int skip)
        {
            using (var ctx = new ScavengePadDbContext())
            {
                return await ctx.Users
                    .OrderByDescending(u => u.Id)
                    .Skip(skip)
                    .Take(take)
                    .ToArrayAsync();
            }
        }

        internal static async Task<User> GetUser(long id)
        {
            using (var ctx = new ScavengePadDbContext())
            {
                return await ctx.Users
                    .Where(u => u.Id == id)
                    .FirstOrDefaultAsync();
            }
        }

        internal static async Task<User> GetUser(string name)
        {
            using (var ctx = new ScavengePadDbContext())
            {
                return await ctx.Users
                    .Where(u => u.Username == name.Normalize().ToByteArray())
                    .FirstAsync();
            }
        }

        internal static async Task<User> InsertNewUser(string name, string password, string authkey)
        {
            using (var ctx = new ScavengePadDbContext())
            {
                var team = await ctx.Teams
                    .Where(t => t.Authkey == authkey)
                    .FirstOrDefaultAsync();
                if (team == null)
                {
                    team = new Team()
                    {
                        Authkey = authkey,
                        Teamname = "default_teamname"
                    };
                    ctx.Teams.Add(team);
                }
                var user = new User()
                {
                    Username = name.ToByteArray(),
                    Password = password.ToByteArray(), // switch to hashed passwords some day, but not now
                    Team = team
                };
                ctx.Users.Add(user);
                await ctx.SaveChangesAsync();
                return user;
            }
        }

        internal static async Task<Operation> ModifyOperation(WebSocketClient client, Operation modifiedOperation)
        {
            Operation dbOperation;
            bool newOp = false;
            using (var ctx = new ScavengePadDbContext())
            {
                dbOperation = await ctx.Operations
                    .Where(c => c.Id == modifiedOperation.Id)
                    .Where(c => c.TeamId == client.User.TeamId)
                    .AsNoTracking()
                    .FirstOrDefaultAsync();
                
                if (dbOperation == null)
                {
                    dbOperation = new Operation()
                    {
                        TeamId = client.User.TeamId,
                        Title = modifiedOperation.Title,
                        Objectives = modifiedOperation.Objectives
                    };
                    ctx.Operations.Add(dbOperation);
                    newOp = true;
                }
                else
                {
                    ctx.Operations.Update(modifiedOperation);
                    dbOperation = modifiedOperation;
                }
                await ctx.SaveChangesAsync();
                if (newOp)
                {
                    dbOperation.OperationPadSuffix = WebUtility.UrlEncode(ScavengePadUtils.SHA256($"{dbOperation.Id}{ScavengePadUtils.GetRandomInt()}{ScavengePadUtils.GetRandomInt()}{ScavengePadUtils.GetRandomInt()}{ScavengePadUtils.GetRandomInt()}"));
                }
                foreach (var objective in dbOperation.Objectives)
                {
                    if (objective.ObjectivePadSuffix == "default")
                    {
                        objective.ObjectivePadSuffix = WebUtility.UrlEncode(ScavengePadUtils.SHA256($"{objective.Id}{ScavengePadUtils.GetRandomInt()}{ScavengePadUtils.GetRandomInt()}{ScavengePadUtils.GetRandomInt()}{ScavengePadUtils.GetRandomInt()}"));
                    }
                }
                await ctx.SaveChangesAsync();
            }
            return await GetOperation(dbOperation.Id);
        }

        public static async Task<List<Operation>> GetOperations(long userId)
        {
            using (var ctx = new ScavengePadDbContext())
            {
                var teamId = await ctx.Users
                    .Where(u => u.Id == userId)
                    .Select(u => u.TeamId)
                    .FirstOrDefaultAsync();
                return await ctx.Operations
                    .Where(op => op.TeamId == teamId)
                    .Include(op => op.Objectives)
                    .ThenInclude(obj => obj.Files)
                    .OrderByDescending(op => op.Id)
                    .AsNoTracking()
                    .ToListAsync();
            }
        }

        public static async Task<Operation> GetOperation(long operationId)
        {
            using (var ctx = new ScavengePadDbContext())
            {
                var operation =  await ctx.Operations
                    .Where(c => c.Id == operationId)
                    .Include(c => c.Files)
                    .AsNoTracking()
                    .FirstAsync();
                operation.Objectives = await ctx.Objectives
                    .Where(c => c.OperationId == operationId)
                    .Include(c => c.Files)
                    .OrderBy(f => f.Id)
                    .ToListAsync();
                return operation;
            }
        }

        public static async Task ChangeObjectiveStatus(long objectiveId, bool newStatus)
        {
            using (var ctx = new ScavengePadDbContext())
            {
                var objective = await ctx.Objectives
                    .Where(obj => obj.Id == objectiveId)
                    .FirstAsync();
                objective.Solved = newStatus;
                await ctx.SaveChangesAsync();
            }
        }

        public static async Task InsertFilesForObjective(IEnumerable<IFormFile> files, long uploaderId, long objectiveId, long operationId)
        {
            using (var ctx = new ScavengePadDbContext())
            {
                var objective = await ctx.Objectives
                    .Where(obj => obj.Id == objectiveId)
                    .Include(c => c.Files)
                    .FirstAsync();

                foreach (var formFile in files)
                {
                    File file = new File()
                    {
                        Name = formFile.FileName,
                        UploaderId = uploaderId,
                        MimeType = "//TODO",
                        Timestamp = DateTime.UtcNow
                    };
                    objective.Files.Add(file);
                    await ctx.SaveChangesAsync();
                    var filePath = $"{Startup.HostingEnvironment.WebRootPath}/uploads/{file.Id}";
                    using (var stream = new System.IO.FileStream(filePath, System.IO.FileMode.Create))
                    {
                        await formFile.CopyToAsync(stream);
                    }
                }
                await ScavengePadController.DispatchOperationUpdate((await ctx.Users.FindAsync(uploaderId)).TeamId, operationId);
            }
        }
    }
}
