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
import MainFunctions from 'app/services/MainFunctions'
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
    "dialog_open",
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
          // this.editCal ? this.handleEventClicked(info) : null;
          // console.log(this.$q.platform.is.desktop)
          if (this.$q.platform.is.desktop) {
            // Handle event click on mobile device
            if (this.clickTimeout) {
              clearTimeout(this.clickTimeout);
              this.clickTimeout = null;
              this.editCal ? this.handleEventClicked(info) : null; // Handle double click
            } else {
              this.clickTimeout = setTimeout(() => {
                this.clickTimeout = null;
                // Handle single click if necessary
              }, 500); // Wait for 250ms before deciding if it's a single or double click
            }
          } else {
            this.editCal ? this.handleEventClicked(info) : null;
          }
        },
        dateClick: (info) => {
          // console.log('Date clicked:', info.dateStr);
          if (this.$q.platform.is.desktop) {
            // Handle event click on mobile device
            if (this.clickTimeout) {
              clearTimeout(this.clickTimeout);
              this.clickTimeout = null;
              this.editCal ? this.handleDateClicked(info) : null; // Handle double click
            } else {
              this.clickTimeout = setTimeout(() => {
                this.clickTimeout = null;
                // Handle single click if necessary
              }, 500); // Wait for 250ms before deciding if it's a single or double click
            }
          } else {
            this.editCal ? this.handleDateClicked(info) : null;
          }
          
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
        eventColor: '#ffffff',
        // eventTextColor: '#000000',
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
      event_id: ref(),
      clickTimeout: ref(null),
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
    
    dialog_open: {
      immediate: true,
      handler(newValue) {
        console.log("Shifts updated:", newValue)
        if (!newValue) {
          this.resetEventColor(this.event_id)
        }
      }
    },
  },

  methods: {
    handleDateChange(date) {
      let calendarApi = this.$refs.fullCalendar.getApi();
      calendarApi.gotoDate(date);
    },

    handleEventChange(info) {
      // console.log('Event changed:', info.event);
      let event = {
        id: parseInt(info.event.id),
        title: info.event.title,
        start: info.event.start,
        shift: info.event.extendedProps.shift_name_id,
        shift_type: info.event.extendedProps.shift_type_id,
        shift_date: info.event.start.toLocaleDateString(),
      }
      // console.log(event)
      this.$emit("send_events", event)
      const calEvent = this.$refs.fullCalendar.getApi().getEventById(info.event.id);
      console.log("Event:", calEvent, calEvent.id, calEvent.title, calEvent.start, calEvent.extendedProps)
      let update = this.calendarOptions.events.find(obj => obj.id == calEvent.id)
      update.start = calEvent.start
      let shift = this.shifts.find(obj => obj.id == calEvent.id)
      shift.start = calEvent.start
    },

    set_event_color(id) {
      this.event_id = id
      let eventIndex = this.calendarOptions.events.findIndex(obj => obj.id == id);
      if (eventIndex !== -1) {
        let event = this.calendarOptions.events[eventIndex];
        console.log(event, event.borderColor)
        let color = event.borderColor
        event.backgroundColor = color
        event.textColor = MainFunctions.getTextColor(event.borderColor)
      }
    },
    
    resetEventColor(id) {
      let eventIndex = this.calendarOptions.events.findIndex(obj => obj.id == id);
      if (eventIndex !== -1) {
        let event = this.calendarOptions.events[eventIndex];
        console.log(event, event.borderColor)
        event.backgroundColor = '#ffffff'
        event.textColor = event.borderColor
      }
    },

    handleEventClicked(info) {
      let event = this.$refs.fullCalendar.getApi().getEventById(info.event.id);
      console.log('Event clicked:', info.event, info.event.id, info.event.title, info.event.start);
      console.log(this.calendarOptions.events, event)
      this.set_event_color(info.event.id)
      this.$emit("edit_event", info.event)
    },

    handleDateClicked(info) {
      console.log('Date clicked:', info.dateStr);
      this.$emit("date_clicked", info.dateStr)
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
          new_shift["backgroundColor"] = shift["borderColor"]
          new_shift["textColor"] = this.isDarkColor(shift["textColor"]) ? "#FFFFFF" : "#000000"
          this.calendarOptions.events.push(new_shift)
          localStorage.setItem("filtered_user", this.user)
        }        
      })
    },

    async clearFilters() {
      this.calendarOptions.events = []
      console.log(this.shifts)      
      this.shifts.map(shift => {
        let new_shift = JSON.parse(JSON.stringify(shift))
        // console.log(new_shift)
        this.calendarOptions.events.push(new_shift)
      })
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

