const month_abbrev = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

class MainFunctions {
  date_to_number(date) {
    let new_date = new Date(date + " 01");
    let year = new_date.getFullYear();
    let month = new_date.getMonth() + 1; // getMonth() returns month index starting from 0
    month = month < 10 ? '0' + month : month; // prepend 0 if month is less than 10
    let formattedDate = `${year}-${month}`;
    return(formattedDate);
  }

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

  mapVueProxyToObject(proxy) {
  // Get the names of the proxy's own properties
    let names = Object.getOwnPropertyNames(proxy);
    // Create a new object
    let object = {};
    // Loop through the names and assign the corresponding values from the proxy to the object
    for (let name of names) {
      object[name] = proxy[name];
    }
    delete object.length ? object.length : null
    // Return the object
    return object;
  }

  getBrightness(color) {
    let r, g, b, hsp;
    if (color.match(/^rgb/)) {
      color = color.match(/^rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*(\d+(?:\.\d+)?))?\)$/);
      r = color[1];
      g = color[2];
      b = color[3];
    } else {
      color = +("0x" + color.slice(1).replace(color.length < 5 && /./g, '$&$&'));
      r = color >> 16;
      g = color >> 8 & 255;
      b = color & 255;
    }
    hsp = Math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b));
    return hsp;
  }

  getTextColor(color) {
    return this.getBrightness(color) > 175 ? '#000000' : '#ffffff';
  }

  view_date() {
    let pathArray = window.location.pathname.split("/");
    pathArray = pathArray.filter((path) => path != "");
    if (pathArray.length > 1 && Number.isInteger(pathArray[0]) && month_abbrev.includes(pathArray[1])) {
      // console.log(pathArray.length, pathArray)
      return { year: pathArray[0], month: pathArray[1] };
    } else if (pathArray.length == 1 && Number.isInteger(pathArray[0])) {
      return { year: pathArray[0] };
    } else {
      // window.location.pathname = "/"
      return null;
    }
  }

  splitDate(date) {
    let shift_date = new Date(date);
    let month = shift_date.toLocaleString("default", { month: "short" });
    let day = shift_date.toLocaleString("default", { weekday: "short" });
    let day_date = date.slice(8, 10);
    let date_string = `${day} - ${month} ${day_date} ${date.slice(
      0,
      4
    )} - ${date.slice(11, 16)}`;
    return date_string;
  }

  async file_upload() {
    console.log("and for ALL the marbles...!");
    if (this.file) {
      this.user_shifts = [];
      localStorage.setItem("gmail", this.gmail);
      let formData = new FormData();
      let file = this.file;
      await formData.append("file", file);
      await formData.append("date", this.date);
      await APIService.upload_file(formData).then((res) => {
        if (res.status == 200) {
          Notify.create({
            message: "Successfully uploaded shifts!",
            color: "green",
            position: "center",
            timeout: 300,
          });
        } else {
          Notify.create({
            message: "Something went wrong",
            color: "red",
            position: "center",
            timeout: 300,
          });
        }
      });
      this.getShiftsYear();
      this.clearFile();
      this.clearFilters();
    }
  }

  async clearFile() {
    this.file = null;
    this.enable_file = false;
  }

  async timeMin() {
    let tz_offset = new Date().getTimezoneOffset() * 60000;
    let date_start = new Date(`01 ${this.date}`);
    let start =
      new Date(date_start - tz_offset).toISOString().slice(0, -5) + "Z";
    return start;
  }

  async timeMax() {
    let tz_offset = new Date().getTimezoneOffset() * 60000;
    let date_start = new Date(`01 ${this.date}`);
    let date_end = new Date(
      date_start.getFullYear(),
      date_start.getMonth() + 1,
      0,
      23,
      59
    );
    let end = new Date(date_end).toISOString().slice(0, -5) + "Z";
    console.log(end);
    return end;
  }

  async get_users() {
    let calendarApi = this.$refs.fullCalendar.getApi();
    console.log("triggered");
    if (this.file) {
      this.loading = true;
      localStorage.setItem("gmail", this.gmail);
      let formData = new FormData();
      let file = this.file;
      await formData.append("file", file);
      await formData.append("date", this.date);
      // await formData.append("gmail", this.gmail)
      console.log(file);
      console.log("formData: ", formData);
      APIService.get_user_list(formData).then((res) => {
        console.log(res.data);
        console.log(this.date, res.data["month"]);
        if (res.data["month"] != "false") {
          if (!this.date.includes(res.data["month"])) {
            this.date = res.data["month"] + this.date.slice(3);
            let new_date = new Date(
              "01 " + res.data["month"] + this.date.slice(3)
            );
            console.log(new_date.toISOString());
            calendarApi.gotoDate(new_date.toISOString());
            calendarApi.setOption("contentHeight", "auto");
            calendarApi.updateSize();
          }
        }
        this.users = res.data["users"];
        this.show_users = true;
        this.loading = false;
        this.getShiftsYear();
      });
    }
  }
}

export default new MainFunctions();
