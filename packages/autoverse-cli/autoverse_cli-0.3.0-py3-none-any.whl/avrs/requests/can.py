from avrs.requests.request import AvrsApiRequest
import can
import cantools
import time
import os
import pandas as pd
import datetime

# class Can():
#     def __init__(self, parser, cfg):
#         psr = parser.add_parser('can', help='Peforms a variety of CAN commands')
#         sps = psr.add_subparsers(required= True, help='sub-command of NPC')
#         SendCan(sps, dbc)
#         #TestCanRates(sps, cfg)
#         LogCan(sps, dbc)  


# class SendCan(AvrsApiRequest):
#     def __init__(self, parser, dbc):
#         psr = parser.add_parser('send', help='sends CAN data for given duration (seconds) with given throttle and steer percent values')
#         psr.add_argument('duration', type=float, help='Length of time to send Can data')
#         psr.add_argument('hertz', type=float, help = 'Frequency of Can Messages')
#         psr.add_argument('throttle', type=float, help='throttle (in percent)')
#         psr.add_argument('steer', type=float, help='steer (in percent)')
#         self.dbc = dbc
#         psr.set_defaults(func=self.send_can_values)


#     def send_can_values(self, args):
#         with can.interface.Bus('vcan0', bustype='socketcan') as bus:
#             message_1 = self.dbc.get_message_by_name("HL_Msg_01")
#             message_2 = self.dbc.get_message_by_name("HL_Msg_02")
#             signals_1 = {
#                 "HL_TargetThrottle": args.throttle,
#                 "HL_TargetGear": 1,
#                 "HL_TargetPressure_RR": 0,
#                 "HL_TargetPressure_RL": 0,
#                 "HL_TargetPressure_FR": 0,
#                 "HL_TargetPressure_FL": 0,
#                 "HL_Alive_01": 0, 
#             }

#             signals_2 = {
#                 "HL_Alive_02": 0, 
#                 "HL_PSA_Profile_Vel_rad_s": 0,
#                 "HL_PSA_Profile_Dec_rad_s2": 0,
#                 "HL_PSA_Profile_Acc_rad_s2": 0,
#                 "HL_TargetPSAControl": args.steer,
#                 "HL_PSA_ModeOfOperation": 0,
#             }

#             start_time = time.time()

#             print('sending can data...')
#             while time.time() - start_time < args.duration:
#                 data = message_1.encode(signals_1)
#                 msg = can.Message(arbitration_id=message_1.frame_id, data=data, is_extended_id=False)
#                 bus.send(msg)

#                 data = message_2.encode(signals_2)
#                 msg = can.Message(arbitration_id=message_2.frame_id, data=data, is_extended_id=False)
#                 bus.send(msg)
#                 time.sleep(args.hertz)
#             print('done')
    

# # class TestCanRates(AvrsApiRequest):
# #     def __init__(self, parser, cfg):
# #         AvrsApiRequest.__init__(self, parser, cfg, 'TestCanRates')
# #         psr = parser.add_parser('test-rates', help='get average can message rates over given duration for all can messages on vcan0')
# #         psr.add_argument('duration', type=float, help='Length of time to test Can rates')
# #         psr.set_defaults(func=self.send_request)
        

# #     def get_request_body(self, args):
# #         return {
# #             'Duration': args.duration,
# #         }
    
# class LogCan(AvrsApiRequest):
#     def __init__(self, parser, dbc):
#         psr = parser.add_parser('log', help='logs csv CAN data for given duration (seconds) to the given absolute file path. Will append numbers to colliding file names')
#         psr.add_argument('duration', type=float, help='length of time to log Can data')
#         psr.add_argument('path', help='absoulte file path')
#         psr.set_defaults(func=self.log_can)
#         self.dbc = dbc
    
#     def log_can(self, args):
#         start_time = time.time()

#         # Check and remove the existing 'messages.csv' file
#         file_no = 1
#         tmp_file_path = args.path
#         print(tmp_file_path)
#         while os.path.exists(tmp_file_path):
#             tmp_file_path = args.path.replace('.csv', '{}.csv'.format(file_no))
#             file_no += 1
#         args.path = tmp_file_path

#         messages_list = []
#         databases = [self.dbc]
#         print('logging can data...')
        
#         with can.interface.Bus('vcan0', bustype='socketcan') as bus:
#             while time.time() - start_time < args.duration:
#                 message = bus.recv()
#                 # If a message was received
#                 if message is not None:
#                     for db in databases:
#                         decoded = self.decode_message(message)
#                         if decoded:
#                             messages_list.append(decoded)
#                             break
#             df = pd.DataFrame(messages_list)
#             df.to_csv(args.path, index=False)
#         print('done')


#     def decode_message(self, message):
#         try:
#             decoded_message = self.dbc.decode_message(message.arbitration_id, message.data)
#             message_name = self.dbc.get_message_by_frame_id(message.arbitration_id).name
#             timestamp = datetime.datetime.now().isoformat()
#             return {'timestamp': timestamp, 'name': message_name, 'data': decoded_message}
#         except KeyError:
#             # Return None if decoding fails
#             return None
    

        

