from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from .QuotationsAPI.utils import quotation, to_usd, validate_patrimonio, updated_full_patrimony_value, \
    updated_full_acoes_value, updated_full_fiis_value
from .models import Ativos, Registro, Patrimonio
from .serializers import AtivosSerializer


class GetPostAtivosBRL(GenericAPIView):
    serializer_class = AtivosSerializer
    queryset = Ativos.objects.all()

    def get(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        serializer = AtivosSerializer(self.queryset)
        return Response(serializer.data)

    def post(self, request, **kwargs):
        patrimonio = validate_patrimonio()
        updated_patrimony = updated_full_patrimony_value(self.queryset)
        updated_acoes = updated_full_acoes_value(self.queryset)
        updated_fiis = updated_full_fiis_value(self.queryset)

        try:
            classe = str(request.stream.path).replace("/ativos/","").lower()
            nome = request.data['nome']
            if self.queryset.filter(nome=nome):
                return Response("Asset already in bank, use patch to update.", status=status.HTTP_400_BAD_REQUEST)
            quantidade = request.data['quantidade']
            preco = request.data['preço']
            dividendos = request.data['dividendos']
            try:
                taxas = request.data['taxas']
            except:
                taxas = 0
        except Exception as e:
            return Response("Failed to collect request body data: " + str(e), status=status.HTTP_400_BAD_REQUEST)
        try:
            custo = preco * quantidade
            valor_atual = quotation(f'{nome}.SAO')
            saldo = valor_atual*quantidade
            lucro_preju = saldo - (custo)
            pminpago = round(preco, 2)
            pmaxpago = round(preco, 2)

            try:
                pm_total = (preco + queryset.filter(nome=nome)['pm']) / 2
            except:
                pm_total = preco

            if classe == 'ações':
                percentual_lucro = f'{0:.2f}%'
                percentual_classe = f'{((saldo/(updated_acoes+saldo))*100):.2f}%'

            elif classe == 'fiis':
                percentual_lucro = f'{0:.2f}%'
                percentual_classe = f'{((saldo / (updated_acoes + saldo)) * 100):.2f}%'

            # elif classe == 'etfs_br':
            #     percentual_lucro = f'{0:.2f}%'
            #     percentual_classe = f'{((saldo / (updated_etfs_br + saldo)) * 100):.2f}%'



            percentual_patrimonio = f'{((saldo/(updated_patrimony+saldo))*100):.2f}%'

        except Exception as e:
            return Response("Failed to calculate data: " + str(e), status=status.HTTP_400_BAD_REQUEST)
        try:
            saldo_USD = to_usd(saldo)
            pm_USD = to_usd(pm_total)
            valor_atual_USD = to_usd(valor_atual)
        except Exception as e:
            return Response("Failed converting data to usd: " + str(e), status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                queryset = Ativos.objects.create(
                    classe=classe,
                    nome=nome,
                    quantidade=quantidade,
                    pm=pm_total,
                    saldo=saldo,
                    valor_atual=valor_atual,
                    lucro_preju=lucro_preju,
                    pminpago=pminpago,
                    pmaxpago=pmaxpago,
                    percentual_classe=percentual_classe,
                    percentual_lucro=percentual_lucro,
                    saldo_USD=saldo_USD,
                    pm_USD=pm_USD,
                    valor_atual_USD=valor_atual_USD,
                    percentual_patrimonio=percentual_patrimonio
                )

                Registro.objects.create(
                    ativo_utilizado='BRL',
                    total_saida=preco*quantidade,
                    ativo_comprado=nome,
                    total_entrada=quantidade,
                    valor_unit_saida=1,
                    valor_unit_entrada=preco,
                    unid_comprada_USD=to_usd(preco),
                    unid_vendida_USD=to_usd(1),
                    taxas=taxas,
                    cambio_USD=quotation('USDBRL'),
                    PM_Ativo_Comprado=preco,
                    origem_dividendos=dividendos
                )
                valor = patrimonio.valor+custo
                if dividendos == True:
                    dividendos_reinvestidos=patrimonio.dividendos_reinvestidos+custo
                else:
                    dividendos_reinvestidos=patrimonio.dividendos_reinvestidos


                if classe == "ações":
                    valor_acoes = patrimonio.valor_acoes+custo
                    percentual_acoes = f'{(valor_acoes*100/valor):.2f}%'

                    Patrimonio.objects.all().filter(id=1).update(
                        valor=valor,
                        valor_acoes=valor_acoes,
                        percentual_acoes=percentual_acoes,
                        dividendos_reinvestidos=dividendos_reinvestidos
                    )

        except Exception as E:
            return Response("Failure updating Patrimony: " + str(E), status=status.HTTP_400_BAD_REQUEST)

        serializer = AtivosSerializer(data=queryset.__dict__)
        if serializer.is_valid():
            queryset.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)