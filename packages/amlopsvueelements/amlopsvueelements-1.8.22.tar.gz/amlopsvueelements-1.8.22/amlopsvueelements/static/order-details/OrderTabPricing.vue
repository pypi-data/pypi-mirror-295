<template>
  <div class="w-full h-full flex flex-col gap-2">
    <SupplyFuelDetailsModal :is-open="isModalOpened" ref="clientInput" @modal-close="closeModal"
      :supply-fuel="supplyFuel" :result-index="selectedModalSupplier!" name="supply-modal" />
    <div class="pricing-step bg-white w-full border border-transparent rounded-md">
      <div class="pricing-step-header flex justify-between py-4 px-3">
        <div class="pricing-step-header-name">Select Supplier Fuel</div>
      </div>
      <div class="pricing-step-content w-full flex flex-col"
        v-if="supplyFuel?.results?.length > 0 && !isLoadingSupplyFuel && !isLoadingSupplierFuelDetails">
        <div class="pricing-step-content-header-wrap w-full flex items-center">
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-header px-3 py-2">Fuel</div>
          </div>
          <div class="pricing-step-content-col w-2/12">
            <div class="pricing-step-content-col-header px-3 py-2">Supplier</div>
          </div>
          <div class="pricing-step-content-col w-2/12">
            <div class="pricing-step-content-col-header px-3 py-2">IPA</div>
          </div>
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-header px-3 py-2">Delivery</div>
          </div>
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-header px-3 py-2">Apron</div>
          </div>
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-header px-3 py-2">Terminal</div>
          </div>
          <div class="pricing-step-content-col w-2/12">
            <div class="pricing-step-content-col-header px-3 py-2">Total Uplift Cost</div>
          </div>
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-header px-3 py-2">&nbsp;</div>
          </div>
          <div class="pricing-step-content-col w-2/12">
            <div class="pricing-step-content-col-header px-3 py-2">&nbsp;</div>
          </div>
        </div>
        <div class="pricing-step-content-data-wrap w-full flex items-center"
          :class="{ 'selected-supplier': selectedSupplier === index || selectedSupplier === null }"
          v-for="(supplier, index) in supplyFuel?.results" :key="index">
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-data px-3 py-2">{{ supplier.fuel_type.name }}</div>
          </div>
          <div class="pricing-step-content-col w-2/12">
            <div class="pricing-step-content-col-data px-3 py-2">{{ supplier.supplier.full_repr }}</div>
          </div>
          <div class="pricing-step-content-col w-2/12">
            <div class="pricing-step-content-col-data px-3 py-2">{{ supplier.ipa.full_repr }}</div>
          </div>
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-data px-3 py-2">{{ supplier.delivery_method?.name ?? 'All' }}</div>
          </div>
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-data px-3 py-2">{{ supplier.apron?.name ?? 'All' }}</div>
          </div>
          <div class="pricing-step-content-col w-1/12">
            <div class="pricing-step-content-col-data px-3 py-2">{{ supplier.terminal?.name ?? 'All' }}</div>
          </div>
          <div class="pricing-step-content-col w-2/12">
            <div class="pricing-step-content-col-data px-3 py-2">{{ supplier.total_uplift_cost }} {{
              supplier.currency.code }}</div>
          </div>
          <div class="pricing-step-content-col w-1/12 relative">
            <div class="pricing-step-content-col-data px-3 py-2 flex gap-2" v-if="supplier.issues.length > 0">
              <div class="hover-wrap contents">
                <img width="20" height="20" src="../../assets/icons/alert.svg" alt="warn" class="warn">
                <div class="pricing-step-tooltip">
                  <div v-for="issue in supplier.issues" v-html="'● ' + issue"></div>
                </div>
              </div>
              <img width="20" height="20" src="../../assets/icons/eye.svg" alt="details" class="cursor-pointer"
                @click="openModal(index)">
            </div>
          </div>
          <div class="pricing-step-content-col w-2/12">
            <div class="pricing-step-content-col-data px-3 py-2 flex justify-center">
              <Button class="button" v-if="selectedSupplier === null"
                @click="selectSupplier(index, supplier)">Select</Button>
              <div class="selection-tick flex items-center justify-center" @click="selectSupplier(null, supplier)"
                v-else>
                <img width="20" height="20" src="../../assets/icons/check.svg" alt="check">
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="pricing-step-content-none w-full flex py-4 pr-3 pl-10 flex flex-col"
        v-if="supplyFuel?.results?.length === 0 && !isLoadingSupplyFuel">
        <img width="20" height="20" src="../../assets/icons/alert.svg" alt="warn" class="warn">
        <div class="pricing-step-content-none-header">There are no supplier fuel supply options available at this
          location</div>
        <div class="pricing-step-content-none-desc">Please update the database with at least one supply option for this
          location and then revisit this page to proceed with the order.</div>
      </div>
      <div class="pricing-step-content w-full flex py-8 px-3 flex flex-col" v-if="isLoadingSupplyFuel">
        <Loading />
      </div>
    </div>
    <div class="pricing-step bg-white w-full border border-transparent rounded-md">
      <div class="pricing-step-header flex justify-between py-4 px-3">
        <div class="pricing-step-header-name">Fuel Pricing Details</div>
        <div class="loading-wrap">
          <Loading v-if="isLoadingPricing" />
        </div>
      </div>
      <div class="pricing-step-content" v-if="orderPricing && order && orderPricing.supplier_id">
        <div class="pricing-step-content-header-big-wrap flex">
          <div class="pricing-step-content-header-big flex w-4/12">
          </div>
          <div class="pricing-step-content-header-big flex w-4/12 p-1">
            <div class="pricing-step-content-header-big-el flex w-full py-1 justify-center rounded">Supplier Pricing
            </div>
          </div>
          <div class="pricing-step-content-header-big flex w-4/12 p-1">
            <div class="pricing-step-content-header-big-el flex w-full py-1 justify-center rounded">Client Pricing</div>
          </div>
        </div>
        <div class="pricing-step-content-header-sub flex">
          <div class="pricing-step-content-header-sub-wrap flex w-4/12 py-2 pl-3 gap-2">
            <div class="pricing-step-content-header-sub-el flex w-8/12 justify-start">Item</div>
            <div class="pricing-step-content-header-sub-el flex w-4/12 justify-start el-border">Quantity</div>
          </div>
          <div class="pricing-step-content-header-sub-wrap flex w-4/12 py-2 pl-3">
            <div class="pricing-step-content-header-sub-el flex w-full justify-start">Unit Price</div>
            <div class="pricing-step-content-header-sub-el flex w-full justify-start el-border">Total Cost</div>
          </div>
          <div class="pricing-step-content-header-sub-wrap flex w-4/12 p-2 pl-3">
            <div class="pricing-step-content-header-sub-el flex w-full justify-start">Unit Price</div>
            <div class="pricing-step-content-header-sub-el flex w-full justify-start">Total Cost</div>
          </div>
        </div>
        <div class="pricing-step-content-element flex">
          <div class="pricing-step-content-element-wrap flex w-4/12 py-2 pl-3 el-border-light gap-2">
            <div class="pricing-step-content-element-el-name flex justify-start items-center w-8/12">{{
              order?.fuel_order?.fuel_category?.name }}</div>
            <div class="pricing-step-content-element-el flex justify-start items-center w-4/12">{{
              order?.fuel_order?.fuel_quantity }} ({{ order?.fuel_order?.fuel_uom?.description_plural }})</div>
          </div>
          <div class="pricing-step-content-element-wrap flex w-4/12 py-2 pl-3 el-border-light">
            <div class="pricing-step-content-element-el flex w-full justify-start items-center">
              {{ parseFloat(orderPricing?.fuel_pricing?.supplier?.unit_price_amount) }}
              {{ orderPricing?.fuel_pricing?.supplier?.unit_price_pricing_unit?.description_short }}</div>
            <div class="pricing-step-content-element-el flex w-full justify-start items-center">
              {{ orderPricing?.fuel_pricing?.supplier?.amount_total }}
              {{ orderPricing?.fuel_pricing?.supplier?.amount_currency?.code }}</div>
          </div>
          <div class="pricing-step-content-element-wrap flex w-4/12 py-2 pl-3">
            <div class="pricing-step-content-element-el flex w-full justify-start items-center">
              <div class="input-wrap flex pr-3">
                <InputField :model-value="orderPricing.fuel_pricing?.client?.unit_price_amount" class="w-6/12 mb-0"
                  :is-white="true" :is-half="true" placeholder=" " @update:model-value="onPriceChange" />
                <SelectField class="w-6/12 mb-0" :is-white="true" :is-half="true" placeholder=" "
                  :options="[orderPricing.fuel_pricing?.client?.unit_price_pricing_unit]" label="description_short"
                  :model-value="orderPricing.fuel_pricing?.client?.unit_price_pricing_unit" />
              </div>
            </div>
            <div class="pricing-step-content-element-el flex w-full justify-start items-center pr-3">
              <InputField :model-value="orderPricing.fuel_pricing?.client?.amount_total" class="roi-input w-full"
                :is-white="true" placeholder=" " :disabled="true">
                <template #suffix>{{ orderPricing.fuel_pricing?.client?.unit_price_pricing_unit?.currency?.code
                  }}</template>
              </InputField>
            </div>
          </div>
        </div>
        <div class="pricing-step-content-divider flex w-full py-2 px-3"
          v-if="orderPricing && orderPricing.fees?.length > 0">
          Fees
        </div>
        <div class="pricing-step-content-element flex" v-for="(fee, key) in orderPricing.fees" :key="key"
          v-if="orderPricing && orderPricing.fees.length > 0">
          <div class="pricing-step-content-element-wrap flex w-4/12 py-2 pl-3 el-border-light gap-2">
            <div class="pricing-step-content-element-el-name flex justify-start items-center w-8/12">{{
              fee.supplier?.suppliers_fuel_fees_rates_row?.supplier_fuel_fee?.local_name ?? 'Fee' }}</div>
            <div class="pricing-step-content-element-el flex justify-start items-center w-4/12">x {{
              parseInt(fee.supplier?.quantity_value) }}</div>
          </div>
          <div class="pricing-step-content-element-wrap flex w-4/12 py-2 pl-3 el-border-light">
            <div class="pricing-step-content-element-el flex w-full justify-start items-center">
              {{ parseFloat(fee.supplier?.unit_price_amount) }}
              {{ fee.supplier?.unit_price_pricing_unit?.description_short }}
            </div>
            <div class="pricing-step-content-element-el flex w-full justify-start items-center">{{
              parseFloat(fee.supplier?.amount_total) }} {{ fee.supplier?.amount_currency?.code }}</div>
          </div>
          <div class="pricing-step-content-element-wrap flex w-4/12 py-2 pl-3">
            <div class="pricing-step-content-element-el flex w-full justify-start items-center">
              <div class="input-wrap flex pr-3">
                <InputField :model-value="fee.client?.unit_price_amount" class="w-6/12 mb-0" :is-white="true"
                  :is-half="true" placeholder=" " @update:model-value="onFeeChange($event, key)" />
                <SelectField class="w-6/12 mb-0" :is-white="true" :is-half="true" placeholder=" "
                  :options="[fee.client?.unit_price_pricing_unit]" label="description_short"
                  :model-value="fee.client?.unit_price_pricing_unit" />
              </div>
            </div>
            <div class="pricing-step-content-element-el flex w-full justify-start items-center pr-3">
              <InputField class="roi-input w-full" :model-value="fee?.client?.amount_total" :is-white="true"
                placeholder=" " :disabled="true">
                <template #suffix>{{ fee?.client?.amount_currency?.code }}</template>
              </InputField>
            </div>
          </div>
        </div>
        <div class="pricing-step-content-divider flex w-full py-2 px-3"
          v-if="orderPricing && orderPricing.taxes.length > 0">
          Taxes
        </div>
        <div class="pricing-step-content-element flex" v-for="(tax, key) in orderPricing.taxes" :key="key"
          v-if="orderPricing && orderPricing.taxes.length > 0">
          <div class="pricing-step-content-element-wrap flex w-4/12 py-2 pl-3 el-border-light gap-2">
            <div class="pricing-step-content-element-el-name flex justify-start items-center w-8/12">{{
              tax.supplier?.tax?.category?.name ?? 'Tax' }}
            </div>
            <div class="pricing-step-content-element-el flex justify-start items-center w-4/12">x 1</div>
          </div>
          <div class="pricing-step-content-element-wrap flex w-4/12 py-2 pl-3 el-border-light">
            <div class="pricing-step-content-element-el flex w-full justify-start items-center">{{
              tax?.supplier?.tax_percentage }} %</div>
            <div class="pricing-step-content-element-el flex w-full justify-start items-center">
              {{ tax?.supplier?.tax_amount_total }}
              {{ tax?.supplier?.tax_amount_currency?.code }}</div>
          </div>
          <div class="pricing-step-content-element-wrap flex w-4/12 py-2 pl-3">
            <div class="pricing-step-content-element-el flex w-full justify-start items-center">{{
              tax?.client?.tax_percentage }} %</div>
            <div class="pricing-step-content-element-el flex w-full justify-start items-center">
              {{ tax?.client?.tax_amount_total }}
              {{ tax?.client?.tax_amount_currency?.code }}</div>
          </div>
        </div>
        <div class="pricing-step-content-results flex">
          <div class="pricing-step-content-results-wrap flex w-4/12 py-2 pl-3">
          </div>
          <div class="pricing-step-content-results-wrap flex w-4/12 py-2">
            <div
              class="pricing-step-content-results-el-name flex items-center w-full p-1 pl-3 justify-start items-center">
              Total Buy
              Price</div>
            <div class="pricing-step-content-results-el-value flex w-full p-1 justify-start items-center">{{
              orderPricing?.pricing_summary?.supplier_total }} {{
                orderPricing?.fuel_pricing?.supplier?.amount_currency?.code }}
            </div>
          </div>
          <div class="pricing-step-content-results-wrap flex w-4/12 py-2">
            <div
              class="pricing-step-content-results-el-name flex items-center w-full p-1 pl-3 justify-start items-center">
              Total Sell
              Price</div>
            <div class="pricing-step-content-results-el-value flex w-full p-1 justify-start items-center">{{
              orderPricing?.pricing_summary?.client_total }} {{
                orderPricing?.fuel_pricing?.client?.amount_currency?.code }}
            </div>
          </div>
        </div>
        <div class="pricing-step-content-margin flex p-3">
          <div class="pricing-step-content-margin-name w-6/12 flex items-center">Margin</div>
          <div class="pricing-step-content-margin-value w-6/12 flex items-center pl-2">{{
            orderPricing?.pricing_summary?.margin_amount }} {{
              orderPricing?.fuel_pricing?.client?.amount_currency?.code }} ({{
              orderPricing?.pricing_summary?.margin_percentage }}%)</div>
        </div>
      </div>
      <div class="pricing-step-content-missing flex items-center justify-center py-5" v-else>
        <Loading v-if="isLoadingSupplierFuelDetails" />
        <span v-else>Please select a Fuel Supply option</span>
      </div>
    </div>
    <div class="pricing-step bg-white w-full border border-transparent rounded-md">
      <div class="pricing-step-header flex justify-between py-4 px-3">
        <div class="pricing-step-header-name">ROI Calculation</div>
        <div class="loading-wrap">
          <Loading v-if="isLoadingRoi" />
        </div>
      </div>
      <div class="pricing-step-content roi flex flex-col" v-if="orderPricing && order && orderPricing.supplier_id">
        <div class="roi-inputs flex">
          <div class="roi-inputs-wrap w-6/12 flex items-center p-3">
            <div class="roi-label w-6/12">Supplier Credit Terms</div>
            <InputField class="roi-input w-6/12" :is-white="true" placeholder=" "
              :model-value="orderRoiDays.supplier_days" @update:model-value="onRoiChange($event, false)">
              <template #suffix>days</template>
            </InputField>
          </div>
          <div class="roi-inputs-wrap w-6/12 flex items-center p-3">
            <div class="roi-label w-6/12">Client Credit Terms</div>
            <InputField class="roi-input w-6/12" :is-white="true" placeholder=" "
              :model-value="orderRoiDays.client_days" @update:model-value="onRoiChange($event, true)">
              <template #suffix>days</template>
            </InputField>
          </div>
        </div>
        <div class="roi-results flex py-3">
          <div class="roi-results-wrap w-6/12 flex items-center px-3">
            <div class="roi-results-label w-6/12">Order Value</div>
            <div class="roi-results-value w-6/12">{{ orderRoi?.calculated_roi_value }} {{
              orderPricing?.fuel_pricing?.client?.unit_price_pricing_unit?.currency?.code }}</div>
          </div>
          <div class="roi-results-wrap w-6/12 flex items-center px-3">
            <div class="roi-results-label w-6/12 ">ROI</div>
            <div class="roi-results-value-green">{{ orderRoi?.calculated_roi }} %</div>
          </div>
        </div>
      </div>
      <div class="pricing-step-content-missing flex items-center justify-center py-5" v-else>
        <Loading v-if="isLoadingSupplierFuelDetails" />
        <span v-else>Please select a Fuel Supply option</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Button } from 'shared/components';
import { computed, ref, watch, type PropType, type Ref } from 'vue';
import { useDebounceFn } from "@vueuse/core"
import InputField from '../forms/fields/InputField.vue';
import { useFetch } from 'shared/composables';
import OrderReferences from '@/services/order/order-references';
import type { IOrder } from '@/types/order/order.types';
import SupplyFuelDetailsModal from '../modals/SupplyFuelDetailsModal.vue';
import SelectField from '../forms/fields/SelectField.vue';
import Loading from '../forms/Loading.vue';
import orderReferences from '@/services/order/order-references';
import { useOrderReferenceStore } from '@/stores/useOrderReferenceStore';

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

const orderReferenceStore = useOrderReferenceStore();

const orderPricing: Ref<any> = ref(null);
const orderRoi: Ref<any> = ref({
  calculated_roi_value: 0,
  calculated_roi: 0,
  roi_parameters: {
    traffic_light: 5,
    background_fill_hex: "3AB050",
    text_colour_hex: "FFFFFF"
  }
});
const orderRoiDays: Ref<any> = ref({
  supplier_days: 0,
  client_days: 0
});
const selectedSupplier: Ref<null | number> = ref(null);

const selectSupplier = async (id: number | null, supplier: any) => {
  if (id !== null) {
    const data = await selectFuelSupplier(props.order.id!, {
      id: supplyFuel.value.id!,
      key: parseInt(supplier.key!)
    })
    if (data) {
      selectedSupplier.value = id;
    }
  } else {
    supplyFuelDetails.value = null;
  }
}

const isModalOpened = ref(false);
const selectedModalSupplier: Ref<null | number> = ref(null);

const openModal = (id: number) => {
  selectedModalSupplier.value = id;
  isModalOpened.value = true;
}

const closeModal = () => {
  selectedModalSupplier.value = null;
  isModalOpened.value = false;
}

const isLoadingSupplyFuel = ref(true);
const isLoadingSupplierFuelDetails = ref(true);
const isLoadingRoi = ref(false);
const isLoadingPricing = ref(false);

const onPriceChange = useDebounceFn((value: any) => {
  orderPricing.value.fuel_pricing.client.unit_price_amount = value;
  updateOrderPricing(props.order.id!)
}, 1000)

const onFeeChange = useDebounceFn((value: any, key: any) => {
  orderPricing.value.fees[key].client.unit_price_amount = value;
  updateOrderPricing(props.order.id!)
}, 1000)

const onRoiChange = useDebounceFn((value: any, isClient) => {
  if (isClient) {
    orderRoiDays.value.client_days = value;
  } else {
    orderRoiDays.value.supplier_days = value;
  }
  updateOrderRoi(props.order.id!);
}, 200)

const {
  data: supplyFuel,
  callFetch: fetchSupplierFuel,
} = useFetch<any, (order: IOrder) => Promise<any>>(async (order: IOrder) => {
  const data = await OrderReferences.fetchSupplierFuel(order)
  console.log(data)
  isLoadingSupplyFuel.value = false;
  return data;
})

const {
  data: supplyFuelDetails,
  callFetch: fetchSupplierFuelDetails,
} = useFetch<any, (supplierId: number, detailsId: number) => Promise<any>>(async (supplierId: number, detailsId: number) => {
  const data = await OrderReferences.fetchSupplierFuelDetails(supplierId, detailsId)
  isLoadingSupplierFuelDetails.value = false;
  return data;
})

const {
  data: { },
  callFetch: selectFuelSupplier,
} = useFetch<any, (orderId: number, payload: { id: number, key: number }) => Promise<any>>(async (orderId: number, payload: { id: number, key: number }) => {
  const data = await OrderReferences.selectFuelSupplier(orderId, payload);
  await fetchOrderPricing(props.order.id!);
  await orderReferenceStore.initiateReferenceStore(props.order.id!);
})

const {
  data: { },
  callFetch: fetchOrderPricing,
} = useFetch<any, (orderId: number) => Promise<any>>(async (orderId: number) => {
  const data = await OrderReferences.fetchOrderPricing(orderId);
  if (typeof data === 'object') {
    orderPricing.value = data;
    const supplierIndex = supplyFuel.value.results?.findIndex((supplier: any) => supplier.supplier.pk === data.supplier_id);
    selectedSupplier.value = supplierIndex === -1 ? null : supplierIndex;
    orderRoiDays.value.client_days = data.terms_days?.client_terms_days;
    orderRoiDays.value.supplier_days = data.terms_days?.supplier_terms_days;
    updateOrderRoi(orderId);
    isLoadingSupplierFuelDetails.value = false;
    return data;
  } else {
    isLoadingSupplierFuelDetails.value = false;
    return null
  }
})

const {
  data: { },
  callFetch: updateOrderPricing,
} = useFetch<any, (orderId: number) => Promise<any>>(async (orderId: number) => {
  isLoadingPricing.value = true;
  let payload: any = {
    unit_price: {
      id: orderPricing.value.fuel_pricing?.client?.id,
      name: 'Fuel Price',
      new_value: orderPricing.value.fuel_pricing?.client?.unit_price_amount
    },
    fees: [],
    terms: {
      supplier: parseInt(orderRoiDays.value.supplier_days),
      client: parseInt(orderRoiDays.value.client_days),
    }
  }

  orderPricing.value.fees.forEach((fee: any) => {
    payload.fees.push({
      id: fee.client?.id,
      name: fee.supplier?.suppliers_fuel_fees_rates_row?.supplier_fuel_fee?.fuel_fee_category?.name,
      new_value: parseFloat(fee.client?.unit_price_amount),
    })
  })

  const data = await OrderReferences.updateOrderPricing(orderId, payload);
  console.log(data)
  if (typeof data === 'object') {
    orderPricing.value = data;
  }
  isLoadingPricing.value = false;
  return data;
})

const {
  data: { },
  callFetch: updateOrderRoi,
} = useFetch<any, (orderId: number) => Promise<any>>(async (orderId: number) => {
  isLoadingRoi.value = true;
  let payload: any = {
    unit_price: parseFloat(orderPricing?.value?.fuel_pricing?.supplier?.unit_price_amount),
    margin_amount: parseFloat(orderPricing?.value?.pricing_summary?.margin_amount),
    margin_percentage: orderPricing?.value?.pricing_summary?.margin_percentage,
    quantity: parseInt(orderPricing?.value?.fuel_pricing?.supplier?.quantity_value),
    quantity_is_litres: true,
    supplier_days: parseInt(orderRoiDays.value.supplier_days),
    client_days: parseInt(orderRoiDays.value.client_days),
  }
  const data = await OrderReferences.updateOrderROI(orderId, payload);
  if (typeof data === 'object') {
    orderRoi.value = data;
  } else {
    orderRoi.value = {
      calculated_roi_value: 0,
      calculated_roi: 0,
      roi_parameters: {
        traffic_light: 5,
        background_fill_hex: "3AB050",
        text_colour_hex: "FFFFFF"
      }
    };
  }
  isLoadingRoi.value = false;
  return data;
})

watch(() => props.order, async (order: IOrder) => {
  await fetchSupplierFuel(order);
  await fetchOrderPricing(order?.id!);
})

</script>

<style lang="scss">
.pricing-step {
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
    top: 2.5rem;
    right: 0;
    min-width: 30vw;

    &::before {
      content: "";
      position: absolute;
      width: 10px;
      height: 10px;
      background-color: rgb(81, 93, 138);
      transform: rotate(45deg);
      right: 1.9rem;
      top: -5px;
    }
  }

  &-header {
    color: rgba(21, 28, 53, 1);
    font-size: 18px;
    font-weight: 600;
  }

  &-content {
    &-data-wrap {
      border-bottom: 1px solid rgba(239, 241, 246, 1);
      background-color: rgba(246, 248, 252, 0.5);

      &.selected-supplier {
        background-color: rgba(255, 255, 255, 1);

        .pricing-step-content-col-data {
          color: rgba(39, 44, 63, 1);
          background-color: rgba(255, 255, 255, 1);

          .warn {
            filter: none;
          }

          .selection-tick {
            display: flex;
            border-radius: 12px;
            background-color: rgba(11, 161, 125, 0.15);
            height: 40px;
            width: 40px;
          }
        }
      }
    }

    &-header-wrap {
      background-color: rgb(246, 248, 252);
    }

    &-header-big-wrap {
      background-color: rgba(246, 248, 252, 1);
    }

    &-header-big {
      &-el {
        background-color: rgba(223, 226, 236, 0.5);
        color: rgba(39, 44, 63, 1);
        font-size: 12px;
        font-weight: 500;
      }
    }

    &-header-sub {
      background-color: rgba(246, 248, 252, 1);

      &-el {
        color: rgba(82, 90, 122, 1);
        font-size: 11px;
        font-weight: 500;
      }
    }

    &-element {
      &-wrap {
        border-bottom: 1px solid rgba(246, 248, 252, 1);
      }

      &-el {
        color: rgba(39, 44, 63, 1);
        font-size: 13px;
        font-weight: 400;

        &-name {
          color: rgba(39, 44, 63, 1);
          font-size: 13px;
          font-weight: 500;
        }
      }
    }

    &-results {
      background-color: rgba(246, 248, 252, 1);

      &-el {
        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 11px;
          font-weight: 500;
          border-left: 1px solid rgb(223, 226, 236);
        }

        &-value {
          color: rgba(39, 44, 63, 1);
          font-size: 13px;
          font-weight: 600;
        }
      }
    }

    &-divider {
      text-transform: capitalize;
      background-color: rgba(246, 248, 252, 1);
      color: rgba(82, 90, 122, 1);
      font-size: 12px;
      font-weight: 500;
    }

    &-margin {
      &-name {
        color: rgba(39, 44, 63, 1);
        font-size: 13px;
        font-weight: 500;
      }

      &-value {
        color: rgba(11, 161, 125, 1);
        font-size: 16px;
        font-weight: 600;
      }
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
        background-color: rgba(246, 248, 252, 0.5);

        .warn {
          filter: brightness(0) saturate(100%) invert(89%) sepia(7%) saturate(740%) hue-rotate(193deg) brightness(88%) contrast(92%);
        }

        .selection-tick {
          display: none;
        }

        .files-button {
          border: 1px solid rgba(223, 226, 236, 1);
          border-radius: 6px;
        }

        .horizontal {
          transform: rotate(90deg);
        }

        .hover-wrap {
          &:hover {
            .pricing-step-tooltip {
              display: block;
            }
          }
        }
      }
    }

    &-none {
      position: relative;
      background-color: rgba(255, 161, 0, 0.08);

      &-header {
        color: rgba(21, 28, 53, 1);
        font-size: 14px;
        font-weight: 600;
      }

      &-desc {
        color: rgba(21, 28, 53, 1);
        font-size: 12px;
        font-weight: 400;
      }

      .warn {
        position: absolute;
        left: 0.75rem;
      }
    }

    &-missing {
      background-color: rgba(246, 248, 252, 1);

      span {
        color: rgba(82, 90, 122, 1);
        font-size: 11px;
        font-weight: 500;
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
}
</style>