<template>
  <v-sheet color="background" class="pa-6" min-height="100vh">
    <v-select
        v-model="selectedUserId"
        :items="users"
        item-title="name"
        item-value="id"
        label="Select a user"
        return-object
        :loading="loading"
        clearable
    />
  </v-sheet>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import userService from '~/services/userService'
import type { User } from '~/types/user'
const {
  goToDashboard,
} = useNavigation();
const users = ref<User[]>([])
const authStore = useAuthStore()
const selectedUserId = ref<User | null>(null)
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    users.value = await userService.getAllUsers()
  } catch (err) {
    console.error('Failed to load users', err)
  } finally {
    loading.value = false
  }
})
watch(selectedUserId, (newUser) => {
  if (newUser) {
    authStore.setUser(newUser)
    goToDashboard()
  }
})
</script>
