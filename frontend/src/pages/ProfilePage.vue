<template>
  <q-page class="items-center flex-center q-my-xl ">

    <div class="row q-mx-md full-width justify-around ">
      <div class="col-10 text-center" style="border: 4px solid #1976D2; border-radius: 10px;">
        <!-- <div class="col-4 q-mx-xl text-center"> -->
        <!-- <ProfileEdit :userInfoLabels="userInfoLabels" :userInfo="user" v-show="edit" /> -->
        <!-- <ProfileView :userInfoLabels="userInfoLabels" :userInfo="user" /> -->
        <q-form>
          <h5 class="text-primary q-py-none q-my-sm">{{ pageTitle }}</h5>
          <div class="row justify-around text-center q-ma-md">
            <!-- <div outline class="col-4 q-px-md q-mx-md" > -->
            <div v-for="(label, key) in userInfoLabels" :key="key" outline class="col-4 q-px-md q-mx-md">
              <q-input v-model="user[key]" :label="label" dense class="q-my-sm" :disable="!edit"></q-input>
            </div>
            <!-- </div> -->
            <div class="col-10 q-px-md q-mx-md" v-show="edit">
              <q-btn class="full-width" label="Save Changes" type="submit" color="primary" />
            </div>
          </div>
        </q-form>
        <q-form @submit="update_pass" method="POST" v-show="edit">
          <div class="row justify-around text-center q-ma-md">
            <div class="col-8 q-px-md q-mx-md">
              <h5 class="text-primary q-py-none q-my-sm">Update Password</h5>
            </div>
            <div class="col-4 q-px-md q-mx-md">
              <q-input label="Password" type="password" v-model="password" dense outlined class="q-my-sm"></q-input>
            </div>
            <div class="col-4 q-px-md q-mx-md">
              <q-input label="Re-enter password" type="password" v-model="password2" dense outlined
                class="q-my-sm"></q-input>
            </div>
            <div class="col-10 q-px-md q-mx-md">
              <q-btn class="full-width" label="Update Password" type="submit" color="primary" :disabled="passDisabled" />
            </div>
          </div>
        </q-form>
        <div class="col-10 q-my-lg">
          <q-btn class="" label="Edit Profile" @click="edit = !edit" color="primary" />
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
import { useDummyData } from "stores/dummy-data.js"
import { storeToRefs } from 'pinia'
import { useMainStore } from 'src/stores/main-store'
// import { validators } from "app/services/ValidateService";

const api = APIService
const form_email = document.getElementById("id_login_email")
const form_pass = document.getElementById("login_password")
const mainStore = useMainStore()

export default defineComponent({
  name: "ProfilePage",
  components: {
    // ProfileEdit,
    // ProfileView
  },
  setup() {
    const store = useDummyData()
    // const { dummyData } = storeToRefs(store)
    return {
      store,
      // dummyData,
      user: ref(mainStore.user),
      userInfoLabels: ref({}),
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
      } else if (newValue.length >= 8 && newValue != this.password) {

      } else {
        this.passDisabled = true
      }
    },
  },

  methods: {
    get_profile() {
      console.log("Getting Profile : ", this.user)
      api.get_user_profile(this.user).then((results) => {
        console.log(results.data)
        // this.user = results.data
      })
    },

    submit() {
      console.log(this.store.dummyData.users[0])
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
    async get_form() {
      await api.get_form().then(async (results) => {
        console.log(results.data);
        this.python_form = results.data;
      })
    },

    async get_csrf() {
      await api.get_csrf().then((results) => {
        console.log(results.data)
        this.csrf_token = results.data
        // document.head.querySelector('meta[name="csrf-token"]');
        // window.axios.defaults.headers.common['X-CSRF-TOKEN'] = results.data
      })
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
    this.get_profile()
    // console.log(this.user)
  }
})
</script>