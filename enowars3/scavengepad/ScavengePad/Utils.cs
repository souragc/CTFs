using Microsoft.AspNetCore.Cryptography.KeyDerivation;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace ScavengePad
{
    public static class UriExtensions
    {
        public static Uri SetPort(this Uri uri, int newPort)
        {
            var builder = new UriBuilder(uri)
            {
                Port = newPort
            };
            return builder.Uri;
        }

        public static Uri SetHost(this Uri uri, string host)
        {
            var builder = new UriBuilder(uri)
            {
                Host = host
            };
            return builder.Uri;
        }
    }

    public static class ExceptionExtensions
    {
        public static string ToFancyString(this Exception e)
        {
            string fancy = $"{e.Message} ({e.GetType()})\n{e.StackTrace}";
            if (e.InnerException != null)
            {
                fancy += $"\nInnerException:\n{ToFancyString(e.InnerException)}";
            }
            return fancy;
        }
    }

    public static class StringExtensions
    {
        internal static byte[] ToByteArray(this string input)
        {
            var bytes = new List<byte>();
            for (int i = 0; i < input.Length; i++)
            {
                bytes.AddRange(BitConverter.GetBytes(input[i]));
            }
            return bytes.ToArray();
        }
    }

    public static class ScavengePadUtils
    {
        private static readonly Random Random = new Random();
        public static int GetRandomInt() => Random.Next();

        public static string SHA256(string input)
        {
            byte[] bytes = Encoding.UTF8.GetBytes(input);
            SHA256Managed hashstring = new SHA256Managed();
            byte[] hash = hashstring.ComputeHash(bytes);
            return Convert.ToBase64String(hash);
        }
    }
}
