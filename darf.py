from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import pandas as pd
from datetime import datetime
from calendar import monthrange
import shutil
import json
import os

class darf():
    def __init__():
        pass
    def insertdata(a1):
        second = datetime.today().strftime('%Y%m%d%H%M%S')
        df = pd.DataFrame(a1).to_json(orient = 'records')
        df = json.loads(df)
        # df = a1
        for i in df:
            try:
                data_atual = datetime.strptime(str(i['Entrada']), '%Y-%m-%d').date()
            except:
                data_atual = datetime.strptime('20'+str(i['Entrada']), '%Y-%m-%d').date()
            data_final = data_atual.replace(day=monthrange(data_atual.year, data_atual.month)[1])
            i['EmissaoDarf']=str(data_final)
            i['CNPJ Tomador'] = str(i['CNPJ Tomador'])
        df = pd.DataFrame(df)
        df = df.groupby(['CNPJ Tomador','Tomador','CNPJ Prestador','EmissaoDarf']).sum()
        df = df.reset_index()
        df = df.to_json(orient = 'records', force_ascii=False)
        df = json.loads(df)
        # print(df)

        impostos = ['CSRF','IRRF']
        for imp in impostos:
            for darf in df:
                if int(darf[imp]) == 0:
                    pass
                else:
                    #arrumando dados
                    try:
                        os.mkdir('darfs'+'//'+second)
                    except:
                        pass
                    arquivo = 'darfs'+'//'+second+'//'+darf['Tomador']+' '+imp+'-'+str(darf['CNPJ Prestador'])+' '+darf['EmissaoDarf']+'.pdf'
                    init = []
                    cnpjp =str(darf['CNPJ Prestador'])
                    for i in range(len(cnpjp),14):
                        init.append('0')
                    cnpjp =''.join(init)+cnpjp
                    cnpjp = cnpjp[:2]+'.'+cnpjp[2:5]+'.'+cnpjp[5:8]+'/'+cnpjp[8:12]+'-'+cnpjp[12:15]
                    emissao =str(darf['EmissaoDarf']).split('-')
                    mes= int(emissao[1])+1
                    if mes < 10:
                        mes = '0'+str(mes)
                    vencimento = '20/'+str(mes)+'/'+emissao[0]
                    emissao = emissao[-1]+'/'+emissao[1]+'/'+emissao[0]
                    
                    init = []
                    cnpjt =str(darf['CNPJ Tomador'])
                    for i in range(len(cnpjt),14):
                        init.append('0')
                    cnpjt =''.join(init)+cnpjt
                    cnpjt = cnpjt[:2]+'.'+cnpjt[2:5]+'.'+cnpjt[5:8]+'/'+cnpjt[8:12]+'-'+cnpjt[12:15]

                    adpt=float(round(532-(len(str(darf[imp]))-4)*5,0))

                    #imprimindo dados
                    cnv = canvas.Canvas(arquivo)
                    cnv.drawImage('b1.jpg',20,705)
                    cnv.setFont('Helvetica-Bold',9.9)
                    cnv.drawString(105,765,'MINISTÉRIO DA FAZENDA')
                    cnv.setFont('Helvetica-Bold',7.8)
                    cnv.drawString(105,750,'SECRETARIA DA RECEITA FEDERAL DO BRASIL')
                    cnv.setFont('Helvetica',7.95)
                    cnv.drawString(105,734,'Documento de Arrecadação de Receitas Federais')
                    cnv.setFont('Helvetica-Bold',9.9)
                    cnv.drawString(105,710,'DARF')
                    cnv.setFont('Helvetica',9.9)
                    cnv.drawString(150,710,imp)
                    cnv.setFont('Helvetica-Bold',9.9)
                    cnv.drawString(13,687,'01')
                    cnv.setFont('Helvetica',6)
                    cnv.drawString(30,690,'NOME / TELEFONE')
                    cnv.setFont('Helvetica',10)
                    cnv.drawString(30,680,darf['Tomador'][:42])
                    cnv.setFont('Helvetica',8)
                    cnv.drawString(30,670,'Prestador: '+cnpjp)
                    cnv.setFont('Helvetica',10)
                    cnv.drawString(130,640,'Veja no verso')
                    cnv.setFont('Helvetica',7)
                    cnv.drawString(105,625,'Instruções para preenchimento')
                    cnv.setFont('Helvetica-Bold',8.9)
                    cnv.drawString(130,600,'ATENÇÃO')
                    cnv.setFont('Helvetica',8.3)
                    cnv.drawString(18,586,'É  vedado  o  recolhimento de tributos administrados pela Secretaria  da')
                    cnv.setFont('Helvetica',8.3)
                    cnv.drawString(18,576,'Receita Federal do Brasil (RFB) cujo valor total seja inferior a R$ 10,00.')
                    cnv.setFont('Helvetica',8.2)
                    cnv.drawString(18,566,'Ocorrendo tal situação, adicione esse valor ao tributo de mesmo código de')
                    cnv.setFont('Helvetica',8.3)
                    cnv.drawString(18,556,'períodos subseqüentes, até que o total seja igual ou superior a R$ 10,00.')
                    cnv.setFont('Helvetica',8.3)
                    cnv.drawString(18,540,'Aprovado pela IN/RFB no. 736 de 2 de maio de 2007')
                    cnv.setFont('Helvetica-Bold',9.9)
                    cnv.drawString(298,769,'02')
                    cnv.drawString(298,746,'03')
                    cnv.drawString(298,722,'04')
                    cnv.drawString(298,698,'05')
                    cnv.drawString(298,674,'06')
                    cnv.drawString(298,651,'07')
                    cnv.drawString(298,627,'08')
                    cnv.drawString(298,603,'09')
                    cnv.drawString(298,579,'10')
                    cnv.drawString(298,555,'11')

                    cnv.setFont('Helvetica',5.9)
                    cnv.drawString(315,773,'PERÍODO DE APURAÇÃO')
                    cnv.drawString(315,749,'NÚMERO DO CPF OU CNPJ')
                    cnv.drawString(315,725,'CÓDIGO DA RECEITA')
                    cnv.drawString(315,701,'NÚMERO DE REFERÊNCIA')
                    cnv.drawString(315,677,'DATA DE VENCIMENTO')
                    cnv.drawString(315,655,'VALOR DO PRINCIPAL')
                    cnv.drawString(315,631,'VALOR DA MULTA')
                    cnv.drawString(315,607,'VALOR DOS JUROS E / OU')
                    cnv.drawString(315,600,'ENCARGOS DL - 1.025/69')
                    cnv.setFont('Helvetica-Bold',6)
                    cnv.drawString(315,583,'VALOR TOTAL')
                    cnv.setFont('Helvetica',5.9)
                    cnv.drawString(315,560,'AUTENTICAÇÃO BANCÁRIA (Somente nas 1ª e 2ª vias)')
                    cnv.setFont('Helvetica',11)
                    cnv.drawString(498,764,emissao)
                    cnv.drawString(455,740,cnpjt)
                    if imp == 'IRRF':
                        cnv.drawString(530,715, '1706')
                    if imp == 'CSRF':
                        cnv.drawString(530,715,'5952')
                    cnv.drawString(500,668,vencimento)
                    cnv.drawString(adpt,642,str(darf[imp]))
                    cnv.drawString(532,620,'0.00')
                    cnv.drawString(532,595,'0.00')
                    cnv.drawString(adpt,570,str(darf[imp]))

                    cnv.setFont('Helvetica-Bold',8)
                    cnv.drawString(391,765,'➜')
                    cnv.drawString(391,741,'➜')
                    cnv.drawString(391,717,'➜')
                    cnv.drawString(391,693,'➜')
                    cnv.drawString(391,669,'➜')
                    cnv.drawString(391,645,'➜')
                    cnv.drawString(391,621,'➜')
                    cnv.drawString(391,597,'➜')
                    cnv.drawString(391,573,'➜')

                    cnv.rect(10, 531, 285, 249)
                    cnv.rect(295, 567, 270, 213)
                    cnv.rect(400, 567, 0, 213)
                    cnv.rect(10, 662, 285, 36)
                    cnv.rect(10, 531, 285, 84)
                    cnv.rect(295, 732, 270, 24)
                    cnv.rect(295, 684, 270, 24)
                    cnv.rect(295, 638, 270, 24)
                    cnv.rect(295, 591, 270, 24)

                    cnv.rect(10, 450, 255, 0)
                    cnv.setFont('Helvetica-Bold',6)
                    cnv.drawString(275,450,'Corte aqui')
                    cnv.rect(320, 450, 250, 0)

                    ##### parte dois
                    cnv.drawImage('b1.jpg',20,302)
                    cnv.setFont('Helvetica-Bold',9.9)
                    cnv.drawString(105,361,'MINISTÉRIO DA FAZENDA')
                    cnv.setFont('Helvetica-Bold',7.8)
                    cnv.drawString(105,346,'SECRETARIA DA RECEITA FEDERAL DO BRASIL')
                    cnv.setFont('Helvetica',7.95)
                    cnv.drawString(105,330,'Documento de Arrecadação de Receitas Federais')
                    cnv.setFont('Helvetica-Bold',9.9)
                    cnv.drawString(105,306,'DARF')
                    cnv.setFont('Helvetica',9.9)
                    cnv.drawString(150,306,imp)
                    cnv.setFont('Helvetica-Bold',9.9)
                    cnv.drawString(13,283,'01')
                    cnv.setFont('Helvetica',6)
                    cnv.drawString(30,286,'NOME / TELEFONE')
                    cnv.setFont('Helvetica',10)
                    cnv.drawString(30,276,darf['Tomador'][:42])
                    cnv.setFont('Helvetica',8)
                    cnv.drawString(30,266,'Prestador: '+cnpjp)
                    cnv.setFont('Helvetica',10)
                    cnv.drawString(130,236,'Veja no verso')
                    cnv.setFont('Helvetica',7)
                    cnv.drawString(105,221,'Instruções para preenchimento')
                    cnv.setFont('Helvetica-Bold',8.9)
                    cnv.drawString(130,196,'ATENÇÃO')
                    cnv.setFont('Helvetica',8.3)
                    cnv.drawString(18,182,'É  vedado  o  recolhimento de tributos administrados pela Secretaria  da')
                    cnv.setFont('Helvetica',8.3)
                    cnv.drawString(18,172,'Receita Federal do Brasil (RFB) cujo valor total seja inferior a R$ 10,00.')
                    cnv.setFont('Helvetica',8.2)
                    cnv.drawString(18,162,'Ocorrendo tal situação, adicione esse valor ao tributo de mesmo código de')
                    cnv.setFont('Helvetica',8.3)
                    cnv.drawString(18,152,'períodos subseqüentes, até que o total seja igual ou superior a R$ 10,00.')
                    cnv.setFont('Helvetica',8.3)
                    cnv.drawString(18,136,'Aprovado pela IN/RFB no. 736 de 2 de maio de 2007')
                    cnv.setFont('Helvetica-Bold',9.9)
                    cnv.drawString(298,365,'02')
                    cnv.drawString(298,342,'03')
                    cnv.drawString(298,318,'04')
                    cnv.drawString(298,294,'05')
                    cnv.drawString(298,270,'06')
                    cnv.drawString(298,247,'07')
                    cnv.drawString(298,223,'08')
                    cnv.drawString(298,199,'09')
                    cnv.drawString(298,175,'10')
                    cnv.drawString(298,151,'11')

                    cnv.setFont('Helvetica',5.9)
                    cnv.drawString(315,369,'PERÍODO DE APURAÇÃO')
                    cnv.drawString(315,345,'NÚMERO DO CPF OU CNPJ')
                    cnv.drawString(315,321,'CÓDIGO DA RECEITA')
                    cnv.drawString(315,297,'NÚMERO DE REFERÊNCIA')
                    cnv.drawString(315,273,'DATA DE VENCIMENTO')
                    cnv.drawString(315,251,'VALOR DO PRINCIPAL')
                    cnv.drawString(315,227,'VALOR DA MULTA')
                    cnv.drawString(315,203,'VALOR DOS JUROS E / OU')
                    cnv.drawString(315,196,'ENCARGOS DL - 1.025/69')
                    cnv.setFont('Helvetica-Bold',6)
                    cnv.drawString(315,179,'VALOR TOTAL')
                    cnv.setFont('Helvetica',5.9)
                    cnv.drawString(315,156,'AUTENTICAÇÃO BANCÁRIA (Somente nas 1ª e 2ª vias)')
                    cnv.setFont('Helvetica',11)
                    # cnv.setFontSize(12)
                    cnv.drawString(498,360,emissao)
                    cnv.drawString(455,336,cnpjt)
                    if imp == 'IRRF':
                        cnv.drawString(530,311,'1708')
                    if imp == 'CSRF':
                        cnv.drawString(530,311,'5952')
                    cnv.drawString(500,264,vencimento)
                    cnv.drawString(adpt,238,str(darf[imp]))
                    cnv.drawString(532,216,'0.00')
                    cnv.drawString(532,191,'0.00')
                    cnv.drawString(adpt,166,str(darf[imp]))
                    cnv.setFont('Helvetica-Bold',8)
                    cnv.drawString(391,361,'➜')
                    cnv.drawString(391,337,'➜')
                    cnv.drawString(391,313,'➜')
                    cnv.drawString(391,289,'➜')
                    cnv.drawString(391,265,'➜')
                    cnv.drawString(391,241,'➜')
                    cnv.drawString(391,217,'➜')
                    cnv.drawString(391,193,'➜')
                    cnv.drawString(391,169,'➜')

                    cnv.rect(10, 127, 285, 249)
                    cnv.rect(295, 163, 270, 213)
                    cnv.rect(400, 163, 0, 213)
                    cnv.rect(10, 258, 285, 36)
                    cnv.rect(10, 127, 285, 84)
                    cnv.rect(295, 328, 270, 24)
                    cnv.rect(295, 280, 270, 24)
                    cnv.rect(295, 234, 270, 24)
                    cnv.rect(295, 187, 270, 24)
                    cnv.save()
        
        file = 'compactados/darf'+second
        shutil.make_archive(file, 'zip', './','darfs/'+second+'/')
        return file+'.zip'