let calendar_id = ''
import APIService from "./api"

class GoogleFunctions {
  initialize_sync() {
    const keys = APIService.get_keys(
      ["GOOGLE_API_KEY", "GOOGLE_CLIENT_ID", "DISCOVERY_DOC", "SCOPES"]
    )
    console.log(keys)
  }

  gapiLoaded() {
    gapi.load("client", this.initializeGapiClient);
  }

  /**
   * Callback after the API client is loaded. Loads the
   * discovery doc to initialize the API.
   */
  async initializeGapiClient() {
    await 
    await gapi.client.init({
      apiKey: API_KEY,
      discoveryDocs: [DISCOVERY_DOC],
    });
    // this.gapiInitiated = true;
    return true;
    // this.maybeEnableButtons();
  }

  /**
   * Callback after Google Identity Services are loaded.
   */
  gisLoaded() {
    this.tokenClient = google.accounts.oauth2.initTokenClient({
      client_id: CLIENT_ID,
      scope: SCOPES,
      callback: "", // defined later
    });
    // this.gisInited = true;
    return true;
    // this.maybeEnableButtons();
  }

  handleAuthClick() {
    console.log("handleAuthClick");
    this.tokenClient.callback = async (resp) => {
      if (resp.error !== undefined) {
        throw resp;
      }
      this.auth_token = true;
    };

    if (gapi.client.getToken() === null) {
      // Prompt the user to select a Google Account and ask for consent to share their data
      // when establishing a new session.
      this.tokenClient.requestAccessToken({ prompt: "consent" });
    } else {
      // Skip display of account chooser and consent dialog for an existing session.
      this.tokenClient.requestAccessToken({ prompt: "" });
    }
  }

  handleSignoutClick() {
    const token = gapi.client.getToken();
    if (token !== null) {
      google.accounts.oauth2.revoke(token.access_token);
      gapi.client.setToken("");
      this.auth_token = false;
    }
  }

  async sync_google(tokenClient, date, events, user) {
    await this.verify_calendar().then((res) => {
      console.log("syncing...", res);
      let calendar_id = res
      let date_month = new Date("01 " + date).getMonth();
      const cal_events = events.filter(
        (event) => new Date(event.start).getMonth() == date_month
      );
      this.sync_shifts(calendar_id, user, date, cal_events)
        .then((res) => {
          console.log(res)
        })
    });
  }

  async timeMin(date) {
    let tz_offset = new Date().getTimezoneOffset() * 60000;
    let date_start = new Date(`01 ${date}`);
    let start =
      new Date(date_start - tz_offset).toISOString().slice(0, -5) + "Z";
    return start;
  }

  async timeMax(date) {
    let tz_offset = new Date().getTimezoneOffset() * 60000;
    let date_start = new Date(`01 ${date}`);
    let date_end = new Date(
      date_start.getFullYear(),
      date_start.getMonth() + 1, 0, 23, 59
    );
    let end = new Date(date_end).toISOString().slice(0, -5) + "Z";
    // console.log(end);
    return end;
  }

  async list_calendars() {
    return new Promise((resolve) => {
      const get_calendars = gapi.client.calendar.calendarList.list();
      console.log(get_calendars);
      let exists = false;
      let calendar_id = ''
      get_calendars.execute((cal) => {
        let calendar = cal.items.find((o) =>
          o.summary.includes("AMCS Schedule")
        );
        if (calendar != undefined) {
          calendar_id = calendar.id;
          exists = true;
        }
        resolve({ "exists": exists, "calendar_id": calendar_id });
      });
    });
  }

  async add_calendar() {
    return new Promise(async (resolve, reject) => {
      const insert_calendar = gapi.client.calendar.calendars.insert({
        summary: "AMCS Schedule",
      });
      // console.log(insert_calendar)
      await insert_calendar.execute((res) => {
        // console.log(res, res.id, res.summary)
        // this.calendar_id = res.id;
        if (!res.error) {
          resolve(res.id);
          // Notify.create({
          //   message: "Successfully created calendar!",
          //   color: "green",
          // });
        } else {
          reject(false);
        }
      });
    });
  }

  verify_calendar() {
    // console.log(calendar_id);
    return new Promise(async (resolve) => {
      await this.list_calendars().then((response) => {
        console.log(response);
        if (response.exists !== true) {
          console.log("Adding Calendar")
          this.add_calendar().then((res) => {
            console.log(res)
            resolve(res);
          });
        } else {          
          resolve(response.calendar_id);
        }
      });
    })
  }

  async get_google_events(calendar_id, date) {
    let new_calendar_id = ''
    return new Promise(async (resolve) => {
      if (!calendar_id.length > 0) {
        // Need to fix so function waits for this to finish before trying to continue
        this.verify_calendar().then((res) => {
          new_calendar_id = res
          this.get_google_events(new_calendar_id, date)
        })
      } else {
        let params = {
          calendarId: calendar_id,
          timeMin: await this.timeMin(date),
          timeMax: await this.timeMax(date),
        };
        const get_events = gapi.client.calendar.events.list(params);
        // console.log(get_events)
        await get_events.execute((events) => {
          // console.log(events.items)
          resolve(events.items);
        });
      }
    });
  }

  async clear_google_events(calendar_id, date) {
    await this.get_google_events(calendar_id, date).then((res) => {
      // console.log(res)
      if (res.length > 0) {
        var batch = gapi.client.newBatch();
        res.forEach((event) => {
          batch.add(
            gapi.client.calendar.events.delete({
              calendarId: calendar_id,
              eventId: event.id,
            })
          );
        });
        batch.then(() => {
          console.log("all jobs done!!!");
          // Notify.create({
          //   message: "Schedule successfully cleared",
          //   color: "green",
          // });
        });
      }

    });
  }

  async sync_shifts(cal_id, user, date, events) {
    if (cal_id.length > 0) {
      if (user != null) {
        await this.clear_google_events(cal_id, date);
        var batch = gapi.client.newBatch();
        // console.log(this.user)
        let date_month = new Date("01 " + date).getMonth();
        // console.log(date_month)
        // const cal_events = this.calendarOptions.events.filter(
        //   (event) => new Date(event.start).getMonth() == date_month
        // );
        console.log(events)
        events.forEach((event) => {
          // Update this, it syncs entire year to calendar.
          // console.log(event.title)
          // console.log(new Date(event.start).getMonth())
          let shift_start = event.start.replace(/ /g, "T");
          // console.log(event.title, shift_start)
          let shift = {
            summary: event.title,
            start: {
              dateTime: shift_start,
              timeZone: "UTC",
            },
            end: {
              dateTime: shift_start,
              timeZone: "UTC",
            },
            reminders: {
              useDefault: false,
            },
            "source.title": "VetScheduler",
          };
          batch.add(
            gapi.client.calendar.events.insert({
              calendarId: cal_id,
              resource: shift,
            })
          );
        });
        // ====== NOTE: this loads the schedule to Google Calendar =============
        // console.log(batch)
        await batch.then((response) => {
          // this.loading = false;
          // this.submit_button = false;
          // this.clearFilters()
          // this.user_shifts = []
          console.log(response)
          console.log("all jobs done!!!");
          return (true)
          // Notify.create({
          //   message: "Schedule uploaded successfully",
          //   color: "green",
          // });
        });
      } else {
        console.log("failed")
        return (false)
        // Notify.create({
        //   message: "Please select which user to sync.",
        //   color: "red",
        //   position: "center",
        // });
      }
    }
  }

  async upload_shifts() {
    if (this.calendar_id.length > 0) {
      if (this.user != null) {
        var batch = gapi.client.newBatch();
        this.disabled = true;
        console.log(this.user);
        this.calendarOptions.events.forEach((event) => {
          let shift_start = event.start.replace(/ /g, "T");
          console.log(event.title, shift_start);
          let shift = {
            summary: event.title,
            start: {
              dateTime: shift_start,
              timeZone: "UTC",
            },
            end: {
              dateTime: shift_start,
              timeZone: "UTC",
            },
          };
          batch.add(
            gapi.client.calendar.events.insert({
              calendarId: this.calendar_id,
              resource: shift,
            })
          );
        });
        // ====== NOTE: this loads the schedule to Google Calendar =============
        // console.log(batch)
        batch.then(() => {
          this.loading = false;
          this.submit_button = false;
          this.user = null;
          // this.user_shifts = []
          console.log("all jobs done!!!");
          // Notify.create({
          //   message: "Schedule uploaded successfully",
          //   color: "green",
          // });
        });
      } else {
        // Notify.create({
        //   message: "Please select which user to sync.",
        //   color: "red",
        //   position: "center",
        // });
      }
    }
  }

  async test_API() {
    // var requestOptions = {
    //   method: 'POST',
    //   redirect: 'follow'
    // };

    // fetch("https://www.googleapis.com/calendar/v3/calendars/primary/events/quickAdd?calendarId=primary&text=Day Shift on June 21 7am-7pm", requestOptions)
    //   .then(response => response.text())
    //   .then(result => console.log(result))
    //   .catch(error => console.log('error', error));
    let event = {
      summary: "Day Shift on June 21 7am-7pm",
      location: "World Wide Web",
      description: "Testing",
      start: {
        dateTime: "2023-06-21T07:00:00-07:00",
        timeZone: "America/Los_Angeles",
      },
      end: {
        dateTime: "2023-06-21T19:00:00-07:00",
        timeZone: "America/Los_Angeles",
      },
    };

    const request = gapi.client.calendar.events.insert({
      calendarId: "primary",
      resource: event,
    });

    request.execute(function (event) {
      appendPre("Event created: " + event.htmlLink);
    });
  }

  async listUpcomingEvents() {
    let response;
    try {
      const request = {
        calendarId: "primary",
        timeMin: new Date().toISOString(),
        showDeleted: false,
        singleEvents: true,
        maxResults: 10,
        orderBy: "startTime",
      };
      response = await gapi.client.calendar.events.list(request);
    } catch (err) {
      document.getElementById("content").innerText = err.message;
      return;
    }

    const events = response.result.items;
    if (!events || events.length == 0) {
      document.getElementById("content").innerText = "No events found.";
      return;
    }
    // Flatten to string to display
    const output = events.reduce(
      (str, event) =>
        `${str}${event.summary} (${
          event.start.dateTime || event.start.date
        })\n`,
      "Events:\n"
    );
    document.getElementById("content").innerText = output;
  }
}

export default new GoogleFunctions();
