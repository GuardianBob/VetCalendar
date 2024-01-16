<template>
  <q-page class="q-pt-xl">
    <q-form @submit="upload_shifts">
      <div class="row align-start justify-end q-mx-sm items-center">
        <div class="col-xs-8 col-lg-2 col-md-2 col-sm-2 q-mr-xl">
          <q-select class="q-mx-sm" v-model="user" :options="users" dense options-dense
            @update:model-value="filterShifts()">
            <template v-slot:prepend>
              <q-icon name="filter_alt" round color="primary" />
            </template>
            <template v-slot:append>
              <q-btn v-if="user !== null" class="q-ml-md q-px-sm" color="negative" size="md" flat rounded
                id="clear_filters_button" @click.stop.prevent="clearFilters" icon="cancel" />
            </template>
            <q-tooltip class="bg-accent" anchor="center start">Filter Schedule</q-tooltip>
          </q-select>
        </div>
      </div>
      <br>
      <q-spinner v-show="loading" color="primary" size="3em" :thickness="3" />
      <!-- </div> -->
    </q-form>
    <!-- </div> -->
    <div class="row align-start justify-center">
        <Calendar :calEvents="events" :calDate="date" :parHandleCalChange="handleMonthChange" />
      <!-- </div> -->
    </div>
    <!-- Place scroller at bottom -->
  </q-page>
</template>


<script>
import { defineComponent, ref, onMounted } from 'vue'
import { useQuasar, Notify } from "quasar"
import APIService from "../../services/api"
import Calendar from 'components/Calendar.vue'
import MainFunctions from '../../services/MainFunctions'
import CalendarFunctions from 'app/services/CalendarFunctions'
import GoogleFunctions from 'app/services/GoogleFunctions'
// import google from 'googleapis'

export default defineComponent({
  name: "FileUpload",
  components: {
    Calendar
  },
  data() {
    return {
    }
  },
  setup() {
    
    return {
      // calStore,
      // label: "Select File",
      events: ref([{}]),
      date: ref(new Date().toLocaleString('en-US', { year: 'numeric' }) + " " + new Date().toLocaleString('en-US', { month: 'short' })),
      users: ref([]),
      user: ref(null),
      loading: ref(false),
      shifts: ref([]),
      button_size: ref('sm'),
      // onFileSelected(file) {
      //   this.file = file
      //   console.log(file)
      //   this.label = file.name
      // },
      // onFileRemoved(file) {
      //   this.file = null
      //   this.label = "Select File"
      // },
    };
  },
  watch: {
    
  },
  computed: {

  },
  methods: {
    
    async handleMonthChange(newValue, oldValue) {
      let new_date = new Date('01 ' + newValue)
      this.date = new_date.toString().slice(11, 15) + " " + new_date.toString().slice(4, 7)
      // console.log(newValue, oldValue)
      let oldYear = oldValue.slice(0, 4);
      let newYear = newValue.slice(0, 4);
      // console.log(oldYear, newYear)
      if (newYear !== oldYear) {
        console.log("Year changed")
        await this.getShiftsYear()
        if (this.user) {
          this.filterShifts()
        }
      }
    },

    async share_view() {
      // var copyURL = window.location.href;
      // console.log(window.location.href)
      // copyURL.select();
      // copyURL.setSelectionRange(0, 99999); /* For mobile devices */
      if (this.$q.platform.is.mobile) {
        navigator.share(window.location.href)
        console.log("shared on mobile!")
      } else {
        navigator.clipboard.writeText(window.location.href);
      }
      Notify.create({
        message: "URL copied to clipboard",
        color: "green",
        position: 'center',
        timeout: 300,
      })
    },

    // async handleCalendarChange(cal_date) {
    //   let new_date = cal_date.slice(11, 15) + " " + cal_date.slice(4, 7)
    //   this.date = new_date
    // //   console.log(this.date)
    // //   let newPath = MainFunctions.update_path_date(cal_date)
    // //   // console.log(newPath)
    // //   // console.log(this.$route.query.user)
    // //   this.$router.replace({ path: newPath, query: this.$route.query })
    // //   // APIService.return_shifts(this.date)
    // },

    async getShifts() {
      let calendarApi = this.$refs.fullCalendar.getApi()
      let start = calendarApi.view.activeStart
      let end = calendarApi.view.activeEnd
      // console.log(start, end)
      await APIService.return_shifts({ "start": start, "end": end })
        .then(res => {
          // console.log(res.data)
          if (res.data != "No Shifts") {
            this.events = []
            this.shifts = []
            // console.log(events)
            this.users = res.data.users
            res.data.shifts.map(event => {
              // console.log(event)
              this.events.push({
                // Add event to displayed calendar
                "title": event["user"],
                "start": event["start"],
                // "end": shift["end"]["dateTime"],
              })
              this.shifts.push({
                // Add event to displayed calendar
                "title": event["user"],
                "start": event["start"],
                // "end": shift["end"]["dateTime"],
              })
            })
            // 
          }
        })
      // console.log(this.shifts)
      calendarApi.updateSize()
    },

    async getShiftsYear() {
      console.log(this.date)
      this.$q.loading.show()
      // let calendarApi = this.$refs.fullCalendar.getApi()
      let year_start = new Date("01 " + this.date).getFullYear()
      let year_end = new Date("01 " + this.date).getFullYear()
      // console.log(year_start, year_end)
      if (year_end - year_start <= 1) {
        year_end += 1
      }
      let new_start = new Date((year_start - 1).toString() + "/12/15")
      let new_end = new Date((year_end).toString() + "/01/15")
      // console.log(year_start, year_end, parseInt(this.date.slice(4,8)))
      console.log(new_start, new_end)
      await APIService.return_shifts({ "start": new_start, "end": new_end })
        .then(res => {
          // console.log(res.data)
          if (res.data != "No Shifts") {
            this.events = []
            this.shifts = []
            // console.log(events)
            this.users = res.data.users.sort()
            res.data.shifts.map(event => {
              // console.log(event)
              this.events.push({
                // Add event to displayed calendar
                "title": event["user"],
                "start": event["start"],
                // "end": shift["end"]["dateTime"],
              })
              this.shifts.push({
                // Add event to displayed calendar
                "title": event["user"],
                "start": event["start"],
                // "end": shift["end"]["dateTime"],
              })
            })
            // 
          }
        })
      // console.log(this.shifts)
      // calendarApi.updateSize()
      this.$q.loading.hide()
    },

    async set_view() {
      let view_date = MainFunctions.view_date()
      console.log(view_date)
      if (view_date != null) {
        let month = this.date.slice(0, 3)
        if (view_date.month) {
          month = view_date.month
        }
        // console.log("month: ", month)
        this.date = view_date.year + " " + month
      } else {
        // console.log(window.location.pathname)
        this.$router.replace({ path: '/', query: this.$route.query })
      }
      if (this.$route.query.user) {
        // console.log(this.$route.query.user)
        this.user = this.$route.query.user
        this.filterShifts()
      }
    },

    async filterShifts() {
      // console.log(this.user)
      this.events = []
      this.shifts.map(shift => {
        if (shift["title"] == this.user) {
          // console.log("matches")
          this.events.push(shift)
          localStorage.setItem("filtered_user", this.user)
          // this.$router.replace({ query: { user: this.user } })
        }
      })
    },

    async clearFilters() {
      this.events = this.shifts
      // console.log(this.shifts.length)
      this.user = null
      localStorage.removeItem("filtered_user")
      // this.$router.replace({ query: null })
    },

    async clearFile() {
      this.file = null
      this.enable_file = false
    },

    async timeMin() {
      let tz_offset = (new Date()).getTimezoneOffset() * 60000
      let date_start = new Date(`01 ${this.date}`)
      let start = new Date(date_start - tz_offset).toISOString().slice(0, -5) + "Z"
      return start
    },

    async timeMax() {
      let tz_offset = (new Date()).getTimezoneOffset() * 60000
      let date_start = new Date(`01 ${this.date}`)
      let date_end = new Date(date_start.getFullYear(), date_start.getMonth() + 1, 0, 23, 59)
      let end = new Date(date_end).toISOString().slice(0, -5) + "Z"
      console.log(end)
      return end
    },
  },
 
  created() {
    if (this.$q.platform.is.mobile) {
      this.button_size = 'md'
    }
  },
  
  mounted() {
    this.getShiftsYear().then(() => {
      if (this.user) {
        this.filterShifts()
      }
    })
    console.log(new Date().toLocaleString('en-US', { year: 'numeric'}) + " " + new Date().toLocaleString('en-US', { month: 'short' }))
  },

})
</script>
