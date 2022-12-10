from rest_framework import serializers
from .models import Ativos


class AtivosSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    classe = serializers.SerializerMethodField(read_only=True)
    nome = serializers.SerializerMethodField(read_only=True)

    default_fields = (
        'id', 'classe', 'nome', 'pm', 'valor_atual', 'saldo', 'percentual_classe', 'percentual_patrimonio', 'saldo_usd'
    )

    class Meta:
        model = Ativos
        fields = (
            'id', 'classe', 'nome', 'pm', 'valor_atual', 'saldo', 'percentual_classe', 'percentual_patrimonio', 'saldo_USD'
        )

    def get_id(self, instance):
        return self.initial_data['id']

    def get_classe(self, instance):
        return self.initial_data['classe']

    def get_nome(self, instance):
        return self.initial_data['nome']

    def get_pm(self, instance):
        return self.initial_data['pm']

    def get_valor_atual(self, instance):
        return self.initial_data['valor_atual']

    def get_saldo(self, instance):
        return self.initial_data['saldo']

    def get_percentual_classe(self, instance):
        return self.initial_data['percentual_classe']

    def get_perc_patrimonio(self, instance):
        return self.initial_data['percentual_patrimonio']
