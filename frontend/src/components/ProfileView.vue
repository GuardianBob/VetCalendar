<template>
  <div class="row q-mx-md full-width justify-around" style="width: 700px; max-width: 80vw;">
    <div class="col-12 text-center bg-white text-dark" style="border: 4px solid #1976D2; border-radius: 10px;">
      <q-form @submit="update_user()">
        <h5 class="text-primary q-py-none q-my-sm">{{ pageTitle }}</h5>
        <div class="row justify-around text-center q-ma-md">
          <!-- <div outline class="col-4 q-px-md q-mx-md" > -->
          <div v-for="(label, key) in userInfoLabels" :key="key" outline class="col-4 q-px-md q-mx-md">
            <q-input 
              v-model="userData[key]" 
              :mask="store.formFields.userInfoFormat[key]" 
              :type="store.formFields.userInfoType[key]" 
              :label="label" dense class="q-my-sm" 
              :disable="!edit"
              :required="store.formFields.userInfoRequired[key]"
            />
          </div>
          <!-- </div> -->
          <div class="col-10 q-px-md q-mx-md" v-show="edit">
            <q-btn class="full-width" label="Save Changes" type="submit" color="primary" />
          </div>
        </div>
      </q-form>
      <q-form @submit="update_pass" v-show="edit_pw">
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
        <q-btn class="" :label="editLabel" @click="edit = !edit" color="primary" />
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, toRaw } from 'vue'
import { useQuasar, Notify } from "quasar"
import dummyData from "./dummyData.json"
import { useFormFields } from "stores/form-fields.js"
import APIService from "../../services/api"
import MainFunctions from "../../services/MainFunctions.js"

export default {
  name: "ProfileView",
  props: [
    "userInfo",
    "editButton",
    "page_title",
    "parentFunc01",
    "parentFunc02",
    "parentFunc03",
  ],
  setup() {
    const store = useFormFields()
    return {
      store,
      info: ref(false),
      userData: ref(),
      pageTitle: ref('User Details'),
      columnLabels: store.formFields.columnLabels,
      user: ref({}),
      userInfoLabels: ref({}),
      edit: ref(false),
      edit_pw: ref(false),
      remember: ref(false),
      passDisabled: ref(true),
      passError: ref(false),
      password: ref(""),
      password2: ref(""),
      editLabel: ref("Edit User"),
    }
  },

  watch: {
    userInfo(newValue, oldValue) {
      this.userData = this.userInfo
    },
    edit(newValue, oldValue) {
      if (newValue == true) {
        this.editLabel = "Done"
        this.edit_pw = true ? this.editButton != "Add User" : false
      } else {
        this.editLabel = this.editButton
      }
    },
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
    async update_user() {
      // let names = Object.getOwnPropertyNames(this.userData);
      // let object = {};
      // // Loop through the names and assign the corresponding values from the proxy to the object
      // for (let name of names) {
      //   object[name] = this.userData[name];
      // }
      // delete object.length
      // console.log(object)
      let new_obj = MainFunctions.mapVueProxyToObject(this.userData)
      console.log(new_obj)
      APIService.add_user(new_obj)
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

    update_pass() {

    },

    get_user_data(userID) {
      APIService.get_user_data(userID).then((response) => {

      })
    }
  },

  mounted() {
    this.userData = this.userInfo ? this.userInfo : []
    this.edit = true ? this.editButton == "Add User" : false
    this.userInfoLabels = this.store.formFields.userInfoLabels;
    this.editLabel = this.editButton
    this.pageTitle = this.page_title
    // Object.keys(this.userInfoLabels).forEach(key => {
    //   console.log(key)
    // })
    // console.log(this.userInfoLabels)
  }
};
</script>


