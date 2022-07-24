from django.conf import settings
from rest_framework import serializers


class GithubCollectorParamsSerializer(serializers.Serializer):
    """
    Serializer que define os parâmetros necessários para
    realizar a coleta de métricas em um repositório do  github.
    """

    github_token = serializers.CharField(
        required=True,
        help_text=(
            "Github API access token. The collector makes several requests to "
            "the Github API, so, in order not to be blocked by it, you must "
            "have a valid access token for the service to perform requests on "
            "your behalf. To create an access token, go to the following "
            "link: `https://github.com/settings/tokens`. Make sure the token "
            "passed doesn't have any permissions!"
        )
    )

    issues_repository_url = serializers.URLField(
        required=False,
        help_text=(
            'URL of the github repository where issues are stored.'
            'For example: https://github.com/microsoft/vscode'
        ),
    )

    pipelines_repository_url = serializers.URLField(
        required=False,
        help_text=(
            'URL of the github repository where pipelines are associated.'
            'For example: https://github.com/microsoft/vscode'
        ),
    )

    issues_metrics_x_days = serializers.IntegerField(required=False)
    pipeline_metrics_x_days = serializers.IntegerField(required=False)

    issue_labels = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
    )

    build_pipeline_names = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
    )

    @staticmethod
    def has_at_least_one_metrics_params(data):
        """
        Verifica se essa solicitação de coleta de métricas
        define pelo menos um grupo de parâmetro válido

        Alguns dos parâmetros são definidos em grupos, logo é preciso validar
        se pelo menos um dos grupos de parâmetros foi definido. Por exemplo,
        não faz sentido definir `issues_metrics_start_date` e não definir
        `issues_metrics_end_date`.
        """

        has_issue_metrics_params: bool = (
            'issues_metrics_x_days' in data and
            'issues_repository_url' in data
        )

        has_pipeline_metrics_params: bool = (
            'pipeline_metrics_x_days' in data and
            'pipelines_repository_url' in data
        )

        has_issue_labels_metrics_params: bool = (
            'issue_labels' in data and
            has_issue_metrics_params
        )

        return (
            has_issue_metrics_params or
            has_pipeline_metrics_params or
            has_issue_labels_metrics_params
        )

    def validate(self, data):
        """
        Valida se ao menos um dos parâmetros opcionais foi definido.

        E caso exista algum erro é explicado quais parâmetros precisam
        ser definidos para cada uma das métricas suportadas.
        """
        metrics_required_params = {}

        for metric in settings.GITHUB_METRICS:
            metric_default_name = metric['name']
            prefix = metric_default_name.split(' in the last')[0]
            correct_metric_name = f'{prefix} in the last X days'

            if 'label' in correct_metric_name:
                correct_metric_name = correct_metric_name.replace('bug', 'Y')

            metrics_required_params[correct_metric_name] = metric['api_params']

        if not self.has_at_least_one_metrics_params(data):
            raise serializers.ValidationError({
                'not_enough_params': (
                    'Not enough parameters were passed to collect at least '
                    'one metric. The supported metrics and their respective '
                    'parameters are listed bellow.'
                ),
                'supported_metrics': metrics_required_params,
            })

        return data
