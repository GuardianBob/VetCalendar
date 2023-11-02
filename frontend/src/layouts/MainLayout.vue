<template>
  <q-layout view="hHh Lpr lff">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="drawer = !drawer"
        />

        <q-toolbar-title>
          Vet Scheduler
        </q-toolbar-title>

        <div>Version: {{ version }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="drawer"
      bordered
      overlay
      :class="$q.dark.isActive ? 'q-dark' : 'q-light'"
    >
      <q-list>
        <q-item-label
          header
        >
          <!-- <q-icon v-if="$q.platform.is.mobile" name="menu" size="md" color="primary" @click="drawer = !drawer" ></q-icon> -->
          Essential Links
        </q-item-label>
        <q-toggle 
          v-model="toggle_value" 
          :color="toggle_color" 
          size="lg"
          @click="toggle_theme"
          checked-icon="fa-solid fa-moon"
          unchecked-icon="fa-solid fa-sun"
        />

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, colors } from "quasar";
import EssentialLink from 'components/EssentialLink.vue'
import { version } from '../../package.json'

const linksList = [
  {
    title: 'Home',
    caption: '',
    icon: 'home',
    link: '/'
  },
  {
    title: 'Schedule Import',
    caption: '',
    icon: 'code',
    link: '/schedule_import'
  },
  // {
  //   title: 'Discord Chat Channel',
  //   caption: 'chat.quasar.dev',
  //   icon: 'chat',
  //   link: 'https://chat.quasar.dev'
  // },
  // {
  //   title: 'Forum',
  //   caption: 'forum.quasar.dev',
  //   icon: 'record_voice_over',
  //   link: 'https://forum.quasar.dev'
  // },
  // {
  //   title: 'Twitter',
  //   caption: '@quasarframework',
  //   icon: 'rss_feed',
  //   link: 'https://twitter.quasar.dev'
  // },
  // {
  //   title: 'Facebook',
  //   caption: '@QuasarFramework',
  //   icon: 'public',
  //   link: 'https://facebook.quasar.dev'
  // },
  // {
  //   title: 'Quasar Awesome',
  //   caption: 'Community Quasar projects',
  //   icon: 'favorite',
  //   link: 'https://awesome.quasar.dev'
  // }
]

export default defineComponent({
  name: 'MainLayout',

  components: {
    EssentialLink
  },
  data() {
    return {
      version: version,
      toggle_value: ref(false),
      toggle_color: ref(null),
    }
  },
  setup () {
    const $q = useQuasar();
    
    return {
      drawer: ref(false),
      essentialLinks: linksList,
      // toggleLeftDrawer () {
      //   leftDrawerOpen.value = !leftDrawerOpen.value
      // }
    }
  },
  methods: {
    getAppTheme() {
      // get the saved theme from the localStorage
      const storageSavedTheme = localStorage.getItem('JBearSavedTheme'); // Check to see if there a saved theme
      
      if (storageSavedTheme) {
        this.savedTheme = storageSavedTheme;
        // console.log("theme: ", this.savedTheme)
        this.savedTheme === 'light_theme' ? this.set_light() : this.set_dark();
      } else {
        // So, try to get the browser default theme or make your own default
        // Check to see if Media-Queries are supported
        if (window.matchMedia) {
          // console.log("matching")
          // Check if the dark-mode Media-Query matches
          if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            this.savedTheme = 'dark_theme';
            // console.log("dark");
          } else {
            this.savedTheme = 'light_theme';
            this.toggle_theme()
            // console.log("light");
          }
        } else {
          // Default (when Media-Queries are not supported)
          this.savedTheme = this.appTheme;
        }
      }
      localStorage.setItem('JBearSavedTheme', this.savedTheme);
    }, // save the new theme in the localStorage

    toggle_theme() {
      this.savedTheme === 'light_theme' ? this.set_dark() : this.set_light(); // toggle theme
      localStorage.setItem('JBearSavedTheme', this.savedTheme);
      console.log("clicked")
    },

    set_dark() {
      // const $q = useQuasar();
      const div = document.querySelector('body')
      const nav = document.querySelector('aside')
      const table_header = document.querySelector('th')
      div.classList.remove('body--light')
      div.classList.add('body--dark')
      nav.classList.remove('body--light')
      nav.classList.add('q-drawer--dark')
      nav.classList.add('q-dark')
      table_header.style.backgroundColor = "#121212";
      this.savedTheme = 'dark_theme'
      this.toggle_color = 'grey-10'
      this.toggle_value = true
      console.log("dark");
      this.$q.dark.set(true);
    },

    set_light() {
      // const $q = useQuasar();
      const div = document.querySelector('body')
      const nav = document.querySelector('aside')
      const table_header = document.querySelector('th')
      table_header.style.backgroundColor = null;
      nav.classList.remove('q-drawer--dark')
      nav.classList.remove('q-dark')
      div.classList.remove('body--dark')
      div.classList.add('body--light')
      this.savedTheme = 'light_theme'
      this.toggle_color = 'white'
      this.toggle_value = false
      console.log("light");
      this.$q.dark.set(false);
    }
  },

  mounted() {
    this.getAppTheme()
  },
})
</script>
