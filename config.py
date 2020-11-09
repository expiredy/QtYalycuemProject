name_of_bot = None

SERVERS_DATA = {}

servers_theme = 'QPushButton{\n	background-color:#13afbd;\n' \
                '    border-style: outset;\n' \
                '    border-width: 6px;\n' \
                '    border-radius: 8px;\n' \
                '    border-color: beige;\n    font: bold 14px;\n' \
                '    padding: 6px;\n' \
                '    min-width: 10em;\n}\n' \
                '\n\nQPushButton:hover{\n	background-color: #16ccdc;\n' \
                '    border-style: outset;\n' \
                '    border-width: 2px;\n' \
                '    border-radius: 1px;\n' \
                '    border-color: beige;\n' \
                '    font: bold 18px;\n' \
                '    min-width: 10em;\n ' \
                '   padding: 6px;\n}'

music_commands = {'!fast_play': None, '!play': None, '!stop': None, '!skip': None,
                  '!help': None}

music_channels = [765865665437368330, 765374315289247746, 772900005584961536, 764865419445141544, 749690741164343407, 775039445803073587]

music_data = {}

music_icons = {'play': '▶', 'stop': '⏸', 'skip': '⏩', 'break': '⏹', 'loop': '🔂'}

token = 'Njk5Mzc0OTAzNzQ4NDYwNTY0.XpTdog.TNBffWvyhLfZog5Yt-YnPrnGF9Y'

now_playing = None

music_payloads = {}

voice_channel_duplicate, music_play, ban_system, afto_ban = True, True, True, False

duplicated_channels = {}

events = {}

not_in_channel = ['Вы не в канале((((', 'К великому сожалению, вы сейчас не в канале']

unduplicate_pool = [699542957203652638, 700240146229887026, 755887905703985194, 753306124123635884, 747797615823028295,
                    739851946713808937, 752934156249333950, 752934095914401975, 752933978369032302, 738386679097720836]