from datetime import datetime

def report_to_cli(msg):
    print("[%s] %s" % (datetime.now().strftime("%H:%M:%S"), msg))

def store(data, filename, mode='w'):
    f = open('%s%s' % ('', filename), mode)
    f.write(data)
    f.close()

def check_args(parser, args, *argv):
    for arg in argv:
        if getattr(args, arg) is None:
            print("ERROR: required argument %s not set" % arg)
            parser.print_help()
            return False
    return True
