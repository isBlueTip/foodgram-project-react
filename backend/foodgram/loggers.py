import logging

logger_filters = logging.getLogger(__name__)
logger_filters.setLevel(logging.DEBUG)

logger_recipe_serializers = logging.getLogger(__name__)
logger_recipe_serializers.setLevel(logging.DEBUG)

logger_recipe_views = logging.getLogger(__name__)
logger_recipe_views.setLevel(logging.DEBUG)

logger_users_serializers = logging.getLogger(__name__)
logger_users_serializers.setLevel(logging.DEBUG)

logger_users_views = logging.getLogger(__name__)
logger_users_views.setLevel(logging.DEBUG)

logger_tests = logging.getLogger(__name__)
logger_tests.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s | %(name)s |"
                              " %(levelname)s | %(message)s")
