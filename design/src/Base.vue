<script setup lang="ts">
import SiteHeader from "./components/SiteHeader.vue";
import SiteFooter from "./components/SiteFooter.vue";
</script>

<template>
  <SiteHeader />
  <slot>{% block content %}{% endblock %}</slot>
  <SiteFooter />
</template>
