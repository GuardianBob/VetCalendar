<template>
    <div v-touch-swipe.mouse.right="handleRightSwipe" v-touch-swipe.mouse.left="handleLeftSwipe"
      class="col-10 col-md-10 col-sm-10 col-lg-10 col-xs-11 q-mx-sm text-center" style="max-height: fit-content;">
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
      </q-dialog>
    </div>
</template>

<script>
import { ref, nextTick, createApp } from 'vue'
import { useQuasar, Notify } from "quasar"
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin, { Draggable } from '@fullcalendar/interaction';
// import MainFunctions from '../../services/MainFunctions'
import CalendarFunctions from '../../services/CalendarFunctions'
import IconButton from './IconButton.vue'
// import APIService from "../../services/api"

export default {
  name: "VetCalendar",
  props: [
    "calEvents", 
    "calDate",
    "calUsers", 
    "calShifts",
    "editCal",
    "parHandleCalChange",
    "parentFunction01",
    "parentFunction02",
  ],
  components: {
    FullCalendar, 
    // eslint-disable-next-line vue/no-unused-components
    IconButton,
  },
  data() {
    const $q = useQuasar()
    return {
      isDragging: ref(false),
      calfunc: new CalendarFunctions(),
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
        eventDragStart: () => {
          this.isDragging = true;
        },
        eventDragStop: () => {
          this.isDragging = false;
        },
        eventAdd: (info) => {
          this.handleEventChange(info);
        },
        eventChange: (info) => {
          this.handleEventChange(info);
        },
        eventRemove: (info) => {
          this.handleEventChange(info);
        },
        eventClick: (info) => {
          this.editCal ? this.handleEventClicked(info) : null;
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
        plugins: [dayGridPlugin, interactionPlugin],
        editable: this.editCal,
        droppable: this.editCal,
        initialView: 'dayGridMonth',
        weekends: true,
        initialDate: new Date(),
        height: "auto",
        eventDisplay: 'block', // Highlights events with colored bar
        eventColor: 'white',
        eventTextColor: 'black',
        fixedWeekCount: false,
        dayMaxEvents: 4,
        // eventBorderColor: 'primary',
        events: [],
      }),
    }
  },
  setup() {
    return {
      pageTitle: ref('Calendar'),
      date: ref(new Date().toLocaleString('en-US', { year: 'numeric' }) + "-" + new Date().toLocaleString('en-US', { month: 'short' })),
      show_picker: ref(false),
      users: ref([]),
      user: ref(null),
      loading: ref(false),
      shifts: ref([]),
      button_size: ref('sm'),
      updated_events: ref([]),
      editEvents: ref(false),
    }
  },

  watch: {
    date(newValue, oldValue) {
      // console.log(newValue, oldValue)
      this.handleMonthChange(newValue, oldValue)
      this.show_picker = false
      // this.parHandleCalChange(newValue, oldValue)
    },
    calEvents: {
      immediate: true,
      handler(newValue) {
        this.calendarOptions.events = newValue;
      }
    },
    calDate: {
      immediate: true,
      handler(newValue) {
        this.date = newValue;
      }
    },
    calUsers: {
      immediate: true,
      handler(newValue) {
        this.users = newValue;
      }
    },
    calShifts: {
      immediate: true,
      handler(newValue) {
        console.log("Shifts updated:", newValue)
        this.shifts = newValue;
      }
    },
  },

  methods: {
    handleDateChange(date) {
      let calendarApi = this.$refs.fullCalendar.getApi();
      calendarApi.gotoDate(date);
    },

    handleEventChange(info) {
      // console.log('Event changed:', info.event.id, info.event.title, info.event.start);
      let event = {
        id: info.event.id,
        title: info.event.title,
        start: info.event.start,
        shift_id: info.event.extendedProps.shift_id,
        shift_type_id: info.event.extendedProps.shift_type_id,
      }
      this.$emit("send_events", event)
    },

    handleEventClicked(info) {
      console.log('Event clicked:', info.event.id, info.event.title, info.event.start);
      // this.$q.dialog({
      //   title: 'Event Details',
      //   message: 'Event ID: ' + info.event.id + '<br>' + 'Title: ' + info.event.title + '<br>' + 'Start: ' + info.event.start,
      //   ok: 'Close',
      // })
      this.$emit("edit_event", info.event)
    },

    async handleCalendarChange(date_string) {
      let date = new Date(date_string)
      let new_date = date_string.slice(11, 15) + " " + date_string.slice(4, 7)
      let set_date = date.toISOString().slice(0, 10); // Convert to 'YYYY-MM-DD'
      this.calDate, this.date = new_date
      this.$emit("send_date", new_date)
      this.handleDateChange(set_date)
    },

    async handleRightSwipe() {
      if (this.isDragging) return;
      let calendarApi = this.$refs.fullCalendar.getApi();
      calendarApi.prev();
      this.handleCalendarChange(calendarApi.getDate().toString())
      console.log("swiped right")
    },

    async handleLeftSwipe() {
      if (this.isDragging) return;
      let calendarApi = this.$refs.fullCalendar.getApi();
      calendarApi.next();
      this.handleCalendarChange(calendarApi.getDate().toString())
      console.log("swiped left")
    },

    async handleMonthChange(newValue, oldValue) {
      let new_date = new Date('01 ' + this.date)      
      this.handleCalendarChange(new_date.toString())
      let oldYear = oldValue.slice(0, 4);
      let newYear = newValue.slice(0, 4);
      if (newYear !== oldYear) {
        // console.log("Year changed")
        await this.getShiftsYear()
        if (this.user) {
          this.filterShifts()
        }
      }
    },

    async getShiftsYear() {
      const { calendarEvents, shifts, users } = await this.calfunc.getShiftsYear(this.date, this.calendarOptions.events, this.shifts, this.users);
      this.calendarOptions.events = calendarEvents;
      this.shifts = shifts;
      this.users = users;
    },

    isDarkColor(color) {
      let r, g, b, hsp;
      color = +("0x" + color.slice(1).replace(color.length < 5 && /./g, '$&$&'));
      r = color >> 16;
      g = color >> 8 & 255;
      b = color & 255;
      hsp = Math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b));
      return hsp < 175;
    },

    async filterShifts() {
      this.calendarOptions.events = []
      this.shifts.map(shift => {
        if (shift["title"] == this.user) {
          // console.log(shift)
          let new_shift = JSON.parse(JSON.stringify(shift))
          new_shift["backgroundColor"] = shift["textColor"]
          new_shift["textColor"] = this.isDarkColor(shift["textColor"]) ? "#FFFFFF" : "#000000"
          this.calendarOptions.events.push(new_shift)
          localStorage.setItem("filtered_user", this.user)
        }
      })
    },

    async clearFilters() {
      // this.calendarOptions.events = []
      this.calendarOptions.events = this.shifts
      this.user = null
      localStorage.removeItem("filtered_user")
    },
  },

  created() {
  },
  
  mounted() {
    // this.getShiftsYear().then(() => {
    //   if (this.user) {
    //     this.filterShifts()
    //   }
    //   console.log(this.calendarOptions.events)
    // })    
    // console.log(this.date)
    // this.calendarOptions.events = this.calEvents
    // this.date = this.calDate
    // this.users = this.calUsers
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

