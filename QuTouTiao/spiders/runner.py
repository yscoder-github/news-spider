from scrapy.cmdline import execute

try:
    execute(
        [
            'scrapy',
            'runspider',
            'QuTouTiao',
            '-o',
            'out.json',
        ]
    )
except SystemExit:
    pass