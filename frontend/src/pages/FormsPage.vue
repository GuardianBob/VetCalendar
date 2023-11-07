<template>
  <router-view @click="drawer = false" api='api' />
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"
import APIService from "../../services/api"

const api = APIService

export default defineComponent({
  name: "LoginPage",
  setup() {
    return {
    }
  },
  data() {
    return {
      loading: false,
      csrf_token: ref('')
    }
  },

  watch: {

  },

  methods: {

    async get_form(){
      await api.get_form().then(async(results) => {
        console.log(results.data);
        this.python_form = results.data;
      })
    },

    async get_csrf(){
      await api.get_csrf().then((results) => {
        console.log(results.data)
        this.csrf_token = results.data
        // document.head.querySelector('meta[name="csrf-token"]');
        // window.axios.defaults.headers.common['X-CSRF-TOKEN'] = results.data
      } )
    },

    passEnabl() {
      let login_password = document.getElementById("login_password").val();
      console.log("enabling?")
      if (login_password.length >= 8) {
        document.getElementById("login").attr("disabled", false);
      } else {
        document.getElementById("login").attr("disabled", true);
      }
    },
  },
  mounted() {
    // this.get_form()
    // this.get_csrf()
  }
})
</script>