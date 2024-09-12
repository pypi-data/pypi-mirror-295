<template>
  <div v-if="isOpen" class="modal-mask">
    <div class="modal-wrapper">
      <div class="modal-container" ref="target">
        <div class="modal-header flex justify-between px-6 py-5">Supplier Fuel Pricing Details
          <img width="12" height="12" src="../../assets/icons/cross.svg" alt="delete" class="close cursor-pointer"
            @click="emit('modal-close')">
        </div>
        <ScrollBar class="my-0">
          <div class="modal-body">
            <div class="modal-body-header py-4 px-6 flex gap-4">
              <div class="modal-body-header-col w-6/12 flex flex-col gap-2">
                <div class="modal-body-header-el flex gap-2">
                  <div class="modal-body-header-el-name w-6/12">Location</div>
                  <div class="modal-body-header-el-data w-6/12">{{ supplyFuel?.scenario?.airport?.full_repr ?? '--' }}
                  </div>
                </div>
                <div class="modal-body-header-el flex gap-2">
                  <div class="modal-body-header-el-name w-6/12">Into-Plane Agent</div>
                  <div class="modal-body-header-el-data w-6/12">{{ supplyFuel?.results[resultIndex]?.ipa?.full_repr ??
                    '--' }}
                  </div>
                </div>
                <div class="modal-body-header-el flex gap-2">
                  <div class="modal-body-header-el-name w-6/12">Pricing Type</div>
                  <div class="modal-body-header-el-data w-6/12">{{
                    supplyFuel?.scenario?.pricing_unit_usd_usg?.description
                    ?? '--' }}</div>
                </div>
                <div class="modal-body-header-el flex gap-2">
                  <div class="modal-body-header-el-name w-6/12">Handler-Specific Pricing</div>
                  <div class="modal-body-header-el-data w-6/12">{{ supplyFuel?.scenario?.handler_specific_pricing ?
                    'Yes' :
                    'No' }}</div>
                </div>
                <div class="modal-body-header-el flex gap-2">
                  <div class="modal-body-header-el-name w-6/12">Apron-Specific Pricing</div>
                  <div class="modal-body-header-el-data w-6/12">{{ supplyFuel?.scenario?.apron_client_pricing ? 'Yes' :
                    'No' }}</div>
                </div>
              </div>
              <div class="modal-body-header-col w-6/12 flex flex-col gap-2">
                <div class="modal-body-header-el flex gap-2">
                  <div class="modal-body-header-el-name w-6/12">Supplier</div>
                  <div class="modal-body-header-el-data w-6/12">{{ supplyFuel?.results[resultIndex]?.supplier?.full_repr
                    ?? '--' }}</div>
                </div>
                <div class="modal-body-header-el flex gap-2">
                  <div class="modal-body-header-el-name w-6/12">Intermediate Supplier</div>
                  <div class="modal-body-header-el-data w-6/12">{{ supplyFuel?.scenario?.intermediate_supplier ?
                    supplyFuel?.scenario?.intermediate_supplier?.full_repr :
                    'No' }}</div>
                </div>
                <div class="modal-body-header-el flex gap-2">
                  <div class="modal-body-header-el-name w-6/12">Delivery Method</div>
                  <div class="modal-body-header-el-data w-6/12">{{ supplyFuel?.scenario?.delivery_method ?
                    supplyFuel?.scenario?.delivery_method.name :
                    'TBC' }}</div>
                </div>
                <div class="modal-body-header-el flex gap-2">
                  <div class="modal-body-header-el-name w-6/12">Client-Specific Pricing</div>
                  <div class="modal-body-header-el-data w-6/12">{{ supplyFuel?.scenario?.client_specific_pricing ? 'Yes'
                    :
                    'No' }}</div>
                </div>
                <div class="modal-body-header-el flex gap-2">
                  <div class="modal-body-header-el-name w-6/12">Terminal-Specific Pricing</div>
                  <div class="modal-body-header-el-data w-6/12">{{ supplyFuel?.scenario?.terminal_specific_pricing ?
                    'Yes' :
                    'No' }}</div>
                </div>
              </div>
            </div>
            <div class="modal-body-content-wrap flex">
              <div class="modal-body-content flex flex-col p-3 gap-2">
                <div class="modal-body-content-block" v-if="supplyFuel?.results[resultIndex]?.issues.length > 0">
                  <div class="modal-body-content-block-header issues p-3">
                    <img width="20" height="20" src="../../assets/icons/alert.svg" alt="warn" class="warn">
                    {{ supplyFuel?.results[resultIndex]?.issues.length }} Issues Detected
                  </div>
                  <div class="modal-body-content-block-body px-3 py-4 pl-6 gap-3 flex flex-col">
                    <div class="issue-html" v-for="issue in supplyFuel?.results[resultIndex]?.issues" v-html="issue">
                    </div>
                  </div>
                </div>
                <div class="modal-body-content-block">
                  <div class="modal-body-content-block-header p-3">
                    Fuel Pricing
                  </div>
                  <div class="modal-body-content-block-body flex px-3 py-4">
                    <div class="modal-body-content-block-body-name w-4/12">{{ supplyFuelDetails?.fuel_price?.fuel?.name
                      }}
                    </div>
                    <div class="modal-body-content-block-body-desc w-6/12">
                      {{ supplyFuelDetails?.fuel_price?.original_pricing_unit?.description }}
                    </div>
                    <div class="modal-body-content-block-body-value w-2/12">{{ supplyFuelDetails?.fuel_price?.amount }}
                      {{ supplyFuelDetails?.currency?.code }}</div>
                  </div>
                </div>
                <div class="modal-body-content-block">
                  <div class="modal-body-content-block-header p-3">
                    Fees
                  </div>
                  <div
                    class="results modal-body-content-block-body flex px-3 py-6 flex justify-center border border-transparent rounded"
                    v-if="supplyFuelDetails && (Object.keys(supplyFuelDetails?.fees?.list).length === 0 || !supplyFuelDetails.hasOwnProperty('fees'))">
                    <div class="modal-body-content-block-body-name flex flex-col items-center">No fees calculated for
                      this scenario</div>
                  </div>
                  <div class="modal-body-content-block-body flex px-3 py-4" v-else
                    v-for="(fee, key) in supplyFuelDetails?.fees?.list" :key="key">
                    <div class="modal-body-content-block-body-name w-4/12">
                      {{ isNaN(parseInt(key as any)) ? key : 'Custom Fee' }} <div
                        class="modal-body-content-block-body-note hover-wrap contents flex items-center">
                        <img width="12" height="12" src="../../assets/icons/info-circle.svg" alt="warn" class="warn">
                        <div class="modal-body-tooltip">
                          <div v-for="note in fee.notes" v-html="'● ' + note"></div>
                        </div>
                      </div>
                    </div>
                    <div class="modal-body-content-block-body-desc w-6/12">
                    </div>
                    <div class="modal-body-content-block-body-value w-2/12">{{ fee?.amount }} {{
                      supplyFuelDetails?.currency?.code }}</div>
                  </div>
                </div>
                <div class="modal-body-content-block">
                  <div class="modal-body-content-block-header p-3">
                    Taxes
                  </div>
                  <div
                    class="results modal-body-content-block-body flex px-3 py-6 flex justify-center border border-transparent rounded"
                    v-if="supplyFuelDetails && (Object.keys(supplyFuelDetails?.taxes?.list).length === 0 || !supplyFuelDetails.hasOwnProperty('taxes'))">
                    <div class="modal-body-content-block-body-name flex flex-col items-center">No taxes calculated for
                      this scenario</div>
                  </div>
                  <div class="modal-body-content-block-body flex flex-col" v-else>
                    <div class="flex w-full">
                      <div class="modal-body-content-block-body-header w-6/12 text-center">
                        <div class="el-border modal-body-content-block-body-header-el my-2">
                          Official Taxes
                        </div>
                      </div>
                      <div class="modal-body-content-block-body-header w-6/12 text-center">
                        <div class="modal-body-content-block-body-header-el my-2">Supplier-Defined Taxes </div>
                      </div>
                    </div>
                    <div class="flex w-full" v-for="(tax, key) in supplyFuelDetails?.taxes?.list" :key="key">
                      <div class="el-border w-6/12 issues flex px-3 py-4 items-center">
                        <div class="modal-body-content-block-body-name w-8/12">{{ key }}</div>
                        <div class="modal-body-content-block-body-value w-4/12">{{ tax?.official?.amount }}
                          {{ supplyFuelDetails?.currency?.code }}</div>
                      </div>
                      <div class="w-6/12 issues flex px-3 py-4 items-center">
                        <div class="modal-body-content-block-body-name w-8/12">{{ key }}</div>
                        <div class="modal-body-content-block-body-value w-4/12">{{ tax?.supplier?.amount }}
                          {{ supplyFuelDetails?.currency?.code }}</div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="modal-body-content-block">
                  <div class="modal-body-content-block-header p-3">
                    Total cost
                  </div>
                  <div class="modal-body-content-block-body flex flex-col">
                    <div class="flex w-full">
                      <div class="modal-body-content-block-body-header w-6/12 pl-3">
                        <div class="el-border modal-body-content-block-body-header-el my-2">
                          With Official Taxes
                        </div>
                      </div>
                      <div class="modal-body-content-block-body-header w-6/12 pl-3 ">
                        <div class="modal-body-content-block-body-header-el my-2">With Supplier-Defined Taxes</div>
                      </div>
                    </div>
                    <div class="flex w-full">
                      <div class="el-border w-6/12 flex px-3 py-4 items-center">
                        <div class="modal-body-content-block-body-name w-8/12">Fuel</div>
                        <div class="modal-body-content-block-body-value w-4/12">{{
                          supplyFuelDetails?.fuel_price?.amount  }} {{ supplyFuelDetails?.currency?.code }}</div>
                      </div>
                      <div class="w-6/12 flex px-3 py-4 items-center">
                        <div class="modal-body-content-block-body-name w-8/12">Fuel</div>
                        <div class="modal-body-content-block-body-value w-4/12">{{
                          supplyFuelDetails?.fuel_price?.amount }} {{ supplyFuelDetails?.currency?.code }}</div>
                      </div>
                    </div>
                    <div class="flex w-full">
                      <div class="el-border w-6/12 flex px-3 py-4 items-center">
                        <div class="modal-body-content-block-body-name w-8/12">Fees</div>
                        <div class="modal-body-content-block-body-value w-4/12">{{
                          supplyFuelDetails?.fees?.total }} {{ supplyFuelDetails?.currency?.code }}</div>
                      </div>
                      <div class="w-6/12 flex px-3 py-4 items-center">
                        <div class="modal-body-content-block-body-name w-8/12">Fees</div>
                        <div class="modal-body-content-block-body-value w-4/12">{{
                          supplyFuelDetails?.fees?.client_total }} {{ supplyFuelDetails?.currency?.code }}</div>
                      </div>
                    </div>
                    <div class="flex w-full">
                      <div class="el-border w-6/12 flex px-3 py-4 items-center">
                        <div class="modal-body-content-block-body-name w-8/12">Taxes</div>
                        <div class="modal-body-content-block-body-value w-4/12">{{
                          supplyFuelDetails?.taxes?.official_total }} {{ supplyFuelDetails?.currency?.code }}</div>
                      </div>
                      <div class="w-6/12 flex px-3 py-4 items-center">
                        <div class="modal-body-content-block-body-name w-8/12">Taxes</div>
                        <div class="modal-body-content-block-body-value w-4/12">{{
                          supplyFuelDetails?.taxes?.supplier_total }} {{ supplyFuelDetails?.currency?.code }}</div>
                      </div>
                    </div>
                    <div class="flex w-full">
                      <div class="el-border results w-6/12 flex px-3 py-4 items-center">
                        <div class="modal-body-content-block-body-name w-8/12">Total Uplift Cost</div>
                        <div class="modal-body-content-block-body-value w-4/12">{{
                          supplyFuelDetails?.total_official_taxes }} {{ supplyFuelDetails?.currency?.code }}</div>
                      </div>
                      <div class="w-6/12 results flex px-3 py-4 items-center">
                        <div class="modal-body-content-block-body-name w-8/12">Total Uplift Cost</div>
                        <div class="modal-body-content-block-body-value w-4/12">{{
                          supplyFuelDetails?.total }} {{ supplyFuelDetails?.currency?.code }}</div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="modal-body-content-block">
                  <div class="modal-body-content-block-header p-3">
                    Exchange Rates
                  </div>
                  <div class="modal-body-content-block-body flex px-3 py-4">
                    <div class="modal-body-content-block-body-name w-8/12 flex flex-col">Open Exchange Rates
                      <div class="modal-body-content-block-body-sub">Valid at {{
                        toRateTime(supplyFuel?.scenario?.used_currency_rates?.[Object.keys(supplyFuel?.scenario?.used_currency_rates)[0]]?.timestamp
                          + '000') }}</div>
                    </div>
                    <div class="modal-body-content-block-body-value w-4/12 flex items-center justify-end">
                      {{
                        supplyFuel?.scenario?.used_currency_rates?.[Object.keys(supplyFuel?.scenario?.used_currency_rates)[0]]?.rate
                      }}
                      {{ JSON.parse(Object.keys(supplyFuel?.scenario?.used_currency_rates)[0])[0] }}
                      -> {{ JSON.parse(Object.keys(supplyFuel?.scenario?.used_currency_rates)[0])[1] }}</div>
                  </div>
                </div>
                <div class="modal-body-content-block">
                  <div class="modal-body-content-block-header p-3">
                    Fuel-related NOTAMs
                  </div>
                  <div
                    class="results modal-body-content-block-body flex flex-col items-center justify-center px-3 py-6">
                    <div class="modal-body-content-block-body-name flex flex-col items-center">No fuel-related NOTAMs
                      found</div>
                    <div class="modal-body-content-block-body-sub">The FAA NOTAMs API was last chacked for this location
                      at {{ supplyFuelDetails?.notams_last_check }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </ScrollBar>
        <div class="modal-footer px-6 py-5 flex justify-end">
          <div class="modal-footer-el flex justify-between w-6/12">
            <div class="modal-footer-el-name">
              Total Uplift Cost
            </div>
            <div class="modal-footer-el-value">
              {{ supplyFuelDetails?.total }} {{
                supplyFuelDetails?.currency?.code }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from "vue";
import { onClickOutside } from '@vueuse/core'
import ScrollBar from "../forms/ScrollBar.vue";
import { toRateTime } from "@/helpers/order";
import { useFetch } from "shared/composables";
import OrderReferences from "@/services/order/order-references";

const props = defineProps({
  isOpen: Boolean,
  supplyFuel: {
    type: Object,
    default: null
  },
  resultIndex: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(["modal-close", "modal-submit"]);

const target = ref(null);

const isLoadingSupplierFuelDetails = ref(true);

onClickOutside(target, () => emit('modal-close'))

const {
  data: supplyFuelDetails,
  callFetch: fetchSupplierFuelDetails,
} = useFetch<any, (supplierId: number, detailsId: number) => Promise<any>>(async (supplierId: number, detailsId: number) => {
  const data = await OrderReferences.fetchSupplierFuelDetails(supplierId, detailsId)
  isLoadingSupplierFuelDetails.value = false;
  return data;
})


watch([() => props.resultIndex, () => props.supplyFuel], ([a, b]) => {
  if (a !== null && b !== null) {
    fetchSupplierFuelDetails(b?.id, b?.results[a].key)
  }
})


</script>

<style scoped lang="scss">
.modal-mask {
  position: fixed;
  z-index: 1000;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
}

.modal-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.modal-container {
  width: 700px;
  margin: auto;
  background-color: #fff;
  border-radius: .5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
}

.form-body-wrapper {
  max-height: 820px;
  overflow-y: auto;
}

.close {
  filter: brightness(0) saturate(100%) invert(80%) sepia(5%) saturate(2103%) hue-rotate(191deg) brightness(74%) contrast(83%);
}

.modal-header {
  color: rgba(39, 44, 63, 1);
  font-size: 18px;
  font-weight: 600;
}

.modal-body {
  max-height: 70vh;

  &-header {
    border-top: 1px solid rgba(223, 226, 236, 1);
    border-bottom: 1px solid rgba(223, 226, 236, 1);

    &-el {
      align-items: baseline;

      &-name {
        font-size: 13px;
        color: rgba(82, 90, 122, 1);
        font-weight: 500;
      }

      &-data {
        font-size: 14px;
        color: rgba(21, 28, 53, 1);
        font-weight: 500;
      }
    }
  }

  .issues {
    background-color: rgba(255, 161, 0, 0.08);
  }

  .results {
    background-color: rgb(246, 248, 252);
  }

  .el-border {
    border-right: 1px solid rgb(223, 226, 236);
  }

  &-tooltip {
    display: none;
    position: absolute;
    background-color: rgb(81, 93, 138);
    color: rgb(255, 255, 255);
    font-size: 12px;
    font-weight: 400;
    z-index: 10;
    padding: 0.5rem;
    border-radius: 0.5rem;
    bottom: 1.5rem;
    left: 0;
    min-width: 30vw;

    &::before {
      content: "";
      position: absolute;
      width: 10px;
      height: 10px;
      background-color: rgb(81, 93, 138);
      transform: rotate(45deg);
      left: 4.9rem;
      bottom: -5px;
    }
  }


  &-content {
    background-color: rgba(239, 241, 246, 1);

    &-wrap {
      background-color: rgba(239, 241, 246, 1);
    }

    &-block {
      border: 1px solid rgba(223, 226, 236, 1);
      border-radius: 6px;
      background-color: rgb(255, 255, 255);

      &-header {
        color: rgba(21, 28, 53, 1);
        font-size: 15px;
        font-weight: 600;
        border-bottom: 1px solid rgba(223, 226, 236, 1);
      }

      &-body {
        color: rgba(39, 44, 63, 1);
        font-size: 14px;
        font-weight: 500;

        &-header {
          background-color: rgba(246, 248, 252, 1);
          color: rgba(82, 90, 122, 1);
          font-size: 11px;
          font-weight: 500;
        }

        &-name {
          color: rgba(39, 44, 63, 1);
          font-size: 13px;
          font-weight: 500;
          position: relative;

          .hover-wrap {
            &:hover {
              .modal-body-tooltip {
                display: block;
              }
            }
          }
        }

        &-sub {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }

        &-desc {
          color: rgba(39, 44, 63, 1);
          font-size: 13px;
          font-weight: 400;
        }

        &-value {
          color: rgba(39, 44, 63, 1);
          font-size: 13px;
          font-weight: 600;
          text-align: end;
        }

        .issue-html {
          position: relative;

          &::before {
            content: '';
            position: absolute;
            height: 19px;
            width: 4px;
            background-color: rgba(254, 161, 22, 1);
            border-radius: 2px;
            left: -0.8rem;
          }
        }
      }
    }
  }
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  border-top-width: 1px;
  border-color: rgb(75 85 99 / 0.25);
  background-color: rgba(246, 248, 252, 1);
  border-radius: 0 0 0.5rem 0.5rem;

  &-el {
    &-name {
      color: rgba(39, 44, 63, 1);
      font-size: 13px;
      font-weight: 500;
    }

    &-value {
      color: rgba(39, 44, 63, 1);
      font-size: 13px;
      font-weight: 600;
    }
  }

  .modal-button {
    display: flex;
    flex-shrink: 0;
    background-color: rgb(81 93 138) !important;
    padding: 0.5rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    color: rgb(255 255 255) !important;
    border-radius: 0.5rem !important;

    &.cancel {
      background-color: rgba(240, 242, 252, 1) !important;
      color: rgb(81 93 138) !important;
    }
  }
}
</style>