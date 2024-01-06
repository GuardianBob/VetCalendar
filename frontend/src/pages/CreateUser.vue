<template>
  <q-page class="items-center flex flex-center">
    <div class="row q-mx-md full-width justify-around" id="Login Form">
      <div
        class="col-4 text-center"
        style="border: 4px solid #1976d2; border-radius: 10px"
      >
        <h4 class="text-primary q-py-none q-my-sm">Create New User Account</h4>
        <div class="text-center q-ma-md">
          <q-form @submit="submit" method="POST" id="login_form">
            <div v-html="python_form"></div>
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

const api = APIService;
// const form_email = document.getElementById("id_login_email")
// const form_pass = document.getElementById("login_password")
const mainStore = useMainStore();
let cipher_key = process.env.LOCAL_KEY;

export default defineComponent({
  name: "LoginPage",
  setup() {
    const $q = useQuasar();
    return {
      email: ref(""),
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
      console.log(formData);
      // this.$q.cookies.set('csrftoken', dataObj.csrfmiddlewaretoken) //, {
      //   path: '/',
      //   sameSite: 'strict',
      //   secure: false
      // });
      // console.log(this.getCookie('csrftoken'))
      api
        .create_user(formData)
        .then((res) => {
          // console.log(res)
          Notify.create({
            message: res.data.message,
            color: "green",
            textColor: "white",
            position: "center",
            timeout: 3000,
          });
          // this.$router.push('/schedule')
        })
        .catch((error) => {
          // console.log(error.response)
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
      await api
        .create_user()
        .then(async (results) => {
          console.log(results.data);
          let form = results.data;
          this.python_form = form;
        })
        .then(() => {
          // this.add_watcher()
        });
    },

    async get_csrf() {
      await api.get_csrf().then((results) => {
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

    async add_watcher() {
      $("#login_password").on("input", function () {
        // console.log('Input value changed to:', this.value.length);
        if (this.value.length >= 8) {
          $("#submit_btn").prop("disabled", false);
        } else {
          $("#submit_btn").prop("disabled", true);
        }
      });
    },
  },

  mounted() {
    this.get_form(); //.then(() => {
    //   this.add_watcher();
    // })
    // this.get_csrf()
  },
});
</script>

<style></style>
