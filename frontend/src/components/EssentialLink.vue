<template>
  <div>
    <q-item
      v-if="!sublinks"
      clickable
      tag="a"
      :to="link"
    >
      <q-item-section
        v-if="icon"
        avatar
      >
        <q-icon :name="icon" />
      </q-item-section>

      <q-item-section>
        <q-item-label>{{ title }}</q-item-label>
        <q-item-label caption>{{ caption }}</q-item-label>
      </q-item-section>
    </q-item>
    <q-expansion-item
      v-else
      expand-separator
      :label="title"
      :icon="icon"
    >
      <!-- <q-item-section
        v-if="icon"
        avatar
      >
        <q-icon :name="icon" />
      </q-item-section> -->

      <!-- <q-item-section>
        <q-item-label>{{ title }}</q-item-label>
        <q-item-label caption>{{ caption }}</q-item-label>
      </q-item-section> -->
        <q-list class="q-ml-md">
          <q-item
            v-for="sublink in sublinks"
            :key="sublink.title"
            dense
            clickable
            :to="sublink.link"
          >
            <q-item-section
              v-if="sublink.icon"
              avatar
            >
              <q-icon :name="sublink.icon" />
            </q-item-section>
            <q-item-section>{{ sublink.title }}</q-item-section>
          </q-item>
        </q-list>
    </q-expansion-item>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'EssentialLink',
  props: {
    title: {
      type: String,
      required: true
    },

    caption: {
      type: String,
      default: ''
    },

    link: {
      type: String,
      default: '#'
    },

    sublinks: {
      // type: String,
      // default: '#'
    },

    icon: {
      type: String,
      default: ''
    }
  }
})
</script>
