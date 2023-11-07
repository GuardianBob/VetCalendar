<template>
  <q-page class="items-center flex-center q-my-xl">
    <div class="row q-mx-md full-width justify-around ">
      <div class="col-10 text-center" style="border: 4px solid #1976D2; border-radius: 10px;">
        <!-- <div class="col-4 q-mx-xl text-center"> -->
        <ProfileEdit :userInfo="userInfo" v-show="edit" />
        <ProfileView :userInfo="userInfo" v-show="!edit" />
        <div class="col-10 q-my-lg">
          <q-btn class="" label="Edit Profile" @click="edit=!edit" color="primary" />
        </div>
      </div> 
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"
import APIService from "../../services/api"
import ProfileEdit from 'components/ProfileEdit.vue'
import ProfileView from 'components/ProfileView.vue'
// import { validators } from "app/services/ValidateService";

const api = APIService 
const form_email = document.getElementById("id_login_email")
const form_pass = document.getElementById("login_password")

export default defineComponent({
  name: "ProfilePage",
  components: {
    ProfileEdit,
    ProfileView
  },
  setup() {
    return {
      // password: ref(''),
      // password2: ref(''),
      userInfo: ref({
        email: ref('mail@mail'),
        firstName: ref('J'),
        lastName: ref('Bear'),
        nickname: ref(''),
        address: ref(''),
        address2: ref(''),
        userLevel: ref(''),
        apt: ref(''),
        city: ref(''),
        state: ref(''),
        zip: ref(''),
      }),
      edit: ref(false),
      pageTitle: ref('User Details'),
      remember: ref(false),
      // passDisabled: ref(true),
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