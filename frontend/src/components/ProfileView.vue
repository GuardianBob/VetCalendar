<template>
  <!-- <q-page class="q-pt-xl"> -->
    <q-form @submit="submit" method="POST">
      <h5 class="text-primary q-py-none q-my-sm">{{ pageTitle }}</h5>
      <div class="row justify-around text-center q-ma-md">
        <div outline class="col-4 q-px-md q-mx-md">
          <q-input v-model="userData.email" label="E-Mail Address" label-color="black" dense class="q-my-sm" disable ></q-input>
        </div>
        <div class="col-4 q-px-md q-mx-md">
          <q-input v-model="userData.firstName" label="First Name" dense class="q-my-sm" disable></q-input>
        </div>
        <div class="col-4 q-px-md q-mx-md">
          <q-input v-model="userData.lastName" label="Last Name" dense class="q-my-sm" disable></q-input>
        </div>
        <div class="col-4 q-px-md q-mx-md">
          <q-input v-model="userData.nickname" label="Nickname" dense class="q-my-sm" disable></q-input>
        </div>
        <div class="col-4 q-px-md q-mx-md">
          <q-input v-model="userData.address" label="Address" dense class="q-my-sm" disable></q-input>
        </div>
        <div class="col-4 q-px-md q-mx-md">
          <q-input v-model="userData.address2" label="Address2" dense class="q-my-sm" disable></q-input>
        </div>
        <div class="col-4 q-px-md q-mx-md">
          <q-input v-model="userData.userLevel" label="User Level" dense class="q-my-sm" disable></q-input>
        </div>
        <div class="col-4 q-px-md q-mx-md">
          <q-input v-model="userData.apt" label="Apt" dense class="q-my-sm" disable></q-input>
        </div>
        <div class="col-4 q-px-md q-mx-md">
          <q-input v-model="userData.city" label="City" dense class="q-my-sm" disable></q-input>
        </div>
        <div class="col-4 q-px-md q-mx-md">
          <q-input v-model="userData.state" label="State" dense class="q-my-sm" disable></q-input>
        </div>
        <div class="col-4 q-px-md q-mx-md">
          <q-input v-model="userData.zip" label="Zip" dense class="q-my-sm" disable></q-input>
        </div>
        <div class="col-4 q-px-md q-mx-md"></div>          
        
      </div>
    </q-form>
  <!-- </q-page> -->
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"

export default {
  name: "ProfileView",
  props: [ "userInfo" ],
  setup() {
    return {
      info: ref(false),
      userData: ref({}),
      pageTitle: ref('User Details')
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


