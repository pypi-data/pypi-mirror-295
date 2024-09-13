<script setup lang="ts">
import { useForm } from "@inertiajs/vue3";

const form = useForm({
  email: "",
  password: "",
});

const submit = () => {
  form.post("/login/process", {
    preserveScroll: true,
    preserveState: true,
  });

  console.log("test");
};
</script>

<template>
  <div
    className="text-center h-screen flex justify-center flex-col items-center p-4"
  >
    <form @submit.prevent="submit">
      <div>
        <input type="text" v-model="form.email" autocomplete="off" />
      </div>
      <div>
        <input type="password" v-model="form.password" autocomplete="off" />
      </div>
      <div>
        <button type="submit">login</button>
      </div>
    </form>
  </div>
</template>
