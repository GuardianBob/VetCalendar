<template>
  <q-page class="items-center flex-center q-my-xl ">

    <div class="row q-mx-md full-width justify-around ">
      <div class="col-10 text-center" style="border: 4px solid #1976D2; border-radius: 10px;">
        <q-card>
          <q-tabs
            v-model="tab"
            dense
            class="text-grey"
            active-color="primary"
            indicator-color="primary"
            align="justify"
            narrow-indicator
          >
            <q-tab name="shifts" label="Shifts" />
            <q-tab name="profile" label="Profile" />
            <q-tab name="settings" label="Settings" />
          </q-tabs>

          <q-separator />

          <q-tab-panels v-model="tab" animated>
            <q-tab-panel name="profile">
              <div class="text-h6">Profile Information</div>
              <div class="col-12 text-right">
                <q-btn class="" label="Edit Profile" @click="edit = !edit" color="primary" size="sm" />
              </div>
              <q-form @submit="submit">
                <h5 class="text-primary q-py-none q-my-sm">{{ pageTitle }}</h5>
                <div class="row justify-around text-center q-ma-md">
                  <!-- <div outline class="col-4 q-px-md q-mx-md" > -->
                  <div v-for="(label, key) in userInfoLabels" :key="key" outline class="col-4 q-px-md q-mx-md">
                    <!-- User profile is duplicated when email is updated from profile page -->
                    <!-- Disabled editing user email in profile for temp fix -->
                    <span v-if="key == 'email'">
                      <q-input v-model="user[key]" :label="label" dense class="q-my-sm" disable></q-input>
                    </span>
                    <span v-else>
                      <q-input  v-model="user[key]" :label="label" dense class="q-my-sm" :disable="!edit"></q-input>
                    </span>
                  </div>
                  <!-- </div> -->
                  <div class="col-10 q-px-md q-mx-md" v-show="edit">
                    <q-btn class="full-width" label="Save Changes" type="submit" color="primary" />
                  </div>
                </div>
              </q-form>
            </q-tab-panel>

            <q-tab-panel name="settings">
              <div class="row justify-center">
                <div class="text-h6 col-12">Settings</div>
                <div class="col-10 q-my-lg text-left">
                  <q-btn class="" label="Change Password" @click="edit_password = !edit_password" color="primary" size="sm" />
                </div>
                <q-form @submit="update_pass" method="POST" v-show="edit_password">
                  <div class="row justify-around text-center q-ma-md">
                    <div class="col-8 q-px-md q-mx-md">
                      <h5 class="text-primary q-py-none q-my-sm">Update Password</h5>
                    </div>
                    <div class="col-10 q-px-md q-mx-md">
                      <q-input label="Current Password" type="password" v-model="password" dense outlined class="q-my-sm"></q-input>
                    </div>
                    <div class="col-4 q-px-md q-mx-md">
                      <q-input label="New Password" type="password" v-model="newPassword" dense outlined class="q-my-sm"></q-input>
                    </div>
                    <div class="col-4 q-px-md q-mx-md">
                      <q-input label="Re-enter password" type="password" v-model="newPassword2" dense outlined
                        class="q-my-sm"></q-input>
                    </div>
                    <div class="col-10 q-px-md q-mx-md">
                      <q-btn class="full-width" label="Update Password" type="submit" color="primary" :disabled="passDisabled" />
                    </div>
                  </div>
                </q-form>
              </div>
              
            </q-tab-panel>

            <q-tab-panel name="shifts">
              <ShiftData :shiftData="shifts" />
            </q-tab-panel>
          </q-tab-panels>
        </q-card>
        <!-- <div class="col-4 q-mx-xl text-center"> -->
        <!-- <ProfileEdit :userInfoLabels="userInfoLabels" :userInfo="user" v-show="edit" /> -->
        <!-- <ProfileView :userInfoLabels="userInfoLabels" :userInfo="user" /> -->
        
        
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
import { userInfoLabels } from 'src/components/formFields.json'
import { preventDefault } from '@fullcalendar/core/internal'
// import DataTable from 'components/DataTable.vue'
import ShiftData from 'components/ShiftData.vue'
// import { validators } from "app/services/ValidateService";

const api = APIService
const form_email = document.getElementById("id_login_email")
const form_pass = document.getElementById("login_password")
const mainStore = useMainStore()


export default defineComponent({
  name: "ProfilePage",
  components: {
    ShiftData,
    // DataTable,
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
      userInfoLabels: ref(userInfoLabels),
      edit: ref(false),
      edit_password: ref(false),
      pageTitle: ref('User Details'),
      remember: ref(false),
      passDisabled: ref(true),
      passError: ref(false),
      tab: ref('shifts'),
      // innerTab: ref('innerMails'),
      splitterModel: ref(20),
      newPassword: ref(''),
      newPassword2: ref(''),
      password: ref(''),
      shifts: ref([]),

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
    newPassword2(newValue, oldValue) {
      // form_pass.value = newValue
      // console.log(form_pass.value)
      if (newValue.length >= 8 && newValue == this.newPassword) {
        this.passDisabled = false
      } else if (newValue.length >= 8 && newValue != this.newPassword) {

      } else {
        this.passDisabled = true
      }
    },

    // selectedMonth(newValue, oldValue) {
    //   this.shift_count()
    // }
  },

  methods: {
    get_profile() {
      console.log("Getting Profile : ", this.user)
      api.get_user_profile(this.user).then((results) => {
        console.log(results.data)
        this.user = results.data
        // this.shifts = results.data.shifts
        this.shifts = results.data.shifts
        // .map(shift => {
        //   let date = new Date(shift.shift_start);
        //   let days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        //   let dayName = days[date.getDay()];
        //   let formattedDate = `${dayName}, ${date.toLocaleString('default', { month: 'short' })} ${date.getDate()} ${date.getFullYear()} || ${date.getHours() % 12 || 12}:${date.getMinutes().toString().padStart(2, '0')} ${date.getHours() >= 12 ? 'PM' : 'AM'}`;
        //   // let formattedDate = `${date.toLocaleString('default', { month: 'short' })} ${date.getDate()} ${date.getFullYear()} || ${date.getHours() % 12 || 12}:${date.getMinutes().toString().padStart(2, '0')} ${date.getHours() >= 12 ? 'PM' : 'AM'}`;
        //   return { ...shift, shift_date: formattedDate };
        // });
        // this.shift_count()
      })
    },

    submit() {
      // console.log(this.store.dummyData.users[0])
      console.log(this.user)
      api.update_profile(this.user).then((results) => {
        console.log(results.data)
        Notify.create({
          message: "Profile updated successfully",
          color: "green",
          textColor: "white",
          position: "center",
          timeout: 3000
        })
        this.edit = false
      })
      .catch(error => {
        console.log(error)
          Notify.create({
            message: "Error updating profile",
            color: "red",
            textColor: "white",
            position: "center",
            timeout: 3000
          })
        })
    },
    async update_pass() {
      console.log(this.password, this.newPassword, this.newPassword2)
      if (this.newPassword != this.newPassword2) {
        this.passError = true
        Notify.create({
          message: "Passwords do not match",
          color: "red",
          textColor: "white",
          position: "center",
          timeout: 3000
        })
        return
      } 
      if (this.newPassword == this.password) {
        this.passError = true
        Notify.create({
          message: "New password cannot be the same as the old password",
          color: "red",
          textColor: "white",
          position: "center",
          timeout: 3000
        })
        return
      }
        await api.update_password({"email": this.user.email ,"old_password": this.password, "new_password": this.newPassword}).then((results) => {
          console.log(results.data)
          Notify.create({
            message: "Password updated successfully",
            color: "green",
            textColor: "white",
            position: "center",
            timeout: 3000
          })
          this.edit_password = false
        })
        .catch(error => {
          console.log(error.response)
          Notify.create({
            message: error.response.data.message,
            color: "red",
            textColor: "white",
            position: "center",
            timeout: 3000
          })
        })
      
    },

    // async get_form() {
    //   await api.get_form().then(async (results) => {
    //     console.log(results.data);
    //     this.python_form = results.data;
    //   })
    // },

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
    // let date = new Date()
    // this.selectedMonth = months[date.getMonth()]
    // this.selectedYear = date.getFullYear()
    // this.years = Array.from({length: 10}, (v, k) => date.getFullYear() - k)
    this.get_profile()
    // console.log(this.user)
  }
})
</script>