using ClosedXML.Excel;
using Microsoft.AspNetCore.Mvc;

namespace DentalFlowApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ExcelController : ControllerBase
    {
        // POST api/excel/customers
        [HttpPost("customers")]
        public async Task<IActionResult> UploadCustomers(IFormFile file)
        {
            if (file == null || file.Length == 0)
                return BadRequest("No file uploaded");

            using var stream = new MemoryStream();
            await file.CopyToAsync(stream);
            stream.Position = 0;

            using var wb = new XLWorkbook(stream);
            var ws = wb.Worksheet(1);
            var rows = new List<Dictionary<string, string>>();

            // Đọc từng dòng
            foreach (var row in ws.RowsUsed().Skip(1)) // bỏ header
            {
                var r = new Dictionary<string, string>();
                r["Mã KH"] = row.Cell(1).GetString();
                r["Tên khách hàng"] = row.Cell(2).GetString();
                r["Điện thoại"] = NormalizePhone(row.Cell(3).GetString());
                r["Ngày sinh"] = FormatDate(row.Cell(4).GetString());
                r["Giới tính"] = MapGender(row.Cell(5).GetString()).ToString();
                r["Địa chỉ"] = row.Cell(6).GetString();
                r["Nguồn"] = row.Cell(7).GetString();
                rows.Add(r);
            }

            // Xuất file kết quả
            using var outStream = new MemoryStream();
            using (var outWb = new XLWorkbook())
            {
                var outWs = outWb.AddWorksheet("KhachHang");
                // header
                var headers = rows[0].Keys.ToList();
                for (int i = 0; i < headers.Count; i++)
                    outWs.Cell(1, i + 1).Value = headers[i];

                // data
                for (int i = 0; i < rows.Count; i++)
                {
                    var r = rows[i];
                    int col = 1;
                    foreach (var val in r.Values)
                        outWs.Cell(i + 2, col++).Value = val;
                }
                outWb.SaveAs(outStream);
            }
            outStream.Position = 0;
            return File(outStream.ToArray(),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "customers.xlsx");
        }

        // POST api/excel/treatment
        [HttpPost("treatment")]
        public async Task<IActionResult> UploadTreatment(IFormFile file)
        {
            if (file == null || file.Length == 0)
                return BadRequest("No file uploaded");

            using var stream = new MemoryStream();
            await file.CopyToAsync(stream);
            stream.Position = 0;

            using var wb = new XLWorkbook(stream);
            var ws = wb.Worksheet(1);
            var rows = new List<Dictionary<string, string>>();

            foreach (var row in ws.RowsUsed().Skip(1))
            {
                var r = new Dictionary<string, string>();
                r["Mã KH"] = row.Cell(1).GetString();
                r["Tên khách hàng"] = row.Cell(2).GetString().Replace("*", "");
                r["SDT khách hàng"] = NormalizePhone(row.Cell(3).GetString());
                r["Ngày điều trị"] = FormatDateTime(row.Cell(4).GetString());
                r["Thông tin điều trị"] = row.Cell(5).GetString().Replace("*", "");
                r["Tổng tiền"] = (row.Cell(6).GetDouble() + row.Cell(7).GetDouble()).ToString();
                r["Thanh toán"] = row.Cell(6).GetDouble().ToString();
                r["Còn lại"] = row.Cell(7).GetDouble().ToString();
                r["Bác sĩ"] = row.Cell(8).GetString().Replace("*", "");
                rows.Add(r);
            }

            using var outStream = new MemoryStream();
            using (var outWb = new XLWorkbook())
            {
                var outWs = outWb.AddWorksheet("DieuTri");
                var headers = rows[0].Keys.ToList();
                for (int i = 0; i < headers.Count; i++)
                    outWs.Cell(1, i + 1).Value = headers[i];
                for (int i = 0; i < rows.Count; i++)
                {
                    var r = rows[i];
                    int col = 1;
                    foreach (var val in r.Values)
                        outWs.Cell(i + 2, col++).Value = val;
                }
                outWb.SaveAs(outStream);
            }
            outStream.Position = 0;
            return File(outStream.ToArray(),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "treatment.xlsx");
        }

        // === Helpers giống logic Python ===
        private string NormalizePhone(string s)
        {
            if (string.IsNullOrWhiteSpace(s)) return "";
            s = s.Trim().Replace(".0", "");
            if (!s.StartsWith("0") && s.All(char.IsDigit) && s.Length == 9)
                s = "0" + s;
            return s;
        }
        private string FormatDate(string s)
        {
            if (DateTime.TryParse(s, out var d))
                return d.ToString("dd/MM/yyyy");
            return "";
        }
        private string FormatDateTime(string s)
        {
            if (DateTime.TryParse(s, out var d))
                return d.ToString("dd/MM/yyyy HH:mm");
            return "";
        }
        private int MapGender(string g)
        {
            g = g?.Trim().ToLower() ?? "";
            if (g == "nam") return 1;
            if (g == "nữ" || g == "nu") return 2;
            return 3;
        }
    }
}
