def render(variables):
    return html_template.format(styles=styles, **variables)


def read_page_file(file_name):
    file = open('./page/' + file_name)
    contents = file.read()
    file.close()
    return contents


html_template = read_page_file('index.html')
styles = read_page_file('styles.css')
