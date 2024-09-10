<template>
  <div class="w-full h-full flex flex-col gap-2">
    <div class="w-full h-full flex gap-2">
      <div class="order-step bg-white w-6/12 border border-transparent rounded-md">
        <div class="order-step-header flex justify-between py-4 px-3">
          <div class="order-step-header-name">Supplier Order</div>
        </div>
        <div class="order-step-content compliance-status w-full flex p-3 gap-2">
          <div class="order-step-content-el-name flex items-center">Status</div>
          <div class="order-step-content-el-value py-1 px-3">Approval required</div>
        </div>
      </div>
      <div class="order-step bg-white w-6/12 border border-transparent rounded-md">
        <div class="order-step-header flex justify-between py-4 px-3">
          <div class="order-step-header-name">Client Order</div>
        </div>
        <div class="order-step-content compliance-status w-full flex p-3 gap-2">
          <div class="order-step-content-el-name flex items-center">Fuel Release</div>
          <div class="order-step-content-el-value py-1 px-3">Sent to Client</div>
        </div>
      </div>
    </div>
    <div class="order-step bg-white w-full border border-transparent rounded-md">
      <div class="order-step-header flex justify-between py-4 px-3">
        <div class="order-step-header-name">Client Documents</div>
      </div>
      <div class="order-step-content w-full flex p-3 gap-2">

      </div>
    </div>
    <div class="order-step bg-white w-full border border-transparent rounded-md">
      <div class="order-step-header flex justify-between py-4 px-3">
        <div class="order-step-header-name">Flight Tracking</div>
      </div>
      <div class="order-step-content w-full flex p-3 gap-2">

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Button } from 'shared/components';
import { computed, ref, watch, type PropType, type Ref } from 'vue';
import { useFetch } from 'shared/composables';
import OrderReferences from '@/services/order/order-references';
import type { IOrder } from '@/types/order/order.types';
import Loading from '../forms/Loading.vue';

const props = defineProps({
  isLoading: {
    type: Boolean as PropType<boolean>,
    default: false
  },
  order: {
    type: Object as PropType<IOrder>,
    default: null
  }
})


const isLoadingOrder = ref(false);

const {
  data: orderStep,
  callFetch: fetchOrder,
} = useFetch<any, (order: any) => Promise<any>>(async (order: any) => {
  // const data = await OrderReferences.fetchSupplierFuelDetails(supplierId, detailsId)
  // console.log(data);
  isLoadingOrder.value = false;
  return []
  // return data;
})


watch(() => props.order, (order: IOrder) => {
  fetchOrder(order);
})

</script>

<style lang="scss">
.order-step {
  .button {
    background-color: rgba(81, 93, 138, 1) !important;
    color: white !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-2 px-4 rounded-xl #{!important};
  }

  .el-border {
    border-right: 1px solid rgb(223, 226, 236);

    &-light {
      border-right: 1px solid rgba(239, 241, 246, 1)
    }
  }

  .el-border-left {
    border-left: 1px solid rgb(223, 226, 236);

    &-light {
      border-right: 1px solid rgba(239, 241, 246, 1)
    }
  }


  &-header {
    color: rgba(21, 28, 53, 1);
    font-size: 18px;
    font-weight: 600;
  }

  &-content {

    &.compliance-status {
      border-top: 1px solid rgba(239, 241, 246, 1);
    }

    &-el {
      &-name {
        color: rgba(82, 90, 122, 1);
        font-size: 13px;
        font-weight: 500;
        min-width: 100px;
      }

      &-value {
        background-color: rgba(11, 161, 125, 1);
        color: rgb(255, 255, 255);
        border-radius: 6px;
        border: 1px solid transparent;
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;
      }
    }

    &-data-wrap {
      border-bottom: 1px solid rgba(239, 241, 246, 1);
      background-color: rgba(255, 255, 255, 1);
    }

    &-header-wrap {
      background-color: rgb(246, 248, 252);
    }

    &-header-big-wrap {
      background-color: rgba(246, 248, 252, 1);
    }

    &-divider {
      text-transform: capitalize;
      background-color: rgba(246, 248, 252, 1);
      color: rgba(82, 90, 122, 1);
      font-size: 12px;
      font-weight: 500;
    }


    &-col {
      &-header {
        color: rgba(82, 90, 122, 1);
        font-size: 11px;
        font-weight: 500;
        background-color: rgb(246, 248, 252);
      }

      &-data {
        color: rgba(133, 141, 173, 1);
        font-size: 13px;
        font-weight: 400;
        background-color: rgba(256, 256, 256, 1);

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 13px;
          font-weight: 500;
        }

        &-value {
          color: rgba(21, 28, 53, 1);
          font-size: 14px;
          font-weight: 500;
        }
      }
    }

    &-destination-el {
      &-name {
        color: rgba(39, 44, 63, 1);
        font-size: 13px;
        font-weight: 500;
      }

      border-bottom: 1px solid rgba(239, 241, 246, 1);
    }

    &-activity {

      &:nth-of-type(2) {
        background-color: rgba(246, 248, 252, 1);
        ;
      }

      &:first-of-type {
        .order-step-info-side {
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

      .order-step-info {
        position: relative;

        &-date {
          color: rgba(39, 44, 63, 1);
          font-weight: 600;
          font-size: 14px;
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


      .order-step-data {
        color: rgba(39, 44, 63, 1);
        font-weight: 400;
        font-size: 15px;
      }
    }
  }

  .roi {
    border-top: 1px solid rgba(239, 241, 246, 1);

    &-inputs-wrap:first-of-type {
      border-right: 1px solid rgba(239, 241, 246, 1);
    }

    &-results {
      background-color: rgba(246, 248, 252, 1);

      &-wrap {
        background-color: rgba(246, 248, 252, 1);

        &:first-of-type {
          border-right: 1px solid rgba(223, 226, 236, 1)
        }
      }

      &-label {
        color: rgba(82, 90, 122, 1);
        font-size: 16px;
        font-weight: 500;
      }

      &-value {
        color: rgba(39, 44, 63, 1);
        font-size: 16px;
        font-weight: 600;

        &-green {
          color: rgba(255, 255, 255, 1);
          background-color: rgba(11, 161, 125, 1);
          border-radius: 6px;
          padding: 6px 12px;
        }
      }
    }

    &-input {
      flex-direction: row;
      margin-bottom: 0 !important;
    }

    &-label {
      color: rgba(82, 90, 122, 1);
      font-size: 11px;
      font-weight: 500;
    }
  }

  .compliance-credit {
    &-confirmed {
      &-value {
        border-left: 4px solid rgba(98, 132, 254, 1);
        color: rgba(21, 28, 53, 1);
        font-size: 18px;
        font-weight: 600;

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }
      }

      &-graph {
        height: 40px;
        width: 100%;
        background-color: rgba(98, 132, 254, 1);
        border-radius: 4px 0 0 4px;
      }
    }

    &-open {
      &-value {
        border-left: 4px solid rgba(243, 173, 43, 1);
        color: rgba(21, 28, 53, 1);
        font-size: 18px;
        font-weight: 600;

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }
      }

      &-graph {
        height: 40px;
        width: 100%;
        background-color: rgba(243, 173, 43, 1);
      }
    }

    &-maximum {
      &-value {
        border-left: 4px dashed rgba(243, 173, 43, 1);
        color: rgba(21, 28, 53, 1);
        font-size: 18px;
        font-weight: 600;

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }
      }

      &-graph {
        height: 40px;
        width: 100%;
        background: repeating-linear-gradient(120deg,
            rgba(243, 173, 43, 1),
            rgba(243, 173, 43, 1) 1px,
            rgb(223, 243, 231) 0,
            rgb(223, 243, 231) 12px);
      }
    }

    &-remaining {
      &-value {
        border-left: 4px solid rgb(223, 243, 231);
        color: rgba(21, 28, 53, 1);
        font-size: 18px;
        font-weight: 600;

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }
      }

      &-graph {
        height: 40px;
        width: 100%;
        background-color: rgb(223, 243, 231);
      }
    }

    &-overuse {
      &-value {
        border-left: 4px solid rgba(254, 98, 98, 0.12);
        color: rgba(254, 98, 98, 1);
        font-size: 18px;
        font-weight: 600;

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }
      }

      &-graph {
        height: 40px;
        width: 100%;
        background-color: rgba(254, 98, 98, 0.12);
        border-radius: 0 4px 4px 0;
      }
    }
  }
}
</style>