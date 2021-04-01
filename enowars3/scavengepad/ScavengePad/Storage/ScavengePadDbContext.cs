using ScavengePad.Models.Database;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ScavengePad.Storage
{
    public class ScavengePadDbContext : DbContext
    {
        public DbSet<User> Users { get; set; }
        public DbSet<Team> Teams { get; set; }
        public DbSet<Objective> Objectives { get; set; }
        public DbSet<Operation> Operations { get; set; }
        public DbSet<File> Files { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            var database = Environment.GetEnvironmentVariable("DATABASE_DOMAIN") ?? "localhost";
            optionsBuilder.UseNpgsql($@"Server={database};Port=5432;Database=ScavengePadDb;User Id=docker;Password=docker;");
        }

        protected override void OnModelCreating(ModelBuilder builder)
        {
            builder.Entity<User>()
                .HasIndex(u => u.Username)
                .IsUnique();
        }
    }
}
