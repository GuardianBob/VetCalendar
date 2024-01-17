<template>
  <q-layout view="Lhh lpR fff" container class="bg-white text-dark">
    <!-- <div class="col-10"> -->
      <q-form @submit="submit" method="POST">
        <h5 class="text-primary q-py-none q-my-sm">{{ pageTitle }}</h5>
        <div class="row justify-around text-center q-ma-md">
          <div class="col q-px-md q-mx-md">
            <q-select class="q-my-sm" standout="bg-dark-navy text-white" v-model="user" :options="user_list" label="User" />
            <q-select class="q-my-sm" standout="bg-dark-navy text-white" v-model="text" :options="shift" label="Shift" />
            <q-select class="q-my-sm" standout="bg-dark-navy text-white" v-model="text" :options="shift_type" label="Shift Type" />
            <q-select class="q-my-sm" standout="bg-dark-navy text-white" v-model="text" :options="dates" label="Dates" />
          </div>
        </div>
      </q-form>
    <!-- </div> -->
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"
import dummyData from "components/dummyData.json"

export default {
  name: "QuickAdd",
  props: [ "" ],
  setup() {
    return {
      info: ref(false),
      pageTitle: ref('Quick Add Shifts'),
      user: ref(''),
      shift: ref(''),
      type: ref(''),
      user_list: ref([dummyData.users]),
      shift_list: ref([]),
      type_list: ref([]),
      dates: ref([{}]),
    }
  },

  watch: {
    userInfo(newValue, oldValue) {
      this.userData = this.userInfo
    },
    
  },

  mounted() {
    this.userData = this.userInfo
  }
};
</script>


