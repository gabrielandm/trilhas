using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Microsoft.Azure.WebJobs.Host;
using projeto_08.Models;
using System.Collections.Generic;
using System.Linq;
using System.Data.SqlClient;

namespace projeto_08
{
    public static class ProductApi
    {
        static List<Product> products = new List<Product>();
        static private string connectionStr = 
            "Server=tcp:kumulus-paoli.database.windows.net,1433;" + 
            "Initial Catalog=test_database;Persist Security Info=False;" + 
            "User ID=login;Password=Password123;" + 
            "MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=True;Connection Timeout=30;";

        [FunctionName("CreateProduct")]
        public static async Task<IActionResult> CreateProduct(
            [HttpTriggerAttribute(AuthorizationLevel.Anonymous, "post", Route = "product")]HttpRequest req, TraceWriter log)
        {
            log.Info("[POST] Creating new product");
            bool queryDone = false;
            
            // Request body into Product Model
            string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
            var input = JsonConvert.DeserializeObject<ProductCreateModel>(requestBody);
            input.Name = input.Name.ToUpper(); // Formatting Name to be allways UPPER
                
            using (SqlConnection connection = new SqlConnection(connectionStr))
            {
                var sqlQuery = 
                    "INSERT INTO dbo.product " +
                    "VALUES (@name, @description, @price);";
                connection.Open();
                using (SqlCommand command = new SqlCommand(sqlQuery, connection))
                {
                    command.Parameters.AddWithValue("@name", input.Name);
                    command.Parameters.AddWithValue("@description", input.Description);
                    command.Parameters.AddWithValue("@price", input.Price);
                    try
                    {
                        var rows = await command.ExecuteNonQueryAsync();
                        queryDone = true;
                        log.Info("Product created successfully");
                    } 
                    catch
                    {
                        queryDone = false;
                    }
                }
            }
            if (queryDone == false)
            {
                return new BadRequestObjectResult(input);
            }
            return new OkObjectResult(input);
        }

        [FunctionName("GetProducts")]
        public static async Task<IActionResult> GetProducts(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = "product")]HttpRequest req, TraceWriter log)
        {
            log.Info("[GET] Getting all products");
            products.Clear();
            bool queryDone = false;
            using (SqlConnection connection = new SqlConnection(connectionStr))
            {
                connection.Open();
                var sqlQuery = "SELECT * " +
                    "FROM dbo.product;";

                using (SqlCommand command = new SqlCommand(sqlQuery, connection))
                {
                    try
                    {
                        SqlDataReader dReader = command.ExecuteReader();
                        while (dReader.Read())
                        {
                            string name = dReader.GetValue(0).ToString();
                            string description = dReader.GetValue(1).ToString();
                            Decimal price = System.Convert.ToDecimal(dReader.GetValue(2).ToString());
                            
                            var selectedProduct = new Product() {Name = name, Description = description, Price = price};
                            products.Add(selectedProduct);
                        }
                        queryDone = true;
                    } 
                    catch
                    {
                        queryDone = false;
                    }
                }
            }
            if (queryDone == false)
                return new BadRequestResult();
            return new OkObjectResult(products);
        }

        [FunctionName("GetProductByName")]
        public static IActionResult GetProductByName(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = "product/{name}")] HttpRequest req, TraceWriter log, string name)
        {
            log.Info($"[GET] Getting product named: {name}");
            products.Clear();
            bool queryDone = false;
            name = name.ToUpper();
            using (SqlConnection connection = new SqlConnection(connectionStr))
            {
                connection.Open();
                var sqlQuery = 
                    "SELECT * " +
                    "FROM dbo.product " +
                    "WHERE name like @name;";

                using (SqlCommand command = new SqlCommand(sqlQuery, connection))
                {
                    command.Parameters.AddWithValue("@name", name);
                    try
                    {
                        SqlDataReader dReader = command.ExecuteReader();
                        while (dReader.Read())
                        {
                            string description = dReader.GetValue(1).ToString();
                            Decimal price = System.Convert.ToDecimal(dReader.GetValue(2).ToString());
                            
                            var selectedProduct = new Product() {Name = name, Description = description, Price = price};
                            products.Add(selectedProduct);
                        }
                        queryDone = true;
                    } 
                    catch
                    {
                        queryDone = false;
                    }
                }
            }
            if (products.Count == 0)
                return new NotFoundResult();
            if (queryDone == false)
                return new BadRequestResult();
            return new OkObjectResult(products);
        }

        [FunctionName("UpdateProduct")]
        public static async Task<IActionResult> UpdateProduct(
            [HttpTrigger(AuthorizationLevel.Anonymous, "put", Route = "product/{name}")] HttpRequest req, TraceWriter log, string name)
        {
            log.Info($"[PUT] Updating product named: {name}");
            bool queryDone = false;
            // var connectionStr = Environment.GetEnvironmentVariable("AzureSQÇ"); // connection String for Azure
            
            // Request body into Product Model
            string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
            var input = JsonConvert.DeserializeObject<Product>(requestBody);
            name = name.ToUpper(); // Formatting Name to be allways UPPER
            input.Name = name;
                
            using (SqlConnection connection = new SqlConnection(connectionStr))
            {
                string sqlQuery = "";
                if (string.IsNullOrEmpty(input.Description) && input.Price < 100000.00m && input.Price > 0)
                {
                    sqlQuery = 
                        "UPDATE dbo.product " +
                        "SET price = @price " +
                        "WHERE name like @name;";
                    connection.Open();
                    using (SqlCommand command = new SqlCommand(sqlQuery, connection))
                    {
                        command.Parameters.AddWithValue("@name", input.Name);
                        command.Parameters.AddWithValue("@price", input.Price);
                        try
                        {
                            var rows = await command.ExecuteNonQueryAsync();
                            queryDone = true;
                            log.Info("Product updated successfully");
                        } 
                        catch
                        {
                            log.Info("Product not updated successfully");
                            queryDone = false;
                        }
                    }
                } 
                else if (input.Price < 0.01m || input.Price > 99999.99m) 
                {
                    sqlQuery = 
                        "UPDATE dbo.product " +
                        "SET description = @description " +
                        "WHERE name like @name;";
                    connection.Open();
                    using (SqlCommand command = new SqlCommand(sqlQuery, connection))
                    {
                        command.Parameters.AddWithValue("@name", input.Name);
                        command.Parameters.AddWithValue("@description", input.Description);
                        try
                        {
                            var rows = await command.ExecuteNonQueryAsync();
                            queryDone = true;
                            log.Info("Product updated successfully");
                        } 
                        catch
                        {
                            queryDone = false;
                        }
                    }
                }
                else if (!string.IsNullOrEmpty(input.Description) && input.Price < 100000.00m && input.Price > 0)
                {
                    sqlQuery = 
                        "UPDATE dbo.product " +
                        "SET description = @description, price = @price "  +
                        "WHERE name like @name;";
                    connection.Open();
                    using (SqlCommand command = new SqlCommand(sqlQuery, connection))
                    {
                        command.Parameters.AddWithValue("@name", input.Name);
                        command.Parameters.AddWithValue("@description", input.Description);
                        command.Parameters.AddWithValue("@price", input.Price);
                        try
                        {
                            var rows = await command.ExecuteNonQueryAsync();
                            queryDone = true;
                            log.Info("Product updated successfully");
                        } 
                        catch
                        {
                            log.Info("Product not updated successfully");
                            queryDone = false;
                        }
                    }
                }
            }
            if (queryDone == false)
                return new BadRequestObjectResult(input);
            return new OkObjectResult(input);
        }

        [FunctionName("DeleteProduct")]
        public static async Task<IActionResult> DeleteProduct(
            [HttpTrigger(AuthorizationLevel.Anonymous, "delete", Route = "product/{name}")] HttpRequest req, TraceWriter log, string name)
        {
            log.Info($"[DELETE] Deleting product name {name}");
            name = name.ToUpper();
            bool queryDone = false;

            using (SqlConnection connection = new SqlConnection(connectionStr))
            {
                var sqlQuery = 
                    "DELETE FROM dbo.product " +
                    "WHERE name = @name;";
                connection.Open();
                using (SqlCommand command = new SqlCommand(sqlQuery, connection))
                {
                    command.Parameters.AddWithValue("@name", name);
                    try
                    {
                        var rows = await command.ExecuteNonQueryAsync();
                        queryDone = true;
                        log.Info($"Product {name} deleted");
                    } 
                    catch
                    {
                        queryDone = false;
                    }
                }
            }
            if (queryDone == false)
                return new BadRequestResult();
            return new OkResult();
        }
    }
}
