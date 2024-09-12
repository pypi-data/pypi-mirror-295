<template>
  <div class="order-header flex flex-col pt-4">
    <SendViaEmailModal :isOpen="isModalOpened" :organisation-id="order?.client?.id" ref="emailInput"
      @modal-close="isModalOpened = false" @modal-submit="" name="email-modal" />
    <div class="order-status flex w-full justify-between items-center mb-4 px-4">
      <div class="status flex px-2 py-1 border-0 rounded-md"
        :style="{ 'background-color': getColor(), 'color': getTextColor() }"><span>{{
          order?.status?.status_name?.toUpperCase() }}</span></div>
      <div class="status-buttons flex gap-3" v-if="currentStep === 1">
        <ButtonPopover v-show="true || quoteButton?.state === 'active'">
          <template #default>
            <div class="button">{{ quoteButton?.button_text ?? 'Send Client Quote' }}</div>
          </template>
          <template #popup>
            <div class="send-via-email-popup flex gap-2 cursor-pointer">
              <div class="el flex gap-2" @click="isModalOpened = true">
                <img width="20" height="20" src="../../assets/icons/mail.svg" alt="email">
                Send via email
              </div>
            </div>
          </template>
        </ButtonPopover>
        <Button :disabled="!proceedButton"
          class="button button-green flex items-center gap-2">
          Proceed to Order
        </Button>
      </div>
      <div class="status-buttons flex gap-3" v-if="currentStep === 2">
        <Button class="button">
          Proceed to Order
        </Button>
        <Button class="button cancel-button items-center gap-2">
          <img width="12" height="12" src="../../assets/icons/cross.svg" alt="delete">
          Decline Order
        </Button>
        <Button class="button button-green flex items-center gap-2">
          <img src="../../assets/icons/check.svg" alt="approve">
          Approve Order
        </Button>
      </div>
      <div class="status-buttons flex gap-3" v-if="currentStep === 3">
        <ButtonPopover :left="true">
          <template #default>
            <div class="button">
              Send
              <img width="20" height="20" src="../../assets/icons/chevron-down.svg" alt="delete">
            </div>
          </template>
          <template #popup>
            <div class="send-via-email-popup flex flex-col gap-2 cursor-pointer">
              <div class="el flex gap-2" @click="isModalOpened = true">
                <img width="20" height="20" src="../../assets/icons/gas.svg" alt="gas">
                Send via Email
              </div>
            </div>
          </template>
        </ButtonPopover>
        <Button class="button">
          Submit Delivery Ticket Details
        </Button>
        <Button class="button cancel-button items-center gap-2">
          <img width="12" height="12" src="../../assets/icons/cross.svg" alt="delete">
          Mark as No-Uplift
        </Button>
        <Button class="button button-green flex items-center gap-2">
          <img src="../../assets/icons/check.svg" alt="approve">
          Confirm Supplier Order
        </Button>
      </div>
    </div>
    <div class="order-name-wrap mb-4 px-4 flex flex-col">
      <div class="order-name-row flex gap-2 items-center">
        <div class="order-name">
          {{ order?.aml_order_number }}
        </div>
        <div class="order-linked flex items-center px-2 gap-2 cursor-pointer" v-if="order?.linked_order"
          v-on:click="redirectToLinkedOrder(order?.linked_order?.uri!)">
          <img src="../../assets/icons/linked.svg" alt="linked">
          <div class="order-linked-text">
            {{ order?.linked_order?.aml_order_number }}
          </div>
        </div>
        <Avatar v-if="order?.assigned_aml_person" :first-name="order?.assigned_aml_person?.details?.first_name"
          :last-name="order?.assigned_aml_person?.details?.last_name" :is-small="true"></Avatar>
      </div>
      <div class="order-company">{{ order?.client?.details?.registered_name }}</div>
    </div>
    <div class="order-content flex pb-4 px-4 gap-2" v-if="order?.type?.is_fuel">
      <div class="order-content-col w-4/12">
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            Uplift Time (UTC)
          </div>
          <div class="order-content-data w-8/12">
            {{ order?.fuel_order?.fueling_time_utc ? order?.fuel_order?.arrival_time_tbc ?
              order?.fuel_order?.fueling_time_utc + ' (Time TBC)' : order?.fuel_order?.fueling_time_utc : 'TBC' }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            Aircraft
          </div>
          <div class="order-content-data w-8/12" v-if="order?.aircraft">
            {{ `${order?.aircraft?.registration} - ${order?.aircraft?.type?.manufacturer}
            ${order?.aircraft?.type?.model} (${order?.aircraft?.type?.designator})` }}
          </div>
          <div class="order-content-data w-8/12" v-else-if="order?.aircraft_type">
            {{ order?.aircraft_type?.full_repr }}
          </div>
          <div class="order-content-data w-8/12" v-else>
            Any aircraft
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            IPA
          </div>
          <div class="order-content-data w-8/12">
            TBC
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            Operator
          </div>
          <div class="order-content-data w-8/12">
            {{ order?.operator?.details?.registered_name }}
          </div>
        </div>
      </div>
      <div class="order-content-col w-4/12">
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-5/12">
            Uplift Time (Local)
          </div>
          <div class="order-content-data w-7/12">
            {{ order?.fuel_order?.fueling_time_utc ? order?.fuel_order?.arrival_time_tbc ?
              order?.fuel_order?.fueling_time_utc + ' (Time TBC)' : toLocalTime(order?.fuel_order?.fueling_time_utc) :
              'TBC' }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-5/12">
            Fuel
          </div>
          <div class="order-content-data w-7/12">
            {{ `${order?.fuel_order?.fuel_category?.name}, ${order?.fuel_order?.fuel_quantity}
            ${order?.fuel_order?.fuel_uom?.description_plural}` }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-5/12">
            Supplier
          </div>
          <div class="order-content-data w-7/12">
            {{ order?.fuel_order?.supplier?.details?.registered_name ?? 'TBC' }}
          </div>
        </div>
      </div>
      <div class="order-content-col w-4/12">
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            Callsign
          </div>
          <div class="order-content-data w-8/12">
            {{ order?.callsign }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            Location
          </div>
          <div class="order-content-data w-8/12">
            {{ order?.location?.full_repr }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            Handler
          </div>
          <div class="order-content-data w-8/12">
            {{ order?.fuel_order?.ground_handler?.details?.registered_name ?? 'TBC' }}
          </div>
        </div>
      </div>
    </div>
    <div class="order-content flex pb-4 px-4 gap-2" v-if="order?.type?.is_gh">
      <div class="order-content-col w-5/12">
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            Callsign
          </div>
          <div class="order-content-data w-8/12">
            {{ order?.callsign }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            ETA (UTC)
          </div>
          <div class="order-content-data w-8/12">
            {{ order?.gh_order?.arrival_time_tbc ?
              order?.gh_order?.arrival_datetime_utc + ' (Time TBC)' : order?.gh_order?.arrival_datetime_utc }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            ETA (Local)
          </div>
          <div class="order-content-data w-8/12">
            {{ order?.gh_order?.arrival_time_tbc ?
              order?.gh_order?.arrival_datetime_utc + ' (Time TBC)' : toLocalTime(order?.gh_order?.arrival_datetime_utc!)
            }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            Location
          </div>
          <div class="order-content-data w-8/12">
            {{ order?.location?.full_repr }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            Operator
          </div>
          <div class="order-content-data w-8/12">
            {{ order?.operator?.details?.registered_name }}
          </div>
        </div>
      </div>
      <div class="order-content-col w-5/12">
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            Aircraft
          </div>
          <div class="order-content-data w-8/12">
            {{ `${order?.aircraft?.registration} - ${order?.aircraft?.type?.manufacturer}
            ${order?.aircraft?.type?.model} (${order?.aircraft?.type?.designator})` }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            ETD (UTC)
          </div>
          <div class="order-content-data w-8/12">
            {{ order?.gh_order?.departure_time_tbc ?
              order?.gh_order?.departure_datetime_utc + ' (Time TBC)' : order?.gh_order?.departure_datetime_utc }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            ETD (Local)
          </div>
          <div class="order-content-data w-8/12">
            {{ order?.gh_order?.departure_time_tbc ?
              order?.gh_order?.departure_datetime_utc + ' (Time TBC)' :
              toLocalTime(order?.gh_order?.departure_datetime_utc!)
            }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            Supplier
          </div>
          <div class="order-content-data w-8/12">
            {{ order?.gh_order?.ground_handler?.details?.registered_name ?? 'TBC' }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">
            S&F Request
          </div>
          <div class="order-content-data w-8/12">
            {{ order?.gh_order?.sf_request?.id! || 'TBC' }}
          </div>
        </div>
      </div>
    </div>
    <ArrowProgress></ArrowProgress>
  </div>
</template>

<script lang="ts" setup>
import { computed, onBeforeMount, ref, type PropType } from 'vue'
import type { BaseValidation } from '@vuelidate/core'
import { useOrderStore } from '@/stores/useOrderStore'
import { Button } from 'shared/components'
import type { IOrder, IOrderStatus } from '@/types/order/order.types'
import OrderReferences from '@/services/order/order-references'
import { useFetch } from '@/composables/useFetch'
import { toLocalTime } from '@/helpers/order'
import ArrowProgress from '../forms/ArrowProgress.vue'
import Avatar from '../forms/Avatar.vue'
import ButtonPopover from '../forms/ButtonPopover.vue'
import SendViaEmailModal from '../modals/SendViaEmailModal.vue'
import { useOrderReferenceStore } from '@/stores/useOrderReferenceStore'

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

const orderStore = useOrderStore();
const currentStep = computed(() => orderStore.currentStep);

const orderReferenceStore = useOrderReferenceStore();
const quoteButton = computed(() => orderReferenceStore.quoteButton);
const proceedButton = computed(() => orderReferenceStore.proceedButton);

const isModalOpened = ref(false);

const {
  loading: isLoadingOrderStatuses,
  data: orderStatuses,
  callFetch: fetchOrderStatuses
} = useFetch<IOrderStatus[], () => Promise<IOrderStatus[]>>(async () => {
  return await OrderReferences.fetchOrderStatuses()
})

function getColor() {
  const status = orderStatuses?.value?.find((el: IOrderStatus) => el.name === props.order?.status?.status_name);
  return status?.fill_colour_hex ?? '#fff'
}

function getTextColor() {
  const status = orderStatuses?.value?.find((el: IOrderStatus) => el.name === props.order?.status?.status_name);
  return status?.text_colour_hex ?? '#000'
}

const redirectToLinkedOrder = (uri: string) => {
  console.log(uri)
}

onBeforeMount(async () => {
  await Promise.allSettled([fetchOrderStatuses()]);
})

</script>

<style lang="scss">
.order-header {
  .button {
    background-color: rgba(240, 242, 252, 1) !important;
    color: rgba(81, 93, 138, 1) !important;
    @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-2 px-4 rounded-xl #{!important};

    &-green {
      background-color: rgba(11, 161, 125, 1) !important;
      color: rgba(255, 255, 255, 1) !important;

      img {
        filter: brightness(0) saturate(100%) invert(100%) sepia(100%) saturate(0%) hue-rotate(251deg) brightness(102%) contrast(103%);
      }
    }

    &:disabled {
      background-color: rgba(139, 148, 178, 0.12) !important;
      color: rgb(139, 148, 178) !important;
    }
  }

  .cancel-button {
    background-color: rgba(254, 98, 98, 0.12) !important;
    color: rgba(254, 98, 98, 1) !important;

    img {
      filter: brightness(0) saturate(100%) invert(71%) sepia(81%) saturate(4491%) hue-rotate(321deg) brightness(100%) contrast(108%);
    }
  }

  .send-via-email-popup {
    .el {
      color: rgba(21, 28, 53, 1);
      font-size: 16px;
      font-weight: 500;

      &-red {
        color: rgba(254, 98, 98, 1);
      }
    }
  }

  .status {
    font-size: 12px;
  }

  .order-name {
    font-size: 22px;
    font-weight: bold;
  }

  .order-linked {
    border: 1px solid rgba(223, 226, 236, 1);
    border-radius: 6px;

    &-text {
      font-size: 12px;
      font-weight: 500;
      color: rgba(82, 90, 122, 1);
    }

    img {
      width: 12px !important;
      height: 12px !important;
    }
  }

  .order-company {
    color: rgba(60, 67, 93, 1);
    font-size: 15px;
    font-weight: 400;
  }

  .order-content-header {
    font-size: 14px;
    color: rgba(82, 90, 122, 1);
  }

  .order-content-data {
    font-size: 16px;
    color: rgba(21, 28, 53, 1);
    font-weight: 500;
  }
}
</style>