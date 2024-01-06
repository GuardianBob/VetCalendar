<template>
  <q-page class="items-center flex flex-center">
    <div class="row q-mx-md full-width justify-around " id="Login Form">
      <div class="col-4 text-center" style="border: 4px solid #1976D2; border-radius: 10px;">
      <!-- <div class="col-4 q-mx-xl text-center"> -->
        <h4 class="text-primary q-py-none q-my-sm">User Login:</h4>
      <!-- </div> -->

      <div class="text-center q-ma-md">
      <q-form @submit="submit" method="POST" id="login_form">
        <!-- <q-field  class="q-my-sm "> -->
            <!-- <q-input v-model="email" label="E-mail address" dense outlined class="q-my-sm"></q-input> -->
        <!-- </q-field> -->
        <!-- <q-field class="q-my-sm" dense> -->
          <!-- <q-input label="Password" type="password" v-model="password" dense outlined class="q-my-sm"></q-input> -->
        <!-- </q-field> -->
        <div v-html="python_form"></div>
        <q-checkbox label="Remember me" v-model="remember"></q-checkbox>
        <br>
        <q-btn id="submit_btn" label="Submit" type="submit" color="primary" :disabled="passDisabled" />
      </q-form>
    </div>
  </div> 
</div>
<!-- <div id="Python_Form" v-html="python_form" ></div> -->
      <!-- </div> -->
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify, Cookies } from "quasar"
import APIService from "../../services/api"
import { useMainStore } from "stores/main-store.js"

const api = APIService 
// const form_email = document.getElementById("id_login_email")
// const form_pass = document.getElementById("login_password")
const mainStore = useMainStore();
let cipher_key = process.env.LOCAL_KEY



export default defineComponent({
  name: "LoginPage",
  setup() {
    const $q = useQuasar()
    return {
      password: ref(''),
      email: ref(''),
      remember: ref(false),
      passDisabled: ref(true),
      passEl: ref(),
    }
  },
  data() {
    return {
      loading: false,
      python_form: ref([]),
      csrf_token: ref('')
    }
  },

  watch: {
    // password(newValue, oldValue) {
    //   // form_pass.value = newValue
    //   // console.log(form_pass.value)
    //   if (newValue.length >= 8) {
    //     this.passDisabled = false
    //   } else {
    //     this.passDisabled = true
    //   }
    // },

    // passEl(newValue, oldValue) {
    //   console.log(newValue)
    // },
  },

  methods: {
    getCookie(name) {
      let cookieValue = null;
      if(document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = jQuery.trim(cookies[i]);
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
          }
        }
      return cookieValue;
    },

    submit(event) {
      console.log(event)
      event.preventDefault();
      const formData = new FormData(event.target);
      // console.log(formData)
      // this.$q.cookies.set('csrftoken', dataObj.csrfmiddlewaretoken) //, {
      //   path: '/',
      //   sameSite: 'strict',
      //   secure: false
      // });
      // console.log(this.getCookie('csrftoken'))
      api.login(formData)
      // api.login({ token: this.csrf_token, data: {email: this.email, password: this.password, remember: this.remember}})
      // .then((res) => {
      //   console.log(res)
      //   Notify.create({
      //     message: "Logged in successfully",
      //     color: "green",
      //     textColor: "white",
      //     position: "center",
      //     timeout: 3000
      //   })
      // })
      // .catch(error => {
      //   console.log(error)
      //     Notify.create({
      //       message: error.response.data,
      //       color: "red",
      //       textColor: "white",
      //       position: "center",
      //       timeout: 3000
      //     })
      //   })
    },
    async get_form(){
      await api.get_form().then(async(results) => {
        let form = results.data
        // form = form.replaceAll("<input ", "<q-input ")
        // console.log(form);
        this.python_form = form;
      })
    },

    async get_csrf(){
      await api.get_csrf().then((results) => {
        console.log(results.data)
        this.csrf_token = results.data['token'];
        let token_expire = new Date().setDate(new Date().getDate() + 10)
        let cookieString = 'd_csrfToken=' + this.csrf_token + '; expires = ' + token_expire + '; path=/';
        document.cookie = cookieString;
        mainStore.setCsrfToken(this.csrf_token);
        // localStorage.setItem("csrf_token", this.csrf_token)
        // document.head.querySelector('meta[name="csrf-token"]');
        // window.axios.defaults.headers.common['X-CSRF-TOKEN'] = results.data
        document.cookie = 'csrfToken =; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        console.log(mainStore.csrfToken)
        console.log(document.cookie);
      } )
    },

    async add_watcher() {
      $('#login_password').on('input', function () {
        // console.log('Input value changed to:', this.value.length);
        if (this.value.length >= 8) {
          $('#submit_btn').prop('disabled', false);
        } else {
          $('#submit_btn').prop('disabled', true);
        }
      });
    },

  },

  mounted() {
    this.get_form().then(() => {
      this.add_watcher();
    })
    // this.get_csrf()
  }
})
</script>

<style>
.input-field {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin: 5px 0;
  outline: none;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
  width: 100%;
  box-sizing: border-box;
}

.input-field:focus {
  border-color: #3f51b5;
  box-shadow: 0 0 5px rgba(63, 81, 181, 0.5);
}
</style>