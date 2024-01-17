<template>
  <!-- <q-page class="items-center flex flex-center"> -->
    <div class="row q-mx-md full-width justify-around" style="width: 700px; max-width: 60vw;">
      <div class="col-12 text-center bg-white text-dark" style="border: 4px solid #1976d2; border-radius: 10px">
        <div class="text-right">
          <q-btn flat v-close-popup icon="close"/>
        </div>  
        <div class="text-center q-ma-md" ref="form">
          <q-form @submit="submit" method="POST" id="login_form">
            <div v-html="data" class="text-left"></div>
            <q-btn id="submit_btn" label="Submit" type="submit" color="primary" v-close-popup/>
          </q-form>
        </div>
      </div>
    </div>
  <!-- </q-page> -->
</template>

<script>
import { defineComponent, ref } from "vue";
import { useQuasar, Notify } from "quasar";
import APIService from "../../services/api";
import { api } from "boot/axios";

export default defineComponent({
  name: "ProfileForm",
  props: [
    "user_id",
    "adminEdit",
    "api_string",
    "editButton",
    "page_title",
    "parentFunc01",
    "parentFunc02",
    "parentFunc03",
  ],
  setup() {
    return {};
  },
  data() {
    return {
      loading: false,
      data: ref([]),
      csrf_token: ref(""),
      info: ref(false),
      userData: ref(),
      api_call: ref(""),
      api_data: ref(),
      editLabel: ref("Edit User"),
      pageTitle: ref('User Details'),
      // columnLabels: store.formFields.columnLabels,
      user: ref({}),
      userInfoLabels: ref({}),
      edit: ref(false),
      edit_pw: ref(false),
      remember: ref(false),
      passDisabled: ref(true),
      passError: ref(false),
      password: ref(""),
      password2: ref(""),
    };

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
  },  

  methods: {
    submit(event) {
      console.log(event);
      event.preventDefault();
      const formData = new FormData(event.target);
      console.log(formData);
      api
        .post(this.api_call, formData)
        .then((res) => {
          console.log(res.data);
          this.parentFunc02();
          Notify.create({
            message: res.data.message,
            color: "green",
            textColor: "white",
            position: "center",
            timeout: 3000,
          });
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
      let params = { "id": this.user_id, "admin": this.adminEdit}
      // console.log(params)
      // console.log(this.api_call, params);
      await api.get(this.api_call, { params }).then(async (results) => {
        console.log(results.data);
        this.data = results.data;
        
      });
    },

    async get_csrf() {
      await APIService.get_csrf().then((results) => {
        console.log(results);
        this.csrf_token = results.data;
      });
    },
  },
  mounted() {
    this.api_call = this.api_string;
    this.api_data = this.userId;
    this.get_form();
  },
});
</script>
