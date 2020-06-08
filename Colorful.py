from colorama import init as init_colorama, Fore as F, Back as B, Style as S
init_colorama()

BOLD = '\033[1m'

def get_terminal_size():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])


def colorprint(*args, fore='', back='', style='', end='\n', **kwargs):
    return print(*[fore + back + style + args[0] if len(args) >= 1 else ''] + list(args[1:]) , **kwargs, end=f'{S.RESET_ALL}{end}')


def linecolorprint(*args, pos='left', filler='', fore='', back='', style='', end='\n', **kwargs):
    width, height = get_terminal_size()
    text = ('{}' * len(args)).format(*args)

    if pos == 'left':
        pattern = '{:' + filler + f'<{width}' + '}'
    elif pos == 'right':
        pattern = '{:' + filler + f'>{width}' + '}'
    else:
        pattern = '{:' + filler + f'^{width}' + '}'

    return colorprint(pattern.format(text), fore=fore, back=back, style=style, end=end, **kwargs)


