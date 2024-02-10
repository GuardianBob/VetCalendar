import APIService from "./api.js";

export default class CalendarFunctions {
  update_path_date(date) {
    // console.log(window.location.pathname)
    // console.log(date)
    let year = date.slice(11, 15);
    let month = date.slice(4, 7);
    let pathArray = window.location.pathname.split("/");
    pathArray = pathArray.filter((path) => path != "");
    // console.log(pathArray)
    pathArray[0] = year;
    pathArray[1] = month;
    let newPath = "";
    for (let i = 0; i < pathArray.length; i++) {
      newPath += "/";
      newPath += pathArray[i];
    }
    // console.log(newPath)
    // this.$router.replace({ path: newPath })
    return newPath;
  }

  view_date() {
    let pathArray = window.location.pathname.split("/");
    pathArray = pathArray.filter((path) => path != "");
    if (pathArray.length > 1) {
      // console.log(pathArray.length, pathArray)
      return { year: pathArray[0], month: pathArray[1] };
    } else if (pathArray.length == 1) {
      return { year: pathArray[0] };
    } else {
      return null;
    }
  }

  async handleRightSwipe() {
    // console.log("handleRightSwipe")
    let calendarApi = this.$refs.fullCalendar.getApi();
    calendarApi.prev();
    let new_date = calendarApi.getDate().toString();
    // console.log("eventPrev", calendarApi.getDate());
    this.handleCalendarChange(new_date, -1);
    // this.panel = this.panel - 1
  }

  async handleLeftSwipe() {
    // console.log("handleLeftSwipe")
    let calendarApi = this.$refs.fullCalendar.getApi();
    calendarApi.next();
    let new_date = calendarApi.getDate().toString();
    this.handleCalendarChange(new_date, 1).then(() => {
      // this.panel = this.panel + 1
    });
  }

  async handleMonthChange(newValue, oldValue) {
    let calendarApi = this.$refs.fullCalendar.getApi();
    let new_date = new Date("01 " + this.date);
    calendarApi.gotoDate(new_date.toISOString());
    // console.log(newValue, oldValue)
    if (
      newValue.slice(0, 3) == "Jan" &&
      oldValue.slice(0, 3) == "Dec" &&
      newValue.slice(4, 8) > oldValue.slice(4, 8)
    ) {
      console.log("moved forward year");
      await this.getShiftsYear();
      if (this.user) {
        this.filterShifts();
      }
    }
    if (
      newValue.slice(0, 3) == "Dec" &&
      oldValue.slice(0, 3) == "Jan" &&
      newValue.slice(4, 8) < oldValue.slice(4, 8)
    ) {
      console.log("moved backward year");
      await this.getShiftsYear();
      if (this.user) {
        this.filterShifts();
      }
    }
  }

  handleCalendarChange(date_string) {
    let date = new Date(date_string)
    let new_date = date_string.slice(11, 15) + " " + date_string.slice(4, 7)
    let set_date = date.toISOString().slice(0, 10); // Convert to 'YYYY-MM-DD'
    // console.log(new_date, set_date);
    return { new_date, set_date };
  }

  async getShifts() {
    let calendarApi = this.$refs.fullCalendar.getApi();
    let start = calendarApi.view.activeStart;
    let end = calendarApi.view.activeEnd;
    await APIService.return_shifts({ start: start, end: end }).then((res) => {
      // console.log(res.data)
      if (res.data != "No Shifts") {
        this.calendarOptions.events = [];
        this.shifts = [];
        // console.log(events)
        this.users = res.data.users;
        res.data.shifts.map((event) => {
          // console.log(event)
          this.calendarOptions.events.push({
            // Add event to displayed calendar
            title: event["user"],
            start: event["start"],
            // "end": shift["end"]["dateTime"],
          });
          this.shifts.push({
            // Add event to displayed calendar
            title: event["user"],
            start: event["start"],
            // "end": shift["end"]["dateTime"],
          });
        });
        //
      }
    });
    // console.log(this.shifts)
    calendarApi.updateSize();
  }

  async getShiftsYear(date, calendarEvents, shifts, users) {
    let year_start = new Date("01 " + date).getFullYear()
    let year_end = new Date("01 " + date).getFullYear()
    if (year_end - year_start <= 1) {
      year_end += 1
    }
    let new_start = new Date((year_start - 1).toString() + "/12/15")
    let new_end = new Date((year_end).toString() + "/01/15")
    await APIService.return_shifts({ "start": new_start, "end": new_end })
      .then(res => {
        if (res.data != "No Shifts") {
          // console.log(res.data)
          calendarEvents = []
          shifts = []
          users = res.data.users.sort()
          res.data.shifts.map(event => {
            calendarEvents.push({
              "title": event["user"],
              "start": event["start"],
              "textColor": event["color"],
            })
            shifts.push({
              "title": event["user"],
              "start": event["start"],
              "textColor": event["color"],
            })
          })
        }
      })
    return { calendarEvents, shifts, users };
  }

  async getShiftsYearOld(date, calendarEvents, shifts, users) {
    let year_start = new Date("01 " + date).getFullYear()
    let year_end = new Date("01 " + date).getFullYear()
    if (year_end - year_start <= 1) {
      year_end += 1
    }
    let new_start = new Date((year_start - 1).toString() + "/12/15")
    let new_end = new Date((year_end).toString() + "/01/15")
    await APIService.return_shifts_old({ "start": new_start, "end": new_end })
      .then(res => {
        if (res.data != "No Shifts") {
          calendarEvents = []
          shifts = []
          users = res.data.users.sort()
          res.data.shifts.map(event => {
            calendarEvents.push({
              "title": event["user"],
              "start": event["start"],
            })
            shifts.push({
              "title": event["user"],
              "start": event["start"],
            })
          })
        }
      })
    return { calendarEvents, shifts, users };
  }

  async set_view() {
    let view_date = this.view_date();
    let month = this.date.slice(0, 3);
    if (view_date != null) {
      if (view_date.month) {
        month = view_date.month;
      }
      // console.log("month: ", month)
      this.date = view_date.year + " " + month;
    }
    if (this.$route.query.user) {
      // console.log(this.$route.query.user)
      this.user = this.$route.query.user;
      this.filterShifts();
    }
  }

  async filterShifts() {
    // console.log(this.user)
    this.calendarOptions.events = [];
    this.shifts.map((shift) => {
      if (shift["title"] == this.user) {
        // console.log("matches")
        this.calendarOptions.events.push(shift);
        localStorage.setItem("filtered_user", this.user);
        this.$router.replace({ query: { user: this.user } });
      }
    });
  }

  async clearFilters() {
    this.calendarOptions.events = this.shifts;
    // console.log(this.shifts.length)
    this.user = null;
    localStorage.removeItem("filtered_user");
    this.$router.replace({ query: null });
  }
}

// export default new CalendarFunctions();
