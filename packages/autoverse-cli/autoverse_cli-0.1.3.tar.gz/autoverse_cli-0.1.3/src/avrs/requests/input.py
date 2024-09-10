from avrs.requests.request import AvrsApiRequest

class InputRequest(AvrsApiRequest):
    def __init__(self, parser, cfg):
        psr = parser.add_parser('user-input', help='Commands related to controlling the vehicles with controllers')
        sps = psr.add_subparsers(required= True, help='sub-command of Input')
        EnableInput(sps, cfg)
        DisableInput(sps, cfg)
        ChangeInput(sps, cfg)
        
class EnableInput(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'EnableInput', 'Ego')
        psr = parser.add_parser('enable', help='Enable user input on car')
        psr.add_argument('controller', help='type of way to control the actor', nargs = 1,
                         choices=('keyboard', 'xbox', 'wheel', 'can'))
        psr.set_defaults(func=self.send_request)

    def get_request_body(self, args):
        return {
            'Controller': args.controller
        }

class DisableInput(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'DisableInput', 'Ego')
        psr = parser.add_parser('disable', help='disable user input on car')
        psr.set_defaults(func=self.send_request)

    def get_request_body(self, args):
        return {
        }

class ChangeInput(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'ChangeInput', 'Ego')
        psr = parser.add_parser('change', help='change the input type if input is already enabled')
        psr.add_argument('controller', help='type of way to control the actor', nargs = 1,
                         choices=('keyboard', 'xbox', 'wheel'))
        psr.set_defaults(func=self.send_request)

    def get_request_body(self, args):
        return {
            'Controller': args.controller
        }

