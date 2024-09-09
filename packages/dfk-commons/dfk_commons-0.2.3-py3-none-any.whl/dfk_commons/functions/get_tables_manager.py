from dfk_commons.classes.TablesManager import TablesManager


def get_tables_manager(isProd):
    return TablesManager(isProd)