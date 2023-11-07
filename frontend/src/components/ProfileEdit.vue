<template>
  <q-page class="q-pt-xl">
          <!-- <div class="col-4 q-mx-xl text-center"> -->
            <h5 class="text-primary q-py-none q-my-sm">{{ pageTitle }}</h5>
          <!-- </div> -->

          <q-form @submit="submit" method="POST">
            <div class="row justify-around text-center q-ma-md">
              <div class="col-4 q-px-md q-mx-md">
                <q-input v-model="userData.email" label="E-mail address" dense outlined class="q-my-sm"></q-input>
              </div>
              <div class="col-4 q-px-md q-mx-md">
                <q-input v-model="userData.firstName" label="First Name" dense outlined class="q-my-sm"></q-input>
              </div>
              <div class="col-4 q-px-md q-mx-md">
                <q-input v-model="userData.lastName" label="Last Name" dense outlined class="q-my-sm"></q-input>
              </div>
              <div class="col-4 q-px-md q-mx-md">
                <q-input v-model="userData.nickname" label="Nickname" dense outlined class="q-my-sm"></q-input>
              </div>
              <div class="col-4 q-px-md q-mx-md">
                <q-input v-model="userData.address" label="Address" dense outlined class="q-my-sm"></q-input>
              </div>
              <div class="col-4 q-px-md q-mx-md">
                <q-input v-model="userData.address2" label="Address2" dense outlined class="q-my-sm"></q-input>
              </div>
              <div class="col-4 q-px-md q-mx-md">
                <q-input v-model="userData.userLevel" label="User Level" dense outlined class="q-my-sm"></q-input>
              </div>
              <div class="col-4 q-px-md q-mx-md">
                <q-input v-model="userData.apt" label="Apt" dense outlined class="q-my-sm"></q-input>
              </div>
              <div class="col-4 q-px-md q-mx-md">
                <q-input v-model="userData.city" label="City" dense outlined class="q-my-sm"></q-input>
              </div>
              <div class="col-4 q-px-md q-mx-md">
                <q-input v-model="userData.state" label="State" dense outlined class="q-my-sm"></q-input>
              </div>
              <div class="col-4 q-px-md q-mx-md">
                <q-input v-model="userData.zip" label="Zip" dense outlined class="q-my-sm"></q-input>
              </div>
              <div class="col-4 q-px-md q-mx-md"></div>          
              <div class="col-10 q-px-md q-mx-md">
                <q-btn class="full-width" label="Submit" type="submit" color="primary" />
              </div>
            </div>
          </q-form>
          <q-form @submit="update_pass" method="POST">
            <div class="row justify-around text-center q-ma-md">
              <div class="col-8 q-px-md q-mx-md">
                <h5 class="text-primary q-py-none q-my-sm">Update Password</h5>
              </div>
              <div class="col-4 q-px-md q-mx-md">
                <q-input label="Password" type="password" v-model="password" dense outlined class="q-my-sm"></q-input>
              </div>
              <div class="col-4 q-px-md q-mx-md">
                <q-input label="Re-enter password" type="password" v-model="password2" dense outlined class="q-my-sm"></q-input>
              </div>
              <div class="col-10 q-px-md q-mx-md">
                <q-btn class="full-width" label="Update Password" type="submit" color="primary" :disabled="passDisabled" />
              </div>
            </div>
          </q-form>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"

export default {
  name: "ProfileEdit",
  props: [ "userInfo" ],
  setup() {
    return {
      info: ref(false),
      userData: ref({}),
      passDisabled: ref(true),
      password: ref(''),
      password2: ref(''),
      pageTitle: ref('Update User Details')
    }
  },

  watch: {
    userInfo(newValue, oldValue) {
      this.userData = this.userInfo
    },
    password2(newValue, oldValue) {
      // form_pass.value = newValue
      console.log(newValue)
      if (newValue.length >= 8 && newValue == this.password) {
        this.passDisabled = false
      } else if (newValue.length >= 8 && newValue != this.password) {
      } else {
        this.passDisabled = true
      }
    },
  },

  mounted() {
    this.userData = this.userInfo
  }
};
</script>


