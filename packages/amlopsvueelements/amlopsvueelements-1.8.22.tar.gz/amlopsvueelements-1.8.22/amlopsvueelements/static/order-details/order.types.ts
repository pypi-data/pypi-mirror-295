import type { IAirport } from '@/types/order/airport.types'
import type { IAircraft } from './aircraft.types'
import type { ITypeReference } from '../general.types'

export interface IOrderStatus {
  id: string,
  name: string,
  status_name: string,
  fill_colour_hex: string,
  text_colour_hex: string
}

export interface IGetOrderStatus {
  id: number,
  status_name: string,
  status_code: string,
  is_active: boolean,
  achieved_at: string
}

export interface IOrderType {
  id: number,
  name: string,
  is_fuel: boolean,
  is_gh: boolean
}

export interface ILinkedOrder {
  id: number,
  aml_order_number: string,
  uri: string,
}

export interface IProgress {
  order: IStatus,
  pricing: IStatus,
  invoicing?: IStatus,
  fulfilment: IStatus,
}

export interface IStatus {
  status: string
}

export interface ICode {
  code: string,
  name: string
}

export interface IClientDetails {
  registered_name: string,
  trading_name: string | null,
  type: ITypeReference,
}

export interface IClient {
  id: number,
  tiny_repr: string,
  short_repr: string,
  full_repr: string,
  details: IClientDetails
}

export interface IOperatorDetails {
  contact_email: string,
  contact_phone: string | null,
}

export interface IOperator {
  id: number,
  details: IClientDetails,
  operator_details: IOperatorDetails
}

export interface IUser {
  id: number,
  details: IUserDetails,
  initials: string,
  is_staff: boolean,
}

export interface IUserDetails {
  contact_email: string,
  contact_phone: string | null,
  title: ITypeReference,
  first_name: string,
  middle_name: string | null,
  last_name: string,
  full_name: string,
}

export interface IFuelUom {
  id: number,
  description: string,
  description_plural: string,
  code: string,
}

export interface IFuelOrder {
  id?: number,
  is_open_release: boolean,
  arrival_datetime_utc: string,
  arrival_datetime_is_local: boolean,
  arrival_time_tbc: boolean,
  departure_datetime_utc: string,
  departure_datetime_is_local: boolean,
  departure_time_tbc: boolean,
  fuel_category: ITypeReference,
  fuel_type: ITypeReference | null,
  fuel_quantity: string,
  fuel_uom: IFuelUom,
  fueling_time_utc?: string | null,
  fueling_on: "A" | "D",
  post_pre_minutes: number,
  supplier?: IOperator | null,
  ipa?: IOperator | null,
  ground_handler?: IOperator | null,
  approved_at?: string | null,
  approved_by?: string | null,
  updated_at?: string | null,
  updated_by?: IUser | null,
  created_at?: string,
  created_by?: IUser,
}

export interface IGroundHandler {
  id: number,
  details: IGroundHandlerDetails,
  handler_details: IHandlerDetails,
}

export interface IGroundHandlerDetails {
  registered_name: string,
  trading_name: string | null
}

export interface IHandlerDetails {
  contact_phone: string | null,
  contact_email: string,
  ops_phone: string | null,
  ops_email: string | null,
  ops_frequency: string | null,
  has_pax_lounge: boolean | null,
  has_crew_room: boolean | null,
  has_vip_lounge: boolean | null,
}

export interface IGhOrder {
  id?: number,
  mission_type: ITypeReference,
  arrival_datetime_utc: string,
  arrival_datetime_is_local: boolean,
  arrival_time_tbc: boolean,
  departure_datetime_utc: string,
  departure_datetime_is_local: boolean,
  departure_time_tbc: boolean,
  ground_handler: IGroundHandler,
  sf_request?: any | null,
  updated_at?: string | null,
  updated_by?: IUser | null,
  created_at?: string,
  created_by?: IUser,
}

export interface IOrderNote {
  id: number,
  content: string,
  is_active: boolean,
  created_at: string,
  created_by: IUser,
}

export interface IOrderBase {
  id?: number,
  aml_order_number?: string,
  type: IOrderType,
  status: IGetOrderStatus,
  client: IClient,
  progress?: IProgress,
  primary_client_contact?: any,
  location: IAirport,
  operator: IOperator,
  aircraft: IAircraft,
  homebase: IAirport,
  aircraft_type: any,
  is_any_aircraft: boolean,
  aircraft_sub_allowed: boolean,
  callsign: string,
  flight_type: ICode,
  is_private: boolean,
  destination: IAirport,
  destination_int_dom: ICode,
  linked_order?: ILinkedOrder,
  original_order?: ILinkedOrder,
  assigned_aml_person?: IUser,
  pricing_calculation_record: { id: number } | null,
  updated_at?: string | null,
  updated_by?: IUser | null,
  created_at?: string,
  created_by?: IUser,
}

export interface IOrderWithFuel extends IOrderBase {
  fuel_order: IFuelOrder,
  gh_order: null,
}

export interface IOrderWithGh extends IOrderBase {
  fuel_order: null,
  gh_order: IGhOrder,
}

export type IOrder = IOrderWithFuel | IOrderWithGh;

export type IMappedFuel = {
  is_open_release: boolean;
  fuel_category: number;
  fuel_type?: any;
  fuel_quantity: number;
  fuel_uom: number;
  arrival_datetime: string;
  arrival_datetime_is_local?: boolean;
  arrival_time_tbc?: boolean;
  departure_datetime: string;
  departure_datetime_is_local?: boolean;
  departure_time_tbc?: boolean;
  fueling_on?: "A" | "D";
  post_pre_minutes?: number;
}

export type IMappedGh = {
  mission_type: number;
  arrival_datetime: string;
  arrival_datetime_is_local?: boolean;
  arrival_time_tbc?: boolean;
  departure_datetime: string;
  departure_datetime_is_local?: boolean;
  departure_time_tbc?: boolean;
  ground_handler: number;
}

export type IMappedOrder = {
  status: string;
  type: number;
  client: number;
  location: number;
  operator: number;
  aircraft: number;
  aircraft_type?: number;
  is_any_aircraft: boolean;
  aircraft_sub_allowed: boolean;
  callsign: string;
  destination?: number;
  destination_int_dom?: string;
  primary_client_contact: number;
  fuel_order?: IMappedFuel;
  gh_order?: IMappedGh;
}