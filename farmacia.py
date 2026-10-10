"""
===========================================================
ASSISTENTE DE FARMÁCIA - VERSÃO TELEGRAM
===========================================================
"""

import re
from datetime import datetime
import telebot
from flask import Flask
from threading import Thread
import os

# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

# Cole aqui o TOKEN que o BotFather te deu
TOKEN = os.environ.get("BOT_TOKEN")

ARQUIVO_LOG = "conversas_farmacia.log"

bot = telebot.TeleBot(TOKEN)


# ==========================================================
# BASE DE CONHECIMENTO + MEDICAMENTOS
# ==========================================================

# (Cole aqui exatamente o mesmo RESPOSTAS, PALAVRAS_CHAVE 
#  e MEDICAMENTOS que você já tem no seu código)

RESPOSTAS = {
    "saudacao": (
        "Olá! Sou o assistente virtual da farmácia. "
        "Posso verificar a disponibilidade de medicamentos "
        "e informar para que eles servem. Como posso ajudar?"
    ),
    "horario_funcionamento": (
        "Nossa farmácia funciona de segunda a sábado, "
        "das 08:00 às 20:00, e aos domingos das 09:00 às 13:00."
    ),
    "verificar_estoque": (
        "Vou verificar a disponibilidade do medicamento para você. "
        "Por favor, informe o nome do remédio."
    ),
    "para_que_serve": (
        "Posso te informar a indicação do medicamento. "
        "Qual o nome do remédio que você deseja saber?"
    ),
    "precisa_receita": (
        "Alguns medicamentos só podem ser vendidos com receita médica. "
        "Informe o nome do remédio para eu verificar."
    ),
    "despedida": (
        "Foi um prazer ajudar. Cuide-se e volte sempre!"
    ),
}

PALAVRAS_CHAVE = {
    "saudacao": ["oi", "ola", "olá", "bom dia", "boa tarde", "boa noite", "hey"],
    "horario_funcionamento": ["horario", "horário", "funcionamento", "abre", "fecha", "aberto"],
    "verificar_estoque": ["tem", "têm", "disponivel", "disponível", "estoque", "vende", "vocês têm", "voces tem", "tem aí", "tem ai"],
    "para_que_serve": ["serve", "para que serve", "indicação", "indicacao", "para que é", "para que e", "função", "funcao", "trata"],
    "precisa_receita": ["receita", "receituario", "receituário", "controlado", "preciso de receita"],
    "despedida": ["tchau", "até mais", "ate mais", "até logo", "ate logo", "falou", "obrigado", "obrigada"]
}

# ==========================================================
# COLE AQUI O SEU DICIONÁRIO MEDICAMENTOS COMPLETO (os 523)
# ==========================================================
#MEDICAMENTOS = {
    # ... cole todo o conteúdo do MEDICAMENTOS aqui ...
#}


# -*- coding: utf-8 -*-
# Banco de dados de medicamentos para o Assistente de Farmácia
# Total de medicamentos: 523

MEDICAMENTOS = {
    "aas": {
        "disponivel": True,
        "indicacao": "Usado para dores, febre e prevenção cardiovascular em baixa dose.",
        "precisa_receita": False
    },
    "abilify": {
        "disponivel": False,
        "indicacao": "Antipsicótico atípico usado em esquizofrenia e bipolar.",
        "precisa_receita": True
    },
    "aceclofenaco": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório usado em dores musculoesqueléticas.",
        "precisa_receita": False
    },
    "acetaminofeno": {
        "disponivel": True,
        "indicacao": "Indicada para dores leves a moderadas e febre.",
        "precisa_receita": False
    },
    "acetato de medroxiprogesterona": {
        "disponivel": False,
        "indicacao": "Injetável anticoncepcional e em endometriose.",
        "precisa_receita": True
    },
    "acetazolamida": {
        "disponivel": True,
        "indicacao": "Inibidor da anidrase carbônica usado em glaucoma e mal de altitude.",
        "precisa_receita": True
    },
    "acetilcisteína": {
        "disponivel": False,
        "indicacao": "Mucolítico usado para fluidificar secreções respiratórias.",
        "precisa_receita": False
    },
    "aciclovir": {
        "disponivel": True,
        "indicacao": "Antiviral usado em infecções por herpes.",
        "precisa_receita": True
    },
    "adapaleno": {
        "disponivel": True,
        "indicacao": "Retinoide tópico usado em acne.",
        "precisa_receita": False
    },
    "advil": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório à base de ibuprofeno.",
        "precisa_receita": False
    },
    "aero-flat": {
        "disponivel": True,
        "indicacao": "Usada para alívio de gases intestinais e desconforto abdominal.",
        "precisa_receita": False
    },
    "aerolin": {
        "disponivel": True,
        "indicacao": "Broncodilatador usado em crises de asma e broncoespasmo.",
        "precisa_receita": True
    },
    "agomelatina": {
        "disponivel": True,
        "indicacao": "Antidepressivo com ação em receptores melatonínicos.",
        "precisa_receita": True
    },
    "albendazol": {
        "disponivel": True,
        "indicacao": "Antiparasitário de amplo espectro.",
        "precisa_receita": False
    },
    "aldactone": {
        "disponivel": True,
        "indicacao": "Diurético poupador de potássio usado em hipertensão e insuficiência cardíaca.",
        "precisa_receita": True
    },
    "alendronato": {
        "disponivel": False,
        "indicacao": "Usado no tratamento e prevenção da osteoporose.",
        "precisa_receita": True
    },
    "alfuzosina": {
        "disponivel": True,
        "indicacao": "Usada em sintomas de hiperplasia prostática.",
        "precisa_receita": True
    },
    "alivium": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório à base de ibuprofeno.",
        "precisa_receita": False
    },
    "alivium 600": {
        "disponivel": True,
        "indicacao": "Ibuprofeno 600mg.",
        "precisa_receita": False
    },
    "alopurinol": {
        "disponivel": True,
        "indicacao": "Usado na prevenção de crises de gota e hiperuricemia.",
        "precisa_receita": True
    },
    "alprazolam": {
        "disponivel": False,
        "indicacao": "Benzodiazepínico usado principalmente em transtornos de ansiedade.",
        "precisa_receita": True
    },
    "amaryl": {
        "disponivel": True,
        "indicacao": "Antidiabético oral da classe das sulfonilureias.",
        "precisa_receita": True
    },
    "ambroxol": {
        "disponivel": True,
        "indicacao": "Expectorante e mucolítico usado em tosse produtiva.",
        "precisa_receita": False
    },
    "amicacina": {
        "disponivel": False,
        "indicacao": "Aminoglicosídeo de amplo espectro.",
        "precisa_receita": True
    },
    "amilorida": {
        "disponivel": True,
        "indicacao": "Diurético poupador de potássio.",
        "precisa_receita": True
    },
    "amiodarona": {
        "disponivel": False,
        "indicacao": "Antiarrítmico usado em arritmias cardíacas.",
        "precisa_receita": True
    },
    "amitriptilina": {
        "disponivel": True,
        "indicacao": "Antidepressivo tricíclico usado em depressão e dores crônicas.",
        "precisa_receita": True
    },
    "amlovasc": {
        "disponivel": False,
        "indicacao": "Anti-hipertensivo usado no controle da pressão arterial.",
        "precisa_receita": True
    },
    "amoxicilina": {
        "disponivel": False,
        "indicacao": "Antibiótico usado no tratamento de infecções bacterianas.",
        "precisa_receita": True
    },
    "amoxicilina + clavulanato": {
        "disponivel": True,
        "indicacao": "Antibiótico de amplo espectro para infecções bacterianas.",
        "precisa_receita": True
    },
    "amoxicilina + sulbactam": {
        "disponivel": False,
        "indicacao": "Antibiótico combinado.",
        "precisa_receita": True
    },
    "amoxil": {
        "disponivel": False,
        "indicacao": "Antibiótico usado no tratamento de infecções bacterianas.",
        "precisa_receita": True
    },
    "amoxilina": {
        "disponivel": True,
        "indicacao": "Antibiótico usado no tratamento de infecções bacterianas.",
        "precisa_receita": True
    },
    "ampicilina": {
        "disponivel": True,
        "indicacao": "Antibiótico penicilínico de amplo espectro.",
        "precisa_receita": True
    },
    "ampicilina + sulbactam": {
        "disponivel": True,
        "indicacao": "Antibiótico combinado.",
        "precisa_receita": True
    },
    "anador": {
        "disponivel": True,
        "indicacao": "Dipirona.",
        "precisa_receita": False
    },
    "anastrozol": {
        "disponivel": True,
        "indicacao": "Inibidor de aromatase usado em câncer de mama.",
        "precisa_receita": True
    },
    "anfotericina b": {
        "disponivel": True,
        "indicacao": "Antifúngico usado em micoses sistêmicas graves.",
        "precisa_receita": True
    },
    "anlodipino": {
        "disponivel": True,
        "indicacao": "Anti-hipertensivo usado no controle da pressão arterial.",
        "precisa_receita": True
    },
    "anlodipino + losartana": {
        "disponivel": True,
        "indicacao": "Associação anti-hipertensiva.",
        "precisa_receita": True
    },
    "arcoxia": {
        "disponivel": False,
        "indicacao": "Etoricoxibe.",
        "precisa_receita": True
    },
    "aripiprazol": {
        "disponivel": True,
        "indicacao": "Antipsicótico atípico usado em esquizofrenia e bipolar.",
        "precisa_receita": True
    },
    "artemeter + lumefantrina": {
        "disponivel": True,
        "indicacao": "Antimalárico combinado.",
        "precisa_receita": True
    },
    "atenol": {
        "disponivel": True,
        "indicacao": "Beta-bloqueador usado para pressão alta e problemas cardíacos.",
        "precisa_receita": True
    },
    "atenolol": {
        "disponivel": True,
        "indicacao": "Beta-bloqueador usado para pressão alta e problemas cardíacos.",
        "precisa_receita": True
    },
    "atorvastatina": {
        "disponivel": True,
        "indicacao": "Redutor de colesterol da classe das estatinas.",
        "precisa_receita": True
    },
    "atropina": {
        "disponivel": True,
        "indicacao": "Anticolinérgico usado em diversas situações.",
        "precisa_receita": True
    },
    "avanafila": {
        "disponivel": True,
        "indicacao": "Usada no tratamento de disfunção erétil.",
        "precisa_receita": True
    },
    "azitromicina": {
        "disponivel": True,
        "indicacao": "Antibiótico macrolídeo usado em infecções respiratórias e outras.",
        "precisa_receita": True
    },
    "bacitracina": {
        "disponivel": True,
        "indicacao": "Antibiótico de uso tópico.",
        "precisa_receita": False
    },
    "baclofeno": {
        "disponivel": True,
        "indicacao": "Relaxante muscular de ação central.",
        "precisa_receita": True
    },
    "beclometasona": {
        "disponivel": True,
        "indicacao": "Corticosteroide inalatório usado em asma.",
        "precisa_receita": True
    },
    "benegrip": {
        "disponivel": True,
        "indicacao": "Associação para sintomas de gripe e resfriado.",
        "precisa_receita": False
    },
    "benicar": {
        "disponivel": True,
        "indicacao": "Anti-hipertensivo usado no controle da pressão arterial.",
        "precisa_receita": True
    },
    "betahistina": {
        "disponivel": False,
        "indicacao": "Usada no tratamento de labirintite e doença de Ménière.",
        "precisa_receita": True
    },
    "betametasona": {
        "disponivel": False,
        "indicacao": "Corticosteroide tópico de média/alta potência.",
        "precisa_receita": False
    },
    "betaserc": {
        "disponivel": True,
        "indicacao": "Betahistina - labirintite e Ménière.",
        "precisa_receita": True
    },
    "bimatoprosta": {
        "disponivel": True,
        "indicacao": "Usada no glaucoma e crescimento de cílios.",
        "precisa_receita": True
    },
    "bisacodil": {
        "disponivel": True,
        "indicacao": "Laxante estimulante usado em constipação.",
        "precisa_receita": False
    },
    "bisoprolol": {
        "disponivel": True,
        "indicacao": "Beta-bloqueador usado para hipertensão e insuficiência cardíaca.",
        "precisa_receita": True
    },
    "brimonidina": {
        "disponivel": True,
        "indicacao": "Usada no tratamento do glaucoma.",
        "precisa_receita": True
    },
    "bromazepam": {
        "disponivel": True,
        "indicacao": "Benzodiazepínico usado em estados de ansiedade.",
        "precisa_receita": True
    },
    "bromexina": {
        "disponivel": False,
        "indicacao": "Mucolítico usado para facilitar a eliminação de secreções.",
        "precisa_receita": False
    },
    "bromoprida": {
        "disponivel": True,
        "indicacao": "Procinético usado para náuseas e distúrbios digestivos.",
        "precisa_receita": False
    },
    "budesonida": {
        "disponivel": True,
        "indicacao": "Corticosteroide inalatório ou nasal usado em asma e rinite.",
        "precisa_receita": True
    },
    "bupropiona": {
        "disponivel": True,
        "indicacao": "Antidepressivo também usado em cessação do tabagismo.",
        "precisa_receita": True
    },
    "buscopan": {
        "disponivel": False,
        "indicacao": "Antiespasmódico usado para cólicas e dores abdominais.",
        "precisa_receita": False
    },
    "buscopan composto": {
        "disponivel": True,
        "indicacao": "Antiespasmódico + analgésico para cólicas.",
        "precisa_receita": False
    },
    "busonid": {
        "disponivel": False,
        "indicacao": "Corticosteroide inalatório ou nasal usado em asma e rinite.",
        "precisa_receita": True
    },
    "buspirona": {
        "disponivel": True,
        "indicacao": "Ansiolítico não benzodiazepínico.",
        "precisa_receita": True
    },
    "candesartana": {
        "disponivel": False,
        "indicacao": "Anti-hipertensivo da classe dos BRA.",
        "precisa_receita": True
    },
    "capoten": {
        "disponivel": False,
        "indicacao": "Anti-hipertensivo usado no tratamento da hipertensão.",
        "precisa_receita": True
    },
    "captopril": {
        "disponivel": False,
        "indicacao": "Anti-hipertensivo usado no tratamento da hipertensão.",
        "precisa_receita": True
    },
    "carbamazepina": {
        "disponivel": True,
        "indicacao": "Anticonvulsivante usado em epilepsia e neuralgia do trigêmeo.",
        "precisa_receita": True
    },
    "carbonato de cálcio": {
        "disponivel": True,
        "indicacao": "Suplemento de cálcio usado em deficiência e osteoporose.",
        "precisa_receita": False
    },
    "carbonato de lítio": {
        "disponivel": True,
        "indicacao": "Estabilizador de humor usado no transtorno bipolar.",
        "precisa_receita": True
    },
    "carisoprodol": {
        "disponivel": True,
        "indicacao": "Relaxante muscular usado em dores musculoesqueléticas.",
        "precisa_receita": True
    },
    "carvedilol": {
        "disponivel": True,
        "indicacao": "Beta-bloqueador usado em insuficiência cardíaca e hipertensão.",
        "precisa_receita": True
    },
    "carvão ativado": {
        "disponivel": True,
        "indicacao": "Usado em intoxicações para adsorver substâncias.",
        "precisa_receita": False
    },
    "cataflam": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório à base de diclofenaco.",
        "precisa_receita": False
    },
    "cataflan": {
        "disponivel": True,
        "indicacao": "Diclofenaco.",
        "precisa_receita": False
    },
    "cefaclor": {
        "disponivel": False,
        "indicacao": "Cefalosporina usada em infecções respiratórias e de pele.",
        "precisa_receita": True
    },
    "cefadroxila": {
        "disponivel": True,
        "indicacao": "Cefalosporina de primeira geração oral.",
        "precisa_receita": True
    },
    "cefalexina": {
        "disponivel": True,
        "indicacao": "Antibiótico cefalosporina usado em infecções de pele e urinárias.",
        "precisa_receita": True
    },
    "cefalium": {
        "disponivel": True,
        "indicacao": "Associação para dores de cabeça.",
        "precisa_receita": False
    },
    "cefalotina": {
        "disponivel": True,
        "indicacao": "Cefalosporina de primeira geração.",
        "precisa_receita": True
    },
    "cefazolina": {
        "disponivel": True,
        "indicacao": "Cefalosporina de primeira geração usada em profilaxia cirúrgica.",
        "precisa_receita": True
    },
    "cefepima": {
        "disponivel": True,
        "indicacao": "Cefalosporina de quarta geração.",
        "precisa_receita": True
    },
    "cefotaxima": {
        "disponivel": True,
        "indicacao": "Cefalosporina de terceira geração.",
        "precisa_receita": True
    },
    "ceftazidima": {
        "disponivel": False,
        "indicacao": "Cefalosporina de terceira geração com ação antipseudomonas.",
        "precisa_receita": True
    },
    "ceftriaxona": {
        "disponivel": True,
        "indicacao": "Cefalosporina de terceira geração.",
        "precisa_receita": True
    },
    "cefuroxima": {
        "disponivel": True,
        "indicacao": "Cefalosporina de segunda geração.",
        "precisa_receita": True
    },
    "celebra": {
        "disponivel": True,
        "indicacao": "Celecoxibe.",
        "precisa_receita": True
    },
    "celecoxibe": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório seletivo COX-2.",
        "precisa_receita": True
    },
    "cetirizina": {
        "disponivel": True,
        "indicacao": "Anti-histamínico usado para rinite alérgica e urticária.",
        "precisa_receita": False
    },
    "cetoconazol": {
        "disponivel": True,
        "indicacao": "Antifúngico usado em micoses (uso restrito sistêmico).",
        "precisa_receita": True
    },
    "cetoprofeno": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório usado para dores musculares, articulares e cólicas.",
        "precisa_receita": False
    },
    "cetorolaco": {
        "disponivel": False,
        "indicacao": "Anti-inflamatório potente para dores agudas.",
        "precisa_receita": True
    },
    "cialis": {
        "disponivel": True,
        "indicacao": "Usada no tratamento de disfunção erétil e hiperplasia prostática.",
        "precisa_receita": True
    },
    "cianocobalamina": {
        "disponivel": True,
        "indicacao": "Vitamina B12.",
        "precisa_receita": False
    },
    "ciclobenzaprina": {
        "disponivel": True,
        "indicacao": "Relaxante muscular usado em espasmos musculares.",
        "precisa_receita": False
    },
    "ciclopentolato": {
        "disponivel": True,
        "indicacao": "Midríatico e cicloplégico.",
        "precisa_receita": True
    },
    "cicloserina": {
        "disponivel": True,
        "indicacao": "Tuberculostático de segunda linha.",
        "precisa_receita": True
    },
    "ciclosporina": {
        "disponivel": True,
        "indicacao": "Imunossupressor usado em transplantes e doenças autoimunes.",
        "precisa_receita": True
    },
    "cimegripe": {
        "disponivel": True,
        "indicacao": "Associação para sintomas gripais.",
        "precisa_receita": False
    },
    "cipramil": {
        "disponivel": True,
        "indicacao": "Antidepressivo ISRS usado em depressão.",
        "precisa_receita": True
    },
    "ciprofibrato": {
        "disponivel": False,
        "indicacao": "Fibrato usado no controle de dislipidemias.",
        "precisa_receita": True
    },
    "ciprofloxacino": {
        "disponivel": True,
        "indicacao": "Antibiótico quinolona usado em infecções urinárias e outras.",
        "precisa_receita": True
    },
    "ciprofloxacino colírio": {
        "disponivel": True,
        "indicacao": "Antibiótico oftálmico.",
        "precisa_receita": True
    },
    "citalopram": {
        "disponivel": True,
        "indicacao": "Antidepressivo ISRS usado em depressão.",
        "precisa_receita": True
    },
    "claritin": {
        "disponivel": True,
        "indicacao": "Anti-histamínico usado para alergias e rinite.",
        "precisa_receita": False
    },
    "claritromicina": {
        "disponivel": False,
        "indicacao": "Antibiótico macrolídeo usado em infecções respiratórias.",
        "precisa_receita": True
    },
    "clavulin": {
        "disponivel": True,
        "indicacao": "Amoxicilina + clavulanato.",
        "precisa_receita": True
    },
    "clexane": {
        "disponivel": True,
        "indicacao": "Heparina de baixo peso molecular usada como anticoagulante.",
        "precisa_receita": True
    },
    "clindamicina": {
        "disponivel": True,
        "indicacao": "Antibiótico usado em infecções anaeróbias e acne.",
        "precisa_receita": True
    },
    "clo zapina": {
        "disponivel": False,
        "indicacao": "Antipsicótico atípico usado em esquizofrenia refratária.",
        "precisa_receita": True
    },
    "clobetasol": {
        "disponivel": True,
        "indicacao": "Corticosteroide tópico de altíssima potência.",
        "precisa_receita": True
    },
    "clonazepam": {
        "disponivel": True,
        "indicacao": "Benzodiazepínico usado em ansiedade, convulsões e insônia.",
        "precisa_receita": True
    },
    "clonidina": {
        "disponivel": True,
        "indicacao": "Anti-hipertensivo de ação central.",
        "precisa_receita": True
    },
    "clopidogrel": {
        "disponivel": True,
        "indicacao": "Antiagregante plaquetário usado em prevenção de eventos cardiovasculares.",
        "precisa_receita": True
    },
    "clorana": {
        "disponivel": False,
        "indicacao": "Diurético usado no controle da pressão arterial.",
        "precisa_receita": True
    },
    "cloreto de potássio": {
        "disponivel": True,
        "indicacao": "Reposição de potássio.",
        "precisa_receita": True
    },
    "cloroquina": {
        "disponivel": True,
        "indicacao": "Usada em malária e algumas doenças reumáticas.",
        "precisa_receita": True
    },
    "clorpromazina": {
        "disponivel": True,
        "indicacao": "Antipsicótico típico clássico.",
        "precisa_receita": True
    },
    "clortalidona": {
        "disponivel": True,
        "indicacao": "Diurético tiazídico usado em hipertensão.",
        "precisa_receita": True
    },
    "clotrimazol": {
        "disponivel": False,
        "indicacao": "Antifúngico tópico usado em micoses.",
        "precisa_receita": False
    },
    "clozapina": {
        "disponivel": True,
        "indicacao": "Antipsicótico atípico usado em esquizofrenia refratária.",
        "precisa_receita": True
    },
    "codeína": {
        "disponivel": False,
        "indicacao": "Analgésico opioide e antitussígeno.",
        "precisa_receita": True
    },
    "colchicina": {
        "disponivel": True,
        "indicacao": "Usada no tratamento de crises de gota.",
        "precisa_receita": True
    },
    "coltrax": {
        "disponivel": True,
        "indicacao": "Tiocolchicosídeo.",
        "precisa_receita": False
    },
    "complexo b": {
        "disponivel": True,
        "indicacao": "Suplemento de vitaminas do complexo B.",
        "precisa_receita": False
    },
    "concor": {
        "disponivel": True,
        "indicacao": "Beta-bloqueador usado para hipertensão e insuficiência cardíaca.",
        "precisa_receita": True
    },
    "coreg": {
        "disponivel": True,
        "indicacao": "Beta-bloqueador usado em insuficiência cardíaca e hipertensão.",
        "precisa_receita": True
    },
    "coristina d": {
        "disponivel": True,
        "indicacao": "Associação para resfriado.",
        "precisa_receita": False
    },
    "crestor": {
        "disponivel": True,
        "indicacao": "Estatina usada para reduzir colesterol e triglicerídeos.",
        "precisa_receita": True
    },
    "cymbalta": {
        "disponivel": True,
        "indicacao": "Antidepressivo dual usado em depressão e dor neuropática.",
        "precisa_receita": True
    },
    "cálcio + vitamina d": {
        "disponivel": True,
        "indicacao": "Associação para saúde óssea.",
        "precisa_receita": False
    },
    "dalsy": {
        "disponivel": True,
        "indicacao": "Ibuprofeno pediátrico.",
        "precisa_receita": False
    },
    "daonil": {
        "disponivel": True,
        "indicacao": "Antidiabético oral da classe das sulfonilureias.",
        "precisa_receita": True
    },
    "dapagliflozina": {
        "disponivel": True,
        "indicacao": "Inibidor de SGLT2 usado no diabetes tipo 2.",
        "precisa_receita": True
    },
    "dapoxetina": {
        "disponivel": True,
        "indicacao": "Usada no tratamento de ejaculação precoce.",
        "precisa_receita": True
    },
    "daptomicina": {
        "disponivel": False,
        "indicacao": "Antibiótico usado em infecções graves por Gram-positivos.",
        "precisa_receita": True
    },
    "decadron": {
        "disponivel": True,
        "indicacao": "Corticosteroide potente usado em inflamações e alergias.",
        "precisa_receita": True
    },
    "depakene": {
        "disponivel": True,
        "indicacao": "Anticonvulsivante e estabilizador de humor.",
        "precisa_receita": True
    },
    "desloratadina": {
        "disponivel": True,
        "indicacao": "Anti-histamínico de segunda geração para alergias.",
        "precisa_receita": False
    },
    "desmopressina": {
        "disponivel": False,
        "indicacao": "Usada em diabetes insipidus e enurese noturna.",
        "precisa_receita": True
    },
    "desogestrel": {
        "disponivel": False,
        "indicacao": "Pílula só de progestagênio.",
        "precisa_receita": True
    },
    "desvenlafaxina": {
        "disponivel": True,
        "indicacao": "Antidepressivo dual usado em depressão.",
        "precisa_receita": True
    },
    "dexametasona": {
        "disponivel": True,
        "indicacao": "Corticosteroide potente usado em inflamações e alergias.",
        "precisa_receita": True
    },
    "dexclorfeniramina": {
        "disponivel": True,
        "indicacao": "Anti-histamínico clássico usado em alergias.",
        "precisa_receita": False
    },
    "dextrometorfano": {
        "disponivel": False,
        "indicacao": "Antitussígeno usado em tosse seca.",
        "precisa_receita": False
    },
    "diamicron": {
        "disponivel": True,
        "indicacao": "Antidiabético oral usado no controle da glicemia.",
        "precisa_receita": True
    },
    "diazepam": {
        "disponivel": True,
        "indicacao": "Benzodiazepínico usado em ansiedade, espasmos e convulsões.",
        "precisa_receita": True
    },
    "diclofenaco": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório indicado para dores e inflamações.",
        "precisa_receita": False
    },
    "diclofenaco potássico": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório de ação rápida.",
        "precisa_receita": False
    },
    "diclofenaco sódico": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório de uso comum.",
        "precisa_receita": False
    },
    "dienogeste": {
        "disponivel": True,
        "indicacao": "Progestagênio usado em endometriose.",
        "precisa_receita": True
    },
    "digoxina": {
        "disponivel": True,
        "indicacao": "Usada em insuficiência cardíaca e controle de frequência em FA.",
        "precisa_receita": True
    },
    "dilatrend": {
        "disponivel": True,
        "indicacao": "Beta-bloqueador usado em insuficiência cardíaca e hipertensão.",
        "precisa_receita": True
    },
    "dimenidrinato": {
        "disponivel": False,
        "indicacao": "Usado em enjoo de movimento e vertigem.",
        "precisa_receita": False
    },
    "dimeticona": {
        "disponivel": True,
        "indicacao": "Antiflatulento usado para gases e distensão abdominal.",
        "precisa_receita": False
    },
    "diosmina + hesperidina": {
        "disponivel": True,
        "indicacao": "Usado em insuficiência venosa e hemorróidas.",
        "precisa_receita": False
    },
    "diovan": {
        "disponivel": False,
        "indicacao": "Anti-hipertensivo da classe dos antagonistas da angiotensina.",
        "precisa_receita": True
    },
    "dipirona": {
        "disponivel": True,
        "indicacao": "Usada para aliviar dores e reduzir febre.",
        "precisa_receita": False
    },
    "dipirona + cafeína": {
        "disponivel": True,
        "indicacao": "Associação analgésica usada em dores e enxaqueca.",
        "precisa_receita": False
    },
    "dipirona sodica": {
        "disponivel": True,
        "indicacao": "Usada para aliviar dores e reduzir febre.",
        "precisa_receita": False
    },
    "dipirona sódica": {
        "disponivel": True,
        "indicacao": "Usada para aliviar dores e reduzir febre.",
        "precisa_receita": False
    },
    "domperidona": {
        "disponivel": True,
        "indicacao": "Procinético usado para náuseas e lentidão gástrica.",
        "precisa_receita": False
    },
    "donepezila": {
        "disponivel": True,
        "indicacao": "Usada no tratamento da doença de Alzheimer.",
        "precisa_receita": True
    },
    "dorflex": {
        "disponivel": True,
        "indicacao": "Relaxante muscular usado para dores musculares e tensionais.",
        "precisa_receita": False
    },
    "doril": {
        "disponivel": True,
        "indicacao": "Associação analgésica clássica.",
        "precisa_receita": False
    },
    "dorzolamida": {
        "disponivel": True,
        "indicacao": "Usada no tratamento do glaucoma.",
        "precisa_receita": True
    },
    "doxazosina": {
        "disponivel": True,
        "indicacao": "Usada em hipertensão e hiperplasia prostática.",
        "precisa_receita": True
    },
    "doxiciclina": {
        "disponivel": True,
        "indicacao": "Antibiótico tetraciclina usado em infecções variadas e acne.",
        "precisa_receita": True
    },
    "dramin": {
        "disponivel": True,
        "indicacao": "Dimenidrinato - enjoo e labirintite.",
        "precisa_receita": False
    },
    "dulaglutida": {
        "disponivel": True,
        "indicacao": "Análogo de GLP-1 de aplicação semanal.",
        "precisa_receita": True
    },
    "duloxetina": {
        "disponivel": True,
        "indicacao": "Antidepressivo dual usado em depressão e dor neuropática.",
        "precisa_receita": True
    },
    "dutasterida": {
        "disponivel": False,
        "indicacao": "Usada em hiperplasia prostática benigna.",
        "precisa_receita": True
    },
    "effexor": {
        "disponivel": False,
        "indicacao": "Antidepressivo dual usado em depressão e ansiedade.",
        "precisa_receita": True
    },
    "empagliflozina": {
        "disponivel": False,
        "indicacao": "Inibidor de SGLT2 usado no diabetes e insuficiência cardíaca.",
        "precisa_receita": True
    },
    "enalapril": {
        "disponivel": True,
        "indicacao": "Anti-hipertensivo usado no controle da pressão alta.",
        "precisa_receita": True
    },
    "enalapril + hidroclorotiazida": {
        "disponivel": False,
        "indicacao": "Associação anti-hipertensiva.",
        "precisa_receita": True
    },
    "engov": {
        "disponivel": False,
        "indicacao": "Associação usada em sintomas de ressaca.",
        "precisa_receita": False
    },
    "enoxaparina": {
        "disponivel": True,
        "indicacao": "Heparina de baixo peso molecular usada como anticoagulante.",
        "precisa_receita": True
    },
    "entacapona": {
        "disponivel": False,
        "indicacao": "Inibidor da COMT usado em Parkinson.",
        "precisa_receita": True
    },
    "eplerenona": {
        "disponivel": True,
        "indicacao": "Antagonista da aldosterona usado em insuficiência cardíaca.",
        "precisa_receita": True
    },
    "eritromicina": {
        "disponivel": True,
        "indicacao": "Antibiótico macrolídeo usado em infecções e acne.",
        "precisa_receita": True
    },
    "ertapenem": {
        "disponivel": False,
        "indicacao": "Antibiótico carbapenêmico.",
        "precisa_receita": True
    },
    "escitalopram": {
        "disponivel": True,
        "indicacao": "Antidepressivo ISRS usado em depressão e ansiedade.",
        "precisa_receita": True
    },
    "escopolamina": {
        "disponivel": True,
        "indicacao": "Antiespasmódico e antiemético.",
        "precisa_receita": False
    },
    "esomeprazol": {
        "disponivel": False,
        "indicacao": "Inibidor de bomba de prótons para refluxo e gastrite.",
        "precisa_receita": False
    },
    "espironolactona": {
        "disponivel": True,
        "indicacao": "Diurético poupador de potássio usado em hipertensão e insuficiência cardíaca.",
        "precisa_receita": True
    },
    "estreptomicina": {
        "disponivel": True,
        "indicacao": "Aminoglicosídeo usado em tuberculose.",
        "precisa_receita": True
    },
    "etambutol": {
        "disponivel": True,
        "indicacao": "Tuberculostático de primeira linha.",
        "precisa_receita": True
    },
    "etinilestradiol + levonorgestrel": {
        "disponivel": True,
        "indicacao": "Anticoncepcional oral combinado.",
        "precisa_receita": True
    },
    "etionamida": {
        "disponivel": True,
        "indicacao": "Tuberculostático de segunda linha.",
        "precisa_receita": True
    },
    "etoricoxibe": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório seletivo COX-2 usado em osteoartrite e artrite.",
        "precisa_receita": True
    },
    "euthyrox": {
        "disponivel": True,
        "indicacao": "Hormônio tireoidiano usado no hipotireoidismo.",
        "precisa_receita": True
    },
    "ezetimiba": {
        "disponivel": True,
        "indicacao": "Medicamento que reduz a absorção de colesterol no intestino.",
        "precisa_receita": True
    },
    "fenitoína": {
        "disponivel": True,
        "indicacao": "Anticonvulsivante clássico usado em epilepsia.",
        "precisa_receita": True
    },
    "fenofibrato": {
        "disponivel": False,
        "indicacao": "Usado para reduzir triglicerídeos e colesterol.",
        "precisa_receita": True
    },
    "fentanila": {
        "disponivel": False,
        "indicacao": "Opioide potente usado em dores severas e anestesia.",
        "precisa_receita": True
    },
    "ferripolimaltose": {
        "disponivel": True,
        "indicacao": "Suplemento de ferro de melhor tolerância.",
        "precisa_receita": False
    },
    "fexofenadina": {
        "disponivel": True,
        "indicacao": "Anti-histamínico não sedativo para alergias.",
        "precisa_receita": False
    },
    "finasterida": {
        "disponivel": False,
        "indicacao": "Usada em hiperplasia prostática e queda de cabelo masculina.",
        "precisa_receita": True
    },
    "finasterida 1mg": {
        "disponivel": True,
        "indicacao": "Usada em calvície androgenética.",
        "precisa_receita": True
    },
    "flanax": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório à base de naproxeno.",
        "precisa_receita": False
    },
    "fluconazol": {
        "disponivel": True,
        "indicacao": "Antifúngico usado em candidíase e outras micoses.",
        "precisa_receita": True
    },
    "fluconazol 150mg": {
        "disponivel": True,
        "indicacao": "Dose única comum para candidíase vaginal.",
        "precisa_receita": True
    },
    "fluimucil": {
        "disponivel": False,
        "indicacao": "Mucolítico usado para fluidificar secreções respiratórias.",
        "precisa_receita": False
    },
    "flumazenil": {
        "disponivel": True,
        "indicacao": "Antídoto de benzodiazepínicos.",
        "precisa_receita": True
    },
    "flunarizina": {
        "disponivel": True,
        "indicacao": "Usada em enxaqueca e distúrbios vestibulares.",
        "precisa_receita": True
    },
    "fluoresceína": {
        "disponivel": False,
        "indicacao": "Corante usado em exames oftalmológicos.",
        "precisa_receita": False
    },
    "fluoxetina": {
        "disponivel": False,
        "indicacao": "Antidepressivo ISRS usado em depressão, TOC e bulimia.",
        "precisa_receita": True
    },
    "formoterol": {
        "disponivel": False,
        "indicacao": "Broncodilatador de longa duração usado em asma e DPOC.",
        "precisa_receita": True
    },
    "forxiga": {
        "disponivel": True,
        "indicacao": "Inibidor de SGLT2 usado no diabetes tipo 2.",
        "precisa_receita": True
    },
    "fosamax": {
        "disponivel": True,
        "indicacao": "Usado no tratamento e prevenção da osteoporose.",
        "precisa_receita": True
    },
    "fosfomicina": {
        "disponivel": True,
        "indicacao": "Antibiótico usado em infecções urinárias não complicadas.",
        "precisa_receita": True
    },
    "frontal": {
        "disponivel": True,
        "indicacao": "Benzodiazepínico usado principalmente em transtornos de ansiedade.",
        "precisa_receita": True
    },
    "furosemida": {
        "disponivel": True,
        "indicacao": "Diurético de alça usado em retenção de líquidos e hipertensão.",
        "precisa_receita": True
    },
    "gabapentina": {
        "disponivel": True,
        "indicacao": "Usada em dor neuropática e como adjuvante em epilepsia.",
        "precisa_receita": True
    },
    "galantamina": {
        "disponivel": True,
        "indicacao": "Usada no tratamento da doença de Alzheimer.",
        "precisa_receita": True
    },
    "gasec": {
        "disponivel": True,
        "indicacao": "Usado para problemas de estômago, refluxo e azia.",
        "precisa_receita": False
    },
    "gatifloxacino": {
        "disponivel": True,
        "indicacao": "Antibiótico oftálmico.",
        "precisa_receita": True
    },
    "gemifloxacino": {
        "disponivel": True,
        "indicacao": "Quinolona respiratória.",
        "precisa_receita": True
    },
    "gentamicina": {
        "disponivel": True,
        "indicacao": "Aminoglicosídeo usado em infecções graves.",
        "precisa_receita": True
    },
    "ginkgo biloba": {
        "disponivel": True,
        "indicacao": "Fitoterápico usado em circulação e memória.",
        "precisa_receita": False
    },
    "glibenclamida": {
        "disponivel": True,
        "indicacao": "Antidiabético oral da classe das sulfonilureias.",
        "precisa_receita": True
    },
    "gliclazida": {
        "disponivel": True,
        "indicacao": "Antidiabético oral usado no controle da glicemia.",
        "precisa_receita": True
    },
    "glifage": {
        "disponivel": False,
        "indicacao": "Medicamento de primeira linha para diabetes tipo 2.",
        "precisa_receita": True
    },
    "glifage xr": {
        "disponivel": True,
        "indicacao": "Medicamento de primeira linha para diabetes tipo 2.",
        "precisa_receita": True
    },
    "glimepirida": {
        "disponivel": True,
        "indicacao": "Antidiabético oral da classe das sulfonilureias.",
        "precisa_receita": True
    },
    "griseofulvina": {
        "disponivel": True,
        "indicacao": "Antifúngico usado em dermatofitoses.",
        "precisa_receita": True
    },
    "guaifenesina": {
        "disponivel": True,
        "indicacao": "Expectorante usado em tosse com catarro.",
        "precisa_receita": False
    },
    "haloperidol": {
        "disponivel": True,
        "indicacao": "Antipsicótico típico usado em psicose e agitação.",
        "precisa_receita": True
    },
    "hidralazina": {
        "disponivel": True,
        "indicacao": "Vasodilatador usado no tratamento da hipertensão.",
        "precisa_receita": True
    },
    "hidratina": {
        "disponivel": True,
        "indicacao": "Anticonvulsivante clássico usado em epilepsia.",
        "precisa_receita": True
    },
    "hidroclorotiazida": {
        "disponivel": True,
        "indicacao": "Diurético usado no controle da pressão arterial.",
        "precisa_receita": True
    },
    "hidrocortisona": {
        "disponivel": True,
        "indicacao": "Corticosteroide tópico de baixa potência.",
        "precisa_receita": False
    },
    "hidroxicloroquina": {
        "disponivel": True,
        "indicacao": "Usada em lúpus, artrite reumatoide e malária.",
        "precisa_receita": True
    },
    "hidroxizina": {
        "disponivel": True,
        "indicacao": "Anti-histamínico com efeito ansiolítico e antipruriginoso.",
        "precisa_receita": True
    },
    "hidróxido de alumínio": {
        "disponivel": True,
        "indicacao": "Antiácido usado para azia e hiperacidez.",
        "precisa_receita": False
    },
    "hioscina": {
        "disponivel": True,
        "indicacao": "Antiespasmódico usado em cólicas.",
        "precisa_receita": False
    },
    "humulin n": {
        "disponivel": True,
        "indicacao": "Insulina de ação intermediária usada no diabetes.",
        "precisa_receita": True
    },
    "humulin r": {
        "disponivel": True,
        "indicacao": "Insulina de ação rápida usada no diabetes.",
        "precisa_receita": True
    },
    "ibandronato": {
        "disponivel": False,
        "indicacao": "Bifosfonato usado em osteoporose.",
        "precisa_receita": True
    },
    "ibuprofeno": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório usado para dores, inflamação e febre.",
        "precisa_receita": False
    },
    "ibuprofeno + arginina": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório de absorção mais rápida.",
        "precisa_receita": False
    },
    "imipenem": {
        "disponivel": True,
        "indicacao": "Antibiótico carbapenêmico.",
        "precisa_receita": True
    },
    "indapamida": {
        "disponivel": True,
        "indicacao": "Diurético tiazídico-like usado em hipertensão.",
        "precisa_receita": True
    },
    "inderal": {
        "disponivel": True,
        "indicacao": "Beta-bloqueador usado para pressão alta, enxaqueca e ansiedade.",
        "precisa_receita": True
    },
    "insulina asparte": {
        "disponivel": True,
        "indicacao": "Insulina de ação rápida.",
        "precisa_receita": True
    },
    "insulina degludeca": {
        "disponivel": True,
        "indicacao": "Insulina de ação ultra-prolongada.",
        "precisa_receita": True
    },
    "insulina detemir": {
        "disponivel": True,
        "indicacao": "Insulina de ação prolongada.",
        "precisa_receita": True
    },
    "insulina glargina": {
        "disponivel": True,
        "indicacao": "Insulina de ação prolongada usada no diabetes.",
        "precisa_receita": True
    },
    "insulina lispro": {
        "disponivel": True,
        "indicacao": "Insulina de ação rápida.",
        "precisa_receita": True
    },
    "insulina nph": {
        "disponivel": True,
        "indicacao": "Insulina de ação intermediária usada no diabetes.",
        "precisa_receita": True
    },
    "insulina regular": {
        "disponivel": True,
        "indicacao": "Insulina de ação rápida usada no diabetes.",
        "precisa_receita": True
    },
    "irbesartana": {
        "disponivel": False,
        "indicacao": "Anti-hipertensivo da classe dos BRA.",
        "precisa_receita": True
    },
    "isoniazida": {
        "disponivel": True,
        "indicacao": "Tuberculostático de primeira linha.",
        "precisa_receita": True
    },
    "isotretinoína": {
        "disponivel": True,
        "indicacao": "Retinoide oral usado em acne grave.",
        "precisa_receita": True
    },
    "itraconazol": {
        "disponivel": True,
        "indicacao": "Antifúngico de amplo espectro.",
        "precisa_receita": True
    },
    "ivermectina": {
        "disponivel": True,
        "indicacao": "Antiparasitário usado em diversas parasitoses.",
        "precisa_receita": False
    },
    "januvia": {
        "disponivel": True,
        "indicacao": "Inibidor de DPP-4 usado no diabetes tipo 2.",
        "precisa_receita": True
    },
    "jardiance": {
        "disponivel": True,
        "indicacao": "Inibidor de SGLT2 usado no diabetes e insuficiência cardíaca.",
        "precisa_receita": True
    },
    "keppra": {
        "disponivel": True,
        "indicacao": "Anticonvulsivante de nova geração usado em epilepsia.",
        "precisa_receita": True
    },
    "lactulose": {
        "disponivel": True,
        "indicacao": "Laxante osmótico usado em constipação e encefalopatia hepática.",
        "precisa_receita": False
    },
    "lamictal": {
        "disponivel": True,
        "indicacao": "Anticonvulsivante e estabilizador de humor.",
        "precisa_receita": True
    },
    "lamotrigina": {
        "disponivel": True,
        "indicacao": "Anticonvulsivante e estabilizador de humor.",
        "precisa_receita": True
    },
    "lansoprazol": {
        "disponivel": True,
        "indicacao": "Usado no tratamento de refluxo e úlceras gástricas.",
        "precisa_receita": False
    },
    "lantus": {
        "disponivel": True,
        "indicacao": "Insulina de ação prolongada usada no diabetes.",
        "precisa_receita": True
    },
    "lasix": {
        "disponivel": True,
        "indicacao": "Diurético de alça usado em retenção de líquidos e hipertensão.",
        "precisa_receita": True
    },
    "latanoprosta": {
        "disponivel": True,
        "indicacao": "Análogo de prostaglandina usado no glaucoma.",
        "precisa_receita": True
    },
    "levetiracetam": {
        "disponivel": True,
        "indicacao": "Anticonvulsivante de nova geração usado em epilepsia.",
        "precisa_receita": True
    },
    "levodopa + benserazida": {
        "disponivel": True,
        "indicacao": "Usada no tratamento da doença de Parkinson.",
        "precisa_receita": True
    },
    "levodopa + carbidopa": {
        "disponivel": True,
        "indicacao": "Usada no tratamento da doença de Parkinson.",
        "precisa_receita": True
    },
    "levofloxacino": {
        "disponivel": True,
        "indicacao": "Antibiótico quinolona de amplo espectro.",
        "precisa_receita": True
    },
    "levomepromazina": {
        "disponivel": True,
        "indicacao": "Antipsicótico com efeito sedativo potente.",
        "precisa_receita": True
    },
    "levonorgestrel": {
        "disponivel": True,
        "indicacao": "Usado em pílula do dia seguinte e DIU hormonal.",
        "precisa_receita": True
    },
    "levotiroxina": {
        "disponivel": True,
        "indicacao": "Hormônio tireoidiano usado no hipotireoidismo.",
        "precisa_receita": True
    },
    "lexapro": {
        "disponivel": False,
        "indicacao": "Antidepressivo ISRS usado em depressão e ansiedade.",
        "precisa_receita": True
    },
    "lexotan": {
        "disponivel": True,
        "indicacao": "Benzodiazepínico usado em estados de ansiedade.",
        "precisa_receita": True
    },
    "lincomicina": {
        "disponivel": True,
        "indicacao": "Antibiótico similar à clindamicina.",
        "precisa_receita": True
    },
    "linezolida": {
        "disponivel": False,
        "indicacao": "Antibiótico usado em infecções por Gram-positivos resistentes.",
        "precisa_receita": True
    },
    "lipitor": {
        "disponivel": True,
        "indicacao": "Redutor de colesterol da classe das estatinas.",
        "precisa_receita": True
    },
    "liraglutida": {
        "disponivel": True,
        "indicacao": "Análogo de GLP-1 usado em diabetes e obesidade.",
        "precisa_receita": True
    },
    "lisador": {
        "disponivel": True,
        "indicacao": "Dipirona + orfenadrina + cafeína.",
        "precisa_receita": False
    },
    "lomefloxacino": {
        "disponivel": True,
        "indicacao": "Quinolona.",
        "precisa_receita": True
    },
    "loratadina": {
        "disponivel": True,
        "indicacao": "Anti-histamínico usado para alergias e rinite.",
        "precisa_receita": False
    },
    "lorax": {
        "disponivel": False,
        "indicacao": "Benzodiazepínico usado em ansiedade e insônia.",
        "precisa_receita": True
    },
    "lorazepam": {
        "disponivel": True,
        "indicacao": "Benzodiazepínico usado em ansiedade e insônia.",
        "precisa_receita": True
    },
    "losartana": {
        "disponivel": True,
        "indicacao": "Medicamento para controle da pressão arterial.",
        "precisa_receita": True
    },
    "losartana + hidroclorotiazida": {
        "disponivel": True,
        "indicacao": "Associação anti-hipertensiva.",
        "precisa_receita": True
    },
    "losartana potassica": {
        "disponivel": True,
        "indicacao": "Medicamento para controle da pressão arterial.",
        "precisa_receita": True
    },
    "losartana potássica": {
        "disponivel": True,
        "indicacao": "Medicamento para controle da pressão arterial.",
        "precisa_receita": True
    },
    "losec": {
        "disponivel": True,
        "indicacao": "Usado para problemas de estômago, refluxo e azia.",
        "precisa_receita": False
    },
    "lovastatina": {
        "disponivel": True,
        "indicacao": "Estatina usada para redução do colesterol.",
        "precisa_receita": True
    },
    "luftal": {
        "disponivel": True,
        "indicacao": "Usada para alívio de gases intestinais e desconforto abdominal.",
        "precisa_receita": False
    },
    "lurasidona": {
        "disponivel": True,
        "indicacao": "Antipsicótico atípico usado em esquizofrenia e bipolar.",
        "precisa_receita": True
    },
    "lyrica": {
        "disponivel": True,
        "indicacao": "Usada em dor neuropática, fibromialgia e transtornos de ansiedade.",
        "precisa_receita": True
    },
    "lágrima artificial": {
        "disponivel": True,
        "indicacao": "Lubrificante ocular usado em olho seco.",
        "precisa_receita": False
    },
    "lítio": {
        "disponivel": False,
        "indicacao": "Estabilizador de humor usado no transtorno bipolar.",
        "precisa_receita": True
    },
    "magnésia": {
        "disponivel": True,
        "indicacao": "Antiácido e laxante suave.",
        "precisa_receita": False
    },
    "manitol": {
        "disponivel": True,
        "indicacao": "Diurético osmótico usado em edema cerebral.",
        "precisa_receita": True
    },
    "marevan": {
        "disponivel": True,
        "indicacao": "Anticoagulante oral usado na prevenção de tromboses.",
        "precisa_receita": True
    },
    "mebendazol": {
        "disponivel": True,
        "indicacao": "Antiparasitário usado em verminoses.",
        "precisa_receita": False
    },
    "meclizina": {
        "disponivel": True,
        "indicacao": "Usada em labirintite e enjoo de movimento.",
        "precisa_receita": False
    },
    "meloxicam": {
        "disponivel": False,
        "indicacao": "Anti-inflamatório usado em dores articulares e osteoartrite.",
        "precisa_receita": False
    },
    "memantina": {
        "disponivel": True,
        "indicacao": "Usada no tratamento da doença de Alzheimer moderada a grave.",
        "precisa_receita": True
    },
    "meropenem": {
        "disponivel": False,
        "indicacao": "Antibiótico carbapenêmico de amplo espectro.",
        "precisa_receita": True
    },
    "metamizol": {
        "disponivel": False,
        "indicacao": "Outro nome da dipirona.",
        "precisa_receita": False
    },
    "metformina": {
        "disponivel": True,
        "indicacao": "Medicamento de primeira linha para diabetes tipo 2.",
        "precisa_receita": True
    },
    "metformina + dapagliflozina": {
        "disponivel": False,
        "indicacao": "Associação antidiabética.",
        "precisa_receita": True
    },
    "metformina + glibenclamida": {
        "disponivel": True,
        "indicacao": "Associação antidiabética.",
        "precisa_receita": True
    },
    "metformina + sitagliptina": {
        "disponivel": False,
        "indicacao": "Associação antidiabética.",
        "precisa_receita": True
    },
    "meticorten": {
        "disponivel": True,
        "indicacao": "Corticosteroide usado em inflamações e alergias severas.",
        "precisa_receita": True
    },
    "metildopa": {
        "disponivel": True,
        "indicacao": "Anti-hipertensivo usado especialmente na gestação.",
        "precisa_receita": True
    },
    "metimazol": {
        "disponivel": True,
        "indicacao": "Usado no tratamento do hipertireoidismo.",
        "precisa_receita": True
    },
    "metoclopramida": {
        "disponivel": True,
        "indicacao": "Antiemético e procinético usado para náuseas e vômitos.",
        "precisa_receita": False
    },
    "metoprolol": {
        "disponivel": True,
        "indicacao": "Beta-bloqueador usado para hipertensão e insuficiência cardíaca.",
        "precisa_receita": True
    },
    "metotrexato": {
        "disponivel": True,
        "indicacao": "Imunossupressor usado em artrite reumatoide e algumas neoplasias.",
        "precisa_receita": True
    },
    "metronidazol": {
        "disponivel": True,
        "indicacao": "Antibiótico e antiparasitário usado em infecções anaeróbias e protozoários.",
        "precisa_receita": True
    },
    "miconazol": {
        "disponivel": True,
        "indicacao": "Antifúngico tópico e oral.",
        "precisa_receita": False
    },
    "minoxidil": {
        "disponivel": True,
        "indicacao": "Usado em calvície (tópico) e hipertensão (oral).",
        "precisa_receita": False
    },
    "mirabegrona": {
        "disponivel": True,
        "indicacao": "Usada em bexiga hiperativa.",
        "precisa_receita": True
    },
    "mirtazapina": {
        "disponivel": True,
        "indicacao": "Antidepressivo tetracíclico com efeito sedativo.",
        "precisa_receita": True
    },
    "mometasona": {
        "disponivel": True,
        "indicacao": "Corticosteroide tópico e nasal.",
        "precisa_receita": False
    },
    "mononitrato de isossorbida": {
        "disponivel": True,
        "indicacao": "Vasodilatador usado em angina.",
        "precisa_receita": True
    },
    "montelucaste": {
        "disponivel": True,
        "indicacao": "Antileucotrieno usado em asma e rinite alérgica.",
        "precisa_receita": True
    },
    "morfina": {
        "disponivel": True,
        "indicacao": "Analgésico opioide potente usado em dores severas.",
        "precisa_receita": True
    },
    "moxifloxacino": {
        "disponivel": True,
        "indicacao": "Antibiótico quinolona de amplo espectro.",
        "precisa_receita": True
    },
    "mucosolvan": {
        "disponivel": False,
        "indicacao": "Expectorante e mucolítico usado em tosse produtiva.",
        "precisa_receita": False
    },
    "mupirocina": {
        "disponivel": False,
        "indicacao": "Antibiótico tópico usado em infecções de pele.",
        "precisa_receita": False
    },
    "naloxona": {
        "disponivel": True,
        "indicacao": "Antídoto de opioides.",
        "precisa_receita": True
    },
    "naproxeno": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório usado para dores e processos inflamatórios.",
        "precisa_receita": False
    },
    "nebivolol": {
        "disponivel": True,
        "indicacao": "Beta-bloqueador de terceira geração.",
        "precisa_receita": True
    },
    "neomicina": {
        "disponivel": True,
        "indicacao": "Antibiótico aminoglicosídeo de uso tópico.",
        "precisa_receita": False
    },
    "neosaldina": {
        "disponivel": True,
        "indicacao": "Usada para alívio de dores de cabeça.",
        "precisa_receita": False
    },
    "neosaldina cafeína": {
        "disponivel": False,
        "indicacao": "Associação para dores de cabeça.",
        "precisa_receita": False
    },
    "neostigmina": {
        "disponivel": False,
        "indicacao": "Inibidor da colinesterase usado em miastenia e íleo paralítico.",
        "precisa_receita": True
    },
    "neurontin": {
        "disponivel": True,
        "indicacao": "Usada em dor neuropática e como adjuvante em epilepsia.",
        "precisa_receita": True
    },
    "nexium": {
        "disponivel": True,
        "indicacao": "Inibidor de bomba de prótons para refluxo e gastrite.",
        "precisa_receita": False
    },
    "nifedipino": {
        "disponivel": True,
        "indicacao": "Anti-hipertensivo e vasodilatador.",
        "precisa_receita": True
    },
    "nimesulida": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório indicado para dores e inflamações agudas.",
        "precisa_receita": False
    },
    "nistatina": {
        "disponivel": True,
        "indicacao": "Antifúngico usado em candidíase oral e intestinal.",
        "precisa_receita": False
    },
    "nisulid": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório indicado para dores e inflamações agudas.",
        "precisa_receita": False
    },
    "nitazoxanida": {
        "disponivel": False,
        "indicacao": "Antiparasitário de amplo espectro.",
        "precisa_receita": False
    },
    "nitrofurantoína": {
        "disponivel": True,
        "indicacao": "Antibiótico usado especificamente em infecções urinárias.",
        "precisa_receita": True
    },
    "norfloxacino": {
        "disponivel": False,
        "indicacao": "Quinolona usada em infecções urinárias.",
        "precisa_receita": True
    },
    "nortriptilina": {
        "disponivel": True,
        "indicacao": "Antidepressivo tricíclico usado em depressão e dores.",
        "precisa_receita": True
    },
    "norvasc": {
        "disponivel": True,
        "indicacao": "Anti-hipertensivo usado no controle da pressão arterial.",
        "precisa_receita": True
    },
    "novalgina": {
        "disponivel": True,
        "indicacao": "Analgésico e antitérmico à base de dipirona.",
        "precisa_receita": False
    },
    "novolin n": {
        "disponivel": True,
        "indicacao": "Insulina de ação intermediária usada no diabetes.",
        "precisa_receita": True
    },
    "novolin r": {
        "disponivel": True,
        "indicacao": "Insulina de ação rápida usada no diabetes.",
        "precisa_receita": True
    },
    "ofloxacino": {
        "disponivel": True,
        "indicacao": "Quinolona de amplo espectro.",
        "precisa_receita": True
    },
    "olanzapina": {
        "disponivel": True,
        "indicacao": "Antipsicótico atípico usado em esquizofrenia e transtorno bipolar.",
        "precisa_receita": True
    },
    "olmesartana": {
        "disponivel": True,
        "indicacao": "Anti-hipertensivo usado no controle da pressão arterial.",
        "precisa_receita": True
    },
    "omeoprazol": {
        "disponivel": True,
        "indicacao": "Usado para problemas de estômago, refluxo e azia.",
        "precisa_receita": False
    },
    "omeprazol": {
        "disponivel": True,
        "indicacao": "Usado para problemas de estômago, refluxo e azia.",
        "precisa_receita": False
    },
    "ondansetrona": {
        "disponivel": True,
        "indicacao": "Antiemético usado para náuseas e vômitos intensos.",
        "precisa_receita": True
    },
    "orfenadrina": {
        "disponivel": True,
        "indicacao": "Relaxante muscular com efeito analgésico.",
        "precisa_receita": False
    },
    "orlistat": {
        "disponivel": True,
        "indicacao": "Inibidor de lipase usado no tratamento da obesidade.",
        "precisa_receita": False
    },
    "oseltamivir": {
        "disponivel": True,
        "indicacao": "Antiviral usado em influenza.",
        "precisa_receita": True
    },
    "oxibutinina": {
        "disponivel": True,
        "indicacao": "Usada em bexiga hiperativa e incontinência urinária.",
        "precisa_receita": True
    },
    "oxicodona": {
        "disponivel": True,
        "indicacao": "Analgésico opioide usado em dores crônicas intensas.",
        "precisa_receita": True
    },
    "ozempic": {
        "disponivel": True,
        "indicacao": "Análogo de GLP-1 usado no diabetes e emagrecimento.",
        "precisa_receita": True
    },
    "paliperidona": {
        "disponivel": True,
        "indicacao": "Antipsicótico atípico.",
        "precisa_receita": True
    },
    "pantop": {
        "disponivel": True,
        "indicacao": "Inibidor de bomba de prótons usado em refluxo e úlceras.",
        "precisa_receita": False
    },
    "pantoprazol": {
        "disponivel": False,
        "indicacao": "Inibidor de bomba de prótons usado em refluxo e úlceras.",
        "precisa_receita": False
    },
    "pantozol": {
        "disponivel": False,
        "indicacao": "Inibidor de bomba de prótons usado em refluxo e úlceras.",
        "precisa_receita": False
    },
    "paracetamol": {
        "disponivel": True,
        "indicacao": "Indicada para dores leves a moderadas e febre.",
        "precisa_receita": False
    },
    "paracetamol + cafeína": {
        "disponivel": True,
        "indicacao": "Analgésico usado em dores de cabeça e enxaqueca.",
        "precisa_receita": False
    },
    "paracetamol + codeína": {
        "disponivel": True,
        "indicacao": "Analgésico combinado para dores moderadas a intensas.",
        "precisa_receita": True
    },
    "paroxetina": {
        "disponivel": True,
        "indicacao": "Antidepressivo ISRS usado em depressão e transtornos de ansiedade.",
        "precisa_receita": True
    },
    "passiflora": {
        "disponivel": False,
        "indicacao": "Fitoterápico usado em ansiedade leve.",
        "precisa_receita": False
    },
    "paxil": {
        "disponivel": True,
        "indicacao": "Antidepressivo ISRS usado em depressão e transtornos de ansiedade.",
        "precisa_receita": True
    },
    "penicilina": {
        "disponivel": True,
        "indicacao": "Antibiótico clássico usado em infecções estreptocócicas.",
        "precisa_receita": True
    },
    "penicilina g benzatina": {
        "disponivel": True,
        "indicacao": "Usada em sífilis e profilaxia de febre reumática.",
        "precisa_receita": True
    },
    "penicilina procaína": {
        "disponivel": True,
        "indicacao": "Forma de penicilina de depósito.",
        "precisa_receita": True
    },
    "peróxido de benzoíla": {
        "disponivel": True,
        "indicacao": "Usado no tratamento da acne.",
        "precisa_receita": False
    },
    "pilocarpina": {
        "disponivel": True,
        "indicacao": "Usada em glaucoma e xerostomia.",
        "precisa_receita": True
    },
    "piperacilina + tazobactam": {
        "disponivel": True,
        "indicacao": "Antibiótico de amplo espectro.",
        "precisa_receita": True
    },
    "pirazinamida": {
        "disponivel": True,
        "indicacao": "Tuberculostático de primeira linha.",
        "precisa_receita": True
    },
    "piridostigmina": {
        "disponivel": True,
        "indicacao": "Usada no tratamento de miastenia gravis.",
        "precisa_receita": True
    },
    "piridoxina": {
        "disponivel": True,
        "indicacao": "Vitamina B6.",
        "precisa_receita": False
    },
    "pirimetamina": {
        "disponivel": False,
        "indicacao": "Usada em toxoplasmose e malária.",
        "precisa_receita": True
    },
    "piroxicam": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório de longa duração usado em dores crônicas.",
        "precisa_receita": False
    },
    "plasil": {
        "disponivel": True,
        "indicacao": "Metoclopramida - náuseas e vômitos.",
        "precisa_receita": False
    },
    "plavix": {
        "disponivel": True,
        "indicacao": "Antiagregante plaquetário usado em prevenção de eventos cardiovasculares.",
        "precisa_receita": True
    },
    "polimixina b": {
        "disponivel": True,
        "indicacao": "Antibiótico usado em infecções por Gram-negativos.",
        "precisa_receita": True
    },
    "pramipexol": {
        "disponivel": True,
        "indicacao": "Agonista dopaminérgico usado em Parkinson e síndrome das pernas inquietas.",
        "precisa_receita": True
    },
    "pravastatina": {
        "disponivel": True,
        "indicacao": "Estatina usada no controle do colesterol.",
        "precisa_receita": True
    },
    "praziquantel": {
        "disponivel": True,
        "indicacao": "Antiparasitário usado em esquistossomose e tênias.",
        "precisa_receita": True
    },
    "prednisolona": {
        "disponivel": True,
        "indicacao": "Corticosteroide usado em processos inflamatórios e alérgicos.",
        "precisa_receita": True
    },
    "prednisona": {
        "disponivel": True,
        "indicacao": "Corticosteroide usado em inflamações e alergias severas.",
        "precisa_receita": True
    },
    "pregabalina": {
        "disponivel": True,
        "indicacao": "Usada em dor neuropática, fibromialgia e transtornos de ansiedade.",
        "precisa_receita": True
    },
    "primaquina": {
        "disponivel": True,
        "indicacao": "Usada na cura radical da malária por P. vivax.",
        "precisa_receita": True
    },
    "pristiq": {
        "disponivel": False,
        "indicacao": "Antidepressivo dual usado em depressão.",
        "precisa_receita": True
    },
    "profenid": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório à base de cetoprofeno.",
        "precisa_receita": False
    },
    "prometazina": {
        "disponivel": True,
        "indicacao": "Anti-histamínico com efeito sedativo, usado em alergias e náuseas.",
        "precisa_receita": True
    },
    "propafenona": {
        "disponivel": True,
        "indicacao": "Antiarrítmico usado em arritmias supraventriculares.",
        "precisa_receita": True
    },
    "propecia": {
        "disponivel": True,
        "indicacao": "Usada em hiperplasia prostática e queda de cabelo masculina.",
        "precisa_receita": True
    },
    "propranolol": {
        "disponivel": True,
        "indicacao": "Beta-bloqueador usado para pressão alta, enxaqueca e ansiedade.",
        "precisa_receita": True
    },
    "proscar": {
        "disponivel": True,
        "indicacao": "Usada em hiperplasia prostática e queda de cabelo masculina.",
        "precisa_receita": True
    },
    "prozac": {
        "disponivel": True,
        "indicacao": "Antidepressivo ISRS usado em depressão, TOC e bulimia.",
        "precisa_receita": True
    },
    "puran t4": {
        "disponivel": True,
        "indicacao": "Hormônio tireoidiano usado no hipotireoidismo.",
        "precisa_receita": True
    },
    "quetiapina": {
        "disponivel": False,
        "indicacao": "Antipsicótico atípico usado em esquizofrenia, bipolar e como adjuvante.",
        "precisa_receita": True
    },
    "quinina": {
        "disponivel": True,
        "indicacao": "Antimalárico clássico.",
        "precisa_receita": True
    },
    "ramipril": {
        "disponivel": True,
        "indicacao": "Anti-hipertensivo da classe dos inibidores da ECA.",
        "precisa_receita": True
    },
    "ranitidina": {
        "disponivel": True,
        "indicacao": "Antagonista H2 usado para azia e úlceras (uso restrito).",
        "precisa_receita": False
    },
    "rasagilina": {
        "disponivel": True,
        "indicacao": "Inibidor da MAO-B usado em Parkinson.",
        "precisa_receita": True
    },
    "reactine": {
        "disponivel": True,
        "indicacao": "Anti-histamínico usado para rinite alérgica e urticária.",
        "precisa_receita": False
    },
    "renitec": {
        "disponivel": True,
        "indicacao": "Anti-hipertensivo usado no controle da pressão alta.",
        "precisa_receita": True
    },
    "resfenol": {
        "disponivel": True,
        "indicacao": "Associação para sintomas gripais.",
        "precisa_receita": False
    },
    "rifampicina": {
        "disponivel": True,
        "indicacao": "Antibiótico usado em tuberculose e algumas infecções.",
        "precisa_receita": True
    },
    "risedronato": {
        "disponivel": False,
        "indicacao": "Bifosfonato usado em osteoporose.",
        "precisa_receita": True
    },
    "risperdal": {
        "disponivel": True,
        "indicacao": "Antipsicótico atípico usado em esquizofrenia e mania.",
        "precisa_receita": True
    },
    "risperidona": {
        "disponivel": False,
        "indicacao": "Antipsicótico atípico usado em esquizofrenia e mania.",
        "precisa_receita": True
    },
    "rivaroxabana": {
        "disponivel": True,
        "indicacao": "Anticoagulante oral de ação direta.",
        "precisa_receita": True
    },
    "rivastigmina": {
        "disponivel": True,
        "indicacao": "Usada no tratamento da doença de Alzheimer.",
        "precisa_receita": True
    },
    "rivotril": {
        "disponivel": True,
        "indicacao": "Benzodiazepínico (clonazepam) usado em ansiedade e convulsões.",
        "precisa_receita": True
    },
    "rivotril gotas": {
        "disponivel": True,
        "indicacao": "Clonazepam em gotas.",
        "precisa_receita": True
    },
    "rosuvastatina": {
        "disponivel": True,
        "indicacao": "Estatina usada para reduzir colesterol e triglicerídeos.",
        "precisa_receita": True
    },
    "rybelsus": {
        "disponivel": True,
        "indicacao": "Análogo de GLP-1 usado no diabetes e emagrecimento.",
        "precisa_receita": True
    },
    "salbutamol": {
        "disponivel": False,
        "indicacao": "Broncodilatador usado em crises de asma e broncoespasmo.",
        "precisa_receita": True
    },
    "sconyx": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório indicado para dores e inflamações agudas.",
        "precisa_receita": False
    },
    "secnidazol": {
        "disponivel": True,
        "indicacao": "Antiparasitário usado em amebíase e giardíase.",
        "precisa_receita": False
    },
    "selegilina": {
        "disponivel": True,
        "indicacao": "Inibidor da MAO-B usado em Parkinson.",
        "precisa_receita": True
    },
    "selo-zok": {
        "disponivel": True,
        "indicacao": "Beta-bloqueador usado para hipertensão e insuficiência cardíaca.",
        "precisa_receita": True
    },
    "seloken": {
        "disponivel": True,
        "indicacao": "Beta-bloqueador usado para hipertensão e insuficiência cardíaca.",
        "precisa_receita": True
    },
    "semaglutida": {
        "disponivel": True,
        "indicacao": "Análogo de GLP-1 usado no diabetes e emagrecimento.",
        "precisa_receita": True
    },
    "seroquel": {
        "disponivel": False,
        "indicacao": "Antipsicótico atípico usado em esquizofrenia, bipolar e como adjuvante.",
        "precisa_receita": True
    },
    "sertralina": {
        "disponivel": True,
        "indicacao": "Antidepressivo ISRS usado em depressão e transtornos de ansiedade.",
        "precisa_receita": True
    },
    "sildenafila": {
        "disponivel": True,
        "indicacao": "Usada no tratamento de disfunção erétil.",
        "precisa_receita": True
    },
    "silodosina": {
        "disponivel": True,
        "indicacao": "Usada em sintomas de hiperplasia prostática.",
        "precisa_receita": True
    },
    "simeticona": {
        "disponivel": True,
        "indicacao": "Usada para alívio de gases intestinais e desconforto abdominal.",
        "precisa_receita": False
    },
    "sinvastatina": {
        "disponivel": True,
        "indicacao": "Usada para reduzir o colesterol e prevenir problemas cardiovasculares.",
        "precisa_receita": True
    },
    "sitagliptina": {
        "disponivel": True,
        "indicacao": "Inibidor de DPP-4 usado no diabetes tipo 2.",
        "precisa_receita": True
    },
    "solifenacina": {
        "disponivel": True,
        "indicacao": "Usada em bexiga hiperativa.",
        "precisa_receita": True
    },
    "sonridor": {
        "disponivel": True,
        "indicacao": "Paracetamol + cafeína.",
        "precisa_receita": False
    },
    "soro fisiológico": {
        "disponivel": True,
        "indicacao": "Solução de cloreto de sódio 0,9% para hidratação e limpeza.",
        "precisa_receita": False
    },
    "stilnox": {
        "disponivel": False,
        "indicacao": "Hipnótico usado no tratamento de curto prazo da insônia.",
        "precisa_receita": True
    },
    "stugeron": {
        "disponivel": True,
        "indicacao": "Cinarizina - labirintite e vasculopatia cerebral.",
        "precisa_receita": False
    },
    "sulfadiazina": {
        "disponivel": True,
        "indicacao": "Usada em toxoplasmose em associação.",
        "precisa_receita": True
    },
    "sulfadiazina de prata": {
        "disponivel": True,
        "indicacao": "Usada em queimaduras para prevenção de infecção.",
        "precisa_receita": False
    },
    "sulfametoxazol + trimetoprima": {
        "disponivel": True,
        "indicacao": "Antibiótico combinado usado em infecções urinárias e outras.",
        "precisa_receita": True
    },
    "sulfato de magnésio": {
        "disponivel": True,
        "indicacao": "Usado em deficiência de magnésio e em obstetrícia.",
        "precisa_receita": True
    },
    "sulfato ferroso": {
        "disponivel": True,
        "indicacao": "Suplemento de ferro usado em anemia ferropriva.",
        "precisa_receita": False
    },
    "sultamicilina": {
        "disponivel": True,
        "indicacao": "Pró-droga de ampicilina + sulbactam.",
        "precisa_receita": True
    },
    "sumatriptana": {
        "disponivel": True,
        "indicacao": "Usada no tratamento de crises de enxaqueca.",
        "precisa_receita": True
    },
    "synthroid": {
        "disponivel": True,
        "indicacao": "Hormônio tireoidiano usado no hipotireoidismo.",
        "precisa_receita": True
    },
    "tadalafila": {
        "disponivel": True,
        "indicacao": "Usada no tratamento de disfunção erétil e hiperplasia prostática.",
        "precisa_receita": True
    },
    "tamoxifeno": {
        "disponivel": True,
        "indicacao": "Modulador seletivo de receptor de estrógeno usado em câncer de mama.",
        "precisa_receita": True
    },
    "tansulosina": {
        "disponivel": True,
        "indicacao": "Usada no tratamento de sintomas de hiperplasia prostática.",
        "precisa_receita": True
    },
    "tegre tol": {
        "disponivel": True,
        "indicacao": "Anticonvulsivante usado em epilepsia e neuralgia do trigêmeo.",
        "precisa_receita": True
    },
    "tegretol": {
        "disponivel": True,
        "indicacao": "Anticonvulsivante usado em epilepsia e neuralgia do trigêmeo.",
        "precisa_receita": True
    },
    "teicoplanina": {
        "disponivel": True,
        "indicacao": "Antibiótico glicopeptídeo.",
        "precisa_receita": True
    },
    "telmisartana": {
        "disponivel": True,
        "indicacao": "Anti-hipertensivo da classe dos BRA.",
        "precisa_receita": True
    },
    "tenoxicam": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório usado em processos inflamatórios.",
        "precisa_receita": False
    },
    "terazosina": {
        "disponivel": False,
        "indicacao": "Usada em hipertensão e hiperplasia prostática.",
        "precisa_receita": True
    },
    "terbinafina": {
        "disponivel": True,
        "indicacao": "Antifúngico usado em onicomicoses e dermatofitoses.",
        "precisa_receita": True
    },
    "tiamina": {
        "disponivel": True,
        "indicacao": "Vitamina B1 usada em deficiência e alcoolismo.",
        "precisa_receita": False
    },
    "tibolona": {
        "disponivel": True,
        "indicacao": "Usada em terapia hormonal da menopausa.",
        "precisa_receita": True
    },
    "timolol": {
        "disponivel": True,
        "indicacao": "Betabloqueador ocular usado no glaucoma.",
        "precisa_receita": True
    },
    "tinidazol": {
        "disponivel": True,
        "indicacao": "Antiparasitário similar ao metronidazol.",
        "precisa_receita": False
    },
    "tiocolchicosídeo": {
        "disponivel": True,
        "indicacao": "Relaxante muscular usado em contraturas.",
        "precisa_receita": False
    },
    "tizanidina": {
        "disponivel": True,
        "indicacao": "Relaxante muscular de ação central.",
        "precisa_receita": True
    },
    "tobramicina": {
        "disponivel": True,
        "indicacao": "Antibiótico oftálmico e sistêmico.",
        "precisa_receita": True
    },
    "tobramicina + dexametasona": {
        "disponivel": True,
        "indicacao": "Associação antibiótico + corticosteroide oftálmica.",
        "precisa_receita": True
    },
    "tolterodina": {
        "disponivel": True,
        "indicacao": "Usada em bexiga hiperativa.",
        "precisa_receita": True
    },
    "tolvaptano": {
        "disponivel": True,
        "indicacao": "Usado em hiponatremia e doença renal policística.",
        "precisa_receita": True
    },
    "topamax": {
        "disponivel": True,
        "indicacao": "Anticonvulsivante também usado em enxaqueca.",
        "precisa_receita": True
    },
    "topiramato": {
        "disponivel": True,
        "indicacao": "Anticonvulsivante também usado em enxaqueca.",
        "precisa_receita": True
    },
    "torasemida": {
        "disponivel": True,
        "indicacao": "Diurético de alça.",
        "precisa_receita": True
    },
    "toujeo": {
        "disponivel": True,
        "indicacao": "Insulina de ação prolongada usada no diabetes.",
        "precisa_receita": True
    },
    "tramadol": {
        "disponivel": True,
        "indicacao": "Analgésico opioide fraco usado em dores moderadas a intensas.",
        "precisa_receita": True
    },
    "tramal": {
        "disponivel": False,
        "indicacao": "Tramadol.",
        "precisa_receita": True
    },
    "travoprosta": {
        "disponivel": True,
        "indicacao": "Usada no tratamento do glaucoma.",
        "precisa_receita": True
    },
    "trazodona": {
        "disponivel": True,
        "indicacao": "Antidepressivo com efeito sedativo usado em insônia.",
        "precisa_receita": True
    },
    "tretinoína": {
        "disponivel": True,
        "indicacao": "Retinoide tópico usado em acne e fotoenvelhecimento.",
        "precisa_receita": True
    },
    "triantereno": {
        "disponivel": True,
        "indicacao": "Diurético poupador de potássio.",
        "precisa_receita": True
    },
    "tritate": {
        "disponivel": True,
        "indicacao": "Anti-hipertensivo da classe dos inibidores da ECA.",
        "precisa_receita": True
    },
    "tropicamida": {
        "disponivel": False,
        "indicacao": "Midríatico usado em exames oftalmológicos.",
        "precisa_receita": True
    },
    "tylenol": {
        "disponivel": True,
        "indicacao": "Analgésico e antitérmico à base de paracetamol.",
        "precisa_receita": False
    },
    "tylenol dc": {
        "disponivel": True,
        "indicacao": "Paracetamol + cafeína.",
        "precisa_receita": False
    },
    "tylex": {
        "disponivel": True,
        "indicacao": "Paracetamol + codeína.",
        "precisa_receita": True
    },
    "valaciclovir": {
        "disponivel": True,
        "indicacao": "Antiviral usado em herpes zoster e genital.",
        "precisa_receita": True
    },
    "valeri ana": {
        "disponivel": True,
        "indicacao": "Fitoterápico usado em ansiedade e insônia leve.",
        "precisa_receita": False
    },
    "valium": {
        "disponivel": True,
        "indicacao": "Benzodiazepínico usado em ansiedade, espasmos e convulsões.",
        "precisa_receita": True
    },
    "valpakine": {
        "disponivel": True,
        "indicacao": "Anticonvulsivante e estabilizador de humor.",
        "precisa_receita": True
    },
    "valsartana": {
        "disponivel": True,
        "indicacao": "Anti-hipertensivo da classe dos antagonistas da angiotensina.",
        "precisa_receita": True
    },
    "valsartana + hidroclorotiazida": {
        "disponivel": True,
        "indicacao": "Associação anti-hipertensiva.",
        "precisa_receita": True
    },
    "vancomicina": {
        "disponivel": True,
        "indicacao": "Antibiótico usado em infecções graves por Gram-positivos.",
        "precisa_receita": True
    },
    "vardenafila": {
        "disponivel": False,
        "indicacao": "Usada no tratamento de disfunção erétil.",
        "precisa_receita": True
    },
    "varfarina": {
        "disponivel": True,
        "indicacao": "Anticoagulante oral usado na prevenção de tromboses.",
        "precisa_receita": True
    },
    "venlafaxina": {
        "disponivel": True,
        "indicacao": "Antidepressivo dual usado em depressão e ansiedade.",
        "precisa_receita": True
    },
    "viagra": {
        "disponivel": True,
        "indicacao": "Usada no tratamento de disfunção erétil.",
        "precisa_receita": True
    },
    "vildagliptina": {
        "disponivel": True,
        "indicacao": "Inibidor de DPP-4 usado no controle glicêmico.",
        "precisa_receita": True
    },
    "vitamina c": {
        "disponivel": True,
        "indicacao": "Suplemento para reforço do sistema imunológico.",
        "precisa_receita": False
    },
    "vitamina d": {
        "disponivel": True,
        "indicacao": "Suplemento usado em deficiência de vitamina D e saúde óssea.",
        "precisa_receita": False
    },
    "vitamina k": {
        "disponivel": True,
        "indicacao": "Usada em deficiência e como antídoto de varfarina.",
        "precisa_receita": True
    },
    "voltaren": {
        "disponivel": True,
        "indicacao": "Anti-inflamatório indicado para dores e inflamações.",
        "precisa_receita": False
    },
    "voltaren emulgel": {
        "disponivel": True,
        "indicacao": "Diclofenaco tópico.",
        "precisa_receita": False
    },
    "vonau flash": {
        "disponivel": True,
        "indicacao": "Ondansetrona de dissolução oral.",
        "precisa_receita": True
    },
    "voriconazol": {
        "disponivel": True,
        "indicacao": "Antifúngico usado em aspergilose e micoses graves.",
        "precisa_receita": True
    },
    "vortioxetina": {
        "disponivel": True,
        "indicacao": "Antidepressivo multimodal.",
        "precisa_receita": True
    },
    "wegovy": {
        "disponivel": True,
        "indicacao": "Análogo de GLP-1 usado no diabetes e emagrecimento.",
        "precisa_receita": True
    },
    "ziprasidona": {
        "disponivel": False,
        "indicacao": "Antipsicótico atípico.",
        "precisa_receita": True
    },
    "zitromax": {
        "disponivel": True,
        "indicacao": "Antibiótico macrolídeo usado em infecções respiratórias e outras.",
        "precisa_receita": True
    },
    "zocor": {
        "disponivel": True,
        "indicacao": "Usada para reduzir o colesterol e prevenir problemas cardiovasculares.",
        "precisa_receita": True
    },
    "zofran": {
        "disponivel": True,
        "indicacao": "Antiemético usado para náuseas e vômitos intensos.",
        "precisa_receita": True
    },
    "zoloft": {
        "disponivel": True,
        "indicacao": "Antidepressivo ISRS usado em depressão e transtornos de ansiedade.",
        "precisa_receita": True
    },
    "zolpidem": {
        "disponivel": False,
        "indicacao": "Hipnótico usado no tratamento de curto prazo da insônia.",
        "precisa_receita": True
    },
    "zopiclona": {
        "disponivel": True,
        "indicacao": "Hipnótico usado em insônia.",
        "precisa_receita": True
    },
    "zyprexa": {
        "disponivel": True,
        "indicacao": "Antipsicótico atípico usado em esquizofrenia e transtorno bipolar.",
        "precisa_receita": True
    },
    "zyrtec": {
        "disponivel": True,
        "indicacao": "Anti-histamínico usado para rinite alérgica e urticária.",
        "precisa_receita": False
    },
    "ácido acetilsalicílico": {
        "disponivel": True,
        "indicacao": "Usado para dores, febre e como antiagregante plaquetário.",
        "precisa_receita": False
    },
    "ácido acetilsalicílico 100mg": {
        "disponivel": True,
        "indicacao": "Antiagregante plaquetário usado em prevenção cardiovascular.",
        "precisa_receita": False
    },
    "ácido azelaico": {
        "disponivel": True,
        "indicacao": "Usado em acne e melasma.",
        "precisa_receita": False
    },
    "ácido fusídico": {
        "disponivel": True,
        "indicacao": "Antibiótico tópico usado em infecções de pele.",
        "precisa_receita": False
    },
    "ácido fólico": {
        "disponivel": True,
        "indicacao": "Vitamina usada em deficiência e na gestação.",
        "precisa_receita": False
    },
    "ácido valproico": {
        "disponivel": True,
        "indicacao": "Anticonvulsivante e estabilizador de humor.",
        "precisa_receita": True
    },
    "óxido de zinco": {
        "disponivel": True,
        "indicacao": "Protetor cutâneo e adstringente.",
        "precisa_receita": False
    },
}





# ==========================================================
# FUNÇÕES DE PLN (iguais às suas)
# ==========================================================

def normalizar_texto(texto):
    texto = texto.lower()
    texto = texto.strip()
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto


def tokenizar(texto):
    return texto.split()


def detectar_medicamento(texto):
    texto = normalizar_texto(texto)
    for nome in MEDICAMENTOS.keys():
        if nome in texto:
            return nome
    return None


def identificar_intencao(tokens, texto_original):
    texto = " ".join(tokens)
    for intencao, palavras in PALAVRAS_CHAVE.items():
        for palavra in palavras:
            if " " in palavra:
                if palavra in texto:
                    return intencao
            else:
                if palavra in tokens:
                    return intencao
    return None


def resposta_fallback():
    return (
        "Não entendi muito bem.\n"
        "Você pode perguntar, por exemplo:\n"
        "• Vocês têm dipirona?\n"
        "• Para que serve o omeprazol?\n"
        "• Qual o horário de funcionamento?"
    )


def registrar_log(mensagem_usuario, intencao, resposta):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = (
        f"[{data_hora}] "
        f"USUARIO: {mensagem_usuario} | "
        f"INTENCAO: {intencao} | "
        f"BOT: {resposta}\n"
    )
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)


def processar_mensagem(mensagem):
    texto_normalizado = normalizar_texto(mensagem)
    tokens = tokenizar(texto_normalizado)
    intencao = identificar_intencao(tokens, mensagem)
    medicamento = detectar_medicamento(mensagem)

    if medicamento:
        dados = MEDICAMENTOS[medicamento]

        if intencao == "verificar_estoque" or intencao is None:
            if dados["disponivel"]:
                resposta = (
                    f"Sim, temos *{medicamento}* disponível.\n"
                    f"Indicação: {dados['indicacao']}"
                )
                if dados["precisa_receita"]:
                    resposta += "\n\n⚠️ Este medicamento precisa de receita médica."
            else:
                resposta = (
                    f"No momento *não temos* {medicamento} em estoque.\n"
                    f"Indicação: {dados['indicacao']}"
                )
            intencao = "verificar_estoque"

        elif intencao == "para_que_serve":
            resposta = (
                f"O medicamento *{medicamento}* serve para:\n"
                f"{dados['indicacao']}"
            )
            if dados["precisa_receita"]:
                resposta += "\n\n⚠️ Este medicamento é controlado e precisa de receita."

        elif intencao == "precisa_receita":
            if dados["precisa_receita"]:
                resposta = f"Sim, o medicamento *{medicamento}* precisa de receita médica."
            else:
                resposta = f"Não, o medicamento *{medicamento}* pode ser comprado sem receita."

        else:
            if dados["disponivel"]:
                resposta = (
                    f"Temos *{medicamento}* disponível.\n"
                    f"Indicação: {dados['indicacao']}"
                )
            else:
                resposta = (
                    f"Não temos *{medicamento}* no momento.\n"
                    f"Indicação: {dados['indicacao']}"
                )

    elif intencao is not None:
        resposta = RESPOSTAS[intencao]
    else:
        intencao = "desconhecida"
        resposta = resposta_fallback()

    registrar_log(mensagem, intencao, resposta)
    return resposta


# ==========================================================
# HANDLERS DO TELEGRAM
# ==========================================================

@bot.message_handler(commands=['start', 'ajuda', 'help'])
def enviar_boas_vindas(message):
    texto = (
        "Olá! Sou o *Assistente Virtual da Farmácia*.\n\n"
        "Posso te ajudar com:\n"
        "• Verificar se temos um medicamento\n"
        "• Informar para que o medicamento serve\n"
        "• Dizer se precisa de receita\n"
        "• Horário de funcionamento\n\n"
        "É só mandar sua pergunta!"
    )
    bot.reply_to(message, texto, parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def responder(message):
    try:
        resposta = processar_mensagem(message.text)
        bot.reply_to(message, resposta, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, "Desculpe, ocorreu um erro. Tente novamente.")
        print(f"Erro: {e}")

app = Flask('')
@app.route('/')
def home():
    return "Bot online"
# ==========================================================
# INICIAR O BOT
# ==========================================================

if __name__ == "__main__":
    print("Bot da Farmácia iniciado...")
    print("Pressione Ctrl + C para parar.")
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    bot.infinity_polling()
