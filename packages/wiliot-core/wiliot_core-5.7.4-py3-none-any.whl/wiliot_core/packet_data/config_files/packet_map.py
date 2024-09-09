#  """
#    Copyright (c) 2016- 2024, Wiliot Ltd. All rights reserved.
#
#    Redistribution and use of the Software in source and binary forms, with or without modification,
#     are permitted provided that the following conditions are met:
#
#       1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#       2. Redistributions in binary form, except as used in conjunction with
#       Wiliot's Pixel in a product or a Software update for such product, must reproduce
#       the above copyright notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
#
#       3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
#       may be used to endorse or promote products or services derived from this Software,
#       without specific prior written permission.
#
#       4. This Software, with or without modification, must only be used in conjunction
#       with Wiliot's Pixel or with Wiliot's cloud service.
#
#       5. If any Software is provided in binary form under this license, you must not
#       do any of the following:
#       (a) modify, adapt, translate, or create a derivative work of the Software; or
#       (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
#       discover the source code or non-literal aspects (such as the underlying structure,
#       sequence, organization, ideas, or algorithms) of the Software.
#
#       6. If you create a derivative work and/or improvement of any Software, you hereby
#       irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
#       royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
#       right and license to reproduce, use, make, have made, import, distribute, sell,
#       offer for sale, create derivative works of, modify, translate, publicly perform
#       and display, and otherwise commercially exploit such derivative works and improvements
#       (as applicable) in conjunction with Wiliot's products and services.
#
#       7. You represent and warrant that you are not a resident of (and will not use the
#       Software in) a country that the U.S. government has embargoed for use of the Software,
#       nor are you named on the U.S. Treasury Department’s list of Specially Designated
#       Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
#       You must not transfer, export, re-export, import, re-import or divert the Software
#       in violation of any export or re-export control laws and regulations (such as the
#       United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
#       and use restrictions, all as then in effect
#
#     THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
#     OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
#     WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
#     QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
#     IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
#     ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#     OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
#     FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
#     (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
#     (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
#     CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
#     (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
#     (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
#  """

import numpy as np
from enum import Enum


class FieldsLength(Enum):
    HEADER = 4
    EXTENDED_HEADER = 4
    ADVA = 12
    ADI = 4
    EN = 2
    TYPE = 2
    DATA_UID = 4
    GROUP_ID = 6
    NONCE = 8
    ENC_UID = 12
    MIC = 12
    ENC_PAYLOAD = 16


class BridgeParams(Enum):
    PACKET_DATA_INFO = 4  # 1E16
    SERVICE_UUID_LENGTH = 4  # AFFD
    BRG_SERVICE_UUID = 'C6FC'


class GWPacketLength(Enum):
    STAT_PARAM_LENGTH = 4
    RSSI_LENGTH = 2
    GW_DATA_LENGTH = STAT_PARAM_LENGTH + RSSI_LENGTH


BITS_IN_CHAR = 4

PACKET_DECRYPT_MASK = 0xc
GROUP_ID_MASK = 0xFFFF00
RAW_GROUP_ID_MASK = 0xFFFFC0

BLE5_SHIFT = FieldsLength.HEADER.value + FieldsLength.EXTENDED_HEADER.value + FieldsLength.ADI.value
ADI_LOCATION = FieldsLength.HEADER.value + FieldsLength.EXTENDED_HEADER.value + FieldsLength.ADVA.value
FLOW_VER_SIZE = 4

PAYLOAD_LENGTH = 16
BLE_PAYLOAD_LENGTH = 62
BLE_DOUBLE_PAYLOAD_LENGTH = 78
WILIOT_EN_TYPE = ['1E16', '2616']
WILIOT_DATA_UID = ['C6FC', 'AFFD']

packet_structure = [{'name': 'header', 'len': FieldsLength.HEADER.value},
                    {'name': 'extended_header', 'len': FieldsLength.EXTENDED_HEADER.value},
                    {'name': 'adv_address', 'len': FieldsLength.ADVA.value},
                    {'name': 'adi', 'len': FieldsLength.ADI.value},
                    {'name': 'en', 'len': FieldsLength.EN.value},
                    {'name': 'type', 'len': FieldsLength.TYPE.value},
                    {'name': 'data_uid', 'len': FieldsLength.DATA_UID.value},
                    {'name': 'raw_group_id', 'len': FieldsLength.GROUP_ID.value},
                    {'name': 'nonce', 'len': FieldsLength.NONCE.value},
                    {'name': 'enc_uid', 'len': FieldsLength.ENC_UID.value},
                    {'name': 'mic', 'len': FieldsLength.MIC.value},
                    {'name': 'enc_payload', 'len': FieldsLength.ENC_PAYLOAD.value}
                    ]
gw_bit_structure = [{'name': 'rssi', 'bit_len': GWPacketLength.RSSI_LENGTH.value * BITS_IN_CHAR},
                    {'name': 'crc_valid', 'bit_len': 1},
                    {'name': 'gw_clock', 'bit_len': GWPacketLength.STAT_PARAM_LENGTH.value * BITS_IN_CHAR - 1},
                    ]
BLE5_ONLY_FIELDS = ['header', 'extended_header', 'adi']

packet_data_dict = {'raw_packet': '',
                    'adv_address': (0, 12),
                    'decrypted_packet_type': (24, 1),
                    'group_id': (20, 6),
                    'raw_group_id': '',
                    'test_mode': 0,
                    'header': '',
                    'extended_header': '',
                    'adi': '',
                    'en': (12, 2),
                    'type': (14, 2),
                    'data_uid': (16, 4),
                    'nonce': (26, 8),
                    'enc_uid': (34, 12),
                    'mic': (46, 12),
                    'enc_payload': (58, 16),
                    'packet_length': None}

gw_result_dict = {'gw_packet': 'gw_packet',
                  'rssi': 'rssi',
                  'stat_param': 'stat_param',
                  'crc_valid': (0, 1),  # bits in stat param
                  'gw_clock': (1, 16),  # bits in stat param
                  'time_from_start': 'time_from_start',
                  'counter_tag': 'counter_tag',
                  'is_valid_tag_packet': 'is_valid_tag_packet',
                  'is_packet_from_bridge': 'is_packet_from_bridge'}

packet_length_types = {
    '4225': {'name': 'LEGACY', 'packet_tag_length': 78, 'bytes_shift': 0, 'length_modifier': None},
    '4729': {'name': 'BLE5-EXT', 'packet_tag_length': 86, 'bytes_shift': BLE5_SHIFT, 'length_modifier': None},
    '4731': {'name': 'BLE5-DBL-EXT', 'packet_tag_length': 102, 'bytes_shift': BLE5_SHIFT,
             'length_modifier': {'enc_payload': (PAYLOAD_LENGTH * 2)}}
}


def parse_packet(packet_data_input, is_full_packet, ignore_crc):
    pixie_result = {}
    gw_result = {}

    # check packet type:
    for full_key in packet_length_types.keys():
        if packet_data_input.startswith(full_key):
            is_full_packet = True

    if is_full_packet is None:
        packet_data_input, expected_length = check_packet_length_with_no_indication(packet_data_input)
        if expected_length is None:
            raise Exception(f'invalid packet length for packet {packet_data_input}, '
                            f'these are the valid tag packet length: {packet_length_types}')
    elif is_full_packet:
        expected_length = packet_length_types[packet_data_input[:FieldsLength.HEADER.value]]
    else:
        packet_data_input = '4225' + packet_data_input
        expected_length = packet_length_types[packet_data_input[:FieldsLength.HEADER.value]]

    # check if packet from bridge
    from_bridge = is_packet_from_bridge(packet_data_input)

    # check if packet length is valid
    received_len = len(packet_data_input)

    if received_len == expected_length['packet_tag_length'] + GWPacketLength.GW_DATA_LENGTH.value:
        pass  # valid length
    elif received_len == expected_length['packet_tag_length']:
        packet_data_input += '0' * GWPacketLength.GW_DATA_LENGTH.value
    else:
        gw_result['is_valid_tag_packet'] = np.array(False)
        raise Exception(f'invalid packet length for packet {packet_data_input}, '
                        f'expected tag packet length: {expected_length["packet_tag_length"]}')

    try:
        # Parse pixie data
        pixie_result.update(parse_pixie(packet_data_input, expected_length, from_bridge))

        # Parse GW
        gw_result.update(parse_gw(packet_data_input, from_bridge, ignore_crc))
        gw_result['is_valid_tag_packet'] = np.array(True)

    except Exception as e:
        print('Packet string cannot be parsed due to {}'.format(e))
        gw_result['is_valid_tag_packet'] = np.array(False)

    return pixie_result, gw_result


def parse_gw(packet_data, is_from_bridge, ignore_crc):
    result = {}
    gw_data = packet_data[-GWPacketLength.GW_DATA_LENGTH.value:]
    try:
        result['gw_packet'] = np.array(gw_data, dtype='<U6')
        result['rssi'] = np.array(int(gw_data[:GWPacketLength.RSSI_LENGTH.value], 16))
        result['stat_param'] = np.array(int(gw_data[GWPacketLength.RSSI_LENGTH.value:
                                                    GWPacketLength.RSSI_LENGTH.value +
                                                    GWPacketLength.STAT_PARAM_LENGTH.value], 16))
        stat_param_bits = format(result['stat_param'].item(), '04b').zfill(
            GWPacketLength.STAT_PARAM_LENGTH.value * BITS_IN_CHAR)
        if ignore_crc:
            result['crc_valid'] = np.array(1)
        else:
            result['crc_valid'] = np.array(int(stat_param_bits[
                                           gw_result_dict['crc_valid'][0]:gw_result_dict['crc_valid'][1]]))
        result['gw_clock'] = np.array(int(stat_param_bits[
                                          gw_result_dict['gw_clock'][0]:gw_result_dict['gw_clock'][1]], 2))
        result['time_from_start'] = np.array(float('nan'))
        result['counter_tag'] = np.array(float('nan'))
        result['is_packet_from_bridge'] = np.array(is_from_bridge)

        return result

    except Exception as e:
        print('Issue parsing GW data: {}'.format(e))
        return


def parse_pixie(packet_data, packet_len_dict, is_from_bridge):
    try:
        result = {'raw_packet': packet_data}
        valid_length = packet_len_dict['packet_tag_length'] + GWPacketLength.GW_DATA_LENGTH.value
        start_index = FieldsLength.HEADER.value if packet_len_dict['name'] == 'LEGACY' else 0

        result['header'] = packet_data[:FieldsLength.HEADER.value]
        result['raw_packet'] = packet_data[start_index:-GWPacketLength.GW_DATA_LENGTH.value]
        result['packet_length'] = valid_length
        result.update(parser(result['raw_packet'], packet_len_dict, is_from_bridge))
        result['decrypted_packet_type'] = (int(result['decrypted_packet_type'], 16) & PACKET_DECRYPT_MASK) >> 2

    except Exception as e:
        raise Exception(f'packet_map: parse_packet: could not parse packet: {packet_data} due to {e}')

    return result


def extract_fields(packet_data, shift=0, length_modifier=None):
    result = {}
    for key, value in packet_data_dict.items():
        if isinstance(value, tuple):
            start, length = value

            if length_modifier and key in length_modifier:
                length = length_modifier[key]

            start_ind = start + shift
            if shift == BLE5_SHIFT and key == 'adv_address':
                start_ind -= FieldsLength.ADI.value

            result[key] = packet_data[start_ind:start_ind + length]
            if key == 'group_id':
                result['raw_group_id'] = \
                    hex(int(result[key], 16) & RAW_GROUP_ID_MASK)[2:].zfill(FieldsLength.GROUP_ID.value).upper()
                result[key] = hex(int(result[key], 16) & GROUP_ID_MASK)[2:].zfill(FieldsLength.GROUP_ID.value).upper()

    return result


def parser(packet_data, len_dict, is_from_bridge):
    result = extract_fields(packet_data, len_dict['bytes_shift'], len_dict['length_modifier'])
    if (is_from_bridge and '**' not in result['adv_address']) or result['adv_address'].startswith('***'):
        result['flow_ver'] = hex(0)
    else:
        result['flow_ver'] = hex(int(result['adv_address'][:2] + result['adv_address'][-2:], 16))
    result['ble_type'] = len_dict['name']
    test_mode = test_mode_check(result)
    result['test_mode'] = test_mode
    if len_dict['name'] != 'LEGACY':
        result['extended_header'] = packet_data[FieldsLength.HEADER.value:
                                                FieldsLength.HEADER.value + FieldsLength.EXTENDED_HEADER.value]
        result['adi'] = packet_data[ADI_LOCATION:ADI_LOCATION + FieldsLength.ADI.value]

    return result


def test_mode_check(pixie_dict):
    flow_version = hex(int(pixie_dict.get('flow_ver', '0x0'), 16))

    if int(flow_version, 16) < 0x42c:
        if 'FFFFFFFF' in pixie_dict.get('adv_address', ''):
            return 1
    elif int(flow_version, 16) < 0x500:
        adv_address = pixie_dict.get('adv_address', '')
        if adv_address.startswith('FFFF') or adv_address.endswith('FFFF'):
            return 1
    else:
        if int(pixie_dict.get('data_uid', '0'), 16) == 5:
            return 1
    return 0


def is_packet_from_bridge(packet_data):
    service_uuid_index = FieldsLength.HEADER.value + FieldsLength.ADVA.value + BridgeParams.PACKET_DATA_INFO.value
    service_uuid = packet_data[service_uuid_index: service_uuid_index + BridgeParams.SERVICE_UUID_LENGTH.value]
    return service_uuid == BridgeParams.BRG_SERVICE_UUID.value


def extract_group_id(raw_group_id):
    """
    Extract group ID from the raw group ID packet by removing the two last bits.
    :param raw_group_id: as it received by the gateway
    :type raw_group_id: str
    :return: the group ID
    :rtype: str
    """
    raw_group_id_list = [x for x in raw_group_id]
    last_half_byte = raw_group_id_list[4]
    byte_without_2_last_bits = int(last_half_byte, 16) & 3
    raw_group_id_list[4] = str(byte_without_2_last_bits)
    return ''.join(raw_group_id_list)


def hex2bin(hex_value, min_digits=0, zfill=True):
    binary_value = format(int(hex_value, 16), 'b')

    if zfill:
        binary_value = binary_value.zfill(24)

    if len(binary_value) < min_digits:
        binary_value = binary_value.zfill(min_digits)

    return binary_value


def check_packet_length_with_no_indication(packet_data_input):
    expected_length = None
    received_len = len(packet_data_input)
    for packet_prefix, length_dict in packet_length_types.items():
        if received_len == length_dict['packet_tag_length']:
            packet_data_input += '0' * GWPacketLength.GW_DATA_LENGTH.value
            expected_length = length_dict

        elif received_len == length_dict['packet_tag_length'] + GWPacketLength.GW_DATA_LENGTH.value:
            expected_length = length_dict

        elif length_dict['name'] == 'LEGACY':
            if received_len == length_dict['packet_tag_length'] - FieldsLength.HEADER.value:
                packet_data_input = packet_prefix + packet_data_input + '0' * GWPacketLength.GW_DATA_LENGTH.value
                expected_length = length_dict
            elif received_len == \
                    length_dict['packet_tag_length'] - FieldsLength.HEADER.value + GWPacketLength.GW_DATA_LENGTH.value:
                packet_data_input = packet_prefix + packet_data_input
                expected_length = length_dict

        if expected_length is not None:
            break

    return packet_data_input, expected_length


def construct_packet_from_fields(packet_data, fields_to_zero=None, fields_to_convert=None, gw_data='', prefix=False,
                                 gw_fields_to_convert=None):
    """
    fields_to_zero : a list of fields names, need to be zero
    fields_to_convert : dict of field name as key and its value based on packet_structure variable
    gw_fields_to_convert : if gw_data is not specified,
                           dict of field name as key and its value based on gw_bit_structure variable
    """
    new_packet = []
    is_legacy_packet = packet_length_types.get(packet_data['header'], {'name': 'LEGACY'})['name'] == 'LEGACY'
    for field in packet_structure:
        if is_legacy_packet and field['name'] in BLE5_ONLY_FIELDS:
            continue  # do not add ble5 fields to legacy packets
        if fields_to_zero and field['name'] in fields_to_zero:
            new_packet.append('0' * field['len'])
        elif fields_to_convert and field['name'] in fields_to_convert:
            new_packet.append(fields_to_convert[field['name']].upper())
        else:
            new_packet.append(packet_data.get(field['name'], ''))

    construct_packet = ''.join(new_packet)
    if gw_data == '' and gw_fields_to_convert is not None:
        gw_bit_data = ''
        if 'crc_valid' not in gw_fields_to_convert.keys():
            gw_fields_to_convert['crc_valid'] = 1
        for field in gw_bit_structure:
            if field['name'] in gw_fields_to_convert.keys():
                bin_field = bin(int(gw_fields_to_convert[field['name']]))[2:]
            else:
                bin_field = '0'
            bin_field = bin_field.zfill(field['bit_len'])
            bin_field = bin_field[-field['bit_len']:]
            gw_bit_data += str(bin_field)
        gw_data = hex(int(gw_bit_data, 2))[2:].upper()

    construct_packet += gw_data

    if prefix:
        construct_packet = f'process_packet("{construct_packet}")' if is_legacy_packet \
            else f'full_packet("{construct_packet}")'
    return construct_packet


def convert_cloud_to_packet(cloud_packet, original_packet=None):
    if original_packet is None:
        adva = ''.join(['*'] * FieldsLength.ADVA.value)
        en = ''.join(['*'] * FieldsLength.EN.value)
        b_type = ''.join(['*'] * FieldsLength.TYPE.value)
        e_header = ''.join(['*']) * FieldsLength.EXTENDED_HEADER.value
        adi = ''.join(['*']) * FieldsLength.ADI.value
        gw_packet = ''
    else:
        adva = original_packet.packet_data['adv_address']
        en = original_packet.packet_data['en']
        b_type = original_packet.packet_data['type']
        e_header = original_packet.packet_data['extended_header'] \
            if 'extended_header' in original_packet.packet_data.keys() else \
            ''.join(['*']) * FieldsLength.EXTENDED_HEADER.value
        adi = original_packet.packet_data['adi'] \
            if 'adi' in original_packet.packet_data.keys() else \
            ''.join(['*']) * FieldsLength.ADI.value
        gw_packet = np.take(original_packet.gw_data['gw_packet'], 0)

    if any(cloud_packet.startswith(x) for x in WILIOT_EN_TYPE) and len(cloud_packet) == BLE_PAYLOAD_LENGTH:
        return adva + cloud_packet + gw_packet
    if any(cloud_packet.startswith(x) for x in WILIOT_DATA_UID) and \
            len(cloud_packet) == BLE_PAYLOAD_LENGTH - FieldsLength.EN.value - FieldsLength.TYPE.value:
        return adva + en + b_type + cloud_packet + gw_packet

    if any(cloud_packet.startswith(x) for x in WILIOT_EN_TYPE) and \
            len(cloud_packet) == BLE_DOUBLE_PAYLOAD_LENGTH:
        header = [k for k, v in packet_length_types.items() if v['name'] == 'BLE5-DBL-EXT']
        return header[0] + adva + e_header + adi + cloud_packet + gw_packet
    if any(cloud_packet.startswith(x) for x in WILIOT_DATA_UID) and \
            len(cloud_packet) == BLE_DOUBLE_PAYLOAD_LENGTH - FieldsLength.EN.value - FieldsLength.TYPE.value:
        header = [k for k, v in packet_length_types.items() if v['name'] == 'BLE5-DBL-EXT']
        return header[0] + adva + e_header + adi + en + b_type + cloud_packet + gw_packet

    return cloud_packet


def reverse_data(data):
    data_reversed = ''
    for i in range(len(data), 0, -2):
        data_reversed += data[i - 2:i]
    return data_reversed
