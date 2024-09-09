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
import pandas as pd


class StatisticsCalc(object):
    def __init__(self, packet_df, sprinkler_df):
        """
        :type packet_df pd.DateFrame
        :type sprinkler_df pd.DataFrame
        """
        self.packet_df = packet_df[packet_df['crc_valid'] == 1]
        self.sprinkler_df = sprinkler_df[sprinkler_df['crc_valid'] == 1]
        self.packet_df.reset_index(inplace=True, drop=True)
        self.sprinkler_df.reset_index(inplace=True, drop=True)
        self.n_packets = self.packet_df.shape[0]
        self.n_cycles = self.sprinkler_df.shape[0]
        self.n_bad_packets = (packet_df['crc_valid'] == 0).sum()

    @staticmethod
    def _get_stat(col_in, nan_val=None, added_val=None, added_n=None):
        """
        :param col_in the array for the statistics
        :type col_in pd.Series or np.ndarray
        :param nan_val value of the nan statistics, the default is float('nan')
        :type None or float or int
        :param added_val list of values to add to the statistics, instead of add it to the col_in to improve performance
        :type added_val list
        :param added_n corresponding to added_val, list of the amount of each value from add_val that is needed to be
                       add to the statistics, instead of add it to the col_in to improve performance
        :type added_n list
        """
        if nan_val is None:
            nan_val = float('nan')

        if all(pd.isnull(col_in)):
            return {'mean': nan_val,
                    'std': nan_val,
                    'min': nan_val,
                    'max': nan_val}
        if added_val is None or added_val == [] or added_n is None or added_n == []:
            return {'mean': np.nanmean(col_in),
                    'std': np.nanstd(col_in),
                    'min': np.nanmin(col_in),
                    'max': np.nanmax(col_in)}
        n = sum(added_n + [np.count_nonzero(~np.isnan(col_in))])
        total_val = sum([a_v * a_n for a_v, a_n in zip(added_n, added_val)])
        return {'mean':  (np.nansum(col_in) + total_val) / n,
                'std': -1.0,
                'min': min([np.nanmin(col_in)] + added_val),
                'max': max([np.nanmax(col_in)] + added_val)}

    def _get_unique_list(self, param, param_name=None):
        if param_name is None:
            param_name = param
        return {param_name: ','.join(self.sprinkler_df[param].unique().astype(str))}

    def get_counting(self):
        return {'num_packets': self.n_packets,
                'num_cycles': self.n_cycles,
                'num_bad_crc_packets': self.n_bad_packets
                }

    def get_sprinkler_counter_stat(self):
        stat = self._get_stat(self.sprinkler_df['num_packets_per_sprinkler'])
        return {f'sprinkler_counter_{k}': v for k, v in stat.items()}

    def get_tbp_stat(self):
        tbp_for_calc = self.sprinkler_df['tbp'].replace(to_replace=-1, value=np.nan, inplace=False)
        stat = self._get_stat(tbp_for_calc, -1)
        stat_out = {f'tbp_{k}': v for k, v in stat.items()}
        stat_out['tbp_num_vals'] = sum(~(pd.isnull(tbp_for_calc)))
        return stat_out

    def get_per_stat(self):
        stat = self._get_stat(self.sprinkler_df['per'])
        stat_out = {f'per_{k}': v for k, v in stat.items() if k in ['mean', 'std']}
        return stat_out

    def get_rssi_stat(self):
        stat = self._get_stat(self.packet_df['rssi'])
        return {f'rssi_{k}': v for k, v in stat.items()}

    def get_time_stat(self):
        stat = self._get_stat(self.packet_df['time_from_start'])
        stat_out = {'ttfp': stat['min'],
                    'end_time': stat['max'],
                    'duration': stat['max'] - stat['min']}
        if stat_out.get('duration', 0) > 0:
            stat_out['rx_rate'] = self.n_packets / stat_out['end_time']
            stat_out['rx_rate_normalized'] = self.n_packets / stat_out['duration']
        return stat_out

    def get_flow_ver(self):
        return self._get_unique_list(param='flow_ver')

    def get_asset_id(self):
        if 'asset_id' in self.sprinkler_df:
            return self._get_unique_list(param='asset_id', param_name='asset_id')
        if 'assetId' in self.sprinkler_df:
            return self._get_unique_list(param='assetId', param_name='asset_id')
        return {}
