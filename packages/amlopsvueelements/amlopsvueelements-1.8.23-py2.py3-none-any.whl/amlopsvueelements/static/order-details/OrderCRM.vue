<template>
  <div class="pricing-step bg-white w-full border border-transparent rounded-md">
    <div class="pricing-step-header flex justify-between py-2 px-3">
      <div class="pricing-step-header-name">CRM Activity</div>
      <div class="pricing-step-header-actions flex gap-4">
        <img width="20" height="20" src="../../assets/icons/filter.svg" alt="filter" class="cursor-pointer">
        <Button class="button flex items-center gap-2">
          <img src="../../assets/icons/plus.svg" alt="add">
          Add Activity
        </Button>
      </div>
    </div>
    <div class="pricing-step-content w-full flex flex-col" v-if="mockCRM.length">
      <div class="pricing-step-content-header-wrap w-full flex items-center">
        <div class="pricing-step-content-col w-1/12">
          <div class="pricing-step-content-col-header px-3 py-2">Recorded by</div>
        </div>
        <div class="pricing-step-content-col w-1/12">
          <div class="pricing-step-content-col-header px-3 py-2">Date & Time</div>
        </div>
        <div class="pricing-step-content-col w-1/12">
          <div class="pricing-step-content-col-header px-3 py-2">Activity Type</div>
        </div>
        <div class="pricing-step-content-col w-1/12">
          <div class="pricing-step-content-col-header px-3 py-2">Opportunity / order</div>
        </div>
        <div class="pricing-step-content-col w-2/12">
          <div class="pricing-step-content-col-header px-3 py-2">Applicable person</div>
        </div>
        <div class="pricing-step-content-col w-4/12">
          <div class="pricing-step-content-col-header px-3 py-2">Description</div>
        </div>
        <div class="pricing-step-content-col w-2/12">
          <div class="pricing-step-content-col-header px-3 py-2">Attachments</div>
        </div>
      </div>
      <div class="pricing-step-content-data-wrap selected-supplier w-full flex items-center"
        v-for="(activity, index) in mockCRM" :key="activity.date">
        <div class="pricing-step-content-col w-1/12">
          <div class="pricing-step-content-col-data px-3 py-2 flex gap-1 items-center">
            <Avatar :first-name="activity.recorder_by.split(' ')[0]" :last-name="activity.recorder_by.split(' ')[1]"
              :is-small="true" />
            {{ activity.recorder_by }}
          </div>
        </div>
        <div class="pricing-step-content-col w-1/12">
          <div class="pricing-step-content-col-data px-3 py-2">{{ activity.date }}</div>
        </div>
        <div class="pricing-step-content-col w-1/12">
          <div class="pricing-step-content-col-data px-3 py-2">{{ activity.activity_type }}</div>
        </div>
        <div class="pricing-step-content-col w-1/12">
          <div class="pricing-step-content-col-data px-3 py-2">{{ activity.opportunity ?? '--' }}</div>
        </div>
        <div class="pricing-step-content-col w-2/12">
          <div class="pricing-step-content-col-data px-3 py-2">{{ activity.person ?? '--' }}</div>
        </div>
        <div class="pricing-step-content-col w-4/12">
          <div class="pricing-step-content-col-data px-3 py-2">{{ activity.description }}</div>
        </div>
        <div class="pricing-step-content-col w-10pc">
          <div class="pricing-step-content-col-data px-3 py-2">
            <div class="files-button flex gap-2 justify-center cursor-pointer" v-if="activity.attachments.length > 0">
              <img width="12" height="12" src="../../assets/icons/paperclip.svg" alt="file"> {{
                activity.attachments.length }} files
            </div>
            <div v-else>--</div>
          </div>
        </div>
        <div class="pricing-step-content-col w-6pc">
          <div class="pricing-step-content-col-data px-3 py-2 flex justify-center">
            <img width="20" height="20" src="../../assets/icons/dots-vertical.svg" alt="options"
              class="horizontal cursor-pointer">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { Button } from 'shared/components';
import { ref } from 'vue';
import Avatar from '../forms/Avatar.vue';


const mockCRM = ref([{
  recorder_by: 'John Doe',
  date: new Date().toDateString(),
  activity_type: 'In-Person Meeting',
  opportunity: null,
  person: null,
  description: 'Meeting with Frans and co to demo the latest version of the Mil App',
  attachments: [1, 2, 3]
},
{
  recorder_by: 'John Doe',
  date: new Date().toDateString(),
  activity_type: 'In-Person Meeting',
  opportunity: null,
  person: null,
  description: 'Meeting with Frans and co to demo the latest version of the Mil App',
  attachments: [1, 2, 3]
}])

</script>

<style lang="scss">
.button {
  background-color: rgba(81, 93, 138, 1) !important;
  color: white !important;
  font-weight: 500 !important;
  font-size: 16px !important;
  @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-2 px-4 rounded-xl #{!important};
}

.w-10pc {
  width: 10%;
}
.w-6pc {
  width: 6.66666%;
}
</style>