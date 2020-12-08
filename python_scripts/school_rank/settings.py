BOT_NAME = 'school_rank'

SPIDER_MODULES = ['school_rank.spiders']
NEWSPIDER_MODULE = 'school_rank.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False  # I'm putting False here for no particular reason, really.

ITEM_PIPELINES = {
    #'school_rank.pipelines.CsvPipeline': 300,
    'school_rank.pipelines.SqlitePipeline': 800,
}

