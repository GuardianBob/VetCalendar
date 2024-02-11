<template>
  <span>
    <q-item v-if="$q.platform.is.mobile" class="column" >
      <q-btn class="q-mx-xs" color="primary" size="md" id="enable_file" @click="enable_file = !enable_file">
        <q-icon name="attach_file" class="q-mr-xs" /> Upload File
        <q-tooltip class="bg-accent" anchor="bottom middle">Upload File</q-tooltip>
      </q-btn>
    </q-item>
    <q-btn v-if="$q.platform.is.desktop" class="q-mr-xs" color="primary" round size="sm" id="enable_file" @click="enable_file = !enable_file">
      <q-icon name="attach_file" />
      <q-tooltip class="bg-accent" anchor="bottom middle">Upload File</q-tooltip>
    </q-btn>
    <q-dialog v-model="enable_file" transition-show="slide-down" transition-hide="slide-up">
      <div class="row items-center justify-center" style="background-color: white; min-width: 85%;">
        <div class="col-lg-10 col-md-10 col-sm-10 col-xs-8 text-center">
          <q-file v-model="file" label="Select File" accept=".docx, .doc" class="q-my-sm" counter>
            <!-- <q-btn class="q-ml-md q-px-sm" color="primary" size="md" flat rounded id="clear_filters_button" @click="clearFile" icon="cancel"/> -->
            <template v-slot:prepend>
              <q-icon name="attach_file" />
            </template>
            <template v-slot:append>
              <q-icon name="cancel" color="negative" v-if="file !== null" @click="file = null" class="cursor-pointer" />
            </template>
          </q-file>
        </div>
        <div class="col-1 text-center">
          <q-btn class="q-ml-sm" size="sm" color="primary" round id="upload_button" @click="file_upload" v-show="file">
            <q-icon name="upload"></q-icon>
            <q-tooltip class="bg-accent">Upload File</q-tooltip>
          </q-btn>
        </div>
      </div>
    </q-dialog>
  </span>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"
import APIService from 'app/services/api';

export default {
  name: "UploadSchedule",
  props: [ 
    "parentFunction",
    // "user_shifts",
    "calDate",
  ],
  data() {
    return {
      enable_file: ref(false),
    }
  },
  setup() {
    return {
      pageTitle: ref('User Details'),
      // enable_file: ref(false),
      file: ref(null),
      date: ref(''),
    }
  },

  watch: {
    calDate: {
      immediate: true,
      handler(newValue) {
        this.date = newValue;
      }
    },
    file(newValue, oldValue) {
      if (newValue != null) {
        console.log(this.date)
        let file_name = newValue["name"].toLowerCase()
        console.log(file_name)
        // Extract the month from the file name
        const monthMatch = file_name.match(/(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)/);
        let new_month = monthMatch ? monthMatch[0] : '';
        if (new_month) {
          // Convert the month to its 3-character shorthand
          const date = new Date(new_month + ' 1 1970');
          new_month = date.toLocaleString('default', { month: 'short' });
        }
        // Extract the year from the file name
        let yearMatch = file_name.match(/\d{4}/);
        if (!yearMatch) {
          yearMatch = file_name.match(/\d{2}/);
        }
        let new_year = yearMatch ? yearMatch[0] : this.date.slice(0, 5);
        new_year = parseInt(new_year)
        // console.log(new_year)
        this.date = new_year.toString() + " " + new_month
        this.$emit('updateDate', this.date)
      }
    },
  },

  methods: {
    childFunction(data) {
      // Need to pass parentFunction as a prop to child
      this.parentFunction(data)
    },

    show_upload(){
      this.enable_file = !this.enable_file
      console.log("show dialog")
      this.$emit('clickDialog')
    },

    async file_upload() {
      console.log("and for ALL the marbles...!")
      if (this.file) {
        let formData = new FormData()
        let file = this.file
        formData.append("file", file)
        formData.append("date", this.date)
        await APIService.upload_file(formData)
          .then((res) => {
            this.enable_file = false
            this.file = null
            if (res.status == 200) {
              this.$emit('refreshEvents')
              Notify.create({
                message: "Successfully uploaded shifts!",
                color: "green",
                position: 'center',
                timeout: 300,
              })
            } else {
              Notify.create({
                message: "Something went wrong",
                color: "red",
                position: 'center',
                timeout: 300,
              })
            }
          })
      }
    },

  },

  mounted() {
  }
};
</script>


