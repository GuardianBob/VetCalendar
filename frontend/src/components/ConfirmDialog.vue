<template>
  <div class="row q-mx-md full-width justify-around ">
    <!-- <q-dialog v-model="show_confirm" persistent> -->
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="report" color="negative" text-color="white" />
          <span class="q-ml-sm">{{ displayText }}</span>
        </q-card-section>
        <q-card-section v-if="doubleVerify">
          <q-toggle
            v-model="verify_delete"
            checked-icon="check"
            color="red"
            label="Click to confirm you want to perform this action."
            unchecked-icon="clear"
          />
        </q-card-section>
        <q-card-actions align="right" >
          <q-btn flat :label="cancelBtn" color="primary" v-close-popup @click="deny_choice"/>
          <q-btn flat :disable="!verify_delete && doubleVerify" :label="confirmBtn" color="negative" @click="confirm_choice" />
        </q-card-actions>
      </q-card>
    <!-- </q-dialog>  -->
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"

export default {
  name: "ConfirmDialog",
  props: [ 
    "parentFunction",
    "confirm",
    "text",
    "cancelText",
    "doubleVerify",
    "confirmText",
   ],
  setup(props) {
    
    return {
      pageTitle: ref('Confirmation Required'),
      cancelBtn: ref('Cancel'),
      confirmBtn: ref('Confirm'),
      displayText: ref('Are you sure you want to perform this action?'),
      show_confirm: ref(false),
      verify_delete: ref(false),
    }
  },

  watch: {
    // confirm: {
    //   immediate: true,
    //   handler(newVal, oldVal) {
    //     if (newVal) {
    //       this.show_confirm = newVal
    //       console.log("confirm: ", newVal)
    //     }
    //   }
    // },
    text: {
      immediate: true,
      handler(newVal, oldVal) {
        if (newVal) {
          this.displayText = newVal
          // console.log("text: ", newVal)
        }
      }
    },
    cancelText: {
      immediate: true,
      handler(newVal, oldVal) {
        if (newVal) {
          this.cancelBtn = newVal
          // console.log("cancelText: ", newVal)
        }
      }
    },
    confirmText: {
      immediate: true,
      handler(newVal, oldVal) {
        if (newVal) {
          this.confirmBtn = newVal
          // console.log("confirmText: ", newVal)
        }
      }
    }
  },

  methods: {
    childFunction(data) {
      // Need to pass parentFunction as a prop to child
      this.parentFunction(data)
    },

    deny_choice() {
      this.$emit("confirmed", false)
      // Notify.create({
      //   message: "Action cancelled.",
      //   color: "primary",
      //   position: "top",
      //   timeout: 2000,
      // });
    },

    confirm_choice() {
      this.$emit("confirmed", true)
      // Notify.create({
      //   message: "Action confirmed.",
      //   color: "negative",
      //   position: "top",
      //   timeout: 2000,
      // });
    }
  },

  mounted() {
    // this.userData = this.users
  }
};
</script>


