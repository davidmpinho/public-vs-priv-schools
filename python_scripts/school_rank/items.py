import scrapy


class SchoolRankItem(scrapy.Item):
    name_file = scrapy.Field()
    table_main = scrapy.Field()
    table_aux = scrapy.Field()

    def __str__(self):
        return ""
