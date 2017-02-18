# Service Specific Configurations
server = {
    'port': '8888',
    'host': '0.0.0.0',
}


# Pecan Application Configurations
app = {
    'root': 'pig_manage.api.controllers.root.RootController',
    'modules': ['pig_manage.api'],
    'static_root': '/etc/pig/public',
}
