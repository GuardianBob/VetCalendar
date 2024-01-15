<template>
  <q-page class="items-center flex flex-center">
    <div class="row q-mx-md full-width justify-around" id="Login Form">
      <div
        class="col-4 text-center"
        style="border: 4px solid #1976d2; border-radius: 10px"
      >
        <div class="text-center q-ma-md">
          <q-form @submit="submit" method="POST" id="login_form">
            <div v-html="python_form"></div>
            <q-checkbox 
              label="Remember Me" 
              v-model="remember" 
              id="remember_me" 
              name="remember_me"
              class="form_control input_field">
            </q-checkbox>
            <br />
            <q-btn
              id="submit_btn"
              label="Submit"
              type="submit"
              color="primary"
            />
          </q-form>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from "vue";
import { useQuasar, Notify, Cookies } from "quasar";
import APIService from "../../services/api";
import { useMainStore } from "stores/main-store.js";
import { api } from "boot/axios";

// const form_email = document.getElementById("id_login_email")
// const form_pass = document.getElementById("login_password")
const mainStore = useMainStore();
let cipher_key = process.env.LOCAL_KEY;

export default defineComponent({
  name: "LoginPage",
  setup() {
    const $q = useQuasar();
    return {
      password: ref(""),
      email: ref(""),
      remember: ref(false),
      api_call: ref(""),
    };
  },
  data() {
    return {
      loading: false,
      python_form: ref([]),
      csrf_token: ref(""),
    };
  },

  watch: {},

  methods: {
    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = jQuery.trim(cookies[i]);
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },

    submit(event) {
      console.log(event);
      event.preventDefault();
      const formData = new FormData(event.target);
      if (this.remember == false) {
        formData.append("remember_me", false)
      }
      console.log(formData)
      // this.$q.cookies.set('csrftoken', dataObj.csrfmiddlewaretoken) //, {
      //   path: '/',
      //   sameSite: 'strict',
      //   secure: false
      // });
      // console.log(this.getCookie('csrftoken'))
      console.log(this.api_call);
      api
        .post(this.api_call, formData)
        .then((res) => {
          console.log(res);
          localStorage.setItem('access_token', res.data.access);
          localStorage.setItem('refresh_token', res.data.refresh);
          Notify.create({
            message: "Logged in successfully",
            color: "green",
            textColor: "white",
            position: "center",
            timeout: 3000,
          });
          this.$router.push("/");
        })
        .catch((error) => {
          console.log(error.response);
          Notify.create({
            message: error.response.data.message,
            color: "red",
            textColor: "white",
            position: "center",
            timeout: 3000,
          });
        });
    },
    async get_form() {
      await api.get(this.api_call).then(async (results) => {
        console.log(results);
        this.python_form = results.data;
      });
    },

    async get_csrf() {
      await APIService.get_csrf().then((results) => {
        console.log(results.data);
        this.csrf_token = results.data["token"];
        let token_expire = new Date().setDate(new Date().getDate() + 10);
        let cookieString =
          "d_csrfToken=" +
          this.csrf_token +
          "; expires = " +
          token_expire +
          "; path=/";
        document.cookie = cookieString;
        mainStore.setCsrfToken(this.csrf_token);
        // localStorage.setItem("csrf_token", this.csrf_token)
        // document.head.querySelector('meta[name="csrf-token"]');
        // window.axios.defaults.headers.common['X-CSRF-TOKEN'] = results.data
        document.cookie = "csrfToken =; expires=Thu, 01 Jan 1970 00:00:01 GMT;";
        console.log(mainStore.csrfToken);
        console.log(document.cookie);
      });
    },

    async add_verify_watcher() {},
  },

  mounted() {
    this.api_call = this.$route.path;
    if (!this.api_call.includes("login")) {
      this.api_call = "/login" + this.api_call;
    }
    console.log(this.api_call);
    this.get_form();
    // APIService.login().then(async (results) => {
    //   let form = results.data
    //   this.python_form = form;

    // }).then(() => {

    //   this.add_watcher()
    // })
    // this.get_form().then(() => {
    //   this.add_watcher();
    // })
    // this.get_csrf()
  },
});
</script>

<style></style>
