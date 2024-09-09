<template>
  <div class="order-sidebar flex bg-white rounded-md" :class="{ 'is-sidebar-closed': isSidebarClosed }">
    <AddNoteModal :isOpen="isModalOpened" ref="noteInput"
      @modal-close="isModalOpened = false" @modal-submit="" name="note-modal" />
    <div class="order-sidebar-content w-full flex flex-col">
      <div class="order-sidebar-content-header px-3 py-2 flex justify-between items-center">
        {{ activeTab.name }}
        <Button class="button flex items-center gap-2" v-if="activeTab.name === 'Notes'" @click="isModalOpened = true">
          <img src="../../assets/icons/plus.svg" alt="add">
          Add Note
        </Button>
      </div>
      <ScrollBar class="my-3">
        <div class="order-sidebar-content-data px-3 flex flex-col gap-3 max-h-full" v-if="activeTab.name === 'Notes'">
          <div class="order-sidebar-content-data-note border-0 rounded-lg p-2 flex flex-col" v-for="note in orderNotes"
            :key="note.id">
            <div class="note-header">
              <div class="note-header-info flex gap-2 pb-2">
                <Avatar :first-name="note.created_by?.details?.first_name"
                  :last-name="note.created_by?.details?.last_name" />
                <div class="note-header-info-wrap">
                  <div class="note-header-info-name">{{ note.created_by?.details?.full_name }}</div>
                  <div class="note-header-info-date">{{ toNoteTime(note.created_at) }}</div>
                </div>
              </div>
              <div class="note-header-actions"></div>
            </div>
            <div class="note-content flex">{{ note.content }}</div>
          </div>
        </div>
        <div class="order-sidebar-content-data" v-else-if="activeTab.name === 'Chat'">
        </div>
        <div class="order-sidebar-content-data" v-else-if="activeTab.name === 'Activity'">
          <div class="order-sidebar-content-data-activity border-0 rounded-lg pl-3 pt-0 flex"
            v-for="activity in mockActivity" :key="activity.name">
            <div class="order-activity-info-side flex flex-col items-center">
              <div class="line-top"></div>
              <div class="circle"></div>
              <div class="line-bottom"></div>
            </div>
            <div class="order-activityp-info-wrap p-3 flex flex-col w-full">
              <div class="order-activity-info flex justify-between">
                <div class="order-activity-info-name">{{ activity.name }}</div>
                <div class="order-activity-info-date">{{ toNoteTime(activity.date) }}</div>
              </div>
              <div class="order-activity-data">{{ activity.description }}</div>
            </div>
          </div>
        </div>
        <div class="order-sidebar-content-data" v-else>
          No tab
        </div>
      </ScrollBar>
    </div>
    <div class="order-sidebar-menu w-2/12 py-4 px-3 flex flex-col gap-4">
      <div class="order-sidebar-menu-el flex flex-col items-center" :class="{ 'active': activeTab.name === el.name }"
        v-for="el in sidebar" :key="el.name" v-on:click="changeTab(el)">
        <div class="img-wrap flex items-center justify-center p-2 border-0 rounded-lg"><img
            :src="getImageUrl(`assets/icons/${el.icon}.svg`)" :alt="el.icon"></div>
        {{ el.name }}
      </div>

      <div class="close-sidebar img-wrap cursor-pointer flex items-center justify-center p-2"
        :class="{ 'is-closed': isSidebarClosed }" v-on:click="changeSidebar">
        <img src="../../assets/icons/sidebar-close.svg" alt="sidebar_close">
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onBeforeMount, ref, watch, type PropType } from 'vue'
import type { BaseValidation } from '@vuelidate/core'
import { useOrderFormStore } from '@/stores/useOrderFormStore'
import { useOrderStore } from '@/stores/useOrderStore'
import { Button } from 'shared/components'
import type { IOrder, IOrderNote } from '@/types/order/order.types'
import OrderReferences from '@/services/order/order-references'
import { useFetch } from '@/composables/useFetch'
import { toNoteTime } from '@/helpers/order'
import ScrollBar from '../forms/ScrollBar.vue'
import Avatar from '../forms/Avatar.vue'
import AddNoteModal from '../modals/AddNoteModal.vue'
import { getImageUrl } from '@/helpers'

const props = defineProps({
  validationInfo: {
    type: Object as PropType<BaseValidation>,
    default: () => { }
  },
  isLoading: {
    type: Boolean as PropType<boolean>,
    default: false
  },
  order: {
    type: Object as PropType<IOrder>,
    default: null
  }
})

const sidebar = ref([
  { name: 'Notes', icon: 'notes' },
  { name: 'Chat', icon: 'chat' },
  { name: 'Activity', icon: 'activity' },
])

const activeTab = ref(sidebar.value[0]);
const isSidebarClosed = ref(false);

const isModalOpened = ref(false);

const orderFormStore = useOrderFormStore();
const orderStore = useOrderStore();

const mockActivity = [{ name: 'John Doe', date: new Date().toDateString(), description: 'Admin Edit Session: End. A really long message there to show the correct expansion of the element on the side. This element should be way bigger then the other.' },
{ name: 'John Doe', date: new Date().toDateString(), description: 'Admin Edit Session: End' }
]

const {
  loading: isLoadingOrderNotes,
  data: orderNotes,
  callFetch: fetchOrderNotes
} = useFetch<IOrderNote[], () => Promise<IOrderNote[]>>(async () => {
  return await OrderReferences.fetchOrderNotes(props.order!.id!)
})

function changeTab(el: any) {
  activeTab.value = el;
}

const changeSidebar = () => {
  isSidebarClosed.value = !isSidebarClosed.value;
}

watch(() => props.order, (order: IOrder) => {
  fetchOrderNotes();
})

</script>

<style lang="scss">
.button {
  background-color: rgba(81, 93, 138, 1) !important;
  color: white !important;
  font-weight: 500 !important;
  font-size: 16px !important;
  @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-2 px-4 rounded-xl #{!important};
}

.order-sidebar {
  justify-content: flex-end;
  width: 35%;

  &-content {
    &-header {
      font-size: 18px;
      font-weight: 600;
      color: rgba(21, 28, 53, 1);
      border-bottom: 1px solid rgba(239, 241, 246, 1);
      min-height: 3.5rem;
    }

    &-data {
      height: 100%;
      max-height: 460px;
      // overflow-y: auto;

      &-note {
        background-color: rgba(255, 161, 0, 0.1);

        .note-header {
          &-info {
            &-name {
              font-size: 14px;
              font-weight: 600;
              color: rgba(39, 44, 63, 1);
            }

            &-date {
              font-size: 12px;
              font-weight: 400;
              color: rgba(82, 90, 122, 1);
            }
          }
        }

        .note-content {
          font-size: 15px;
          font-weight: 400;
          color: rgba(39, 44, 63, 1);
        }
      }

      &-activity {
        &:first-of-type {
          .order-activity-info-side {
            padding-top: 12px;
          }

          .line-top {
            display: none;
          }
        }

        &:last-of-type {
          .line-bottom {
            display: none;
          }
        }

        .order-activity-info {
          position: relative;

          &-name {
            color: rgba(39, 44, 63, 1);
            font-weight: 600;
            font-size: 14px;
          }

          &-date {
            color: rgba(133, 141, 173, 1);
            font-weight: 400;
            font-size: 12px;
          }

          &-side {
            .circle {
              height: 8px;
              width: 8px;
              background-color: rgba(255, 255, 255, 1);
              border: 2px solid rgba(125, 148, 231, 1);
              border-radius: 50%;
              left: -1rem;
            }

            .line-bottom {
              width: 1px;
              background-color: rgba(223, 226, 236, 1);
              border: 1px solid rgba(223, 226, 236, 1);
              height: 100%;
              top: 6px;
              left: 1.5px;
            }


            .line-top {
              width: 1px;
              background-color: rgba(223, 226, 236, 1);
              border: 1px solid rgba(223, 226, 236, 1);
              height: 12px;
              top: 6px;
              left: 1.5px;
            }
          }

        }

        .order-activity-data {
          color: rgba(39, 44, 63, 1);
          font-weight: 400;
          font-size: 15px;
        }
      }
    }
  }

  &.is-sidebar-closed {
    width: 73px;

    .order-sidebar-content {
      display: none;
      transition: 0.5s;
    }

    .order-sidebar-menu {
      width: 100%;
    }
  }

  &-menu {
    position: relative;
    border-left: 1px solid rgba(239, 241, 246, 1);
    max-width: 73px;

    &-el {
      color: rgba(21, 28, 53, 1);
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;

      .img-wrap {
        width: 40px !important;
        height: 40px !important;
      }

      img {
        width: 20px !important;
        height: 20px !important;
      }

      &.active {
        color: rgba(81, 93, 138, 1);

        .img-wrap {
          background-color: rgba(125, 148, 231, 0.1);
        }
      }
    }

    .close-sidebar {
      position: absolute;
      width: 100%;
      bottom: 1rem;
      left: 0;

      &.is-closed {
        transform: rotate(180deg)
      }
    }
  }
}
</style>