from avrs.requests.request import AvrsApiRequest

class Teleport(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'Teleport', "Ego")
        psr = parser.add_parser('teleport', help='Teleports the car to the given x,y,z in either enu or lla.')
        psr.add_argument('x', type=float, help='new x position')
        psr.add_argument('y', type=float, help='new y position')
        psr.add_argument('z', type=float, help='new z position')
        #psr.add_argument('nav', help='lla or enu coordinate system.', nargs=1, choices=('lla', 'enu'))
        psr.set_defaults(func=self.send_request)


    def get_request_body(self, args):
        return { 
            "X": args.x,
            "Y": args.y,
            "Z": args.z
            #'NavFrame': args.nav 
        }