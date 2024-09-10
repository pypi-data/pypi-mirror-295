from avrs.requests.request import AvrsApiRequest

class AvrsDemoRequest(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'DemoSendConfig', '')
        psr = parser.add_parser('demo', help='Sends a request used for a demonstration')
        psr.add_argument('--ego-type-index', type=int, default=0, help='')
        psr.add_argument('--num-npcs', type=int, default=0, help='')
        psr.add_argument('--npc-trajs', type=int, default=[0, 0, 0, 0], nargs='+', help='')
        psr.add_argument('--npc-type-index', default=0, type=int)
        psr.add_argument('--env-type-index', default=0, type=int)
        psr.add_argument('--weather-type-index', default=0, type=int)
        psr.set_defaults(func=self.send_request)

    def get_request_body(self, args):
        return {
            'IndexEgoType': args.ego_type_index,
            'NumberNPCS': args.num_npcs,
            'NPCTrajectories': args.npc_trajs,
            'IndexNPCType': args.npc_type_index,
            'IndexEnvironmentType': args.env_type_index,
            'TypeIndexIndex': args.weather_type_index
        }
