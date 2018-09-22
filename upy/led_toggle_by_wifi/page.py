html_file = open('index.html')
html_template = html_file.read()
html_file.close()


def render(variables):
    return html_template % variables
