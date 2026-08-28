<template>
  <div id="app">
    <AppNavbar v-model="page" />

    <main class="container section">
      <!-- Trang chủ -->
      <section v-if="page === 'home'">
        <div class="section-head">
          <h2 class="h3 mb-1">Trang chủ</h2>
          <p class="lead text-muted">
            Chào mừng bạn đến bộ công cụ Excel cho Simlydent.
          </p>
        </div>

        <div class="row">
          <div class="col-lg-6 mb-4">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">Nha Khoa So Plus</h5>
                <p class="text-muted mb-3">
                  Xử lý dữ liệu từ thiết bị Nha Khoa So Plus (xuất ra file
                  Excel).
                </p>
                <button class="btn btn-success" @click="page = 'nhakhoaso'">
                  Mở công cụ
                </button>
              </div>
            </div>
          </div>

          <div class="col-lg-6 mb-4">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">Dental Flow</h5>
                <p class="text-muted mb-3">
                  Xử lý dữ liệu từ thiết bị Dental Flow (xuất ra file Excel).
                </p>
                <button class="btn btn-success" @click="page = 'dental'">
                  Mở công cụ
                </button>
              </div>
            </div>
          </div>

          <div class="col-lg-6 mb-4">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">BambuFit</h5>
                <p class="text-muted mb-3">
                  Xử lý dữ liệu từ thiết bị Bambufit (xuất ra file Excel).
                </p>
                <router-link
                  v-if="$router"
                  class="btn btn-success"
                  to="/bambufit"
                  >Mở công cụ</router-link
                >
                <button
                  v-else
                  class="btn btn-success"
                  @click="page = 'bambufit'"
                >
                  Mở công cụ
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Nha khoa số -->
      <section v-else-if="page === 'nhakhoaso'">
        <h2 class="h4 mb-3">🩺 Nha khoa số</h2>
        <div class="card">
          <div class="card-body">
            <p class="mb-0 text-muted">Nội dung/tiện ích cho Nha khoa số…</p>
            <NhakhoasoComponent />
          </div>
        </div>
      </section>

      <!-- Dental Flow -->
      <section v-else-if="page === 'dental'">
        <h2 class="h4 mb-3">⚙️ Dental Flow</h2>
        <div class="card">
          <div class="card-body text-muted">
            Mô tả, link tài liệu…
            <DentalflowComponent />
          </div>
        </div>
      </section>

      <!-- Bambufit -->
      <section v-else-if="page === 'bambufit'">
        <h2 class="h4 mb-3">📊 Bambufit</h2>
        <div class="card">
          <div class="card-body text-muted">
            Công cụ xử lý dữ liệu Bambufit.
            <BambuFitComponent />
          </div>
        </div>
      </section>

      <!-- Chia file (đang nhúng bambufit) -->
      <section v-else-if="page === 'split'">
        <h2 class="h4 mb-3">✂️ Chia / Xử lý file</h2>
        <bambufit />
      </section>

      <!-- Gộp file -->
      <section v-else-if="page === 'merge'">
        <h2 class="h4 mb-3">🔗 Gộp file</h2>
        <div class="card">
          <div class="card-body text-muted">
            Cắm component gộp file tại đây.
          </div>
        </div>
      </section>

      <!-- Hình nền -->
      <section v-else-if="page === 'wall'">
        <h2 class="h4 mb-3">🖼️ Hình nền</h2>
        <div class="card">
          <div class="card-body text-muted">Chọn/đổi wallpaper…</div>
        </div>
      </section>

      <!-- Liên hệ -->
      <section v-else-if="page === 'contact'">
        <h2 class="h4 mb-3">📞 Liên hệ</h2>
        <div class="card">
          <div class="card-body text-muted">Thông tin liên hệ / form…</div>
        </div>
      </section>
    </main>

    <footer class="app-footer">
      <small>© {{ year }} doananhdung</small>
    </footer>
  </div>
</template>

<script>
import AppNavbar from "@/components/AppNavbar.vue";
import BambuFitComponent from "@/components/bambufit.vue";
import DentalflowComponent from "@/components/DentalFlow.vue";
import NhakhoasoComponent from "@/components/NhaKhoaSo.vue";

export default {
  name: "App",
  components: {
    AppNavbar,
    BambuFitComponent,
    DentalflowComponent,
    NhakhoasoComponent,
  },
  data() {
    return { page: "home" };
  },
  computed: {
    year() {
      return new Date().getFullYear();
    },
  },
};
</script>
