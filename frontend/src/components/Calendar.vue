<template>
  <!-- <div class="row align-start justify-center"> -->
    <div v-touch-swipe.mouse.right="handleRightSwipe" v-touch-swipe.mouse.left="handleLeftSwipe"
      class="col-10 col-md-10 col-sm-8 col-lg-6 col-xs-11 q-mx-sm text-center" style="max-height: fit-content;">
      <div class="column items-center" >
        <q-select class="q-mx-sm" v-model="user" :options="users" dense options-dense
          @update:model-value="filterShifts()" style="max-width: 400px; min-width: 250px;">
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
      <FullCalendar id="fullCalendar" ref="fullCalendar" :options='calendarOptions' />
      <q-dialog v-model="show_picker" transition-show="scale" transition-hide="scale">
          <q-date v-model="date" mask="YYYY MMM">
            <div class="row items-center justify-end">
              <q-btn v-close-popup label="Close" color="accent" flat />
            </div>
          </q-date>
        <!-- </q-popup-proxy> -->
      </q-dialog>
    </div>
  <!-- </div> -->
</template>

<script>
import { defineComponent, ref, nextTick, createApp } from 'vue'
import { useQuasar, Notify } from "quasar"
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import MainFunctions from '../../services/MainFunctions'
import IconButton from './IconButton.vue'
import APIService from "../../services/api"

const month_abbrev = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

export default {
  name: "VetCalendar",
  props: [
    // "calEvents", 
    "calDate", 
    "parHandleCalChange",
    "parentFunction01",
    "parentFunction02",
  ],
  components: {
    FullCalendar, // make the <FullCalendar> tag available
    // eslint-disable-next-line vue/no-unused-components
    IconButton,
  },
  data() {
    const $q = useQuasar()
    return {
      calendarOptions: ref({
        customButtons: {
          datepicker: {
            text: '',
            click: () => {
              // Handle click event if necessary
              this.show_picker = !this.show_picker
            },
          },
          prev: {
            text: "PREV",
            click: () => {
              // console.log("eventPrev");
              let calendarApi = this.$refs.fullCalendar.getApi();
              calendarApi.prev();
              this.handleCalendarChange(calendarApi.getDate().toString())
            }
          },
          next: { // this overrides the next button
            text: "NEXT",
            click: () => {
              // console.log("eventNext");
              let calendarApi = this.$refs.fullCalendar.getApi();
              calendarApi.next();
              this.handleCalendarChange(calendarApi.getDate().toString())
            }
          },
          today: { // this overrides the next button
            text: "Today",
            click: () => {
              // console.log("eventToday");
              let calendarApi = this.$refs.fullCalendar.getApi();
              calendarApi.today();
              this.handleCalendarChange(calendarApi.getDate().toString())
            }
          },
        },
        headerToolbar: $q.screen.xs
          ? {
              left: '',
              center: 'title datepicker today prev next',
              right: ''
            }
          : {
              left: 'title',
              center: 'datepicker',
              right: 'today prev next'
            },
        plugins: [dayGridPlugin],
        initialView: 'dayGridMonth',
        weekends: true,
        initialDate: new Date(),
        height: "auto",
        eventDisplay: 'block', // Highlights events with colored bar
        eventColor: 'white',
        eventTextColor: 'black',
        fixedWeekCount: false,
        // eventBorderColor: 'primary',
        events: [
          {}
        ],
      }),
    }
  },
  setup() {
    return {
      pageTitle: ref('Calendar'),
      // date: ref(new Date().toLocaleString('en-US', { month: 'short', year: 'numeric' })),
      date: ref(new Date().toLocaleString('en-US', { year: 'numeric' }) + " " + new Date().toLocaleString('en-US', { month: 'short' })),
      show_picker: ref(false),
      // events: ref([{}]),
      users: ref([]),
      user: ref(null),
      loading: ref(false),
      shifts: ref([]),
      button_size: ref('sm'),
    }
  },

  watch: {
    date(newValue, oldValue) {
      console.log(newValue, oldValue)
      this.handleMonthChange(newValue, oldValue)
      // this.parHandleCalChange(newValue, oldValue)
    },
    // THis was used to update the calendar events each time events were loaded
    // events(newValue, oldValue) {
    //   let calendarApi = this.$refs.fullCalendar.getApi()
    //   console.log(newValue)
    //   this.calendarOptions.events = newValue
    //   calendarApi.updateSize()
    // },

  },

  methods: {
    // childFunction(data) {
    //   // Need to pass parentFunction as a prop to child
    //   this.parentFunction(data)
    // },

    handleDateChange(date) {
      let calendarApi = this.$refs.fullCalendar.getApi();
      calendarApi.gotoDate(date);
    },

    async handleCalendarChange(date_string) {
      // this.parHandleCalChange(date)
      // console.log(date_string)
      let date = new Date(date_string)
      let new_date = date_string.slice(11, 15) + " " + date_string.slice(4, 7)
      this.calDate, this.date = new_date
      // this.date = new_date
      // console.log(this.date)
      let set_date = date.toISOString().slice(0, 10); // Convert to 'YYYY-MM-DD'
      this.handleDateChange(set_date)
      
      // let newPath = MainFunctions.update_path_date(date)
      // console.log(newPath)
      // console.log(this.$route.query.user)
      // this.$router.replace({ path: newPath, query: this.$route.query })
      // APIService.return_shifts(this.date)
    },

    async handleRightSwipe() {
      let calendarApi = this.$refs.fullCalendar.getApi();
      calendarApi.prev();
      this.handleCalendarChange(calendarApi.getDate().toString())
      console.log("swiped right")
      // let new_date = new Date("01 " + this.date)
      // new_date.setMonth(new_date.getMonth() - 1)
      // this.handleCalendarChange(new_date.toString(), -1)
    },

    async handleLeftSwipe() {
      let calendarApi = this.$refs.fullCalendar.getApi();
      calendarApi.next();
      this.handleCalendarChange(calendarApi.getDate().toString())
      console.log("swiped left")
      // let new_date = new Date("01 " + this.date)
      // new_date.setMonth(new_date.getMonth() + 1)
      // this.handleCalendarChange(new_date.toString(), 1)
    },

    async handleMonthChange(newValue, oldValue) {
      let new_date = new Date('01 ' + this.date)      
      this.handleCalendarChange(new_date.toString())
      // this.parHandleCalChange(newValue, oldValue)
      console.log(newValue, oldValue)
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
      
      // let calendarApi = this.$refs.fullCalendar.getApi()
      // let new_date = new Date('01 ' + this.calDate)
      // calendarApi.gotoDate(new_date.toISOString())
      
      // console.log(newValue, oldValue)
      // if (newValue.slice(0, 3) == "Jan" && oldValue.slice(0, 3) == "Dec" && newValue.slice(4, 8) > oldValue.slice(4, 8)) {
      //   console.log("moved forward year")
      //   await this.getShiftsYear()
      //   if (this.user) {
      //     this.filterShifts()
      //   }
      // }
      // if (newValue.slice(0, 3) == "Dec" && oldValue.slice(0, 3) == "Jan" && newValue.slice(4, 8) < oldValue.slice(4, 8)) {
      //   console.log("moved backward year")
      //   await this.getShiftsYear()
      //   if (this.user) {
      //     this.filterShifts()
      //   }
      // }
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
            this.calendarOptions.events = []
            this.shifts = []
            // console.log(events)
            this.users = res.data.users.sort()
            res.data.shifts.map(event => {
              // console.log(event)
              this.calendarOptions.events.push({
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
            // console.log(this.shifts)
            // 
          }
        })
      console.log(this.shifts)
      // calendarApi.updateSize()
      this.$q.loading.hide()
    },

    async filterShifts() {
      // console.log(this.user)
      this.calendarOptions.events = []
      this.shifts.map(shift => {
        if (shift["title"] == this.user) {
          // console.log("matches")
          this.calendarOptions.events.push(shift)
          localStorage.setItem("filtered_user", this.user)
          // this.$router.replace({ query: { user: this.user } })
        }
      })
    },

    async clearFilters() {
      this.calendarOptions.events = this.shifts
      // console.log(this.shifts.length)
      this.user = null
      localStorage.removeItem("filtered_user")
      // this.$router.replace({ query: null })
    },
  },

  mounted() {
    this.getShiftsYear().then(() => {
      if (this.user) {
        this.filterShifts()
      }
    })    
    nextTick(() => {
      const buttonEl = document.querySelector('.fc-datepicker-button')
      if (buttonEl) {
        const app = createApp(IconButton, { icon: 'event', text: "Select Date" })
        app.mount(buttonEl)
      }
    })
    
  }
};
</script>

