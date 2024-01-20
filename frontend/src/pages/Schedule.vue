<template>
  <q-page class="q-pt-xl" >
    <div class="row align-start justify-center q-mx-sm ">
      <div class="col-4 q-pl-sm">
        <DataTable :users="users" :columns="columnLabels" :shiftCount="shiftCount" title="Schedule Shifts" :rowData="filtered_shifts"/>
      </div>
      <div class="col-8 q-pr-sm">
        <div class="column justify-start">
            <div class="col-2">
              <q-btn color="accent" id="add_shifts" :size="button_size" @click="add_shifts = !add_shifts" icon="more_time" label="Quick Add"></q-btn>
            </div>
          <div class="row align-start justify-center">
            <Calendar @send_date="set_date"/>
          </div>
        </div>
      </div>
    </div>
    <q-dialog v-model="add_shifts" transition-show="slide-down" transition-hide="slide-up">
      <QuickAdd />
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
import QuickAdd from "components/QuickAdd.vue"

const month_abbrev = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

export default defineComponent({
  name: "ScheduleShifts",
  components: {
    Calendar,
    DataTable,
    QuickAdd
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
      user_data: ref({}),
      filtered_shifts: ref([]),
      submit_button: ref(false),
      disabled: ref(true),
      loading: ref(false),
      shifts: ref([]),
      shift_data: ref([]),     
      enable_date: ref(false),
      add_shifts: ref(false),
      button_size: ref('sm'),
      columnLabels: ref([]),
    };
  },
  watch: {
    date(newValue, oldValue) {
      // console.log(newValue, oldValue)
      // this.handleMonthChange(newValue, oldValue)
      let oldYear = oldValue.slice(0, 4);
      let newYear = newValue.slice(0, 4);
      // console.log(oldYear, newYear)
      if (newYear !== oldYear) {
        console.log("Year changed")
        this.getShiftsYear().then(() => {
          this.shift_count()
        });
      } else {
        console.log("Month changed")
        this.shift_count()
      }
    },
  },
  computed: {
      
  },
  methods: {
    set_date(date){
      console.log(date)
      this.date = date
    },

    async shift_count() {
      // calculate on backend with data pull
      // console.log(this.events, this.users)
      let date_filter = MainFunctions.date_to_number(this.date)
      console.log(date_filter)
      console.log(this.shifts)
      this.user_shifts = []
      this.filtered_shifts = []
      for (let user of this.users) {
        let new_mon_arr = this.shifts.filter(shift => shift.start.includes(date_filter) && shift.title.includes(user));
        let new_arr = this.shifts.filter((shift) => { return shift.title == user })
        // this.user_shifts.push({ employee: user, monthTotal: new_mon_arr.length, yearTotal: new_arr.length })
        // this.filtered_shifts.push({ employee: user, monthTotal: new_mon_arr.length, yearTotal: new_arr.length })
        this.user_shifts = [...this.user_shifts, { employee: user, monthTotal: new_mon_arr.length, yearTotal: new_arr.length }];
        this.filtered_shifts = [...this.filtered_shifts, { employee: user, monthTotal: new_mon_arr.length, yearTotal: new_arr.length }];
      }
      console.log(this.user_shifts)
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
          console.log(res.data)
          if (res.data != "No Shifts") {
            // this.calendarOptions.events = []
            this.shifts = []
            // console.log(events)
            this.users = res.data.users.sort()
            res.data.shifts.map(event => {
              // console.log(event)
              // this.calendarOptions.events.push({
              //   // Add event to displayed calendar
              //   "title": event["user"],
              //   "start": event["start"],
              //   // "end": shift["end"]["dateTime"],
              // })
              this.shifts.push({
                // Add event to displayed calendar
                "title": event["user"],
                "start": event["start"],
                // "end": shift["end"]["dateTime"],
              })
            })
            // console.log(this.shifts)
            // 
          }
        })
      console.log(this.shifts)
      // calendarApi.updateSize()
      this.$q.loading.hide()
    },
  },

  created() {
    if (this.$q.platform.is.mobile) {
      this.button_size = 'md'
    }
  },
  
  mounted() {

    console.log(this.store.dummyData.shiftCountColumns)
    this.columnLabels = this.store.dummyData.shiftCountColumns
    // this.get_user_list();
    this.getShiftsYear().then(() => {
      this.shift_count()
    });
  },
  
})
</script>
