<template>
  <div class="container py-4">
    <h2 class="mb-3">🦷 Dental Flow – Xử lý Excel</h2>

    <!-- CARD 1: Khách hàng -->
    <div class="card mb-4 shadow-sm">
      <div class="card-body">
        <h5 class="card-title">1) Khách hàng</h5>
        <p class="text-muted mb-2">
          Đọc sheet đầu tiên, chuẩn hoá SĐT, ngày sinh → dd/mm/yyyy, giới tính
          (Nam=1, Nữ=2, khác=3), loại trùng theo Mã hồ sơ.
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
        <h5 class="card-title">2) Dữ liệu điều trị</h5>
        <p class="text-muted mb-2">
          Fill xuống các cột (Mã HS, Họ tên, SĐT), gộp Ngày + Giờ → dd/mm/yyyy
          hh:mm, chuẩn hoá số tiền, gộp phụ tá.
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
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

export default {
  name: "DentalflowComponent",
  data() {
    return {
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
    s(v) {
      return v == null ? "" : String(v).trim();
    },
    i(v) {
      const n = parseInt(Number(v));
      return isNaN(n) ? 0 : n;
    },
    phone(v) {
      if (!v) return "";
      let s = String(v).trim();
      if (s.endsWith(".0")) s = s.slice(0, -2);
      if (!s.startsWith("0")) s = "0" + s;
      return s;
    },
    gender(g) {
      const x = this.s(g).toLowerCase();
      if (x === "nam") return 1;
      if (x === "nữ" || x === "nu") return 2;
      return 3;
    },
    fmtDate(v) {
      try {
        const d = new Date(v);
        if (isNaN(d)) return this.s(v);
        return `${String(d.getDate()).padStart(2, "0")}/${String(
          d.getMonth() + 1
        ).padStart(2, "0")}/${d.getFullYear()}`;
      } catch {
        return "";
      }
    },
    fmtDateTime(v) {
      try {
        if (!v) return "";

        // Chuỗi dạng dd-mm-yyyy hoặc dd/mm/yyyy
        const parts = String(v).trim().split(/[-/]/);
        let d;

        if (parts.length === 3) {
          const dd = parseInt(parts[0], 10);
          const mm = parseInt(parts[1], 10) - 1; // tháng trong JS 0-11
          const yyyy = parseInt(parts[2], 10);
          d = new Date(yyyy, mm, dd, 0, 0, 0);
        } else {
          // fallback cho trường hợp Excel serial hoặc Date object
          d = new Date(v);
        }

        if (isNaN(d)) return "";

        const dd = String(d.getDate()).padStart(2, "0");
        const mm = String(d.getMonth() + 1).padStart(2, "0");
        const yyyy = d.getFullYear();
        const HH = String(d.getHours()).padStart(2, "0");
        const MM = String(d.getMinutes()).padStart(2, "0");

        return `${dd}/${mm}/${yyyy} ${HH}:${MM}`;
      } catch {
        return "";
      }
    },

    mergePhuTa(a, b) {
      a = this.s(a);
      b = this.s(b);
      return a && b ? `${a}, ${b}` : a || b;
    },

    // CUSTOMER
    onFileCustomer(e) {
      const f = e.target.files[0];
      if (!f) return;
      const r = new FileReader();
      r.onload = (ev) => {
        const wb = XLSX.read(new Uint8Array(ev.target.result), {
          type: "array",
        });
        const ws = wb.Sheets[wb.SheetNames[0]];
        const json = XLSX.utils.sheet_to_json(ws, { defval: "" });
        const seen = new Set(),
          out = [];
        for (const row of json) {
          const id = row["Mã hồ sơ"];
          if (!id || seen.has(id)) continue;
          seen.add(id);
          out.push({
            "Mã KH": parseInt(id) || "",
            "Tên khách hàng* \n(bắt buộc)": this.s(row["Họ tên"]),
            "Điện thoại": this.phone(row["Điện thoại"]),
            Email: "",
            "Ngày sinh \n(DD/MM/YYYY hoặc DD-MM-YYYY)": this.fmtDate(
              row["Ngày sinh"]
            ),
            "Giới tính \n(1. Nam, 2. Nữ, 3. Khác)": this.gender(
              row["Giới tính"]
            ),
            "Địa chỉ": this.s(row["Địa chỉ"]),
            Nguồn: this.s(row["Nguồn khách hàng"]),
            "Ghi chú": "",
          });
        }
        this.customerRows = out;
      };
      r.readAsArrayBuffer(f);
    },
    downloadCustomer() {
      const ws = XLSX.utils.json_to_sheet(this.customerRows);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "KhachHang");
      const out = XLSX.write(wb, { bookType: "xlsx", type: "array" });
      saveAs(
        new Blob([out], { type: "application/octet-stream" }),
        "output_khachhang.xlsx"
      );
    },

    // TREATMENT
    onFileTreatment(e) {
      const f = e.target.files[0];
      if (!f) return;
      const r = new FileReader();
      r.onload = (ev) => {
        const wb = XLSX.read(new Uint8Array(ev.target.result), {
          type: "array",
        });
        const ws = wb.Sheets[wb.SheetNames[0]];
        const json = XLSX.utils.sheet_to_json(ws, { defval: "" });
        const out = json.map((row) => ({
          "Mã KH": this.i(row["Mã hồ sơ"]),
          "Tên khách hàng": this.s(row["Họ tên"]),
          "SDT khách hàng": this.phone(row["Điện thoại"]),
          "Ngày điều trị (*)": this.fmtDateTime(row["Ngày điều trị"]),
          "Thông tin điều trị (*)": this.s(row["Thủ thuật"]),
          "Răng/Chẩn đoán": this.s(row["Nội dung điều trị"]),
          "Tổng tiền": this.i(row["Phải thanh toán"]),
          "Thanh toán": this.i(row["Đã thanh toán"]),
          "Còn lại": this.i(row["Còn lại"]),
          "Bác sĩ": this.s(row["Bác sĩ điều trị"]),
          "Phụ tá": this.mergePhuTa(row["Trợ thủ 1"], row["Trợ thủ 2"]),
          "Nguồn tiền": "",
          "Mã dịch vụ": "",
          "Trạng thái": "",
        }));
        this.treatmentRows = out;
      };
      r.readAsArrayBuffer(f);
    },
    downloadTreatment() {
      const ws = XLSX.utils.json_to_sheet(this.treatmentRows);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "DieuTri");
      const out = XLSX.write(wb, { bookType: "xlsx", type: "array" });
      saveAs(
        new Blob([out], { type: "application/octet-stream" }),
        "output_dieutri.xlsx"
      );
    },
  },
};
</script>
