<template>
  <div class="container py-4">
    <h2 class="mb-3">Bambufi - Xử lý Excel</h2>

    <!-- CARD 1: Khách hàng - BambuFit -->
    <div class="card mb-4 shadow-sm">
      <div class="card-body">
        <h5 class="card-title">1) Khách hàng (BambuFit)</h5>
        <p class="text-muted mb-2">
          Đọc sheet đầu tiên, chuẩn hoá SĐT, Năm sinh → 01/01/yyyy, Giới tính
          (Nam=1, Nữ=2, khác=3), loại trùng theo ID.
        </p>
        <div class="d-flex align-items-center mb-3">
          <input
            type="file"
            accept=".xlsx,.xls"
            @change="onFileCustomer"
            class="form-control-file mr-3"
          />
          <button
            class="btn btn-primary ml-2"
            :disabled="!customerRows.length"
            @click="downloadCustomer"
          >
            📥 Tải kết quả (XLSX)
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
                v-for="(r, idx) in customerRows.slice(0, 50)"
                :key="'rc_' + idx"
              >
                <td v-for="h in customerHeaders" :key="'rc_' + idx + '_' + h">
                  {{ r[h] }}
                </td>
              </tr>
            </tbody>
          </table>
          <small class="text-muted">Hiển thị trước 50 dòng…</small>
        </div>
      </div>
    </div>

    <!-- CARD 2: Điều trị -->
    <div class="card mb-4 shadow-sm">
      <div class="card-body">
        <h5 class="card-title">2) Dữ liệu điều trị (BambuFit)</h5>
        <p class="text-muted mb-2">
          Fill xuống các cột (ID, Họ và tên, Di động), gộp Ngày + Giờ →
          dd/mm/yyyy hh:mm, chuẩn hoá, ép số tiền.
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
                v-for="(r, idx) in treatmentRows.slice(0, 50)"
                :key="'rt_' + idx"
              >
                <td v-for="h in treatmentHeaders" :key="'rt_' + idx + '_' + h">
                  {{ r[h] }}
                </td>
              </tr>
            </tbody>
          </table>
          <small class="text-muted">Hiển thị trước 50 dòng…</small>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Vue 2
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

export default {
  name: "BambuFitComponent",
  data() {
    return {
      // KHÁCH HÀNG
      customerHeaders: [
        "Mã KH",
        "Tên khách hàng* \n(bắt buộc)",
        "Điện thoại",
        "Email",
        "Ngày sinh \n(DD/MM/YYYY hoặc DD-MM-YYYY)",
        "Giới tính \n(1. Nam, 2. Nữ, 3. Khác)",
        "Địa chỉ",
        "Nguồn",
        "Ghi chú",
      ],
      customerRows: [],

      // ĐIỀU TRỊ
      treatmentHeaders: [
        "Mã KH",
        "Tên khách hàng",
        "SDT khách hàng",
        "Ngày điều trị (*)",
        "Thông tin điều trị (*)",
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
    // ======= Helpers (bám theo logic Python) =======
    convertGender(g) {
      const s = String(g || "")
        .trim()
        .toLowerCase();
      if (s === "nam") return 1;
      if (s === "nữ" || s === "nu" || s === "female") return 2;
      return 3;
    },
    normalizePhone(v) {
      // Giống convert_sdt/safe_phone: chỉ chấp nhận 09-10 số bắt đầu bằng 0
      let s = String(v == null ? "" : v).trim();
      if (s.endsWith(".0")) s = s.slice(0, -2);
      s = s.replace(/[^\d]/g, "");
      if (s.length === 9 && !s.startsWith("0")) s = "0" + s;
      else if (s.length === 10 && s.startsWith("0")) {
        // ok
      } else {
        s = "";
      }
      return s;
    },
    formatYearToDate(v) {
      // "1975" -> "01/01/1975", 0/invalid -> ""
      const num = parseInt(String(v || "").trim(), 10);
      if (!isFinite(num) || num === 0) return "";
      return `01/01/${num}`;
    },
    toInt(v) {
      if (v == null || v === "") return 0;
      const n = parseInt(Number(v), 10);
      return isNaN(n) ? 0 : n;
    },
    toStr(v) {
      if (v == null) return "";
      return String(v).trim();
    },
    parseDayFirst(dateStr) {
      // chấp nhận dd/mm/yyyy, dd-mm-yyyy, dd.mm.yyyy
      if (!dateStr) return null;
      const s = String(dateStr).trim();
      const m = s.match(/^(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})$/);

      if (!m) return null;
      let d = parseInt(m[1], 10);
      let mo = parseInt(m[2], 10) - 1;
      let y = parseInt(m[3], 10);
      if (y < 100) y += 2000;
      const dt = new Date(y, mo, d);
      // kiểm tra hợp lệ
      if (dt.getFullYear() !== y || dt.getMonth() !== mo || dt.getDate() !== d)
        return null;
      return dt;
    },
    formatDateTime(ngay, gio) {
      // tương tự format_datetime trong Python: dayfirst, lỗi -> ""
      const dtDate = this.parseDayFirst(this.toStr(ngay));
      let hours = 0;
      let minutes = 0;
      if (gio) {
        const g = String(gio).trim();
        // h:mm or hh:mm
        const mg = g.match(/^(\d{1,2}):(\d{2})$/);
        if (mg) {
          hours = parseInt(mg[1], 10);
          minutes = parseInt(mg[2], 10);
        }
      }
      if (!dtDate) return "";
      dtDate.setHours(hours, minutes, 0, 0);
      const dd = String(dtDate.getDate()).padStart(2, "0");
      const mm = String(dtDate.getMonth() + 1).padStart(2, "0");
      const yyyy = dtDate.getFullYear();
      const HH = String(dtDate.getHours()).padStart(2, "0");
      const MM = String(dtDate.getMinutes()).padStart(2, "0");
      return `${dd}/${mm}/${yyyy} ${HH}:${MM}`;
    },
    forwardFill(rows, columns) {
      // điền xuống giá trị gần nhất ở trên cho các cột chỉ định
      const last = {};
      rows.forEach((r) => {
        columns.forEach((c) => {
          if (r[c] == null || r[c] === "") {
            if (last[c] != null) r[c] = last[c];
          } else {
            last[c] = r[c];
          }
        });
      });
      return rows;
    },

    // ======= FILE HANDLERS =======
    onFileCustomer(e) {
      const file = e.target.files && e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (ev) => {
        const data = new Uint8Array(ev.target.result);
        const wb = XLSX.read(data, { type: "array" });
        const sheetName = wb.SheetNames[0];
        const ws = wb.Sheets[sheetName];
        const json = XLSX.utils.sheet_to_json(ws, { defval: "" });

        // Bám sát cột đầu vào theo file gốc: ID, Họ và tên, Di động, NS, G.Tính, Địa chỉ, Nguồn khách
        // -> mapping ra output_df (y như Python)
        // (lọc dòng ID trống, chuẩn hoá)
        const filtered = json.filter(
          (r) => String(r["ID"] || "").trim() !== ""
        );
        // deduplicate theo ID (giữ bản ghi đầu)
        const seen = new Set();
        const out = [];
        for (const r of filtered) {
          const id = String(r["ID"]).trim();
          if (seen.has(id)) continue;
          seen.add(id);
          out.push({
            "Mã KH": id,
            "Tên khách hàng* \n(bắt buộc)": this.toStr(r["Họ và tên"]),
            "Điện thoại": this.normalizePhone(r["Di động"]),
            Email: "",
            "Ngày sinh \n(DD/MM/YYYY hoặc DD-MM-YYYY)": this.formatYearToDate(
              r["NS"]
            ),
            "Giới tính \n(1. Nam, 2. Nữ, 3. Khác)": this.convertGender(
              r["G.Tính"]
            ),
            "Địa chỉ": this.toStr(r["Địa chỉ"]),
            Nguồn: this.toStr(r["Nguồn khách"]),
            "Ghi chú": "",
          });
        }
        this.customerRows = out;
      };
      reader.readAsArrayBuffer(file);
    },

    onFileTreatment(e) {
      const file = e.target.files && e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (ev) => {
        const data = new Uint8Array(ev.target.result);
        const wb = XLSX.read(data, { type: "array" });
        const sheetName = wb.SheetNames[0];
        const ws = wb.Sheets[sheetName];
        // defval:'' để giữ cột trống thay vì undefined
        const json = XLSX.utils.sheet_to_json(ws, { defval: "" });

        // Fill xuống các cột: "ID", "Họ và tên", "Di động"
        const filled = this.forwardFill(
          json.map((r) => ({ ...r })),
          ["ID", "Họ và tên", "Di động"]
        );

        const out = filled.map((r) => {
          const ngay = r["Ngày"];
          const gio = r["Giờ"];
          return {
            "Mã KH": this.toStr(r["ID"]),
            "Tên khách hàng": this.toStr(r["Họ và tên"]),
            "SDT khách hàng": this.normalizePhone(r["Di động"]),
            "Ngày điều trị (*)": this.formatDateTime(ngay, gio),
            "Thông tin điều trị (*)": this.toStr(r["Thủ thuật"]),
            "Răng/Chẩn đoán": this.toStr(r["Nội dung điều trị"]),
            "Tổng tiền": this.toInt(r["Phải trả"]),
            "Thanh toán": this.toInt(r["Đã thu"]),
            "Còn lại": this.toInt(r["Còn nợ"]),
            "Bác sĩ": this.toStr(r["Bác sỹ"]),
            "Phụ tá": "",
            "Nguồn tiền": "",
            "Mã dịch vụ": "",
            "Trạng thái": "",
          };
        });
        this.treatmentRows = out;
      };
      reader.readAsArrayBuffer(file);
    },

    // ======= EXPORT =======
    downloadCustomer() {
      const ws = XLSX.utils.json_to_sheet(this.customerRows);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "KhachHang");
      const wbout = XLSX.write(wb, { bookType: "xlsx", type: "array" });
      saveAs(
        new Blob([wbout], { type: "application/octet-stream" }),
        "output_khachhang.xlsx"
      );
    },
    downloadTreatment() {
      const ws = XLSX.utils.json_to_sheet(this.treatmentRows);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "DieuTri");
      const wbout = XLSX.write(wb, { bookType: "xlsx", type: "array" });
      saveAs(
        new Blob([wbout], { type: "application/octet-stream" }),
        "output_dieutri.xlsx"
      );
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 980px;
}
.card {
  border-radius: 1rem;
}
</style>
