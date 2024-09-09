<template>
  <div class="w-full flex justify-center">
    <div class="w-full">
      <NewOrder class="mb-3" :is-loading="isLoading" :validation-info="v$?.form" />
      <ErrorBox class="mb-3" v-if="formErrors.length || Object.keys(formErrors)?.length" />
      <div class="pb-[3.75rem] pl-[1.5rem] pr-[1.5rem] m-auto w-full max-w-screen-lg">
        <div class="w-11/12 flex flex-row-reverse items-center justify-between">
          <Button v-if="orderStore.isFirstStep" :class="[$style['ops-page-wrapper__btn']]" :loading="isLoading"
            :disabled="!orderFormStore.validateFirstStep()" @click="orderStore.changeStep()">
            <span>Next step</span>
          </Button>
          <Button v-if="!orderStore.isFirstStep" :class="[$style['ops-page-wrapper__btn']]" :loading="isLoading"
            @click="onValidate">
            <span>Create Order</span>
          </Button>
          <Button v-if="!orderStore.isFirstStep" :class="[$style['ops-page-wrapper__go-back']]"
            @click="orderStore.changeStep()">
            <span>Back</span>
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import NewOrder from '@/components/forms/sections/NewOrder.vue'
import { Button } from 'shared/components'
import { storeToRefs } from 'pinia'
import useVuelidate from '@vuelidate/core'
import { useFetch } from '@/composables/useFetch'
import type { Nullable } from '@/types/generic.types'
import { rules } from '@/utils/rulesForForms'
import { computed, ref, watch } from 'vue'
import { notify } from '@/helpers/toast'
import ErrorBox from '@/components/forms/ErrorBox.vue'
import { useOrderFormStore } from '@/stores/useOrderFormStore'
import { useOrderStore } from '@/stores/useOrderStore'
import type { IOrder } from '@/types/order/order.types'
import order from '@/services/order/order'
import { redirectToURL } from '@/helpers'

const orderFormStore = useOrderFormStore()
const orderStore = useOrderStore()
const { formModel: orderForm, formErrors } = storeToRefs(orderFormStore)
const validationModel = ref({ form: orderForm.value });

let v$ = ref(useVuelidate(rules(), validationModel));

const {
  loading: isCreatingOrder,
  data: createdOrderData,
  callFetch: createOrder
} = useFetch(async (payload: Nullable<IOrder>) => {
  const mappedPayload = orderFormStore.mapForm();
  const res = await order.create(mappedPayload);
  notify('Order created successfully!', 'success');
  redirectToURL(res.data?.id);
})

const isLoading = computed(() => isCreatingOrder?.value)

const orderActions = async () => {
  createOrder(orderForm.value);
}

const onValidate = async () => {
  try {
    const isValid = await v$?.value?.$validate()
    if (!isValid) {
      const value = JSON.parse(JSON.stringify(v$.value));
      const find = value.$errors.find((el: any) => el.$property === 'status');
      if (find) {
        orderStore.changeStep();
      }
      return notify('Error while submitting, form is not valid!', 'error')
    } else {
      await orderActions()
      formErrors.value = []
    }
  } catch (error: any) {
    if (error.response?.data?.errors?.some((err: any) => typeof err === 'string')) {
      return (formErrors.value = error.response?.data?.errors)
    }
  }
}
const goBack = () => {
  window?.history?.go(-1)
}

watch(() => orderForm.value.type, (newVal) => {
  v$ = useVuelidate(rules(), validationModel);
});
</script>

<style lang="scss" module>
.ops {
  &-page-wrapper {
    @apply flex justify-between items-center gap-2 mb-4;

    &__btn {
      @apply flex shrink-0 focus:shadow-none text-white bg-grey-900 mb-0 mt-2 p-2 px-4 #{!important};

      img {
        @apply w-5 h-5 mr-2;
        filter: invert(36%) sepia(14%) saturate(1445%) hue-rotate(190deg) brightness(93%) contrast(84%);
      }

      &:disabled {
        background-color: rgba(81, 93, 138, 0.5) !important
      }
    }

    &__go-back {
      @apply flex shrink-0 focus:shadow-none text-grey-900 bg-grey-75 mb-0 mt-2 p-2 px-4 #{!important};
    }

    &__content {
      @apply pr-0 sm:pr-4 sm:mr-[-1rem] relative;
    }
  }
}
</style>
