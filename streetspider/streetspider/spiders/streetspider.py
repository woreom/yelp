import scrapy

def remove_html(url):
    index=url[::-1].find('/')
    return url[:-index]

class Streetspider(scrapy.Spider):
    name = 'streets'
    start_urls = ['https://geographic.org/streetview/usa/']

    def parse(self, response):
        url='https://geographic.org/streetview/usa/'
        states= response.css('ul li a::text').getall()
        states_url = response.css('ul li a::attr(href)').getall()
        for i in range(len(states)):
            yield response.follow(url+states_url[i],callback=self.parse_states,meta={'state':states[i]})
        
    def parse_states(self, response):
        url=remove_html(response.request.url)
        state = response.meta.get('state')
        counties= response.css('ul li a::text').getall()
        counties_url = response.css('ul li a::attr(href)').getall()
        for i in range(len(counties)):
            yield response.follow(url+counties_url[i],callback=self.parse_counties,meta={'state':state,'county':counties[i]})
        
    def parse_counties(self, response):
        url=remove_html(response.request.url)
        state = response.meta.get('state')
        county = response.meta.get('county')
        cities= response.css('ul li a::text').getall()
        cities_url = response.css('ul li a::attr(href)').getall()
        for i in range(len(cities)):
            yield response.follow(url+cities_url[i],callback=self.parse_cities, meta={'state':state,'county':county,'city':cities[i]})    
        
    def parse_cities(self, response):
        streets= response.css('ul li a::text').getall()
        state = response.meta.get('state')
        county = response.meta.get('county')
        city = response.meta.get('city')
        yield {'state':state,'county':county,'city':city,'streets':streets}