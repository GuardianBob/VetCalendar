<template>
  <!-- <div class="row align-start justify-center"> -->
    <div v-touch-swipe.mouse.right="handleRightSwipe" v-touch-swipe.mouse.left="handleLeftSwipe"
      class="col-10 col-md-10 col-sm-8 col-lg-6 col-xs-11 q-mx-sm text-center" style="max-height: fit-content;">
      <FullCalendar id="fullCalendar" ref="fullCalendar" :options='calendarOptions' />
      <q-dialog v-model="show_picker" transition-show="scale" transition-hide="scale">
        <!-- <q-tooltip class="bg-accent" anchor="bottom middle">Select Date</q-tooltip> -->
        <!-- <q-popup-proxy cover transition-show="scale" transition-hide="scale"> -->
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
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
// import { splitDate } from 'components/MainFunctions.js'
import MainFunctions from '../../services/MainFunctions'

const month_abbrev = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

export default {
  name: "VetCalendar",
  props: [
    "calEvents", 
    "calDate", 
    "parHandleCalChange",
    "parentFunction01",
    "parentFunction02",
  ],
  components: {
    FullCalendar, // make the <FullCalendar> tag available
  },
  data() {
    const $q = useQuasar()
    return {
      calendarOptions: ref({
        customButtons: {
          datepicker: {
            text: 'Datepicker',
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
        // headerToolbar: {
        //   left: 'title',
        //   center: 'datepicker',
        //   right: 'today prev next'
        // },
        headerToolbar: $q.screen.xs
          ? {
              left: 'title',
              center: 'today,datepicker,prev,next',
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
      // date: ref(new Date().toLocaleString('en-US', { month: 'short', year: 'numeric' })),
      date: ref(new Date().toLocaleString('en-US', { year: 'numeric' }) + " " + new Date().toLocaleString('en-US', { month: 'short' })),
      show_picker: ref(false),
    }
  },

  watch: {
    date(newValue, oldValue) {
      console.log(newValue, oldValue)
      this.handleMonthChange(newValue, oldValue)
      // this.parHandleCalChange(newValue, oldValue)
    },
    calEvents(newValue, oldValue) {
      let calendarApi = this.$refs.fullCalendar.getApi()
      console.log(newValue)
      this.calendarOptions.events = newValue
      calendarApi.updateSize()
    },

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
      this.parHandleCalChange(newValue, oldValue)
      console.log(newValue, oldValue)
      let oldYear = oldValue.slice(0, 4);
      let newYear = newValue.slice(0, 4);
      // console.log(oldYear, newYear)
      if (newYear !== oldYear) {
        console.log("Year changed")
        // await this.getShiftsYear()
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
  },

  mounted() {
    // this.$nextTick(() => {
    //   let datepickerButton = document.querySelector('.fc-datepicker-button');
    //   if (datepickerButton) {
    //     let datepicker = this.$refs.datepicker.$el;
    //     datepickerButton.innerHTML = `<div class="tooltip bg-accent">Select Date</div>
    //     <div class="popup-proxy cover scale">
    //       <input type="date" id="date" name="date" />
    //       <div class="row items-center justify-end">
    //         <button class="btn accent flat" onclick="closePopup()">Close</button>
    //       </div>
    //     </div>`;
    //     datepickerButton.appendChild(datepicker);
    //   }
    // });
  }
};
</script>


