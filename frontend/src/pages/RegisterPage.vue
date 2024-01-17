<template>
  <q-page class="items-center flex flex-center">
    <div class="row q-mx-md full-width justify-around " id="Login Form">
      <div class="col-4 text-center" style="border: 4px solid #1976D2; border-radius: 10px;">
      <!-- <div class="col-4 q-mx-xl text-center"> -->
        <h5 class="text-primary q-py-none q-my-sm">User Registration:</h5>
      <!-- </div> -->

      <div class="text-center q-ma-md">
      <q-form @submit="submit" method="POST">
        <!-- <q-field  class="q-my-sm "> -->
            <q-input v-model="email" label="E-mail address" dense outlined class="q-my-sm"></q-input>
        <!-- </q-field> -->
        <!-- <q-field class="q-my-sm" dense> -->
          <q-input label="Password" type="password" v-model="password" dense outlined class="q-my-sm"></q-input>
          <q-input label="Re-enter password" type="password" v-model="password2" dense outlined class="q-my-sm"></q-input>
        <!-- </q-field> -->
        <br>
        <q-btn class="full" label="Submit" type="submit" color="primary" :disabled="passDisabled" />
      </q-form>
      <div class="text-body2 q-my-sm">
        Already have an account? <a href="/login">Login</a>
      </div>
    </div>
  </div> 
</div>
<!-- <div id="Python_Form" v-html="python_form" ></div> -->
      <!-- </div> -->
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"
import APIService from "../../services/api"
// import { validators } from "app/services/ValidateService";

const api = APIService 
const form_email = document.getElementById("id_login_email")
const form_pass = document.getElementById("login_password")

export default defineComponent({
  name: "LoginPage",
  setup() {
    return {
      password: ref(''),
      password2: ref(''),
      email: ref(''),
      remember: ref(false),
      passDisabled: ref(true),
      passError: ref(false),

    }
  },
  data() {
    return {
      // rules: ValidateService.validators,
      loading: false,
      python_form: ref([]),
      csrf_token: ref('')
    }
  },

  watch: {
    password2(newValue, oldValue) {
      // form_pass.value = newValue
      // console.log(form_pass.value)
      if (newValue.length >= 8 && newValue == this.password) {
        this.passDisabled = false
      } else if (newValue.length >= 8 && newValue != this.password){

      } else {
        this.passDisabled = true
      }
    },
  },

  methods: {
    submit() {
      api.login({ token: this.csrf_token, data: {email: this.email, password: this.password, remember: this.remember}})
      .then((res) => {
        console.log(res)
        Notify.create({
          message: "Logged in successfully",
          color: "green",
          textColor: "white",
          position: "center",
          timeout: 3000
        })
      })
      .catch(error => {
        console.log(error)
          Notify.create({
            message: error.response.data,
            color: "red",
            textColor: "white",
            position: "center",
            timeout: 3000
          })
        })
    },
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
    this.get_csrf()
  }
})
</script>