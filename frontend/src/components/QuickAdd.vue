<template>
  <div class="">
    <q-form @submit="submit" method="POST">
      <h5 class="text-primary q-py-none q-my-sm">{{ pageTitle }}</h5>
      <div class="row justify-around text-center q-ma-md">
        <div class="col q-px-md q-mx-md">
          <q-select class="q-mx-sm" v-model="user" :options="user_list" dense options-dense
            @update:model-value="filterShifts()">
            <template v-slot:prepend>
              <q-icon name="filter_alt" round color="primary" />
            </template>
            <template v-slot:append>
              <q-btn v-if="user !== null" class="q-ml-md q-px-sm" color="negative" size="md" flat rounded
                id="clear_filters_button" @click.stop.prevent="clearFilters" icon="cancel" />
              <!-- <q-icon name="close" @click.stop.prevent="clearFilters" class="cursor-pointer" v-if="user !== null" /> -->
            </template>
            <q-tooltip class="bg-accent" anchor="center start">Filter Schedule</q-tooltip>
          </q-select>
        </div>
      </div>
    </q-form>
    
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"
import dummyData from "components/dummyData.json"

export default {
  name: "QuickAdd",
  props: [ "" ],
  setup() {
    return {
      info: ref(false),
      pageTitle: ref('Quick Add Shifts'),
      user: ref(''),
      shift: ref(''),
      type: ref(''),
      user_list: ref([dummyData.users]),
      shift_list: ref([]),
      type_list: ref([]),
      dates: ref([{}]),
    }
  },

  watch: {
    userInfo(newValue, oldValue) {
      this.userData = this.userInfo
    },
    
  },

  mounted() {
    this.userData = this.userInfo
  }
};
</script>


