def run(event, context):
    name = event.get('name', 'World')
    return f'Hello "{name}"'