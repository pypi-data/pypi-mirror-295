<template>
  <div v-if="isOpen" class="modal-mask">
    <div class="modal-wrapper">
      <div class="modal-container" ref="target">
        <div class="modal-body">
          <OrderForm add-default-classes>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">Send Client Quote via Email</div>
                <button @click.stop="emit('modal-close')"> <img width="12" height="12"
                    src="../../assets/icons/cross.svg" alt="delete" class="close"></button>
              </div>
            </template>
            <template #content>
              <ScrollBar>
                <div class="form-body-wrapper">
                  <SelectField label-text="Recepients" label="display" v-model="selectedOptions"
                    :options="organisationPeople ?? []" :multiple="true"></SelectField>
                  <Label label-text="From" :required="false"></Label>
                  <div class="mb-4">john.doe@aml.global</div>
                  <InputField class="w-full" v-model="formModel.jobs!.job_title" :is-validation-dirty="v$?.form?.$dirty"
                    :errors="v$?.form?.jobs?.job_title?.$errors" label-text="Subject"
                    placeholder="Please enter subject" />
                  <TextareaField class="w-full" v-model="formModel.jobs!.job_title"
                    :is-validation-dirty="v$?.form?.$dirty" :errors="v$?.form?.jobs?.job_title?.$errors"
                    label-text="Body Text" placeholder="Please enter body text" />
                </div>
              </ScrollBar>
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
import { ref, watch } from "vue";
import { onClickOutside } from '@vueuse/core'
import OrderForm from '@/components/forms/OrderForm.vue'
import { usePersonFormStore } from "@/stores/usePersonFormStore";
import { personRules } from "@/utils/rulesForForms";
import useVuelidate from "@vuelidate/core";
import InputField from "../forms/fields/InputField.vue";
import { storeToRefs } from "pinia";
import { useFetch } from "shared/composables";
import OrderReferences from "@/services/order/order-references";
import { notify } from "@/helpers/toast";
import Label from "../forms/Label.vue";
import TextareaField from "../forms/fields/TextareaField.vue";
import type { IPerson } from "@/types/order/order-reference.types";
import SelectField from "../forms/fields/SelectField.vue";
import ScrollBar from "../forms/ScrollBar.vue";

const props = defineProps({
  isOpen: Boolean,
  organisationId: {
    type: Number
  }
});

const emit = defineEmits(["modal-close", "modal-submit"]);

const selectedOptions = ref([]);

const target = ref(null);

const personFormStore = usePersonFormStore();

const { formModel } = storeToRefs(personFormStore);

const validationModel = ref({ form: formModel });

let v$ = ref(useVuelidate(personRules(), validationModel));

// onClickOutside(target, () => emit('modal-close'))

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
  loading: isLoadingOrganisationPeople,
  data: organisationPeople,
  callFetch: fetchOrganisationPeople
} = useFetch<IPerson[], (id: number) => Promise<IPerson[]>>(async (id: number) => {
  const data = await OrderReferences.fetchOrganisationPeople(id as number)
  return data
})

watch(() => props.organisationId, (value: any) => {
  fetchOrganisationPeople(value)
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
  max-height: 600px;
}

.close {
  filter: brightness(0) saturate(100%) invert(80%) sepia(5%) saturate(2103%) hue-rotate(191deg) brightness(74%) contrast(83%);
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