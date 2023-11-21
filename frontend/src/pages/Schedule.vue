<template>
  <q-page class="q-pt-xl" >
    <div class="row align-start justify-center q-mx-sm ">
      <div class="col-4 q-pl-sm">
        <DataTable :users="users" :columns="columnLabels" :shiftCount="shiftCount" title="Schedule Shifts" :rowData="filtered_shifts"/>
      </div>
      <div class="col-8 q-pr-sm">
        <div class="column justify-start">
          <div class="row justify-between">
            <div class="col-2">
              <q-btn color="accent" id="add_shifts" :size="button_size" @click="add_shifts = !add_shifts" icon="more_time" label="Quick Add"></q-btn>
            </div>
            <div class="col-5"></div>
            <div class="col-1 text-right">
              <q-btn color="primary" round :size="button_size" id="enable_date" @click="enable_date = !enable_date" icon="event">
                <!-- <q-icon name="event" /> -->
                <q-tooltip class="bg-accent" anchor="bottom middle">Select Date</q-tooltip>
                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                  <q-date v-model="date" mask="MMM YYYY">
                    <div class="row items-center justify-end">
                      <q-btn v-close-popup label="Close" color="accent" flat />
                    </div>
                  </q-date>
                </q-popup-proxy>
              </q-btn>
            </div>
            <div class="col-xs-7 col-lg-3 col-md-3 col-sm-3 q-mx-sm q-pr-sm">          
              <q-select class="" v-model="user" :options="users" dense options-dense @update:model-value="filterShifts()">
                <template v-slot:prepend>
                  <q-icon name="filter_alt" round color="primary"/>
                </template>
                <template v-slot:append>
                  <q-btn v-if="user !== null" class="q-ml-md q-px-sm" color="negative" size="md" flat rounded id="clear_filters_button" @click.stop.prevent="clearFilters" icon="cancel"/>
                </template>
                <q-tooltip class="bg-accent" anchor="center start">Filter Schedule</q-tooltip>
              </q-select>
            </div>
          </div>  
          <div class="row align-start justify-center">
            <div v-touch-swipe.mouse.right="handleRightSwipe" v-touch-swipe.mouse.left="handleLeftSwipe" class="col-12 col-md-12 col-sm-8 col-lg-6 col-xs-11 q-mx-sm q-pr-md text-center" style="max-height: fit-content;">
              <Calendar :calEvents="events" :calDate="date" :parHandleCalChange="handleCalendarChange" />
            </div>
          </div>
        </div>
      </div>
    </div>
    <q-dialog v-model="info" transition-show="slide-down" transition-hide="slide-up">
      <ButtonDefinitions />
    </q-dialog>
  </q-page>
</template>


<script>
import { defineComponent, ref, onMounted } from 'vue'
import { useQuasar, Notify } from "quasar"
import APIService from "../../services/api"
import Calendar from 'components/Calendar.vue'
import MainFunctions from '../../services/MainFunctions'
import { useDummyData } from "stores/dummy-data.js"
import DataTable from "components/DataTable.vue"

const month_abbrev = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

export default defineComponent({
  name: "ScheduleShifts",
  components: {
    Calendar,
    DataTable
  },
  setup() {
    const $q = useQuasar()
    const progress = ref(false)
    const store = useDummyData()
    
    return {
      store,
      events: ref([{}]),
      date: ref(new Date().toLocaleString('en-US', { month: 'short', year: 'numeric' })),
      calendar_button: ref(false),
      auth_token: ref(false),
      users: ref([]),
      user: ref(null),
      show_users: ref(false),
      user_shifts: ref([]),
      filtered_shifts: ref([]),
      submit_button: ref(false),
      disabled: ref(true),
      loading: ref(false),
      shifts: ref([]),
      shift_data: ref([]),     
      enable_date: ref(false),
      info: ref(false),
      button_size: ref('sm'),
      columnLabels: ref([]),
    };
  },
  watch: {
    file(newValue, oldValue) {
      if (newValue != null) {
        console.log("triggered")
        let new_month = ""
        let new_year = parseInt(this.date.slice(-4))
        let file_name = newValue["name"].toLowerCase()
        console.log(file_name)
        month_abbrev.forEach((month) => {
          if (file_name.includes(month.toLowerCase())) {
            console.log(month)
            new_month = month
          }        
        })      
        if (file_name.includes(new_year + 1)) {
          new_year = (new_year + 1).toString()
        }
        this.date = new_month + " " + new_year.toString()
        console.log(new_year)
        // this.user = null
        // this.get_users()      
      }
    },
    date(newValue, oldValue) {
      // console.log(newValue, oldValue)
      this.handleMonthChange(newValue, oldValue)
    },
  },
  computed: {
      
  },
  methods: {
    splitDate(date) {
      let shift_date = new Date(date)
      let month = shift_date.toLocaleString('default', { month: 'short' })
      let day = shift_date.toLocaleString('default', { weekday: 'short' })
      let day_date = date.slice(8, 10)
      let date_string = `${day} - ${month} ${day_date} ${date.slice(0, 4)} - ${date.slice(11, 16)}`
      return date_string
    },

    async handleRightSwipe() {
      let new_date = new Date("01 " + this.date)
      new_date.setMonth(new_date.getMonth() - 1)
      this.handleCalendarChange(new_date.toString(), -1)
    },

    async handleLeftSwipe() {
      let new_date = new Date("01 " + this.date)
      new_date.setMonth(new_date.getMonth() + 1)
      this.handleCalendarChange(new_date.toString(), 1)
    },

    async handleMonthChange(newValue, oldValue) {
      // let calendarApi = this.$refs.fullCalendar.getApi()
      let new_date = new Date('01 ' + this.date)
      // calendarApi.gotoDate(new_date.toISOString())
      this.handleCalendarChange(new_date.toString())
      // console.log(newValue, oldValue)
      if (newValue.slice(0, 3) == "Jan" && oldValue.slice(0, 3) == "Dec" && newValue.slice(4, 8) > oldValue.slice(4, 8)) {
        console.log("moved forward year")
        await this.getShiftsYear()
        if (this.user) {
          this.filterShifts()
        }
      }
      if (newValue.slice(0, 3) == "Dec" && oldValue.slice(0, 3) == "Jan" && newValue.slice(4, 8) < oldValue.slice(4, 8)) {
        console.log("moved backward year")
        await this.getShiftsYear()
        if (this.user) {
          this.filterShifts()
        }
      }
      // await this.getShiftsYear()
      // if (this.user) {
      //   this.filterShifts()
      // }
      // console.log(this.events.length)
    },

    async handleCalendarChange(cal_date) {
      let new_date = cal_date.slice(11, 15) + " " + cal_date.slice(4, 7)
      this.date = new_date
      // console.log(this.date)
      // let newPath = MainFunctions.update_path_date(cal_date)
      // console.log(newPath)
      // console.log(this.$route.query.user)
      // this.$router.replace({ path: newPath, query: this.$route.query })
      // APIService.return_shifts(this.date)
    },

    // async getShifts() {
    //   let calendarApi = this.$refs.fullCalendar.getApi()
    //   let start = calendarApi.view.activeStart
    //   let end = calendarApi.view.activeEnd
    //   await APIService.return_shifts({ "start": start, "end": end })
    //     .then(res => {
    //       // console.log(res.data)
    //       if (res.data != "No Shifts") {
    //         this.events = []
    //         this.shifts = []
    //         // console.log(events)
    //         this.users = res.data.users
    //         res.data.shifts.map(event => {
    //           // console.log(event)
    //           this.events.push({
    //             // Add event to displayed calendar
    //             "title": event["user"],
    //             "start": event["start"],
    //             // "end": shift["end"]["dateTime"],
    //           })
    //           this.shifts.push({
    //             // Add event to displayed calendar
    //             "title": event["user"],
    //             "start": event["start"],
    //             // "end": shift["end"]["dateTime"],
    //           })
    //         })
    //         // 
    //       }
    //     })
    //   // console.log(this.shifts)
    //   calendarApi.updateSize()
    // },

    async getShiftsYear() {
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
      // let view_date = MainFunctions.view_date()
      // let month = this.date.slice(0, 3)
      // if (view_date != null) {
      //   if (view_date.month) {
      //     month = view_date.month
      //   }
      //   // console.log("month: ", month)
      //   this.date = view_date.year + " " + month
      // }
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
          this.$router.replace({ query: { user: this.user } })
        }
      })
      this.filtered_shifts = this.user_shifts.filter((shift) => { return shift.employee == this.user })

    },

    async clearFilters() {
      this.events = this.shifts
      // console.log(this.shifts.length)
      this.user = null
      localStorage.removeItem("filtered_user")
      this.$router.replace({ query: null })
      this.filtered_shifts = this.user_shifts
    },

    async shift_count() {
      // calculate on backend with data pull
      // console.log(this.events, this.users)
      for (let user of this.users) {
        let new_arr = this.shifts.filter((shift) => { return shift.title == user })
        this.user_shifts.push({ employee: user, monthTotal: new_arr.length, yearTotal: new_arr.length })
        this.filtered_shifts.push({ employee: user, monthTotal: new_arr.length, yearTotal: new_arr.length })
      }
      console.log(this.user_shifts)
    },
  },

  created() {
    if (this.$q.platform.is.mobile) {
      this.button_size = 'md'
    }
  },
  
  mounted() {
    this.set_view()
    this.getShiftsYear().then(() => {
      this.shift_count();
      if (this.user) {
        this.filterShifts()
      }
    })
    console.log(this.store.dummyData.shiftCountColumns)
    this.columnLabels = this.store.dummyData.shiftCountColumns
    
  },
  
})
</script>
