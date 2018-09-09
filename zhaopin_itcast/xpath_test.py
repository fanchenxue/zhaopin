from scrapy import Selector

doc = '''
 <div>
     <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>    
'''

sel = Selector(text=doc, type="html")
# res = sel.xpath('//li//@href').extract()
# res = sel.xpath('//li[re:test(@class,"item-\d")]//@href').extract()
# res = sel.xpath('//li[@class=$a]/a/@href',a="item-0").extract()
# res = sel.xpath('//ul[count(li)=$num]',num=5).extract()
res = sel.xpath('./a/@href','li').extract()
print(res)

