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
          color="secondary"
        />

        <q-toolbar-title>
          Shift Management
        </q-toolbar-title>

        <div class="text-secondary">v: {{ version }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="drawer"
      bordered
      overlay
    >
      <q-list>
        <q-item-label
          header
        >
          <q-icon v-if="$q.platform.is.mobile" name="menu" size="md" color="secondary" @click="drawer = !drawer" ></q-icon>
          Menu
        </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
        <q-item
          clickable
          @click="logout"
        >
          <q-item-section
              avatar
            >
              <q-icon name="logout" color="negative "/>
            </q-item-section>
            <q-item-section>
              Logout</q-item-section>
          </q-item>
      </q-list>
    </q-drawer>

    <q-page-container >
      <router-view @click="drawer = false"/>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'
import { version } from '../../package.json'
import { useMainStore } from "stores/main-store.js"
import { useRouter } from 'vue-router';
import APIService from '../../services/api';

const mainStore = useMainStore();

const linksList = [
  {
    title: 'Home',
    caption: '',
    icon: 'home',
    link: '/'
  },
  {
    title: 'Login',
    caption: '',
    icon: 'lock',
    link: '/login',
    sublinks : [
      {
        title: 'Login',
        caption: '',
        icon: 'lock',
        link: '/login'
      },
      {
        title: 'Register',
        caption: '',
        icon: 'lock',
        link: '/register'
      },
    ]
  },
  {
    title: 'Admin',
    caption: '',
    icon: 'admin_panel_settings',
    sublinks : [
      {
        title: 'Schedule Import',
        caption: '',
        icon: 'upload_file',
        link: '/schedule_import'
      },
      {
        title: 'Manage Users',
        caption: '',
        icon: 'people',
        link: '/users'
      },
      {
        title: 'Manage Schedule',
        caption: '',
        icon: 'calendar_month',
        link: '/manage_schedule'
      },
      {
        title: 'Schedule Settings',
        caption: '',
        icon: 'settings',
        link: '/schedule_settings'
      },
      {
        title: 'Admin Settings',
        caption: '',
        icon: 'construction',
        link: '/master_settings'
      },
    ]
  },
  {
    title: 'Testing',
    caption: '',
    icon: 'construction',
    sublinks : [
      {
        title: 'Page Test',
        caption: '',
        icon: 'upload_file',
        link: '/blank'
      },
      {
        title: 'Forms Page Test',
        caption: '',
        icon: 'upload_file',
        link: '/forms_page'
      },
      {
        title: 'Form Test',
        caption: '',
        icon: 'feed',
        link: '/form'
      },
      // {
      //   title: 'Add JSON Form',
      //   caption: '',
      //   icon: 'feed',
      //   link: '/add_json_form'
      // },
    ]
  },
]

export default defineComponent({
  name: 'MainLayout',
  
  components: {
    EssentialLink
  },
  data() {
    return {
      version: version,
    }
  },
  setup () {
    const router = useRouter();
    return {
      drawer: ref(false),
      essentialLinks: linksList,
      // toggleLeftDrawer () {
      //   leftDrawerOpen.value = !leftDrawerOpen.value
      // }
    }
  },
  methods: {
    logout() {
      // router.push({ name: 'login' });
      APIService.logout();
    }
  }
})
</script>
