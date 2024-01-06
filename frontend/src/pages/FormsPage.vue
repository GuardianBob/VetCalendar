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
import { useQuasar, Notify } from "quasar";
import APIService from "../../services/api";
import { api } from "boot/axios";

export default defineComponent({
  name: "LoginPage",
  setup() {
    return {};
  },
  data() {
    return {
      loading: false,
      python_form: ref([]),
      csrf_token: ref(""),
      api_call: ref(""),
    };
  },

  watch: {},

  methods: {
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
        .post(this.api_call, formData)
        .then((res) => {
          console.log(res.data);
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
          console.log(error.response.data);
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
      if (!this.api_call.includes("login")) {
        this.api_call = "/login" + this.api_call;
      }
      console.log(this.api_call);
      await api.get(this.api_call).then(async (results) => {
        console.log(results);
        this.python_form = results.data;
      });
    },

    async get_csrf() {
      await APIService.get_csrf().then((results) => {
        console.log(results);
        this.csrf_token = results.data;
        // document.head.querySelector('meta[name="csrf-token"]');
        // window.axios.defaults.headers.common['X-CSRF-TOKEN'] = results.data
      });
    },
  },
  mounted() {
    let urlParams = this.$route.path;
    // urlParams = urlParams.replace(/^\/+/, "");
    console.log(urlParams);
    this.api_call = urlParams;
    this.get_form();
    // this.get_csrf()
  },
});
</script>
