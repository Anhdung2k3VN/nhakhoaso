<template>
  <div class="container py-4">
    <h2 class="mb-3">🦷 Nha Khoa Số – Xử lý Excel</h2>

    <!-- CARD 1: KHÁCH HÀNG -->
    <div class="card mb-4 shadow-sm">
      <div class="card-body">
        <h5 class="card-title">1) Khách hàng</h5>
        <p class="text-muted mb-2">
          Đọc sheet đầu tiên, lọc khách hàng duy nhất, chuẩn hoá giới tính
          (Nam=1, Nữ=2, khác=3), năm sinh → chuỗi, ánh xạ cột đầu ra theo mẫu
          nhập liệu. (Theo logic trong khachhang.py)
        </p>
        <div class="d-flex align-items-center mb-3">
          <input
            type="file"
            accept=".xlsx,.xls"
            @change="onFileCustomers"
            class="form-control-file mr-3"
          />
          <button
            class="btn btn-primary ml-2"
            :disabled="!customerRows.length"
            @click="downloadCustomers"
          >
            📤 Tải kết quả (XLSX)
          </button>
        </div>

        <div v-if="customerRows.length" class="table-responsive">
          <table class="table table-sm table-striped">
            <thead>
              <tr>
                <th v-for="h in customerHeaders" :key="'hc_' + h">{{ h }}</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(r, idx) in customerRows.slice(0, 100)"
                :key="'rc_' + idx"
              >
                <td v-for="h in customerHeaders" :key="'rc_' + idx + '_' + h">
                  {{ r[h] }}
                </td>
              </tr>
            </tbody>
          </table>
          <small class="text-muted">Hiển thị trước 100 dòng…</small>
        </div>
        <div v-else class="text-muted">
          Chưa có dữ liệu – hãy chọn file Excel khách hàng.
        </div>
      </div>
    </div>

    <!-- CARD 2: ĐIỀU TRỊ -->
    <div class="card mb-4 shadow-sm">
      <div class="card-body">
        <h5 class="card-title">2) Dữ liệu điều trị</h5>
        <p class="text-muted mb-2">
          Chuẩn hoá Ngày điều trị dd/mm/yyyy 00:00, xoá dấu * trong tên, gộp
          tổng tiền = Thực thu + Còn nợ, ánh xạ cột đầu ra theo mẫu. (Theo logic
          trong xulydata.py)
        </p>
        <div class="d-flex align-items-center mb-3">
          <input
            type="file"
            accept=".xlsx,.xls"
            @change="onFileTreatment"
            class="form-control-file mr-3"
          />
          <button
            class="btn btn-success ml-2"
            :disabled="!treatmentRows.length"
            @click="downloadTreatment"
          >
            📥 Tải kết quả (XLSX)
          </button>
        </div>

        <div v-if="treatmentRows.length" class="table-responsive">
          <table class="table table-sm table-striped">
            <thead>
              <tr>
                <th v-for="h in treatmentHeaders" :key="'ht_' + h">{{ h }}</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(r, idx) in treatmentRows.slice(0, 100)"
                :key="'rt_' + idx"
              >
                <td v-for="h in treatmentHeaders" :key="'rt_' + idx + '_' + h">
                  {{ r[h] }}
                </td>
              </tr>
            </tbody>
          </table>
          <small class="text-muted">Hiển thị trước 100 dòng…</small>
        </div>
        <div v-else class="text-muted">
          Chưa có dữ liệu – hãy chọn file Excel điều trị.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

export default {
  name: "NhakhoasoComponent",
  data() {
    return {
      // headers theo mẫu đầu ra trong file Python
      customerHeaders: [
        "Mã KH\n* Để trống hệ thống sẽ tự tạo mã\n* Cập nhật đè dữ liệu căn cứ vào mã KH",
        "Tên khách hàng* \n(bắt buộc)",
        "Điện thoại",
        "Email",
        "Ngày sinh \n(DD/MM/YYYY hoặc DD-MM-YYYY)",
        "Giới tính \n(1. 1, 2. 2, 3. Khác)",
        "Địa chỉ",
        "Nguồn\n* Cần tạo nguồn với tên tương ứng trong hệ thống trước khi nhập liệu",
        "Ghi chú",
      ],
      customerRows: [],

      treatmentHeaders: [
        "Mã KH",
        "Tên khách hàng",
        "SDT khách hàng",
        "Ngày điều trị",
        "Thông tin điều trị",
        "Răng/Chẩn đoán",
        "Tổng tiền",
        "Thanh toán",
        "Còn lại",
        "Bác sĩ",
        "Phụ tá",
        "Nguồn tiền",
        "Mã dịch vụ",
        "Trạng thái",
      ],
      treatmentRows: [],
    };
  },
  methods: {
    // ===== Helpers bám sát logic gốc =====
    s(v) {
      return v == null ? "" : String(v).trim();
    },
    i(v) {
      const n = parseInt(Number(v));
      return isNaN(n) ? 0 : n;
    },
    mapGender(val) {
      // "Nam" -> 1, "Nữ" -> 2, khác -> 3 (khachhang.py) :contentReference[oaicite:2]{index=2}
      const t = this.s(val).toLowerCase();
      if (t === "nam") return 1;
      if (t === "nữ" || t === "nu") return 2;
      return 3;
    },
    fmtDateOnly(x) {
      // Trả về dd/mm/yyyy hoặc chuỗi đầu vào nếu không parse được (giữ gần với cách "to_string" năm sinh) :contentReference[oaicite:3]{index=3}
      try {
        const d = new Date(x);
        if (isNaN(d)) return this.s(x);
        const dd = String(d.getDate()).padStart(2, "0");
        const mm = String(d.getMonth() + 1).padStart(2, "0");
        const yyyy = d.getFullYear();
        return `${dd}/${mm}/${yyyy}`;
      } catch {
        return this.s(x);
      }
    },
    fmtNgayDieuTriZeroTime(x) {
      // dd/mm/yyyy 00:00 như xulydata.py (set giờ 00:00) :contentReference[oaicite:4]{index=4}
      try {
        const d = new Date(x);
        if (isNaN(d)) return "";
        const dd = String(d.getDate()).padStart(2, "0");
        const mm = String(d.getMonth() + 1).padStart(2, "0");
        const yyyy = d.getFullYear();
        return `${dd}/${mm}/${yyyy} 00:00`;
      } catch {
        return "";
      }
    },

    // ===== Khách hàng (theo khachhang.py) =====
    onFileCustomers(e) {
      const file = e.target.files && e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (ev) => {
        const wb = XLSX.read(new Uint8Array(ev.target.result), {
          type: "array",
        });
        const ws = wb.Sheets[wb.SheetNames[0]];
        const raw = XLSX.utils.sheet_to_json(ws, { defval: "" });

        // required cols như file Python: Số HS, Họ và tên, Điện thoại, Năm sinh, Giới tính, Địa chỉ, Nguồn khách :contentReference[oaicite:5]{index=5}
        const need = [
          "Số HS",
          "Họ và tên",
          "Điện thoại",
          "Năm sinh",
          "Giới tính",
          "Địa chỉ",
          "Nguồn khách",
        ];

        // lọc thiếu cột bắt buộc
        const hasAll = (row) =>
          need.every((k) => Object.prototype.hasOwnProperty.call(row, k));
        const rows = raw.filter(hasAll);

        // drop duplicates toàn bản ghi required_cols (gần với .drop_duplicates()) :contentReference[oaicite:6]{index=6}
        const seen = new Set();
        const unique = [];
        for (const r of rows) {
          const key = need.map((k) => this.s(r[k])).join("||");
          if (seen.has(key)) continue;
          seen.add(key);
          unique.push(r);
        }

        const out = unique.map((r) => {
          // Năm sinh -> chuỗi (giữ số/năm) :contentReference[oaicite:7]{index=7}
          let yearStr = "";
          if (r["Năm sinh"] !== "" && r["Năm sinh"] != null) {
            const y = parseInt(Number(r["Năm sinh"]));
            yearStr = Number.isFinite(y) ? String(y) : this.s(r["Năm sinh"]);
          }
          return {
            "Mã KH\n* Để trống hệ thống sẽ tự tạo mã\n* Cập nhật đè dữ liệu căn cứ vào mã KH":
              this.s(r["Số HS"]),
            "Tên khách hàng* \n(bắt buộc)": this.s(r["Họ và tên"]),
            "Điện thoại": this.s(r["Điện thoại"]),
            Email: "",
            "Ngày sinh \n(DD/MM/YYYY hoặc DD-MM-YYYY)": yearStr,
            "Giới tính \n(1. 1, 2. 2, 3. Khác)": this.mapGender(r["Giới tính"]),
            "Địa chỉ": this.s(r["Địa chỉ"]),
            "Nguồn\n* Cần tạo nguồn với tên tương ứng trong hệ thống trước khi nhập liệu":
              this.s(r["Nguồn khách"]),
            "Ghi chú": "",
          };
        });

        this.customerRows = out;
      };
      reader.readAsArrayBuffer(file);
    },
    downloadCustomers() {
      const ws = XLSX.utils.json_to_sheet(this.customerRows);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "KhachHang");
      const out = XLSX.write(wb, { bookType: "xlsx", type: "array" });
      saveAs(
        new Blob([out], { type: "application/octet-stream" }),
        "converted_customers.xlsx"
      );
    },

    // ===== Điều trị (theo xulydata.py) =====
    onFileTreatment(e) {
      const file = e.target.files && e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (ev) => {
        const wb = XLSX.read(new Uint8Array(ev.target.result), {
          type: "array",
        });
        const ws = wb.Sheets[wb.SheetNames[0]];
        const raw = XLSX.utils.sheet_to_json(ws, { defval: "" });

        const out = raw.map((r) => {
          const ten = this.s(r["Họ và tên"]).replace(/\*/g, "").trim(); // xoá * như Python :contentReference[oaicite:8]{index=8}
          const thuThuat = this.s(r["Tên thủ thuật "])
            .replace(/\*/g, "")
            .trim(); // chú ý cột có khoảng trắng cuối :contentReference[oaicite:9]{index=9}
          const tongTien = this.i(r["Thực thu"]) + this.i(r["Còn nợ"]); // Tổng tiền = Thực thu + Còn nợ :contentReference[oaicite:10]{index=10}
          return {
            "Mã KH": this.s(r["Mã KH"]),
            "Tên khách hàng": ten,
            "SDT khách hàng": this.s(r["Điện thoại"]),
            "Ngày điều trị": this.fmtNgayDieuTriZeroTime(r["Ngày"]), // dd/mm/yyyy 00:00 :contentReference[oaicite:11]{index=11}
            "Thông tin điều trị": thuThuat,
            "Răng/Chẩn đoán": this.s(r["Lịch liệu trình"]) || "KHÁM & TƯ VẤN", // mặc định như Python :contentReference[oaicite:12]{index=12}
            "Tổng tiền": tongTien,
            "Thanh toán": this.i(r["Thực thu"]),
            "Còn lại": this.i(r["Còn nợ"]),
            "Bác sĩ": this.s(r["Bác sĩ"]).replace(/\*/g, "").trim(),
            "Phụ tá": "",
            "Nguồn tiền": this.s(r["HTT Toán"]),
            "Mã dịch vụ": "",
            "Trạng thái": "",
          };
        });

        this.treatmentRows = out;
      };
      reader.readAsArrayBuffer(file);
    },
    downloadTreatment() {
      const ws = XLSX.utils.json_to_sheet(this.treatmentRows);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "DieuTri");
      const out = XLSX.write(wb, { bookType: "xlsx", type: "array" });
      saveAs(
        new Blob([out], { type: "application/octet-stream" }),
        "converted_data.xlsx"
      );
    },
  },
};
</script>

<style scoped>
.table thead th {
  border-top: none;
}
</style>
