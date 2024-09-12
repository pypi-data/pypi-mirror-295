import { defineStore } from 'pinia'
import { computed, reactive, ref, } from 'vue'
import type { Nullable } from '@/types/generic.types'

import { defaultFuelOrderForm, defaultGhOrderForm, orderDefaultFormModel } from '@/constants/order.constants'
import type { IMappedOrder, IOrder } from '@/types/order/order.types'
import { useOrderStore } from './useOrderStore'

export const useOrderFormStore = defineStore('OrderForm', () => {
  const formModel = reactive<Nullable<IOrder>>(orderDefaultFormModel())
  const formErrors = ref([])
  const windowWidth = ref(window.innerWidth)
  const orderStore = useOrderStore();
  const airGroupModel = computed(() => orderStore.airGroupModel);
  const fuelGroupModel = computed(() => orderStore.fuelGroupModel);

  // Assigns updated or fetched mission data to form model
  // watch(
  //   () => order.value,
  //   (newMission) => {
  //     if (!newMission) return
  //     Object.assign(formModel, mapExtendedMission(newMission))
  //   }
  // )


  const updateOrderType = (isFuel: boolean) => {
    if (isFuel) {
      formModel.gh_order = defaultGhOrderForm();
    } else {
      formModel.fuel_order = defaultFuelOrderForm();
    }
  }

  const validateFirstStep = () => {
    return formModel.type && formModel.client && formModel.status && formModel.location && (formModel.aircraft || formModel.aircraft_type || formModel.is_any_aircraft) && formModel.flight_type
    // return formModel.type
  }

  const mapForm = () => {
    let mappedForm: IMappedOrder = {
      status: formModel.status!.id!,
      type: formModel.type!.id!,
      client: formModel.client!.id!,
      location: formModel.location!.id!,
      operator: formModel.operator?.id ?? formModel.client!.id!,
      aircrafts: formModel.aircraft ? airGroupModel.value.map((el: any) => {
        return {
          aircraft_id: el.id
        }
      }) : [],
      fuel_aircrafts: formModel.aircraft ? fuelGroupModel.value.map((el: any, index: number) => {
        return {
          aircraft_id: airGroupModel.value[index].id,
          fuel_quantity: el.fuel_quantity! ?? Number(formModel.fuel_order!.fuel_quantity!),
          fuel_uom: el.fuel_uom!.id! ?? formModel.fuel_order!.fuel_uom!.id!,
        }
      }) : [],
      aircraft_type: formModel.aircraft_type?.id ?? null,
      is_any_aircraft: formModel.is_any_aircraft!,
      aircraft_sub_allowed: formModel.aircraft_sub_allowed!,
      callsign: formModel.callsign!,
      is_private: formModel.is_private!,
      flight_type: formModel.flight_type!.code!,
      primary_client_contact: formModel.primary_client_contact?.id ?? null,
    }

    if (formModel.type?.is_fuel) {
      mappedForm.fuel_order = {
        is_open_release: formModel.fuel_order!.is_open_release!,
        fuel_category: formModel.fuel_order!.fuel_category!.id!,
        fuel_type: formModel.fuel_order!.fuel_type?.id ?? null,
        fuel_uom: airGroupModel.value.length > 1 ? fuelGroupModel.value[0].fuel_uom.id : formModel.fuel_order!.fuel_uom!.id!,
        arrival_datetime: formModel.fuel_order!.arrival_datetime_utc!,
        arrival_datetime_is_local: formModel.fuel_order!.arrival_datetime_is_local!,
        arrival_time_tbc: formModel.fuel_order!.arrival_time_tbc!,
        departure_datetime: formModel.fuel_order!.departure_datetime_utc!,
        departure_datetime_is_local: formModel.fuel_order!.departure_datetime_is_local!,
        departure_time_tbc: formModel.fuel_order!.departure_time_tbc!,
        fueling_on: formModel.fuel_order!.fueling_on!,
        post_pre_minutes: Number(formModel.fuel_order!.post_pre_minutes!)
      };
      delete mappedForm.gh_order;
      if (!formModel.aircraft?.id) {
        mappedForm.fuel_order!['fuel_quantity'] = Number(formModel.fuel_order!.fuel_quantity!);
      }
    } else {
      mappedForm.gh_order = {
        mission_type: formModel.gh_order!.mission_type!.id!,
        arrival_datetime: formModel.gh_order!.arrival_datetime_utc!,
        arrival_datetime_is_local: formModel.gh_order!.arrival_datetime_is_local!,
        arrival_time_tbc: formModel.gh_order!.arrival_time_tbc!,
        departure_datetime: formModel.gh_order!.departure_datetime_utc!,
        departure_datetime_is_local: formModel.gh_order!.departure_datetime_is_local!,
        departure_time_tbc: formModel.gh_order!.departure_time_tbc!,
        ground_handler: formModel.gh_order!.ground_handler!.id!
      };
      delete mappedForm.fuel_order;
    }
    if (formModel.destination) {
      mappedForm.destination = formModel.destination!.id!;
    } else {
      mappedForm.destination_int_dom = formModel.destination_int_dom!.code!;
    }
    return mappedForm
  }

  return { formModel, formErrors, windowWidth, updateOrderType, validateFirstStep, mapForm }
})
