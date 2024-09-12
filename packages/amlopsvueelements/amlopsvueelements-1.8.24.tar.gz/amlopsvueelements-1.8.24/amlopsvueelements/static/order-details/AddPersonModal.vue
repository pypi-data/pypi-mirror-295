<template>
  <div v-if="isOpen" class="modal-mask">
    <div class="modal-wrapper">
      <div class="modal-container" ref="target">
        <div class="modal-body">
          <OrderForm add-default-classes>
            <template #header>
              <h2 class="text-[1.25rem] font-medium text-grey-1000">Add New Person</h2>
              <button @click.stop="emit('modal-close')">X</button>
            </template>
            <template #content>
              <div class="form-body-wrapper">
                <InputField id="focusField" class="w-full" v-model="formModel.details!.first_name"
                  :is-validation-dirty="v$?.form?.$dirty" :errors="v$?.form?.details?.first_name?.$errors"
                  label-text="First Name" placeholder="Please enter first name" />
                <InputField class="w-full" v-model="formModel.details!.middle_name"
                  :is-validation-dirty="v$?.form?.$dirty" :errors="v$?.form?.details.middle_name?.$errors"
                  label-text="Middle Name" placeholder="Please enter middle name" />
                <InputField class="w-full" v-model="formModel.details!.last_name"
                  :is-validation-dirty="v$?.form?.$dirty" :errors="v$?.form?.details?.last_name?.$errors"
                  label-text="Last Name" placeholder="Please enter last name" />
                <InputField class="w-full" v-model="formModel.details!.contact_email"
                  :is-validation-dirty="v$?.form?.$dirty" :errors="v$?.form?.details?.contact_email?.$errors"
                  label-text="Direct Email" placeholder="Please enter email" />
                <SelectField class="w-full" v-model="formModel.details!.title" label-text="Title"
                  placeholder="Please select title" :errors="v$?.form?.details?.title?.$errors" :append-to-body="false"
                  :is-validation-dirty="v$?.form?.$dirty" label="name" :options="titles" :loading="false" />
                <SelectField class="w-full" v-model="formModel.jobs!.role" label-text="Job Role"
                  placeholder="Please select role" :errors="v$?.form?.jobs?.role?.$errors" :append-to-body="false"
                  :is-validation-dirty="v$?.form?.$dirty" label="name" :options="roles" :loading="false" />
                <InputField class="w-full" v-model="formModel.jobs!.job_title" :is-validation-dirty="v$?.form?.$dirty"
                  :errors="v$?.form?.jobs?.job_title?.$errors" label-text="Job Title"
                  placeholder="Please enter job title" />
              </div>

            </template>
          </OrderForm>
        </div>
        <div class="modal-footer">
          <button class="modal-button cancel" @click.stop="emit('modal-close')">Cancel</button>
          <button class="modal-button submit" @click.stop="onValidate()">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { onClickOutside } from '@vueuse/core'
import OrderForm from '@/components/forms/OrderForm.vue'
import { usePersonFormStore } from "@/stores/usePersonFormStore";
import { personRules } from "@/utils/rulesForForms";
import useVuelidate from "@vuelidate/core";
import InputField from "../forms/fields/InputField.vue";
import { storeToRefs } from "pinia";
import { onBeforeMount } from "vue";
import type { ITypeReference } from "@/types/general.types";
import { useFetch } from "shared/composables";
import orderReferences from "@/services/order/order-references";
import SelectField from "../forms/fields/SelectField.vue";
import { notify } from "@/helpers/toast";

const props = defineProps({
  isOpen: Boolean,
});

const emit = defineEmits(["modal-close", "modal-submit"]);

const target = ref(null);

const personFormStore = usePersonFormStore();

const { formModel } = storeToRefs(personFormStore);

const validationModel = ref({ form: formModel });

let v$ = ref(useVuelidate(personRules(), validationModel));

onClickOutside(target, () => emit('modal-close'))

const onValidate = async () => {
  const isValid = await v$?.value?.$validate()
  if (!isValid) {
    return notify('Error while submitting, form is not valid!', 'error')
  } else {
    emit('modal-submit');
    emit('modal-close');
  }
}

const {
  loading: isLoadingPersonRoles,
  data: roles,
  callFetch: fetchPersonRoles
} = useFetch<ITypeReference[], () => Promise<ITypeReference[]>>(async () => {
  return await orderReferences.fetchPersonRoles()
})

const {
  loading: isLoadingPersonTitles,
  data: titles,
  callFetch: fetchPersonTitles
} = useFetch<ITypeReference[], () => Promise<ITypeReference[]>>(async () => {
  return await orderReferences.fetchPersonTitles()
})

onBeforeMount(async () => {
  await Promise.allSettled([
    fetchPersonRoles(),
    fetchPersonTitles(),
  ])
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
  width: 520px;
  margin: auto;
  background-color: #fff;
  border-radius: .5rem;
  padding-top: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
}

.form-body-wrapper {
  max-height: 820px;
  overflow-y: auto;
}

.modal-footer {
  padding: 0.5rem 1rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  border-top-width: 1px;
  border-color: rgb(75 85 99 / 0.25);

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