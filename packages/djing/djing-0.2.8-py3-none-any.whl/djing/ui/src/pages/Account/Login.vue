<script lang="ts" setup>
import { useForm, usePage } from "@inertiajs/vue3";

type PageProps = {
  user_id: number;
  djing_config: {
    base_url: string;
    auth: {
      username_field: string;
    };
  };
};

const page = usePage<PageProps>();

const { base_url, auth } = page.props.djing_config;

const form = useForm({
  field: auth.username_field,
  username: "",
  password: "",
});

const submit = () => {
  form.post(`${base_url}/api/login`, {
    onSuccess: () => {
      console.log("Logged in successfully");
    },
    onError: (err) => {
      console.log(err);
    },
  });
};
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600"
  >
    <div class="bg-white shadow-md rounded-lg p-8 max-w-sm w-full">
      <h2 class="text-2xl font-semibold text-gray-700 text-center mb-6">
        Login to your account
      </h2>

      <form @submit.prevent="submit" class="space-y-6">
        <div>
          <label class="block text-gray-700 mb-2">
            <span v-if="auth.username_field == 'email'">Email</span>
            <span v-if="auth.username_field == 'username'">Username</span>
          </label>

          <input
            v-model="form.username"
            required
            :type="auth.username_field === 'email' ? 'email' : 'text'"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-400"
            autocomplete="off"
            :placeholder="
              auth.username_field === 'email' ? 'Enter Email' : 'Enter Username'
            "
            :class="{ 'border-red-500': form.errors.username }"
          />

          <p v-if="form.errors.username" class="text-red-500 text-sm mt-1">
            {{ form.errors.username }}
          </p>
        </div>

        <div>
          <label class="block text-gray-700 mb-2">Password</label>
          <input
            v-model="form.password"
            type="password"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-400"
            autocomplete="off"
            placeholder="Enter your password"
            :class="{ 'border-red-500': form.errors.password }"
          />
          <p v-if="form.errors.password" class="text-red-500 text-sm mt-1">
            {{ form.errors.password }}
          </p>
        </div>

        <div class="flex items-center justify-between">
          <button
            type="submit"
            class="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition duration-200"
          >
            Login
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* You can add custom styles here if needed */
</style>
