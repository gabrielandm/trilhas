using System;
using System.Collections.Generic;
using System.Text;
using System.ComponentModel.DataAnnotations;

namespace projeto_08.Models
{
    public class Product
    {
        [StringLength(32, ErrorMessage = "Can't be bigger than 32 chars")]
        public string Name { get; set; }
        [StringLength(64, ErrorMessage = "Can't be bigger than 64 chars")]
        public string Description { get; set; }
        public decimal Price { get; set; }
    }
    public class ProductCreateModel
    {
        [Required]
        [StringLength(32, ErrorMessage = "Can't be bigger than 32 chars")]
        public string Name { get; set; }
        [StringLength(64, ErrorMessage = "Can't be bigger than 64 chars")]
        public string Description { get; set; }
        public decimal Price { get; set; }
    }
}
