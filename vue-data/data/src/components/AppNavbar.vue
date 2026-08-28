<template>
  <nav class="navbar navbar-expand-lg navbar-dark shadow-sm">
    <div class="container">
      <a class="navbar-brand" href="#" @click.prevent="go('home')"
        >Data Simlydent</a
      >

      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#mainNav"
        aria-controls="mainNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="mainNav">
        <ul class="navbar-nav mr-auto">
          <li
            v-for="item in items"
            :key="item.key"
            class="nav-item"
            :class="{ active: value === item.key }"
          >
            <a class="nav-link" href="#" @click.prevent="go(item.key)">
              <span class="mr-1">{{ item.icon }}</span
              >{{ item.label }}
            </a>
          </li>
        </ul>
        <span class="navbar-text small text-muted">admin</span>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "AppNavbar",
  props: { value: { type: String, default: "home" } },
  data() {
    return {
      items: [
        { key: "home", label: "Trang chủ", icon: "🏠" },
        { key: "nhakhoaso", label: "Nha khoa số", icon: "🩺" },
        { key: "dental", label: "Dental Flow", icon: "⚙️" },
        { key: "bambufit", label: "Bambufit", icon: "📊" },
        { key: "split", label: "Chia file", icon: "✂️" },
        { key: "merge", label: "Gộp file", icon: "🔗" },
        // { key: "wall", label: "Hình nền", icon: "🖼️" },
        // { key: "contact", label: "Liên hệ", icon: "📞" },
      ],
    };
  },
  methods: {
    go(key) {
      this.$emit("input", key);
    },
  },
};
</script>

<style scoped>
.nav-item.active > .nav-link {
  font-weight: 700;
}
</style>
