<template>
  <q-page class="flex flex-center">
    <!-- <img
      alt="Quasar logo"
      src="~assets/quasar-logo-vertical.svg"
      style="width: 200px; height: 200px"
    > -->
    <!-- <q-btn class="q-px-auto dense" color="primary" @click="get_todo">Get Todo</q-btn> -->
    <div>
      <!-- <q-btn class="q-px-auto dense" color="primary" to="/login">Get Form</q-btn> -->
    </div>
    <q-btn class="q-px-auto dense" color="primary" to="/schedule_import">Import Schedule</q-btn>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"
import APIService from "../../services/api"

export default defineComponent({
  name: 'IndexPage',
  data() {
    return {
      savedTheme: 'light_theme',
    }

  },
  methods: {
    async get_todo() {
      console.log("clicked")
      await APIService.get_todo().then(async (results) => {
        console.log(results.data);
      })
    },

    async get_form(){
      await APIService.get_form().then(async(results) => {
        console.log(results.data);
      })
    }
  },
})
</script>
