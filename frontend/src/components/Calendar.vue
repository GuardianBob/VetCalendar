<template>
  <!-- <div class="row align-start justify-center"> -->
    <!-- <div v-touch-swipe.mouse.right="handleRightSwipe" v-touch-swipe.mouse.left="handleLeftSwipe" -->
      <!-- class="col-10 col-md-10 col-sm-8 col-lg-6 col-xs-11 q-mx-sm text-center" style="max-height: fit-content;"> -->
      <FullCalendar id="fullCalendar" ref="fullCalendar" :options='calendarOptions' />
    <!-- </div> -->
  <!-- </div> -->
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
// import { splitDate } from 'components/MainFunctions.js'

const month_abbrev = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

export default {
  name: "VetCalendar",
  props: ["calEvents", "calDate", "parHandleCalChange"],
  components: {
    FullCalendar, // make the <FullCalendar> tag available
  },
  data() {
    return {
      calendarOptions: ref({
        customButtons: {
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
        plugins: [dayGridPlugin],
        initialView: 'dayGridMonth',
        weekends: true,
        initialDate: new Date(),
        height: "auto",
        eventDisplay: 'block', // Highlights events with colored bar
        eventColor: 'white',
        eventTextColor: 'black',
        // eventBorderColor: 'primary',
        events: [
          {}
        ]
      }),
    }
  },
  setup() {
    return {
      pageTitle: ref('Calendar'),
      date: ref(new Date().toLocaleString('en-US', { month: 'short', year: 'numeric' })),

    }
  },

  watch: {
    calDate(newValue, oldValue) {
      // console.log(newValue, oldValue)
      this.handleMonthChange(newValue, oldValue)
    },
    calEvents(newValue, oldValue) {
      let calendarApi = this.$refs.fullCalendar.getApi()
      console.log(newValue)
      this.calendarOptions.events = newValue
      calendarApi.updateSize()
    },

  },

  methods: {
    childFunction(data) {
      // Need to pass parentFunction as a prop to child
      this.parentFunction(data)
    },

    async handleCalendarChange(date) {
      this.parHandleCalChange(date)
    },

    async handleRightSwipe() {
      let calendarApi = this.$refs.fullCalendar.getApi();
      calendarApi.prev();
      let new_date = calendarApi.getDate().toString()
      this.handleCalendarChange(new_date)
    },

    async handleLeftSwipe() {
      // console.log("handleLeftSwipe")
      let calendarApi = this.$refs.fullCalendar.getApi();
      calendarApi.next();
      let new_date = calendarApi.getDate().toString()
      this.handleCalendarChange(new_date)
    },

    async handleMonthChange(newValue, oldValue) {
      let calendarApi = this.$refs.fullCalendar.getApi()
      let new_date = new Date('01 ' + this.calDate)
      calendarApi.gotoDate(new_date.toISOString())
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
  },

  mounted() {

  }
};
</script>


