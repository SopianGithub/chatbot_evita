from app.models.cc import Cc
from app.models.product import Product
from app.models.employe import Employe, Loker
from app.models.am import Am

class DetailPage:

    webhookresponse = ""
    cardResponse = []

    def __init__(self, category, params):

        self.webhookresponse = ""
        self.cardResponse = []

        if category == "customer_page":
            self.detailCC(params)
        elif category == "product_page":
            self.detailProduct(params)
        elif category == "pic_page":
            self.detailPIC(params)
        elif category == "am_page":
            self.detailAM(params)

    def detailCC(self, id):
        cc = Cc.objects(id_cc=id)
        for item in cc:
            mapping = ""
            for ams in item.mapping_am:
                mapping += "Nama AM : " + str(ams.name) + \
                           "\n" + "No. Hp : " + str(ams.mobile) + "\n \n"

            self.webhookresponse = "Nama Pelanggan : " + str(item.name) + \
                              "\n" + "Segmen : " + str(item.segmen.name) + \
                              "\n \n Mapping AM : \n\n" + mapping + \
                              "\n \n Apakah Kamu Masih Membutuhkan Info Sesuatu?"

        self.setCardClose()

        return self.webhookresponse

    def detailProduct(self, id):
        product = Product.objects(id=id)
        self.webhookresponse = ""

        for item in product:
            nameprod = item.name
            desc = item.desc
            prodfile = item.productfile

        self.webhookresponse = "Product : " + str(nameprod) + \
                          "\n Description : " + str(desc) + "\n"


        for filetipe in prodfile:
            for urlfile in filetipe.url_file:
                self.cardResponse.append({
                    "text": filetipe.type_file,
                    "postback": urlfile
                })

        self.setCardClose()

        return self.webhookresponse

    def detailPIC(self, nik):
        pic = Employe.objects(nik=nik)
        # loker = Loker.object(pic.loker)
        for item in pic:
            self.webhookresponse = "Nama PIC : " + str(item.name) + \
                              "\n" + "No.Kontak : " + str(item.mobile) + \
                              "\n" + "Loker : " + str(item.loker.sub_unit) + \
                              "\n \n" + "Apakah Kamu Masih Membutuhkan Info Sesuatu?"

        self.setCardClose()

        return self.webhookresponse

    def detailAM(self, nik):
        am = Am.objects(nik=str(int(nik)))
        for i in am:
            self.webhookresponse = "Nama AM : " + str(i.name) + \
                                   "\n" + "No.Kontak : " + str(i.mobile) + \
                                   "\n \n Apakah Kamu Masih Membutuhkan Info Sesuatu?"

        self.setCardClose()

        return self.webhookresponse

    def setCardClose(self):
        self.cardResponse.append({
            "text": 'Ya',
            "postback": 'Main Menu'
        })
        self.cardResponse.append({
            "text": 'Tidak',
            "postback": 'close'
        })